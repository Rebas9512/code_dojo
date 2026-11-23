"""Electron 与启动器的逐行 JSON 协议。只有主线程操作子进程或写事件。"""

import json
import math
import os
import queue
import shutil
import sqlite3
import subprocess
import sys
import threading
from pathlib import Path

from cryptography.exceptions import InvalidTag

from . import DEFAULT_REPO, DEFAULT_SYNC, VERSION
from .credentials import credential_source, tokens
from .github import GitHub, repository
from .sealed import unseal
from .update import Updates
from .window import UnlockAttempts, data_directory


def emit(kind, **fields):
    print(json.dumps({"type": kind, **fields}, ensure_ascii=False), flush=True)


def lines(stream, inbox, source):
    try:
        for line in stream:
            try:
                value = json.loads(line)
            except (UnicodeError, ValueError):
                value = {}
            message = value if isinstance(value, dict) else {}
            inbox.put((source, message))
            if source == "stdin" and message.get("command") == "quit":
                break
    finally:
        inbox.put((source, None))


class Controller:
    def __init__(self, bundle: Path, data: Path, send=emit):
        self.bundle, self.data, self.send = bundle, data, send
        self.repo = repository(os.environ.get("CODE_DOJO_REPO", DEFAULT_REPO))
        self.sync_repo = repository(os.environ.get("CODE_DOJO_SYNC_REPO", DEFAULT_SYNC))
        if self.repo.casefold() == self.sync_repo.casefold():
            raise ValueError("代码和进度需要两个独立仓库")
        self.api = os.environ.get("CODE_DOJO_GITHUB_API", "https://api.github.com")
        self.attempts = UnlockAttempts(data)
        self.inbox = queue.Queue()
        self.child = None
        self.values = {}
        self.item = None
        self.notice = ""

    def begin(self):
        self.status("正在检查本机凭据…")
        source, self.values = credential_source(tokens(self.data), self.bundle, self.repo, self.sync_repo, self.api)
        if source == "sealed":
            self.send("need_unlock")
            if self.attempts.state()[1]:
                self.unlock_failed()
        elif source == "manual" and not (self.data / "desktop/current.json").is_file():
            self.send("need_tokens")
        else:
            self.update()

    def status(self, message):
        self.send("status", message=message)

    def unlock_failed(self):
        count, wait = self.attempts.state()
        self.send("unlock_failed", remaining=max(0, 5 - count), wait=math.ceil(wait))

    def unlock(self, password):
        if self.attempts.state()[1]:
            self.unlock_failed()
            return
        try:
            sealed = json.loads((self.bundle / "sealed-tokens.json").read_bytes())
            values = unseal(sealed, password, self.repo, self.sync_repo)
        except InvalidTag:
            self.attempts.failed()
            self.unlock_failed()
        except (OSError, TypeError, ValueError):
            self.send("need_tokens", message="令牌包无效或与仓库不匹配，请手动填写")
        else:
            self.save(values)

    def save(self, values):
        try:
            tokens(self.data, values)
            self.notice = ""
        except PermissionError:
            self.notice = "此数据目录无法保护令牌，令牌仅用于本次运行"
        self.values = values
        self.attempts.clear()
        self.update(restart=True)

    def command(self, message):
        name = message.get("command")
        if name == "unlock" and isinstance(message.get("password"), str) and not self.child:
            self.unlock(message["password"])
        elif name == "set_tokens" and isinstance(message.get("code"), str) and isinstance(message.get("sync", ""), str):
            code = message["code"].strip()
            if code:
                self.save(dict(code=code, sync=message.get("sync", "").strip() or code))
            else:
                self.send("need_tokens", message="请填写代码仓库令牌")
        elif name == "sync":
            self.write("sync")
            self.write("status")
        elif name == "check_update":
            self.update()
        else:
            self.send("error", message="无法识别该桌面指令")

    def update(self, restart=False):
        self.status("正在检查更新…")
        updates = Updates(self.data, self.bundle, GitHub(self.repo, self.values.get("code", ""), self.api))
        previous = updates.current()
        result = updates.check(self.status)
        detail = "；".join(filter(None, (result.message, self.notice)))
        if not result.active:
            self.send("error", message=detail or "尚未安装题库", installer=result.installer)
            return
        if self.child and self.item == result.active and not restart:
            self.send("status", message=detail or "题库已是最新版本", installer=result.installer, checked=True)
            return
        self.stop()
        self.status("正在启动本机服务…")
        if not self.start(updates, result.active):
            if not previous or previous == result.active or not self.start(updates, previous):
                self.send("error", message="本机服务启动失败，请重试")
                return
            detail = "新版服务启动失败，已恢复上一版本"
        enabled = os.environ.get("CODE_DOJO_AI_PROVIDER", "claude") == "claude" and bool(
            shutil.which(os.environ.get("CODE_DOJO_CLAUDE_BIN", "claude")))
        self.send("ready", port=self.port, version=VERSION, payload_version=self.item.manifest["version"],
                  ai=enabled, message=detail, installer=result.installer)
        self.write("status")

    def start(self, updates, item):
        config = dict(payload=str(item.root), libraries=str(updates.libraries(item.manifest)), data=str(self.data),
                      api=self.api, repo=self.sync_repo, token=self.values.get("sync") or self.values.get("code", ""))
        script = self.bundle / "start.py"
        if not script.is_file():
            script = self.bundle / "scripts/desktop/start.py"
        child = subprocess.Popen([sys.executable, "-I", "-B", "-X", "utf8", str(script)],
                                 cwd=item.root, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                 text=True, encoding="utf-8", creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        self.child = child
        self.write(json.dumps(config))
        line = child.stdout.readline()
        if not line:
            self.stop()
            return False
        self.port = json.loads(line)["ready"]
        updates.activate(item)
        self.item = item
        threading.Thread(target=lines, args=(child.stdout, self.inbox, child), daemon=True).start()
        return True

    def write(self, command):
        if self.child:
            try:
                self.child.stdin.write(command + "\n")
                self.child.stdin.flush()
            except (OSError, ValueError):
                pass

    def stop(self):
        if self.child:
            child = self.child
            self.write("quit")
            try:
                child.stdin.close()
            except BrokenPipeError:
                pass
            try:
                child.wait(timeout=9)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait()
            child.stdout.close()
            self.child = None

    def loop(self, stdin):
        # 二进制输入由读线程独占，终端 EOF 与 quit 的退出路径相同。
        threading.Thread(target=lines, args=(stdin, self.inbox, "stdin"), daemon=True).start()
        try:
            self.begin()
            while True:
                try:
                    source, msg = self.inbox.get(timeout=2)
                except queue.Empty:
                    self.write("status")
                    continue
                if source == "stdin":
                    if msg is None or msg.get("command") == "quit":
                        break
                    self.command(msg)
                elif source is self.child:
                    if msg is None:
                        self.stop()
                        self.send("error", message="本机服务意外退出，请重启")
                    elif "sync" in msg:
                        self.send("sync", **msg["sync"])
        finally:
            self.stop()


def run(bundle):
    try:
        data = data_directory()
        data.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(data / "desktop.lock", timeout=0) as lock:
            try:
                lock.execute("BEGIN IMMEDIATE")
            except sqlite3.OperationalError:
                emit("error", message="此数据目录已有桌面应用运行")
                return
            # 单独的流不占用解释器退出时要关闭的标准输入缓冲锁。
            with os.fdopen(os.dup(sys.stdin.fileno()), "rb", buffering=0) as stdin:
                Controller(bundle, data).loop(stdin)
    except (ValueError, OSError, sqlite3.Error, KeyError, subprocess.SubprocessError):
        emit("error", message="启动器无法继续，请检查数据目录与安装包后重试")
