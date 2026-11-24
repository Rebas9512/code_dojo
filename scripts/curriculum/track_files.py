"""内容校验与平台共用 track.yaml 的格式、阶段顺序和语言。"""

from pathlib import Path
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "server"))
from app.tracks import Track, load_tracks, normalize_stage


def bank_root() -> Path:
    return Path(os.environ.get("CODE_DOJO_PROBLEMS", ROOT / "problems"))


def verify_projects(language: str, tracks: list[Track], only: str) -> int:
    if not any(t.project_stage for t in tracks):
        return 0
    # 项目使用平台的真实 harness / PGlite，完整脚本同时验证一次。
    python = ROOT / "server/.venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    return subprocess.run([str(python) if python.exists() else sys.executable, str(ROOT / "scripts/verify_bank.py"),
                           "--projects", language, "--only", only]).returncode


def active_tracks(language: str) -> list[Track]:
    tracks, errors = load_tracks(bank_root())
    if errors:
        raise SystemExit("\n".join(f"{e.path}：{e.message}" for e in errors))
    return [t for t in tracks.values() if t.language == language and t.status == "active"]


def stage_dirs(tracks: list[Track]) -> list[Path]:
    return [bank_root() / track.id / stage for track in tracks for stage in track.stages if stage != track.project_stage]


def lesson_files(tracks: list[Track]) -> list[Path]:
    return [path for track in tracks
            for path in sorted((bank_root() / track.id / "lessons").glob("*/lesson.yaml"))]

