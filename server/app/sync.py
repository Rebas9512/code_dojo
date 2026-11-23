"""把本机的待推送事件写入独立仓库，在 SQLite 写锁外完成所有网络操作。"""

from __future__ import annotations

import base64
import itertools
import json
import logging
import os
import re
import shutil
import sqlite3
import subprocess
import tempfile
import threading
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime
from http.client import HTTPException
from pathlib import Path
from uuid import UUID

from .db import Store
from .events import encode

LOG = logging.getLogger(__name__)
MONTH = re.compile(r"\d{4}-(?:0[1-9]|1[0-2])\.jsonl")
INTERVAL = 600
_git_auth = ContextVar("sync_git_auth", default=None)


class SyncError(Exception):
    pass


@contextmanager
def checkout_lock(directory: Path):
    # 锁随进程退出释放。文件在工作树外，多个启动器也不能同时操作同一克隆。
    with (directory / "sync.lock").open("a+b") as file:
        if os.name == "nt":
            import msvcrt
            if not file.tell():
                file.write(b"0")
                file.flush()
            file.seek(0)
            msvcrt.locking(file.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield


def git(directory: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    env = os.environ | {"GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "never", "LC_ALL": "C"}
    if auth := _git_auth.get():
        repo, token = auth
        index = int(env.get("GIT_CONFIG_COUNT", 0))
        basic = base64.b64encode(f"x-access-token:{token}".encode()).decode()
        env.update({f"GIT_CONFIG_KEY_{index}": f"http.{repo}.extraHeader",
                    f"GIT_CONFIG_VALUE_{index}": "Authorization: Basic " + basic,
                    "GIT_CONFIG_COUNT": str(index + 1)})
    # 从 IDE 等环境启动时，外层仓库的工作树或索引不能重定向进度提交。
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                 "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_NAMESPACE"):
        env.pop(name, None)
    result = subprocess.run(["git", "-c", "user.name=code-dojo", "-c", "user.email=dojo@localhost",
                             "-c", "commit.gpgsign=false", "-c", "core.editor=true", *args],
                            cwd=directory, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", env=env, timeout=30)
    if check and result.returncode:
        # Git 原文可能包含凭据或私有仓库地址，按原因显示可操作的信息。
        error = result.stderr.lower()
        if any(word in error for word in ("permission denied", "authentication", "username", "repository not found")):
            raise SyncError("仓库认证失败，请检查地址和登录凭据")
        if "resolve host" in error or "connection" in error:
            raise SyncError("无法连接同步仓库，请检查网络")
        raise SyncError(f"Git {args[0]} 失败（退出码 {result.returncode}），请检查同步仓库")
    return result


def log_path(root: Path, relative: str) -> Path:
    parts = relative.split("/")
    if len(parts) != 2 or not MONTH.fullmatch(parts[1]) or str(UUID(parts[0])) != parts[0]:
        raise SyncError("同步仓库中的日志路径无效")
    path = root / relative
    if path.parent.is_symlink() or path.is_symlink():
        raise SyncError("事件日志路径中含有符号链接")
    return path


def read_lines(lines, relative: str):
    machine, month = relative.split("/")
    for number, line in enumerate(lines, 1):
        try:
            e = json.loads(line)
            if not isinstance(e["id"], str) or str(UUID(e["id"])) != e["id"]:
                raise ValueError
            stamp = datetime.fromisoformat(e["timestamp"])
            if not e["timestamp"].endswith("+00:00") or stamp.isoformat(timespec="microseconds") != e["timestamp"]:
                raise ValueError
            if e["machine"] != machine or e["timestamp"][:7] != month[:7]:
                raise ValueError
            yield e
        except (ValueError, KeyError, TypeError) as exc:
            raise SyncError(f"日志 {relative} 第 {number} 行无效") from exc


def append_missing(root: Path, relative: str, records) -> None:
    path = log_path(root, relative)
    path.parent.mkdir(exist_ok=True)
    seen = set()
    if path.exists():
        with path.open(encoding="utf-8") as file:
            seen = {e["id"] for e in read_lines(file, relative)}
    missing = [e for e in records if e["id"] not in seen]
    if missing:
        # 原子替换避免中断时留下半行；原有内容按行原样保留。
        name = None
        try:
            with tempfile.NamedTemporaryFile(dir=root / ".git", delete=False) as temp:
                name = Path(temp.name)
                if path.exists():
                    with path.open("rb") as source:
                        shutil.copyfileobj(source, temp)
                for e in missing:
                    temp.write((encode(e) + "\n").encode())
            os.replace(name, path)
        finally:
            if name is not None:
                name.unlink(missing_ok=True)


class ProgressSync:
    def __init__(self, store: Store, repo: str):
        self.store = store
        self.repo = str(Path(repo).resolve()) if repo and Path(repo).is_dir() else repo
        self.root = store.path.parent / "sync"
        self.error = ""
        self.github = None
        self._lock = threading.Lock()
        self._wake = threading.Event()
        self._stop = threading.Event()
        self._worker: threading.Thread | None = None

    def status(self) -> dict:
        count, stamp = self.store.sync_status()
        return dict(enabled=bool(self.repo), pending=count, last_sync=stamp or None, error=self.error,
                    syncing=self._lock.locked())

    def _resolve_rebase(self) -> None:
        root = self.root
        while (root / ".git/rebase-merge").exists() or (root / ".git/rebase-apply").exists():
            paths = git(root, "diff", "--name-only", "--diff-filter=U").stdout.splitlines()
            for relative in paths:
                path = log_path(root, relative)
                if path.parent.name != self.store.journal.machine:
                    raise SyncError("其他机器目录有冲突，请检查同步仓库")
                union = {}
                for stage in ("2", "3"):
                    version = git(root, "show", f":{stage}:{relative}", check=False)
                    if version.returncode:
                        raise SyncError("日志删除冲突，请检查同步仓库")
                    for e in read_lines(version.stdout.splitlines(), relative):
                        if e["id"] in union and union[e["id"]] != e:
                            raise SyncError("同一事件的内容不同，请检查同步仓库")
                        union[e["id"]] = e
                with path.open("w", encoding="utf-8", newline="\n") as file:
                    for e in sorted(union.values(), key=lambda e: (e["timestamp"], e["id"])):
                        file.write(encode(e) + "\n")
                git(root, "add", "--", relative)
            result = git(root, "rebase", "--continue", check=False)
            if result.returncode and not git(root, "diff", "--name-only", "--diff-filter=U").stdout:
                raise SyncError("日志合并未完成，请检查同步仓库")

    def _exchange(self) -> None:
        root = self.root
        if root.is_symlink():
            raise SyncError("同步克隆目录不能是符号链接")
        if not (root / ".git").is_dir():
            if root.exists() and (not root.is_dir() or any(root.iterdir())):
                raise SyncError("数据目录下的 sync 已有其他文件，请检查目录")
            # 克隆中途断网或中断时，下次启动可重新克隆。
            with tempfile.TemporaryDirectory(dir=root.parent) as staging:
                checkout = Path(staging) / "checkout"
                git(root.parent, "clone", "--", self.repo, str(checkout))
                if root.exists():
                    root.rmdir()
                checkout.rename(root)
        origin = git(root, "config", "--get", "remote.origin.url").stdout.strip()
        same_local_path = Path(self.repo).is_absolute() and Path(origin) == Path(self.repo)
        if origin != self.repo and not same_local_path:
            raise SyncError("本地 sync 目录与配置的仓库不一致")
        if (root / "server/pyproject.toml").exists() and (root / "problems").is_dir():
            raise SyncError("请使用单独的进度仓库，当前地址指向代码仓库")
        self._resolve_rebase()
        machine = self.store.journal.machine
        pending = self.store.pending_events()
        for month, rows in itertools.groupby(pending, key=lambda e: e["timestamp"][:7]):
            append_missing(root, f"{machine}/{month}.jsonl", rows)
        if (root / machine).is_dir():
            git(root, "add", "--", machine)
            changes = git(root, "diff", "--cached", "--quiet", "--", machine, check=False)
            if changes.returncode == 1:
                git(root, "commit", "--only", "-m", "同步学习记录", "--", machine)
            elif changes.returncode:
                raise SyncError("无法检查本机日志的暂存状态")
        branch = git(root, "symbolic-ref", "--short", "HEAD").stdout.strip()
        for attempt in range(3):
            if git(root, "ls-remote", "--heads", "origin", f"refs/heads/{branch}").stdout:
                result = git(root, "pull", "--rebase", "origin", branch, check=False)
                if result.returncode:
                    if not (root / ".git/rebase-merge").exists() and not (root / ".git/rebase-apply").exists():
                        raise SyncError("拉取失败，请检查网络、权限和同步仓库")
                    self._resolve_rebase()
            head = git(root, "rev-parse", "--verify", "HEAD", check=False)
            revision = head.stdout.strip() if head.returncode == 0 else ""
            if revision:
                self._import_logs(revision)
                if pending:
                    push = git(root, "push", "origin", f"HEAD:refs/heads/{branch}", check=False)
                    if push.returncode:
                        if attempt < 2 and ("rejected" in push.stderr or "fetch first" in push.stderr):
                            continue
                        raise SyncError("推送失败，请检查网络和仓库写权限")
            self.store.confirm_sync(pending, revision)
            return

    def _import_logs(self, revision: str) -> None:
        previous = self.store.imported_revision()
        if revision == previous:
            return
        if previous and not git(self.root, "cat-file", "-e", previous, check=False).returncode:
            paths = git(self.root, "diff", "--name-only", "--diff-filter=AM", "--no-renames",
                        previous, revision, "--", "*/*.jsonl")
        else:
            paths = git(self.root, "ls-files", "--", "*/*.jsonl")
        records = []
        for relative in paths.stdout.splitlines():
            with log_path(self.root, relative).open(encoding="utf-8") as file:
                records.extend(read_lines(file, relative))
        self.store.import_events(records)

    def sync(self) -> dict:
        if self.repo:
            with self._lock:
                try:
                    with checkout_lock(self.root.parent):
                        if self.github and not shutil.which("git"):
                            from .github_sync import exchange
                            exchange(self.github, self.store)
                        else:
                            auth = _git_auth.set((self.repo, self.github.token) if self.github else None)
                            try:
                                self._exchange()
                            finally:
                                _git_auth.reset(auth)
                    self.error = ""
                except (SyncError, ValueError, KeyError, TypeError, sqlite3.Error, OSError, HTTPException, subprocess.TimeoutExpired) as exc:
                    if isinstance(exc, SyncError):
                        self.error = str(exc)
                    elif isinstance(exc, subprocess.TimeoutExpired):
                        self.error = "连接同步仓库超时"
                    elif isinstance(exc, BlockingIOError):
                        self.error = "另一个实例正在同步"
                    else:
                        self.error = f"同步失败，请检查本地日志和仓库（{type(exc).__name__}）"
                    LOG.warning("%s", self.error)
        return self.status()

    def request(self) -> None:
        self._wake.set()

    def start(self) -> None:
        if not self.repo:
            return
        self.sync()
        self._stop.clear()
        self._worker = threading.Thread(target=self._run, name="dojo-sync", daemon=True)
        self._worker.start()

    def _run(self) -> None:
        while not self._stop.is_set():
            self._wake.wait(INTERVAL)
            self._wake.clear()
            if not self._stop.is_set():
                self.sync()

    def close(self) -> None:
        if self._worker:
            self._stop.set()
            self._wake.set()
            self._worker.join()
            self._worker = None
            self.sync()
