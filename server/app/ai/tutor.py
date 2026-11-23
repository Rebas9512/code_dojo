"""AI 助教：教学辅助设定、上下文组装、回复检查。

共享编辑框（2026-11-22 用户决定："共同编辑这个能不能做成就是我们共享的一个编辑框 助手能直接查看，修改当前文本什么的就行"）：
助教看得到学生当前的代码（predict 题是学生写的预测输出），它给出的 edits 由前端直接写进编辑框，
学生可以 Ctrl+Z 撤销；AI 写过的行会标出来，提交时记 ai_lines。

教学上的约束（默认先讲思路、只补卡住的一小块、不一次写完、不透露参考解）全部写在提示词里，是软约束
（用户决定："我们尽量不做硬约束（最多改3行什么的），做成提示词的软约束就行了"）。

代码里只做技术检查：每处修改的 old 必须能在（前面几处改完之后的）内容里唯一定位；old 为空表示接在末尾。
定位不了先带着问题让 AI 重来一次，还不行就丢掉定位不了的那几处。
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from ..problems import Problem
from ..sql_judge import sample_context
from .provider import AIError, AIProvider

EDIT_ITEM = {
    "type": "object",
    "properties": {
        "old": {"type": "string"},
        "new": {"type": "string"},
        "why": {"type": "string"},
    },
    "required": ["old", "new", "why"],
    "additionalProperties": False,
}

SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "reply": {"type": "string"},
        "edits": {"type": "array", "items": EDIT_ITEM},
        "make_extra": {"type": "string"},
        "delete_extras": {"type": "array", "items": {"type": "integer"}},
    },
    "required": ["reply", "edits", "make_extra", "delete_extras"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = """你是 code-dojo 的教学助手。学生正在这个平台上从零开始学 Python 算法和 SQL。你的目标是让他自己学会、自己把代码写出来，而不是替他写完。

## 说话方式
- 用中文，口语化，简短：通常 2–6 句话。学生请你讲思路时可以多说几句，重点讲思路和步骤。
- 先直接回应学生的问题。需要时反问一个关键问题帮他想，不要连续追问。
- 以判题结果为准：没有运行通过，就不要说代码是对的。看到报错时，指出出错的位置和原因，引导他自己改。
- 你能看到参考解，它用来帮你判断学生的思路对不对、离答案还差什么。不要说"参考答案是……"，也尽量不要把参考解整段说出来。
- 题目页旁边有"课"标签，讲了这道题要用的知识点（上下文里附有内容）。学生问到概念时，沿用课里的讲法和例子来解释，需要时提醒他去看课里的哪一段。

## 共享编辑框（edits 字段）
- 你和学生共用一个编辑框，你看到的"学生当前代码"就是框里此刻的内容。你在 edits 里给的修改会直接写进编辑框（学生可以 Ctrl+Z 撤销），所以回复里说"我把……改成了……"即可。
- 默认 edits 为空列表，只讲思路。学生请你帮他写 / 改 / 补，或者这段对话里已经提示过他、他仍然卡在同一处时，再动手改。
- 每处修改：old 是从当前内容里逐字复制的一段连续文本（包括缩进，不带行号，只出现一次）；new 是替换后的文本；why 用一句话说明道理。要在末尾追加，old 写空字符串。多处修改按顺序生效，后一处的 old 要以前一处改完后的内容为准。
- 看数据作答时，正确答案只供你核对，不要直接说出来。单选题只用文字引导，edits 必须为空；短答案题只有一行，只能在答案框局部修改，不要代答。
- 预测输出题没有代码，编辑框里是学生写的预测输出，规则相同。
- 尽量只改他卡住的那一小块（通常几行以内），不要一次把{editor_unit}写完；他要完整答案时，优先写下一步，让他自己试后面的部分。

## 附加题（make_extra、delete_extras 字段）
- 左栏除了"题目""课"，还可以有"附加题 1、附加题 2……"标签，都是照着原题出的相似题。学生和你共用这一段对话，上下文里写着他现在在看哪一道。
- 学生想再练一道类似的（"再来一道""出个类似的巩固一下""换个场景""难一点"），就在 make_extra 里用一句话写出题要求（例如"同样的套路，换成字符串场景，难度不变"），平台会在后台出题并验证，好了自动加一个新的附加题标签。回复里告诉他"正在出一道附加题，好了会出现在左边"，不要在回复里自己写题面。不出题时 make_extra 写空字符串。
- 学生要删掉某几道附加题时，把它们的编号写进 delete_extras（比如 [1, 3]）；否则写空列表。
"""


@dataclass
class TutorReply:
    reply: str
    edits: list[dict[str, str]]
    notes: list[str] = field(default_factory=list)  # 重试 / 丢弃记录，存档用
    make_extra: str = ""                             # 出附加题的要求（空 = 不出）
    delete_extras: list[int] = field(default_factory=list)


def numbered(text: str) -> str:
    return "\n".join(f"{i + 1:>3}| {line}" for i, line in enumerate(text.splitlines())) or "（空）"


def summarize_result(result: dict[str, Any] | None) -> str:
    if not result:
        return "还没有运行过。"
    lines = [f"结果：{result.get('verdict')}，通过 {result.get('passed')}/{result.get('total')}"]
    if misconception := result.get("misconception"):
        lines.append(f"误解：{misconception['name']}。{misconception['line']}")
    if result.get("error"):
        lines.append(f"错误：{str(result['error'])[:600]}")
    bad = next((c for c in result.get("cases", []) if c.get("status") != "passed"), None)
    if bad:
        if bad.get("error"):
            lines.append("报错：" + str(bad["error"])[:600])
        if difference := bad.get("difference"):
            lines.append(str(difference.get("message", "") if isinstance(difference, dict) else difference))
        lines.append(
            "第一个没通过的用例："
            + json.dumps(
                {k: bad.get(k) for k in ("status", "input", "expected", "actual", "error")},
                ensure_ascii=False,
                default=str,
            )[:1200]
        )
        if bad.get("stdout"):
            lines.append(f"print 输出：{str(bad['stdout'])[:400]}")
    return "\n".join(lines)


def build_prompt(
    problem: Problem,
    *,
    code: str,
    answer: str | None,
    last_result: dict[str, Any] | None,
    history: list[dict[str, Any]],
    message: str,
    skill_names: dict[str, str],
    applied_edits: int,
    lesson: list[dict[str, Any]] | None = None,
    current_label: str = "题目（原题）",
    extras: list[dict[str, Any]] | None = None,
) -> str:
    m = problem.meta
    parts = [f"学生现在在看：{current_label}"]
    if extras:
        listing = "；".join(
            f"附加题 {e['seq']}：{e.get('title') or '（出题中）'}"
            + ("（出题中）" if e["status"] == "generating" else "（出题失败）" if e["status"] == "failed" else "")
            for e in extras
        )
        parts.append(f"已有的附加题：{listing}")
    parts += [f"# 题目：{m.title}（{m.track}，阶段 {m.stage}，题型 {m.format}）", problem.statement.strip()]
    if m.signature:
        parts.append(f"函数签名：`{m.signature}`")
    examples = problem.cases("examples")
    if examples:
        parts.append("样例：" + json.dumps(examples, ensure_ascii=False)[:1500])
    introduces = skill_names.get(m.skills.introduces or "", m.skills.introduces or "")
    requires = [skill_names.get(s, s) for s in m.skills.requires]
    parts.append(f"本题新技能：{introduces or '无'}；用到的已学技能：{'、'.join(requires) or '无'}")

    if problem.inspect:
        exercise = problem.inspect
        parts.extend(f"数据块 {b['title']}（{b['kind']}）\n{b['content']}" for b in exercise.data)
        a = exercise.answer
        if a["type"] == "choice":
            options = {str(i): option for i, option in enumerate(a["options"])}
            parts.append("单选题选项：" + json.dumps(options, ensure_ascii=False))
            parts.append("学生当前选择：" + options.get(answer, "（未选择）"))
            reference = options[str(a["correct"])]
        else:
            parts.append("学生当前的短答案：" + (answer or "（空）"))
            reference = json.dumps(a["accept"], ensure_ascii=False)
        parts.append("正确答案（只供判断，不要透露）：" + reference)
    elif m.mode == "predict":
        parts.append("## 题目展示的程序（学生要写出它的输出）\n```python\n" + (problem.read("solution.py") or "") + "\n```")
        parts.append(
            "## 编辑框里学生当前写的预测输出（行号只为定位，edits 的 old 里不要带行号）\n```\n"
            + (numbered(answer) if answer else "（空）")
            + "\n```"
        )
    else:
        reference = problem.read("solution.sql" if problem.track.language == "sql" else "solution.py") or ""
        lang = problem.track.language
        if lang == "sql":
            parts.append(sample_context(problem))
        parts.append(f"## 参考解（只供你判断，不要整段透露）\n```{lang}\n{reference}\n```")
        parts.append("## 编辑框里学生当前的代码（行号只为定位，edits 的 old 里不要带行号）\n```\n" + numbered(code) + "\n```")

    if lesson:
        parts.append(format_lesson(lesson))
    parts.append("## 最近一次运行 / 提交（那时的代码可能和现在不同）\n" + summarize_result(last_result))
    parts.append(f"这道题里你已经改过编辑框 {applied_edits} 次。")
    if history:
        convo = []
        for h in history[-12:]:
            who = "学生" if h["role"] == "user" else "助教"
            text = h["content"]
            for e in h.get("edits") or []:
                text += f"\n（当时改了：{json.dumps(e.get('old'), ensure_ascii=False)} → {json.dumps(e.get('new'), ensure_ascii=False)}）"
            convo.append(f"{who}：{text}")
        parts.append("## 之前的对话\n" + "\n\n".join(convo))
    parts.append("## 学生现在说\n" + message.strip())
    return "\n\n".join(parts)


def format_lesson(sections: list[dict[str, Any]], limit: int = 5000) -> str:
    """这道题的课：新知识写全（讲解、示例、小测），用到的知识只列名字和知识卡第一行。"""
    out = ["## 这道题的课（学生在\"课\"标签里看得到）"]
    used = []
    for sec in sections:
        if sec.get("new"):
            out.append(f"### 新知识：{sec['name']}")
            for st in sec.get("steps", []):
                if st["type"] == "read":
                    out.append(st["md"].strip())
                elif st["type"] == "example":
                    if block := st.get("data"):
                        out.append(f"示例 {block['title']}：\n{block['content']}\n{st.get('md', '')}")
                        continue
                    lang = "sql" if st.get("db") else "python"
                    out.append(f"示例：\n```{lang}\n{st['code'].rstrip()}\n```" + (f"\n{st['md'].strip()}" if st.get("md") else ""))
                elif st["type"] == "quiz":
                    opts = st.get("options", [])
                    ans = opts[st["answer"]] if 0 <= st.get("answer", -1) < len(opts) else ""
                    out.append(f"小测：{st['q'].strip()}（正确答案：{ans}）")
            if not sec.get("steps") and sec.get("card"):
                out.append(sec["card"].strip())
        else:
            first = (sec.get("card") or "").strip().splitlines()[:1]
            used.append(f"- {sec['name']}" + (f"：{first[0]}" if first else ""))
    if used:
        out.append("### 用到的已学知识\n" + "\n".join(used))
    text = "\n\n".join(out)
    return text if len(text) <= limit else text[:limit] + "\n……（课的内容较长，已截断）"


def apply_edits(text: str, edits: list[dict[str, str]], *, single_line: bool = False) -> tuple[str, list[int], list[str]]:
    """按顺序在 text 上模拟修改，返回（结果，能用的修改下标，问题列表）。"""
    ok, issues = [], []
    for i, e in enumerate(edits):
        old, new = e.get("old", ""), e.get("new", "")
        if single_line and ("\n" in new or "\r" in new):
            issues.append("短答案只能写一行")
            continue
        if not old:
            if not new:
                issues.append(f"第 {i + 1} 处修改的 old 和 new 都是空的")
                continue
            text = text + ("\n" if not single_line and text and not text.endswith("\n") else "") + new
            ok.append(i)
            continue
        found = text.count(old)
        if found != 1:
            issues.append(
                f"第 {i + 1} 处修改的 old 在当前内容里"
                + ("找不到（缩进和空格要逐字一致，不要带行号；要追加就把 old 写成空字符串）" if found == 0
                   else f"出现了 {found} 次，要选一段唯一的")
            )
            continue
        text = text.replace(old, new, 1)
        ok.append(i)
    return text, ok, issues


def check(out: dict[str, Any], target: str, *, single_line: bool = False) -> list[str]:
    issues = []
    reply = out.get("reply")
    if not isinstance(reply, str) or not reply.strip():
        issues.append("reply 不能为空")
    _, _, edit_issues = apply_edits(target, list(out.get("edits") or []), single_line=single_line)
    return issues + edit_issues


def ask(
    provider: AIProvider,
    problem: Problem,
    *,
    code: str,
    answer: str | None,
    last_result: dict[str, Any] | None,
    history: list[dict[str, Any]],
    message: str,
    skill_names: dict[str, str],
    applied_edits: int = 0,
    effort: str = "low",
    lesson: list[dict[str, Any]] | None = None,
    current_label: str = "题目（原题）",
    extras: list[dict[str, Any]] | None = None,
) -> TutorReply:
    prompt = build_prompt(
        problem, code=code, answer=answer, last_result=last_result, history=history,
        message=message, skill_names=skill_names, applied_edits=applied_edits, lesson=lesson,
        current_label=current_label, extras=extras,
    )
    target = (answer or "") if problem.meta.mode in ("predict", "inspect") else code
    choice = bool(problem.inspect and problem.inspect.answer["type"] == "choice")
    short = bool(problem.inspect and problem.inspect.answer["type"] == "short")
    unit = "整道题" if problem.inspect else "整条查询" if problem.track.language == "sql" else "整个函数"
    system = SYSTEM_PROMPT.replace("{editor_unit}", unit)
    out = provider.complete(system=system, prompt=prompt, schema=SCHEMA, effort=effort)
    notes: list[str] = []
    if choice:
        out = out | {"edits": []}
    issues = check(out, target, single_line=short)
    if issues:
        notes.append("第一次回复有问题：" + "；".join(issues))
        retry = (
            prompt
            + "\n\n## 你上一次的回复有问题，请重新回复\n"
            + json.dumps(out, ensure_ascii=False)[:2000]
            + "\n问题：" + "；".join(issues)
        )
        out = provider.complete(system=system, prompt=retry, schema=SCHEMA, effort=effort)
    reply = str(out.get("reply") or "").strip()
    if not reply:
        raise AIError("AI 回复为空")
    edits = [
        {"old": e.get("old", ""), "new": e.get("new", ""), "why": e.get("why", "")}
        for e in ([] if choice else out.get("edits") or [])
    ]
    _, ok, still = apply_edits(target, edits, single_line=short)
    if still:
        notes.append("丢掉了定位不了的修改：" + "；".join(still))
        edits = [edits[i] for i in ok]
    make_extra = str(out.get("make_extra") or "").strip()
    delete_extras = list(out.get("delete_extras") or [])  # JSON schema 已限定为整数
    return TutorReply(reply=reply, edits=edits, notes=notes, make_extra=make_extra, delete_extras=delete_extras)
