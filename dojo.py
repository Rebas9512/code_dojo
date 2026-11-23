"""code-dojo 本机启动器。可直接执行 uv run dojo.py。"""

from __future__ import annotations

import argparse
import errno
import hashlib
import json
import os
import shutil
import signal
import socket
import sqlite3
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path

from bootstrap.agents import has_agent

ROOT = Path(__file__).resolve().parent
SERVER = ROOT / "server"
BACKEND_PYTHON = SERVER / (".venv/Scripts/python.exe" if os.name == "nt" else ".venv/bin/python")
WEB = ROOT / "web"
SQL = ROOT / "scripts/curriculum"
HOST = "127.0.0.1"

INSTALL = {
    "git": ("sudo apt install git", "brew install git", "winget install Git.Git"),
    "uv": ("curl -LsSf https://astral.sh/uv/install.sh | sh", "brew install uv", "winget install astral-sh.uv"),
    "Node.js 22.13+ 和 npm": ("sudo snap install node --classic --channel=24/stable", "brew install node",
                            "winget install OpenJS.NodeJS.LTS"),
}


def say(message: str) -> None:
    print(message, flush=True)


def data_directory() -> Path:
    if override := os.environ.get("CODE_DOJO_DATA"):
        return Path(override).expanduser().resolve()
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA") or Path.home() / "AppData/Roaming")
    elif sys.platform == "darwin":
        base = Path.home() / "Library/Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share")
    return base / "code-dojo"


def dependencies() -> bool:
    node = shutil.which("node")
    version = ""
    if node:
        version = subprocess.check_output([node, "--version"], text=True).strip()
    digits = version.lstrip("v").split(".")
    node_ok = len(digits) >= 2 and all(n.isdigit() for n in digits[:2]) and tuple(map(int, digits[:2])) >= (22, 13)
    checks = {"git": shutil.which("git"), "uv": shutil.which("uv"),
              "Node.js 22.13+ 和 npm": version if node_ok and shutil.which("npm") else None}
    for name, value in checks.items():
        say(f"{name}　{value or '缺少或版本过低'}")
        if not value:
            for platform, command in zip(("Linux（Ubuntu）", "macOS（Homebrew）", "Windows"), INSTALL[name]):
                say(f"  {platform}　{command}")
    if not has_agent():
        say("未找到 Claude Code 或 Codex，AI 助教会关闭")
    elif os.environ.get("CODE_DOJO_AI_PROVIDER") == "off":
        say("AI 助教已关闭")
    else:
        say("已找到本机 AI 助教")
    return all(checks.values())


def pull_bank(skip: bool) -> None:
    if skip:
        say("已按 --no-pull 跳过题库同步")
    elif subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT):
        say("工作区有本地改动，跳过题库同步")
    else:
        say("同步题库")
        try:
            subprocess.run(["git", "pull", "--ff-only"], cwd=ROOT, check=True)
        except subprocess.CalledProcessError:
            say("题库未能快进更新，本次使用本地版本")


def installed_lock(directory: Path, lock: bytes) -> bool:
    # 首次启动可接管此前用 npm ci/install 装好的依赖。隐藏锁只包含本机平台需要的包。
    hidden = directory / "node_modules/.package-lock.json"
    if not hidden.is_file():
        return False
    try:
        wanted = json.loads(lock)["packages"]
        installed = json.loads(hidden.read_bytes())["packages"]
        return all(key in wanted and all(wanted[key].get(k) == pkg.get(k) for k in ("version", "integrity"))
                   for key, pkg in installed.items()) and all(
                       not key or pkg.get("optional") or key in installed for key, pkg in wanted.items())
    except (ValueError, KeyError):
        return False


def prepare_node(directory: Path) -> None:
    lock = (directory / "package-lock.json").read_bytes()
    digest = hashlib.sha256(lock).hexdigest()
    stamp = directory / "node_modules/.dojo-lock"
    current = stamp.read_text(encoding="utf-8") == digest if stamp.exists() else installed_lock(directory, lock)
    if not current:
        say(f"安装 {directory.name} 的 Node 依赖")
        subprocess.run([shutil.which("npm"), "ci"], cwd=directory, check=True)
    if not current or not stamp.exists():
        stamp.write_text(digest, encoding="utf-8")


def needs_build(web: Path) -> bool:
    index = web / "dist/index.html"
    if not index.is_file():
        return True
    built = index.stat().st_mtime_ns
    inputs = [web / name for name in ("src", "public", "index.html", "package.json", "package-lock.json",
                                      "tsconfig.json", "vite.config.ts")]
    for entry in inputs:
        if entry.exists() and entry.stat().st_mtime_ns > built:
            return True
        if entry.is_dir() and any(p.stat().st_mtime_ns > built for p in entry.rglob("*")):
            return True
    return False


def bind_port(port: int) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        if os.name == "nt":
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        try:
            sock.bind((HOST, port))
        except OSError as exc:
            if exc.errno not in (errno.EADDRINUSE, errno.EACCES):
                raise
            sock.bind((HOST, 0))
            say(f"端口 {port} 不可用，改用 {sock.getsockname()[1]}")
        return sock
    except BaseException:
        sock.close()
        raise


def serve() -> int:
    import uvicorn
    from app.main import app, progress_sync

    port = int(os.environ.get("CODE_DOJO_PORT", "8765"))
    if not 0 <= port <= 65535:
        raise ValueError("CODE_DOJO_PORT 必须在 0 到 65535 之间")
    with bind_port(port) as sock:
        url = f"http://{HOST}:{sock.getsockname()[1]}"
        say("同步进度" if os.environ.get("CODE_DOJO_SYNC_REPO") else "未开启同步，进度保存在本机")

        class LocalServer(uvicorn.Server):
            last_interrupt = 0.0

            def handle_exit(self, sig, frame):
                # 终端和 uv 可能转发同一次 Ctrl+C，两次紧邻的信号只发起一次正常退出。
                if sig == signal.SIGINT:
                    current = time.monotonic()
                    if current - self.last_interrupt < 0.25:
                        return
                    self.last_interrupt = current
                super().handle_exit(sig, frame)

            async def startup(self, sockets=None):
                await super().startup(sockets=sockets)
                if self.started:
                    say(f"本机服务已就绪，打开浏览器 {url}")
                    threading.Thread(target=webbrowser.open, args=(url,), daemon=True).start()

        try:
            LocalServer(uvicorn.Config(app, host=HOST, port=sock.getsockname()[1],
                                       proxy_headers=False)).run(sockets=[sock])
        finally:
            # 终端和外层启动器可能连续转发中断，Uvicorn 此时会跳过 lifespan 的关闭阶段。
            progress_sync.close()
    return 0


def backend(args: list[str]) -> int:
    command = [str(BACKEND_PYTHON), str(ROOT / "dojo.py"), *args]
    if os.name != "nt":
        os.execv(command[0], command)
    with subprocess.Popen(command) as child:
        try:
            return child.wait()
        except KeyboardInterrupt:
            return child.wait()


def import_legacy(directory: Path) -> None:
    from app.db import Store
    source = directory / "code_dojo.db"
    destination = data_directory() / "code_dojo.db"
    if not source.is_file():
        raise ValueError("旧数据目录中没有 code_dojo.db")
    if destination.exists() and source.samefile(destination):
        raise ValueError("旧库和目标库必须在不同目录")
    say(f"导入了 {Store(destination).import_legacy(directory)} 条历史事件")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="启动本机练习网站")
    parser.add_argument("--no-pull", action="store_true", help="跳过代码和题库同步")
    commands = parser.add_subparsers(dest="command")
    commands.add_parser("doctor", help="检查本机环境")
    commands.add_parser("import-legacy", help="导入旧版做题记录").add_argument("directory", type=Path)
    args = parser.parse_args(argv)
    say("检查运行环境")
    ready = dependencies()
    directory = data_directory()
    say(f"数据目录　{directory}")
    if args.command == "doctor":
        say("后端环境　" + ("已就绪" if BACKEND_PYTHON.is_file() else "启动时安装"))
        for project, label in ((WEB, "前端依赖"), (SQL, "SQL 运行器依赖")):
            say(label + "　" + ("已安装" if (project / "node_modules").is_dir() else "启动时安装"))
        say("进度同步　" + ("已配置" if os.environ.get("CODE_DOJO_SYNC_REPO") else "未开启"))
        say("网页构建　" + ("待构建" if needs_build(WEB) else "已就绪"))
        return 0 if ready else 1
    if not ready:
        return 1
    os.environ["CODE_DOJO_DATA"] = str(directory)
    os.environ["CODE_DOJO_AUTH"] = "off"
    os.environ["CODE_DOJO_WEB_DIST"] = str(WEB / "dist")
    if not has_agent():
        os.environ["CODE_DOJO_AI_PROVIDER"] = "off"
    if not args.command:
        pull_bank(args.no_pull)
    say("准备后端依赖")
    subprocess.run(["uv", "sync"], cwd=SERVER, check=True)
    if args.command == "import-legacy":
        return backend(["--import", str(args.directory.resolve())])
    say("检查前端与 SQL 运行器依赖")
    prepare_node(WEB)
    prepare_node(SQL)
    if needs_build(WEB):
        say("构建前端页面")
        subprocess.run([shutil.which("npm"), "run", "build"], cwd=WEB, check=True)
    return backend(["--serve"])


if __name__ == "__main__":
    try:
        sys.path.insert(0, str(SERVER))
        if sys.argv[1:] == ["--serve"]:
            sys.exit(serve())
        if len(sys.argv) == 3 and sys.argv[1] == "--import":
            import_legacy(Path(sys.argv[2]))
        else:
            sys.exit(main())
    except KeyboardInterrupt:
        pass
    except (OSError, ValueError, sqlite3.Error, subprocess.SubprocessError) as exc:
        sys.exit(f"启动失败：{exc}")
