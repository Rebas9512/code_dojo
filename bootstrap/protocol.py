"""Electron 与启动器的逐行 JSON 协议。只有主线程操作子进程或写事件。"""

import json
import math
import os
import queue
import sqlite3
import subprocess
import sys
import threading
from pathlib import Path

from cryptography.exceptions import InvalidTag

from . import DEFAULT_REPO, DEFAULT_SYNC, VERSION
from .agents import BIN_VARS, service_agents, set_manual_path
from .credentials import clear_tokens, tokens
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
        self.agents = {}
        self.values = {}
        self.item = None

    def begin(self):
        self.status("正在检查本机凭据…")
        self.values = tokens(self.data)
        self.launch()

    def status(self, message):
        self.send("status", message=message)

    def sync_code_failed(self):
        count, wait = self.attempts.state()
        self.send("sync_code_failed", remaining=max(0, 5 - count), wait=math.ceil(wait))

    def connect_sync(self, code):
        envelope = self.bundle / "sealed-tokens.json"
        if not envelope.is_file():
            self.send("error", scope="settings", message="这个安装包不支持同步码")
            return
        if self.attempts.state()[1]:
            self.sync_code_failed()
            return
        try:
            values = unseal(json.loads(envelope.read_bytes()), code, self.repo, self.sync_repo)
        except InvalidTag:
            self.attempts.failed()
            self.sync_code_failed()
            return
        except (OSError, TypeError, ValueError):
            self.send("error", scope="settings", message="令牌包无效或与仓库不匹配")
            return
        notice = ""
        try:
            tokens(self.data, values)
        except PermissionError:
            notice = "此数据目录无法保护令牌，令牌仅用于本次运行"
        self.values = values
        self.attempts.clear()
        self.restart_service(notice)

    def disconnect_sync(self):
        try:
            clear_tokens(self.data)
        except Exception:
            # 钥匙串后端的异常类型因平台而异，清除失败时继续使用现有服务。
            self.send("error", scope="settings", message="无法清除已存凭据，请检查钥匙串和数据目录后重试")
            return
        self.values = {}
        self.restart_service()

    def restart_service(self, notice=""):
        self.status("正在重新启动本机服务…")
        self.stop("quit" if self.values else "disconnect")
        if self.start(self.updates(), self.item):
            self.ready(notice)
        else:
            self.send("error", message="本机服务启动失败，请重试")

    def command(self, message):
        name = message.get("command")
        if name == "connect_sync" and self.child and isinstance(message.get("code"), str):
            self.connect_sync(message["code"])
        elif name == "disconnect_sync" and self.child:
            self.disconnect_sync()
        elif name in ("set_agent_path", "reset_agent_path") and self.child and message.get("agent") in tuple(BIN_VARS):
            agent = message["agent"]
            if name == "set_agent_path" and not isinstance(message.get("path"), str):
                self.send("error", scope="settings", agent=agent, message="请输入命令的完整路径")
                return
            try:
                set_manual_path(self.data, agent, message["path"] if name == "set_agent_path" else None)
            except ValueError as exc:
                self.send("error", scope="settings", agent=agent, message=str(exc))
                return
            except OSError:
                self.send("error", scope="settings", agent=agent, message="无法写入本机的助教设置")
                return
            self.restart_service()
        elif name == "sync":
            self.write("sync")
            self.write("status")
        elif name == "check_update":
            self.update()
        else:
            self.send("error", message="无法识别该桌面指令")

    def updates(self):
        return Updates(self.data, self.bundle, GitHub(self.repo, self.values.get("code", ""), self.api))

    def launch(self):
        self.update(on_launch=True)

    def ready(self, message="", installer=""):
        enabled = os.environ.get("CODE_DOJO_AI_PROVIDER") != "off" and any(a["path"] for a in self.agents.values())
        self.send("ready", port=self.port, version=VERSION, payload_version=self.item.manifest["version"],
                  ai=enabled, agents=self.agents, sync=bool(self.sync_token), message=message, installer=installer)
        self.write("status")

    def update(self, *, on_launch=False):
        self.status("正在检查更新…")
        updates = self.updates()
        if on_launch:
            updates.clean()
        previous = updates.current()
        result = updates.check(self.status, on_launch=on_launch)
        detail = result.message
        if not result.active:
            self.send("error", message=detail or "尚未安装题库", installer=result.installer)
            return
        if self.child and self.item == result.active:
            self.send("status", message=detail or "题库已是最新版本", installer=result.installer, checked=True)
            return
        self.stop()
        self.status("正在启动本机服务…")
        if not self.start(updates, result.active):
            if not previous or previous == result.active or not self.start(updates, previous):
                self.send("error", message="本机服务启动失败，请重试")
                return
            detail = "新版服务启动失败，已恢复上一版本"
        self.ready(detail, result.installer)

    @property
    def sync_token(self):
        return self.values.get("sync") or self.values.get("code", "")

    def start(self, updates, item):
        config = dict(payload=str(item.root), libraries=str(updates.libraries(item.manifest)), data=str(self.data),
                      api=self.api, repo=self.sync_repo, token=self.sync_token)
        script = self.bundle / "start.py"
        if not script.is_file():
            script = self.bundle / "scripts/desktop/start.py"
        env = os.environ.copy()
        self.agents = service_agents(self.data, env)
        child = subprocess.Popen([sys.executable, "-I", "-B", "-X", "utf8", str(script)],
                                 cwd=item.root, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                 text=True, encoding="utf-8", creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        self.child = child
        self.write(json.dumps(config))
        line = child.stdout.readline()
        if not line:
            self.stop()
            return False
        self.port = json.loads(line)["ready"]
        if item != self.item:
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

    def stop(self, command="quit"):
        if self.child:
            child = self.child
            self.write(command)
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
