"""学习线配置。平台与独立的内容检查脚本共用，只依赖 PyYAML。"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


def normalize_stage(v: Any) -> str:
    """数字和带引号的阶段 id 等价，0a / 0b 沿用大写写法。"""
    return str(v).upper() if str(v).lower() in ("0a", "0b") else str(v)


@dataclass
class Track:
    id: str
    name: str
    summary: str
    order: int
    language: str
    runtime: str
    status: str
    requires: list[str]
    skill_prefix: str
    stages: dict[str, str]  # 按学习顺序保留阶段 id 和名称
    units: dict[str, dict[int, str]] = field(default_factory=dict)


@dataclass
class LoadError:
    path: str
    message: str


def load_track(path: Path) -> Track:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or raw.get("id") != path.parent.name:
        raise ValueError(f"学习线 id 应和目录名 {path.parent.name} 相同")
    for key in ("name", "summary", "skill_prefix"):
        if not isinstance(raw.get(key), str) or not raw[key].strip():
            raise ValueError(f"{key} 必须是非空文字")
    for key, choices in (("language", ("python", "sql", "none")), ("runtime", ("python", "pglite", "ds", "none")),
                         ("status", ("active", "planned"))):
        if raw.get(key) not in choices:
            raise ValueError(f"{key} 应为 {' / '.join(choices)}")
    if type(raw.get("order")) is not int:
        raise ValueError("order 必须是整数")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", raw["skill_prefix"]):
        raise ValueError("skill_prefix 必须是小写字母、数字或连字符")
    if not isinstance(raw.get("requires"), list) or not all(isinstance(t, str) and t for t in raw["requires"]):
        raise ValueError("requires 必须是学习线 id 列表")
    if not isinstance(raw.get("stages"), list) or not raw["stages"]:
        raise ValueError("stages 必须是非空阶段列表")
    stages = {}
    units = {}
    for stage in raw["stages"]:
        if not isinstance(stage, dict) or not isinstance(stage.get("name"), str) or not stage["name"].strip():
            raise ValueError("阶段缺少名称")
        value = stage.get("id")
        if type(value) not in (int, str) or not str(value).strip():
            raise ValueError(f"阶段 id 无效：{value!r}")
        sid = normalize_stage(value)
        if sid in stages:
            raise ValueError(f"阶段 id 重复：{sid}")
        stages[sid] = stage["name"]
        names = stage.get("units", {})
        if not isinstance(names, dict) or any(
            type(group) is not int or not isinstance(name, str) or not name.strip()
            for group, name in names.items()
        ):
            raise ValueError(f"阶段 {sid} 的 units 应为整数编号到非空名称的映射")
        units[sid] = names
    return Track(
        id=raw["id"], name=raw["name"], summary=raw["summary"], order=raw["order"],
        language=raw["language"], runtime=raw["runtime"], status=raw["status"],
        requires=raw["requires"], skill_prefix=raw["skill_prefix"], stages=stages, units=units,
    )


def load_tracks(root: Path) -> tuple[dict[str, Track], list[LoadError]]:
    tracks = []
    errors = []
    for directory in sorted(root.glob("*")):
        if not directory.is_dir() or directory.name.startswith((".", "_")):
            continue
        path = directory / "track.yaml"
        try:
            tracks.append(load_track(path))
        except (OSError, ValueError, KeyError, yaml.YAMLError) as exc:
            errors.append(LoadError(str(path), str(exc)))
    tracks.sort(key=lambda t: (t.order, t.id))
    return {t.id: t for t in tracks}, errors

