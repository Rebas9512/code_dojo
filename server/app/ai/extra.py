"""附加题：照着一道原题，让 AI 当场出一道相似题，并在判题沙箱里验证后才交给学生。

用户需求（2026-11-22）："有些时候我想做一些相似题型巩固记忆 我想可以直接和ai助手说 马上就能出新的类似题在左边出现然后我就能当场写"
"如果ai出题的话就加一个tab做成附加题1，然后如果我还想做就加附加题2 这种的设计 ai就可以增加管理这些附加题tab 我也能删除一些不想保留的题目"

验证（调研结论：AI 出的题不验证，约三分之二的测试是错的）：
  - 参考解跑全部用例必须通过；
  - 每个"典型错误写法"至少挂一个用例；complete / fix 题的初始代码也必须挂；
  - predict 题：展示的程序要能正常运行并有输出。
不过就把问题交回 AI 重出，最多 MAX_ATTEMPTS 次。
"""

from __future__ import annotations

import json
import sys
from typing import Any, Literal

from pydantic import BaseModel, Field

from ..config import PROJECT_ROOT
from ..inspect_data import InspectExercise, KINDS, MISCONCEPTIONS, NORMALIZE, nonblank
from ..judge import Judge
from ..problems import Problem
from ..sql_judge import run_node, sample_context
from .provider import AIError, AIProvider

MAX_ATTEMPTS = 3

SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "statement": {"type": "string"},
        "mode": {"type": "string", "enum": ["function", "stdio", "predict", "class"]},
        "entry": {"type": "string"},
        "signature": {"type": "string"},
        "compare": {"type": "string", "enum": ["exact", "unordered", "float"]},
        "starter": {"type": "string"},
        "solution": {"type": "string"},
        "tests_json": {"type": "string"},
        "wrong_solutions": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["title", "statement", "mode", "entry", "signature", "compare", "starter", "solution",
                 "tests_json", "wrong_solutions"],
    "additionalProperties": False,
}


class SqlExtra(BaseModel):
    mode: Literal["dml"] | None = None
    check_query: str | None = None
    title: str = Field(min_length=1)
    statement: str = Field(min_length=1)
    tables: list[str] = Field(min_length=1)
    datasets: list[str] = Field(min_length=3)
    ordered: bool
    solution: str = Field(min_length=1)
    wrong_solutions: list[str] = Field(min_length=1, max_length=2)
    starter: str = ""


SQL_PROMPT = """你是 SQL 出题助手。照原题的技能、题型和难度换一个场景，用中文写题目、示例和约束。
tables 是用到的表名。datasets 每项都是独立的小库，用 CREATE TABLE 和 INSERT INTO 完整建表、填数据。
第一个是题面样例，另给至少两个隐藏数据集。沿用原题的判题模式。查询题省略 mode 和 check_query，提交单条 SELECT 或 WITH 查询。
修改题设 mode 为 dml，solution 和错误写法各写一条 DELETE、UPDATE 或 INSERT，可带 WITH。
check_query 写读取修改后表状态的一条查询，参考解在每个数据集上都应改变这个结果。
要求特定行序就设 ordered 并在结果查询中写 ORDER BY。每段可运行的典型错误写法要被隐藏数据区分。
改错题的 starter 在样例上就要得到错误结果，补全题给挖空的 starter，独立写题可省略 starter。"""


MISCONCEPTION_MAP = {"type": "object", "additionalProperties": {"enum": list(MISCONCEPTIONS)}}

INSPECT_SCHEMA = {
    "type": "object",
    "properties": {
        "mode": {"const": "inspect"},
        "title": {"type": "string"}, "statement": {"type": "string"}, "explain": {"type": "string"},
        "data": {"type": "array", "minItems": 1, "items": {
            "type": "object", "additionalProperties": False, "required": ["kind", "title", "content"],
            "properties": {"kind": {"enum": list(KINDS)}, "title": {"type": "string"}, "content": {"type": "string"}},
        }},
        "answer": {"oneOf": [
            {"type": "object", "additionalProperties": False, "required": ["type", "options", "correct"],
             "properties": {"type": {"const": "choice"}, "options": {"type": "array", "minItems": 2,
                            "items": {"type": "string"}}, "correct": {"type": "integer", "minimum": 0},
                            "misconceptions": MISCONCEPTION_MAP}},
            {"type": "object", "additionalProperties": False, "required": ["type", "accept"],
             "properties": {"type": {"const": "short"}, "misconceptions": MISCONCEPTION_MAP,
                            "normalize": {"type": "array", "items": {"enum": list(NORMALIZE)}},
                            "accept": {"type": "array", "minItems": 1,
                            "items": {"type": "string"}}}},
        ]},
    },
    "required": ["mode", "title", "statement", "explain", "data", "answer"], "additionalProperties": False,
}

INSPECT_PROMPT = """你是面向零基础学生的中文出题助手。围绕原题的技能换一个场景，出一道看数据作答题。
数据块使用内联 content。table 和 csv 用带表头的 CSV，json 用 JSON，values 用 JSON 数组。
schema 用 YAML 的 columns 列表，每列写 name、type、nullable 和 primary_key，后两项用布尔值。
单选的 correct 从 0 数，短答案的 accept 列出可接受的写法。核对它们是否确实能从数据里读出来。
能辨认错误原因时可写 misconceptions，把错误下标或错误短答案映射到 DM01–DM08。沿用原题同一概念的编号。
explain 用一句话讲怎么找到答案。题面和数据块中不要标出正确答案。"""


SYSTEM_PROMPT = """你是 code-dojo 的出题助手。学生刚做（或正在做）一道题，想要一道相似的"附加题"来巩固。照着原题出一道新题。

## 要求
- 练的是同一个知识点 / 同一个套路，只能用原题用到的技能（下面列出了），不要引入学生还没学过的东西。
- 默认保持原题的模式（function / stdio / predict / class）和题型；学生另有要求时照他说的来。
- 换一个场景或数据形态，不要只改数字；也不要和已有的附加题重复。难度和原题相当，学生要求"难一点 / 简单一点"时再调整。
- 题面用中文 Markdown，固定小节：## 题目、## 示例、## 约束。用自己的话写，不要照搬任何网站的原题。

## 各字段
- title：中文短标题。
- mode：function（写函数）/ stdio（读输入、打印输出）/ predict（看程序写输出）/ class（实现一个类，LeetCode 设计题风格）。
- entry：function 模式写函数名，class 模式写类名，其他模式写空字符串。
- signature：function 模式写完整的 def 行（带类型注解），其他模式写空字符串。
- compare：exact；返回列表且顺序无所谓时 unordered；浮点数结果用 float。
- starter：学生拿到的初始代码。write 题：签名加 pass。complete 题：参考解里关键的一两处挖成 ____。fix 题：一段带一个典型 bug 的代码。predict 题：空字符串。
- solution：参考解（Python）。predict 模式下就是要展示给学生的程序（用 print 输出），平台会运行它得到正确输出。
- tests_json：JSON 字符串，{"examples": [...], "hidden": [...]}。examples 至少 2 个、hidden 至少 3 个，hidden 要覆盖边界（空、单元素、重复、负数等）。
  - function：{"args": [位置参数...], "expected": 期望返回值}
  - stdio：{"stdin": "输入", "expected": "期望输出"}
  - class：{"ops": ["类名", "方法", ...], "args": [[构造参数], [方法参数], ...], "expected": [null, 返回值, ...]}
  - predict：{"examples": [], "hidden": []}
- wrong_solutions：1–2 段"典型错误写法"（学生容易犯的错，完整可运行的代码），用来确认测试真能区分对错。predict 模式给空列表。
"""


def build_prompt(parent: Problem, *, request: str, skill_names: dict[str, str], existing: list[str],
                 feedback: list[str] | None, previous: dict[str, Any] | None) -> str:
    m = parent.meta
    skills = [skill_names.get(s, s) for s in [*m.skills.requires, *([m.skills.introduces] if m.skills.introduces else [])]]
    parts = [
        f"# 原题：{m.title}（模式 {m.mode}，题型 {m.format}，难度 {m.difficulty}/100）",
        parent.statement.strip(),
        "题干用中文，学习者要输入或输出的内容用英文。",
        f"原题用到的技能（附加题只能用这些）：{'、'.join(skills) or '无'}",
    ]
    if m.signature:
        parts.append(f"原题签名：`{m.signature}`")
    if parent.track.runtime == "ds":
        parts.append("数据科学沙箱提供 NumPy、pandas 和 CPU 版 PyTorch。函数题返回数组或张量用 allclose，"
                     "期望写数字或嵌套数组；返回表或 Series 用 frame，期望用 columns、data（行数组）、"
                     "可选 index，Series 用 name、data（一维）。沿用原题的写法约束和比较选项："
                     + str(parent.judge_options()["compare_options"]) + "，" + str(m.constraints))
    if parent.inspect:
        parts.append("原题数据和答案：" + json.dumps([parent.inspect.data, parent.inspect.answer], ensure_ascii=False))
    elif parent.track.language == "sql":
        parts.extend([sample_context(parent), "原题参考解：\n```sql\n" + (parent.read("solution.sql") or "") + "\n```"])
        if m.mode == "dml":
            parts.append("原题用来检查修改结果的查询：" + str(m.check_query))
    else:
        parts.append("原题参考解：\n```python\n" + (parent.read("solution.py") or "") + "\n```")
    examples = parent.cases("examples")
    if examples:
        parts.append("原题样例：" + json.dumps(examples, ensure_ascii=False)[:1200])
    if existing:
        parts.append("已有的附加题（不要重复）：" + "；".join(existing))
    parts.append("## 学生的要求\n" + (request.strip() or "出一道相似的题巩固一下"))
    if feedback:
        parts.append(
            "## 你上一次出的题没通过验证，请修好后重新给出完整的题\n"
            + json.dumps(previous, ensure_ascii=False)[:4000]
            + "\n问题：\n- " + "\n- ".join(feedback)
        )
    return "\n\n".join(parts)


def parse(out: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """把 AI 的输出整理成附加题的 spec，顺便做格式检查。"""
    issues: list[str] = []
    try:
        tests = json.loads(out.get("tests_json") or "{}")
    except json.JSONDecodeError as exc:
        tests = {}
        issues.append(f"tests_json 不是合法 JSON：{exc}")
    if not isinstance(tests, dict):
        tests, issues = {}, issues + ["tests_json 要是一个对象 {examples, hidden}"]
    mode = out.get("mode")
    spec = {
        "title": (out.get("title") or "").strip() or "附加题",
        "statement": out.get("statement") or "",
        "mode": mode,
        "entry": out.get("entry") or None,
        "signature": out.get("signature") or None,
        "compare": out.get("compare") or "exact",
        "starter": out.get("starter") or "",
        "solution": out.get("solution") or "",
        "tests": {"examples": list(tests.get("examples") or []), "hidden": list(tests.get("hidden") or [])},
        "wrong_solutions": [w for w in out.get("wrong_solutions") or [] if w.strip()],
    }
    if not spec["solution"].strip():
        issues.append("solution 不能为空")
    if mode in ("function", "class") and not spec["entry"]:
        issues.append(f"{mode} 模式必须有 entry")
    if mode == "function" and not spec["signature"]:
        issues.append("function 模式必须有 signature")
    if mode != "predict":
        if len(spec["tests"]["examples"]) < 2 or len(spec["tests"]["hidden"]) < 3:
            issues.append("examples 至少 2 个、hidden 至少 3 个")
        if not spec["wrong_solutions"]:
            issues.append("至少给 1 段典型错误写法")
    return spec, issues


def verify(judge: Judge, spec: dict[str, Any], *, fmt: str, time_limit_ms: int | None,
           runtime: str = "python", constraints: dict | None = None, compare_options: dict | None = None) -> list[str]:
    if fmt == "inspect":
        try:
            if not all(nonblank(spec.get(k)) for k in ("title", "statement")):
                raise ValueError("附加题需要题名和题面")
            InspectExercise.load(spec)
        except ValueError as exc:
            return [str(exc)]
        return []
    mode = spec["mode"]
    options = dict(runtime=runtime, constraints=constraints, compare_options=compare_options, time_limit_ms=time_limit_ms)
    if spec.get("compare") in ("allclose", "frame") and (runtime != "ds" or mode not in ("function", "class")):
        return ["allclose / frame 需要数据科学沙箱的函数或类方法返回值"]
    if mode == "predict":
        r = judge.run(mode="stdio", code=spec["solution"], cases=[{"stdin": "", "expected": ""}], **options)
        case = (r.get("cases") or [{}])[0]
        if r["verdict"] not in ("accepted", "wrong_answer"):
            return [f"展示的程序运行出错：{r.get('error') or case.get('error')}"]
        if not (case.get("actual") or "").strip():
            return ["展示的程序没有输出"]
        return []
    cases = spec["tests"]["examples"] + spec["tests"]["hidden"]
    common = dict(mode=mode, cases=cases, entry=spec["entry"], compare=spec["compare"], **options)
    issues = []
    r = judge.run(code=spec["solution"], **common)
    if r["verdict"] != "accepted":
        bad = next((c for c in r.get("cases", []) if c["status"] != "passed"), {})
        issues.append(
            f"参考解没通过（{r['verdict']}）：输入 {json.dumps(bad.get('input'), ensure_ascii=False)}，"
            f"期望 {json.dumps(bad.get('expected'), ensure_ascii=False)}，实际 {json.dumps(bad.get('actual'), ensure_ascii=False)} "
            f"{bad.get('error') or r.get('error') or ''}".strip()
        )
        return issues  # 参考解都不对，错误写法的检查没有意义
    for i, wrong in enumerate(spec["wrong_solutions"]):
        result = judge.run(code=wrong, **common)
        if result["verdict"] == "system_error":
            return [f"验证错误写法时判题出错：{result.get('error')}"]
        if result["verdict"] == "accepted":
            issues.append(f"第 {i + 1} 段错误写法居然全部通过了：测试没覆盖到这个错误，要加能抓住它的用例")
    if fmt in ("complete", "fix") and spec["starter"].strip():
        result = judge.run(code=spec["starter"], **common)
        if result["verdict"] == "system_error":
            return [f"验证初始代码时判题出错：{result.get('error')}"]
        if result["verdict"] == "accepted":
            issues.append("初始代码（挖空 / 带 bug）居然全部通过了")
    return issues


def check_practice_scope(spec: dict, language: str, allowed: set[str]) -> None:
    """回退小题与正式题库沿用同一套 AST 和 SQL 技能识别表。"""
    directory = str(PROJECT_ROOT / "scripts/curriculum")
    if directory not in sys.path:
        sys.path.append(directory)
    from check_curve import detect_python, detect_sql

    if language == "sql":
        detected = detect_sql(spec["solution"])
    else:
        detected, _ = detect_python(spec["solution"], spec["mode"], spec.get("entry"))
    outside = sorted({d.skill for d in detected} - allowed)
    if outside:
        raise ValueError("前置小题用到了范围以外的技能：" + "、".join(outside))


def generate(provider: AIProvider, judge: Judge, parent: Problem, *, request: str, skill_names: dict[str, str],
             existing: list[str], effort: str = "medium", allowed: set[str] | None = None,
             review: bool = False) -> tuple[dict[str, Any], list[str]]:
    """出题 + 验证；返回（spec，重试记录）。三次都不过抛 AIError。"""
    feedback: list[str] | None = None
    previous: dict[str, Any] | None = None
    notes: list[str] = []
    for attempt in range(1, MAX_ATTEMPTS + 1):
        prompt = build_prompt(parent, request=request, skill_names=skill_names, existing=existing,
                              feedback=feedback, previous=previous)
        if parent.inspect:
            out = provider.complete(system=INSPECT_PROMPT, prompt=prompt, schema=INSPECT_SCHEMA, effort=effort)
            spec, issues = out, []
        elif parent.track.language == "sql":
            out = provider.complete(system=SQL_PROMPT, prompt=prompt, schema=SqlExtra.model_json_schema(), effort=effort)
            try:
                spec = SqlExtra.model_validate(out).model_dump()
                if allowed is not None:
                    check_practice_scope(spec, "sql", allowed)
                run_node(datasets=[[sql] for sql in spec["datasets"]], solution=spec["solution"],
                         mode=spec["mode"], check_query=spec["check_query"],
                         ordered=spec["ordered"], wrong=spec["wrong_solutions"], requiredTables=spec["tables"],
                         **({"starter": spec["starter"]} if parent.meta.format == "fix" else {}))
                return spec, notes
            except ValueError as exc:
                issues = [str(exc)]
        else:
            schema = SCHEMA
            if parent.track.runtime == "ds":
                schema = SCHEMA | {"properties": SCHEMA["properties"] | {
                    "compare": {"enum": ["exact", "unordered", "float", "allclose", "frame"], "type": "string"}}}
            out = provider.complete(system=SYSTEM_PROMPT, prompt=prompt, schema=schema, effort=effort)
            spec, issues = parse(out)
            if review and spec["mode"] == "predict":
                issues.append("同套路复习需要独立写代码，请出一道从空白做的题。")
            if not issues and allowed is not None:
                try:
                    check_practice_scope(spec, "python", allowed)
                except (SyntaxError, ValueError) as exc:
                    issues.append(str(exc))
        if not issues:
            options = parent.judge_options()
            spec.update(options["compare_options"] if parent.track.runtime == "ds" else {})
            if options["constraints"]:
                spec["constraints"] = options["constraints"]
            issues = verify(judge, spec, fmt=parent.meta.format, time_limit_ms=parent.meta.time_limit_ms,
                            runtime=parent.track.runtime, compare_options=options["compare_options"],
                            constraints=options["constraints"])
        if not issues:
            return spec, notes
        notes.append(f"第 {attempt} 次没通过验证：" + "；".join(issues))
        feedback, previous = issues, out
    raise AIError("出了 3 次都没通过验证：" + "；".join(feedback or []))
