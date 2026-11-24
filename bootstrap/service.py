"""桌面后端子进程：启动参数和控制指令走父子管道，端口由操作系统分配。"""

import errno
import json
import os
import socket
import sys
import tempfile
import threading
from pathlib import Path

from .agents import has_agent
from .github import GitHub
from .update import atomic_json


def judge_python(data: Path) -> str:
    bundle = Path(__file__).resolve().parents[1]
    if not (sys.platform.startswith("linux") and (bundle / "python/bin/python3").is_file()):
        return sys.executable
    # venv 保存解释器的绝对路径。窗口持有实例锁时，将固定链接指向本次挂载。
    desktop = data / "desktop"
    link = desktop / f"python-{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    with tempfile.TemporaryDirectory(dir=desktop) as tmp:
        pending = Path(tmp) / "python"
        pending.symlink_to(bundle / "python", target_is_directory=True)
        pending.replace(link)
    return str(link / "bin/python3")


def serve() -> None:
    from_bootstrap = json.loads(sys.stdin.readline())
    payload = Path(from_bootstrap["payload"])
    data = Path(from_bootstrap["data"])
    os.chdir(payload)
    sys.path[:0] = [str(payload / "server"), from_bootstrap["libraries"]]
    os.environ.update(CODE_DOJO_DATA=str(data), CODE_DOJO_PROBLEMS=str(payload / "problems"),
                      CODE_DOJO_WEB_DIST=str(payload / "web/dist"), CODE_DOJO_SQL_CACHE=str(payload / "sql-cache"),
                      CODE_DOJO_JUDGE="local", CODE_DOJO_AUTH="off", CODE_DOJO_DESKTOP_PYTHON=judge_python(data),
                      CODE_DOJO_JUDGE_ENVS=str(data / "judge-envs"),
                      CODE_DOJO_SYNC_REPO=f"https://github.com/{from_bootstrap['repo']}.git" if from_bootstrap["token"] else "")
    # venv 的 ensurepip 子进程也从只读安装包导入标准库。
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    os.environ.setdefault("CODE_DOJO_JUDGE_TMP", str(data / "judge-tmp"))
    os.environ.setdefault("CODE_DOJO_BANK_WATCH", "off")  # 题库随更新包整体替换，运行中不会改，不用后台扫文件
    os.environ.setdefault("CODE_DOJO_AI_WORKDIR", str(data / "desktop/ai"))
    tmp = data / "desktop/tmp"
    tmp.mkdir(exist_ok=True)
    os.environ.update(TMPDIR=str(tmp), TEMP=str(tmp), TMP=str(tmp))
    if not has_agent():
        os.environ["CODE_DOJO_AI_PROVIDER"] = "off"
    import uvicorn
    from app.main import app, progress_sync

    if from_bootstrap["token"]:
        progress_sync.github = GitHub(from_bootstrap["repo"], from_bootstrap["token"], from_bootstrap["api"])
    progress_sync.root = data / "desktop/sync"
    del from_bootstrap

    def tell(**event):
        print(json.dumps(event), flush=True)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        port_file = data / "desktop/port.json"
        saved = json.loads(port_file.read_bytes())["port"] if port_file.exists() else 0
        preferred = int(os.environ.get("CODE_DOJO_PORT", saved))
        if os.name == "nt":
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        else:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("127.0.0.1", preferred))
        except OSError as exc:
            if exc.errno not in (errno.EACCES, errno.EADDRINUSE):
                raise
            sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]

        class Server(uvicorn.Server):
            async def startup(self, sockets=None):
                await super().startup(sockets=sockets)
                if self.started:
                    atomic_json(port_file, {"port": port})
                    tell(ready=port)
                    threading.Thread(target=commands, daemon=True).start()

        server = Server(uvicorn.Config(app, host="127.0.0.1", port=port, proxy_headers=False,
                                       log_config=None, access_log=False, timeout_graceful_shutdown=10))

        def commands():
            try:
                for line in sys.stdin:
                    command = line.strip()
                    if command == "disconnect":
                        # 等正在进行的交换结束，再跳过退出推送，保留其余待推送事件。
                        with progress_sync._lock:
                            progress_sync.repo = ""
                        break
                    if command == "quit":
                        break
                    if command == "sync":
                        progress_sync.request()
                    if command == "status":
                        tell(sync=progress_sync.status())
            finally:
                # 即使父窗口意外退出，管道 EOF 也会触发最后一次推送。
                try:
                    progress_sync.close()
                finally:
                    server.should_exit = True

        server.run(sockets=[sock])
        if not server.started:
            raise RuntimeError("本机服务启动失败")
