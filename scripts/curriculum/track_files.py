"""内容校验与平台共用 track.yaml 的格式、阶段顺序和语言。"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "server"))
from app.tracks import Track, load_tracks, normalize_stage


def active_tracks(language: str) -> list[Track]:
    tracks, errors = load_tracks(ROOT / "problems")
    if errors:
        raise SystemExit("\n".join(f"{e.path}：{e.message}" for e in errors))
    return [t for t in tracks.values() if t.language == language and t.status == "active"]


def stage_dirs(tracks: list[Track]) -> list[Path]:
    return [ROOT / "problems" / track.id / stage for track in tracks for stage in track.stages]


def lesson_files(tracks: list[Track]) -> list[Path]:
    return [path for track in tracks
            for path in sorted((ROOT / "problems" / track.id / "lessons").glob("*/lesson.yaml"))]

