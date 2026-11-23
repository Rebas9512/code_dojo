"""本机专用的 uv 判题环境与子进程生命周期。"""

from __future__ import annotations

import os
import re
import shutil
import signal
import sqlite3
import subprocess
import sys
import threading
from contextlib import closing
from pathlib import Path

from .config import PROJECT_ROOT

HARNESS = PROJECT_ROOT / "judge" / "python" / "harness.py"
# 和 judge/ds/Dockerfile 锁定相同版本；macOS 的官方 wheel 没有 +cpu 后缀。
DS_PACKAGES = ("numpy==2.5.5", "pandas==3.1.1", "torch==2.15.0" + ("" if sys.platform == "darwin" else "+cpu"))
UV_HELP = (
    "找不到 uv。请安装后重新启动后端：\n"
    "Linux：curl -LsSf https://astral.sh/uv/install.sh | sh\n"
    "macOS：curl -LsSf https://astral.sh/uv/install.sh | sh\n"
    "Windows（PowerShell）：winget install --id=astral-sh.uv -e"
)


class PreparationError(RuntimeError):
    pass


class LocalEnvironments:
    def __init__(self, root: Path):
        self.root = root.absolute()
        self.preparing_ds = threading.Event()
        self._locks = {runtime: threading.Lock() for runtime in ("python", "ds")}

    def _directory(self, runtime: str) -> Path:
        if runtime == "python":
            return self.root / "python-3.14"
        versions = "-".join(package.split("==")[1] for package in DS_PACKAGES)
        return self.root / f"ds-3.14-{versions}"

    def interpreter(self, runtime: str) -> Path:
        directory = self._directory(runtime)
        python = directory / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        ready = directory / ".ready"
        if ready.is_file() and python.is_file():
            return python
        uv = shutil.which("uv")
        if not uv:
            raise PreparationError(UV_HELP)
        with self._locks[runtime]:
            if runtime == "ds":
                self.preparing_ds.set()
            try:
                self.root.mkdir(parents=True, exist_ok=True)
                # 服务和 verify_bank 可能同时首次安装；退出或崩溃后 SQLite 自动释放锁。
                with closing(sqlite3.connect(self.root / (runtime + ".lock"), timeout=1800)) as lock:
                    lock.execute("BEGIN IMMEDIATE")
                    if ready.is_file() and python.is_file():
                        return python
                    # uv venv 会复用 uv 管理的 3.14，缺少时自动执行 Python 下载与安装。
                    self._run_uv([uv, "venv", "--managed-python", "--python", "3.14", "--clear", str(directory)])
                    if runtime == "ds":
                        self._run_uv([uv, "pip", "install", "--compile-bytecode", "--python", str(python),
                                      "--torch-backend", "cpu", *DS_PACKAGES])
                    ready.touch()
            except (OSError, sqlite3.Error, subprocess.SubprocessError) as exc:
                reason = getattr(exc, "stderr", None) or str(exc)
                label = "数据科学" if runtime == "ds" else "Python"
                raise PreparationError(f"准备{label}判题环境失败，请检查网络、磁盘空间及 uv 版本后重试。\n{reason[-1800:]}") from exc
            finally:
                if runtime == "ds":
                    self.preparing_ds.clear()
        return python

    def ds_state(self) -> str:
        if self.preparing_ds.is_set():
            return "preparing"
        return "ready" if (self._directory("ds") / ".ready").is_file() else "unprepared"

    def _run_uv(self, args: list[str]) -> None:
        subprocess.run(args, cwd=self.root, capture_output=True, encoding="utf-8",
                       errors="replace", check=True, timeout=900)


def memory_bytes(value: str) -> int:
    match = re.fullmatch(r"(\d+(?:\.\d+)?)\s*(b|[kmgtp](?:i?b)?)?", value.strip().lower())
    if not match:
        raise ValueError(f"无效的判题内存上限：{value}")
    unit = (match[2] or "b")[0]
    return int(float(match[1]) * 1024 ** "bkmgtp".index(unit))


def run_local(python: Path, work: Path, budget_s: float, memory: str) -> subprocess.CompletedProcess:
    # 用户代码只继承基本系统变量；临时文件、第三方库的缓存均留在本次工作目录。
    env = {key: os.environ[key] for key in ("PATH", "LANG", "SystemRoot", "WINDIR", "ProgramFiles", "ComSpec")
           if key in os.environ}
    env.update({key: str(work) for key in ("HOME", "USERPROFILE", "TEMP", "TMP", "TMPDIR", "XDG_CACHE_HOME")})
    if os.name == "nt":
        env.update(APPDATA=str(work), LOCALAPPDATA=str(work))
    env.update(OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1", MALLOC_ARENA_MAX="1")
    cmd = [str(python), "-I", "-B", "-X", "utf8", str(HARNESS), "job.json", str(memory_bytes(memory))]
    # 文件不会像管道那样因后台子进程继承写端而无限等待 EOF。
    with (work / "stdout").open("w+b") as stdout, (work / "stderr").open("w+b") as stderr:
        with subprocess.Popen(cmd, cwd=work, env=env, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
                              start_new_session=os.name != "nt",
                              creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0) as proc:
            try:
                proc.wait(timeout=budget_s)
            finally:
                if os.name == "nt":
                    if proc.poll() is None:
                        try:
                            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                                           capture_output=True, timeout=5)
                        except (OSError, subprocess.TimeoutExpired):
                            pass  # 仍终止解释器，Windows Job 随它退出。
                        finally:
                            proc.kill()
                else:
                    try:
                        os.killpg(proc.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
        stdout.seek(0)
        stderr.seek(0)
        return subprocess.CompletedProcess(cmd, proc.returncode, stdout.read().decode("utf-8", "replace"),
                                           stderr.read().decode("utf-8", "replace"))
