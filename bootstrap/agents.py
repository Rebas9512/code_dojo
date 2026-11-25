"""桌面安装包和本地启动器的助教命令探测，只使用标准库。"""

import json
import os
import platform
import re
import shutil
import subprocess
import sys
from collections.abc import MutableMapping
from functools import cache
from pathlib import Path

from .update import atomic_json


BIN_VARS = {"claude": "CODE_DOJO_CLAUDE_BIN", "codex": "CODE_DOJO_CODEX_BIN"}


@cache
def _login_path() -> str:
    """每个启动器进程最多读一次，shell 的启动提示不能混进 PATH 或桌面协议。"""
    shell = os.environ.get("SHELL") or ("/bin/zsh" if sys.platform == "darwin" else "/bin/sh")
    command = 'printf "__CODE_DOJO_PATH_BEGIN__%s__CODE_DOJO_PATH_END__" "$PATH"'
    try:
        result = subprocess.run([shell, "-ilc", command], stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=3)
    except (OSError, subprocess.TimeoutExpired):
        return ""
    if result.returncode:
        return ""
    match = re.search(rb"__CODE_DOJO_PATH_BEGIN__(.*?)__CODE_DOJO_PATH_END__", result.stdout, re.DOTALL)
    return os.fsdecode(match[1]) if match else ""


def _extension_codex() -> str | None:
    system = {"darwin": "macos", "win32": "windows"}.get(sys.platform, sys.platform)
    machine = platform.machine().lower()
    arch = {"amd64": "x86_64", "arm64": "aarch64"}.get(machine, machine)
    exe = "codex.exe" if sys.platform == "win32" else "codex"
    extensions = Path.home() / ".vscode/extensions"
    candidates = []
    for folder in extensions.glob("openai.chatgpt-*"):
        match = re.match(r"openai\.chatgpt-(\d+(?:\.\d+)*)", folder.name)
        path = folder / "bin" / f"{system}-{arch}" / exe
        if match and path.is_file() and os.access(path, os.X_OK):
            candidates.append((tuple(map(int, match[1].split("."))), str(path)))
    return max(candidates)[1] if candidates else None


def find_agents(commands: dict[str, str], env: MutableMapping[str, str], *, try_extension: bool) -> dict[str, str | None]:
    def on_path():
        return {name: shutil.which(cmd, path=env.get("PATH")) for name, cmd in commands.items()}

    found = on_path()
    if not any(found.values()) and sys.platform in ("darwin", "linux") and (login_path := _login_path()):
        dirs = dict.fromkeys(os.get_exec_path(env) + login_path.split(os.pathsep))
        env["PATH"] = os.pathsep.join(dirs)
        found = on_path()
    if not found["codex"] and try_extension:
        found["codex"] = _extension_codex()
    return {name: os.path.abspath(path) if path else None for name, path in found.items()}


def has_agent() -> bool:
    commands = {name: os.environ.get(key, name) for name, key in BIN_VARS.items()}
    found = find_agents(commands, os.environ, try_extension=not os.path.isabs(commands["codex"]))
    for name, path in found.items():
        if path:
            os.environ.setdefault(BIN_VARS[name], path)
    return any(found.values())


def manual_paths(data: Path) -> dict[str, str]:
    file = data / "desktop/agents.json"
    return json.loads(file.read_bytes()) if file.exists() else {}


def service_agents(data: Path, env: dict[str, str]) -> dict:
    """只改本次后端的环境，下一次自动探测仍从启动器原有的环境开始。"""
    manual = manual_paths(data)
    commands = {name: env.get(key) or manual.get(name) or name for name, key in BIN_VARS.items()}
    found = find_agents(commands, env, try_extension=commands["codex"] == "codex")
    states = {}
    for name, key in BIN_VARS.items():
        source = "env" if env.get(key) else "manual" if name in manual else "auto"
        states[name] = dict(source=source, path=found[name], manual=manual.get(name))
        if found[name]:
            env[key] = found[name]
        elif source != "auto":
            # 固定到失效的指定位置，后端不会擅自换用同名命令或扩展。
            env[key] = os.path.abspath(commands[name])
    if not any(found.values()):
        env["CODE_DOJO_AI_PROVIDER"] = "off"
    return states


def checked_path(raw: str) -> str:
    path = Path(os.path.expanduser(raw.strip()))
    if not path.is_absolute():
        raise ValueError("请输入命令的完整路径")
    if not path.is_file():
        raise ValueError("这个位置没有可执行文件")
    if not os.access(path, os.X_OK):
        raise ValueError("这个文件没有执行权限")
    try:
        result = subprocess.run([str(path), "--version"], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=5,
                                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
    except subprocess.TimeoutExpired:
        raise ValueError("检查版本超过 5 秒，请确认命令的位置") from None
    except OSError:
        raise ValueError("这个文件无法执行") from None
    if result.returncode:
        raise ValueError(f"运行 --version 失败（退出码 {result.returncode}）")
    if not re.search(rb"\b[vV]?\d+(?:\.\d+)+\b", result.stdout):
        raise ValueError("--version 没有返回版本号")
    return str(path)


def set_manual_path(data: Path, name: str, path: str | None) -> None:
    manual = manual_paths(data)
    if path is None:
        manual.pop(name, None)
    else:
        manual[name] = checked_path(path)
    atomic_json(data / "desktop/agents.json", manual)
