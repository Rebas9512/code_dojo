"""桌面数据目录与持久化的解锁次数，旧调用方仍可从此模块导入。"""

import json
import os
import sys
import time
from pathlib import Path

from .update import atomic_json


def data_directory() -> Path:
    if override := os.environ.get("CODE_DOJO_DATA"):
        return Path(override).expanduser().resolve()
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA") or Path.home() / "AppData/Roaming")
    elif sys.platform == "darwin":
        base = Path.home() / "Library/Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share")
    return base / "code-dojo"


class UnlockAttempts:
    """同一数据目录在关闭窗口或重启应用后仍保留冷却时间。"""

    def __init__(self, data: Path):
        self.path = data / "unlock-attempts.json"

    def state(self) -> tuple[int, float]:
        if self.path.exists():
            record = json.loads(self.path.read_bytes())
            remaining = record["until"] - time.time()
            if remaining > 0 or record["count"] < 5:
                return record["count"], max(0, remaining)
        return 0, 0

    def failed(self) -> None:
        count, _ = self.state()
        atomic_json(self.path, {"count": count + 1, "until": time.time() + 30 if count >= 4 else 0})

    def clear(self) -> None:
        self.path.unlink(missing_ok=True)
