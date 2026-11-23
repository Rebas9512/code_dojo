"""桌面安装包和本地启动器的助教命令探测，只使用标准库。"""

import os
import platform
import re
import shutil
import sys
from pathlib import Path


def find_codex(binary: str) -> str | None:
    if path := shutil.which(binary):
        return path
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


def has_agent() -> bool:
    return bool(shutil.which(os.environ.get("CODE_DOJO_CLAUDE_BIN", "claude"))
                or find_codex(os.environ.get("CODE_DOJO_CODEX_BIN", "codex")))
