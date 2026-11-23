"""运行配置：全部可以用环境变量覆盖。"""

from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    problems_dir: Path
    data_dir: Path
    judge_image: str
    judge_mode: str
    judge_envs: Path
    judge_tmp: Path
    judge_concurrency: int
    ds_image: str
    ds_memory: str
    ds_time_limit_ms: int
    ai_provider: str          # claude | off
    claude_bin: str
    ai_model: str
    ai_effort: str
    ai_workdir: Path
    auth_enabled: bool
    session_days: int
    web_dist: Path | None
    sync_repo: str = ""


def load_settings() -> Settings:
    env = os.environ.get
    judge_mode = env("CODE_DOJO_JUDGE", "auto")
    if judge_mode not in ("auto", "docker", "local"):
        raise ValueError("CODE_DOJO_JUDGE 只能是 auto、docker 或 local")
    data_dir = Path(env("CODE_DOJO_DATA", PROJECT_ROOT / "server" / "data"))
    auth = env("CODE_DOJO_AUTH", "off")
    if auth not in ("on", "off"):
        raise ValueError("CODE_DOJO_AUTH 只能是 on 或 off")
    session_days = int(env("CODE_DOJO_SESSION_DAYS", "30"))
    if session_days < 1:
        raise ValueError("CODE_DOJO_SESSION_DAYS 必须是正整数")
    return Settings(
        problems_dir=Path(env("CODE_DOJO_PROBLEMS", PROJECT_ROOT / "problems")),
        data_dir=data_dir,
        judge_mode=judge_mode,
        judge_envs=Path(env("CODE_DOJO_JUDGE_ENVS", data_dir / "judge-envs")),
        judge_image=env("CODE_DOJO_JUDGE_IMAGE", "code-dojo-judge-py:3.14"),
        judge_tmp=Path(env("CODE_DOJO_JUDGE_TMP", Path(tempfile.gettempdir()) / "code-dojo-judge")),
        judge_concurrency=int(env("CODE_DOJO_JUDGE_CONCURRENCY", "2")),
        ds_image=env("CODE_DOJO_DS_IMAGE", "code-dojo-judge-ds:3.14"),
        ds_memory=env("CODE_DOJO_DS_MEMORY", "1g"),
        ds_time_limit_ms=int(env("CODE_DOJO_DS_TIME_LIMIT_MS", "10000")),
        ai_provider=env("CODE_DOJO_AI_PROVIDER", "claude"),
        claude_bin=env("CODE_DOJO_CLAUDE_BIN", "claude"),
        ai_model=env("CODE_DOJO_AI_MODEL", "claude-opus-5-5"),
        ai_effort=env("CODE_DOJO_AI_EFFORT", "low"),
        ai_workdir=Path(env("CODE_DOJO_AI_WORKDIR", Path(tempfile.gettempdir()) / "code-dojo-ai")),
        auth_enabled=auth == "on",
        session_days=session_days,
        web_dist=Path(dist) if (dist := env("CODE_DOJO_WEB_DIST")) else None,
        sync_repo=env("CODE_DOJO_SYNC_REPO", "").strip(),
    )
