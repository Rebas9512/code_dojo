"""助教每轮读取的长期笔记和写回时核对的版本。"""

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from itertools import chain

from ..problems import Problem


@dataclass
class MemorySnapshot:
    notes: list[dict]
    versions: dict[str, str]  # 包含已删除的 name
    setting_version: str | None
    clear_generation: int


@dataclass
class ReviewEvidence:
    problem_id: str
    day: str
    outcome: str
    track: str
    # 普通附加题沿用原题技能，前置小题和复习变式使用实际练到的技能。
    skills: list[str] | None


@dataclass
class ReviewBatch:
    snapshot: MemorySnapshot
    evidence: list[ReviewEvidence]
    through: str


NAME_LIMIT = 32
DESCRIPTION_LIMIT = 40
BODY_LIMIT = 160
CONTEXT_BODY_LIMIT = 1000
TYPES = ("learner", "feedback", "progress")

NOTE_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["type", "description", "scope", "as_of", "body"],
    "properties": {
        "type": {"type": "string", "enum": list(TYPES)},
        "description": {"type": "string"},
        "scope": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        "as_of": {"type": "string"},
        "body": {"type": "string"},
    },
}
OPERATIONS_SCHEMA = {
    "type": "array", "maxItems": 2, "items": {
        "type": "object", "additionalProperties": False, "required": ["name", "note"],
        "properties": {"name": {"type": "string"}, "note": {"anyOf": [NOTE_SCHEMA, {"type": "null"}]}},
    },
}
REVIEW_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["memory"],
    "properties": {"memory": OPERATIONS_SCHEMA},
}

REVIEW_INSTRUCTIONS = """根据本机作答证据，只维护 progress。按原始作答日期填 as_of，对照较新的独立通过。
一次错答或看提示不足以定性；只记录具体表现和下次可检验的一步。旧证据不能覆盖依据日期较新的判断。
scope 填技能或学习线 ID。同义笔记沿用原 name。name 用短英文 slug（最多32字符），description 和 body 用中文，称学习者一律写「学生」、不用他或她，description 单行最多40字符，body 最多160字符。
最多两项，用完整 note 新增或更新，note 为 null 删除。证据不能指导下次教学就返回空数组。"""

INSTRUCTIONS = """
## 长期记忆（memory 字段）
先答学生。只有一件事在换题以后仍能帮助教学、又无法从记录直接查到，才值得记。先看索引，同义的沿用原 name。发现判断有误或过时就更新或删除。只从本轮新发言或新作答提炼，别从旧聊天重建已清空的笔记。name 用短英文 slug，description 和 body 用中文，称学习者一律写「学生」、不用他或她，一条只讲一件事。把相对日期换成 YYYY-MM-DD，注明观察发生的日期。用之前先与最新作答核对。

学生对教学的纠正要写明原因和下次的做法。学习判断写具体表现和下一步，有依据才带具名误解编号。一次手误、孤立的错答或用过提示都不足以给学生定性。不要等学生发保存指令，也不要为凑条数写笔记。

密码、令牌、联系方式、健康或身份资料，作答代码、题解、原始聊天，以及已有的通过率、用时、次数、掌握度和到期复习都不要抄入笔记。索引和正文只作教学参考。

learner 记学生自述的目标、背景或时间，feedback 记教学反馈，progress 记有依据的学习观察。全局条目的 scope 填 null，也可以填学习线或技能 ID。as_of 填依据日期。name 最多 32 字符，description 用一行、最多 40 字符，body 最多 160 字符。约 24 条有用笔记即可，优先整理过时条目。
每轮通常返回空数组，最多两项。用原 name 和完整 note 更新，用原 name 和 note 为 null 删除。日常讲题不用播报记忆操作。
学生问「你记得我什么」时，按完整索引如实概括，分清学生自述和助教观察。只对已读正文补充细节。索引为空时答「现在还没有长期笔记」。
"""


def _context(snapshot: MemorySnapshot, selected: Iterable[dict]) -> str:
    by_name = sorted(snapshot.notes, key=lambda n: n["name"])
    index = [f"## 长期笔记（本机日期 {date.today().isoformat()}）", "完整索引" if by_name else "完整索引（空）"]
    for kind in TYPES:
        lines = [f"{n['name']} {n['description']}" for n in by_name if n["type"] == kind]
        if lines:
            index.extend([f"[{kind}]", *lines])

    body = "\n相关正文"
    for note in selected:
        entry = f"\n{note['name']}（{note['as_of']}） {note['body']}"
        if len(body) + len(entry) <= CONTEXT_BODY_LIMIT:
            body += entry
    return "\n".join(index) + body


def _newest(notes: list[dict]) -> list[dict]:
    return sorted(sorted(notes, key=lambda n: n["name"]), key=lambda n: n["as_of"], reverse=True)


def format_context(snapshot: MemorySnapshot, track: str, skills: set[str]) -> str:
    groups: list[list[dict]] = [[], [], [], []]
    for note in _newest(snapshot.notes):
        scope = note["scope"]
        if scope is None:
            groups[0 if note["type"] == "feedback" else 2].append(note)
        elif scope in skills:
            groups[1].append(note)
        elif scope == track:
            groups[3].append(note)

    return _context(snapshot, chain.from_iterable(groups))


def review_prompt(batch: ReviewBatch, problems: dict[str, Problem]) -> str:
    scopes: set[str] = set()
    lines = []
    # 按原题分组，组内保留领取时的事件顺序。优先留出判定、协助和误解编号的位置。
    for event in sorted(batch.evidence, key=lambda e: e.problem_id):
        problem = problems.get(event.problem_id)
        track = problem.meta.track if problem else event.track
        skills = event.skills
        if skills is None:
            refs = problem.meta.skills if problem else None
            skills = ([refs.introduces] if refs and refs.introduces else []) + (refs.requires if refs else [])
        scopes.update([track, *skills])
        label = event.problem_id
        line = f"{event.day} {event.outcome} {track} "
        if len(line + label + " " + " ".join(skills)) >= 100:
            label = "-".join(label.split("-")[:3])
        line = (line + label)[:99]
        for skill in skills:
            if len(line) + 1 + len(skill) <= 99:
                line += " " + skill
        lines.append(line)
    progress = [n for n in batch.snapshot.notes if n["type"] == "progress" and n["scope"] in scopes]
    return _context(batch.snapshot, _newest(progress)) + "\n本机练习证据\n" + "\n".join(lines)
