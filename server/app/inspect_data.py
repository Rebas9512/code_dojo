"""看数据作答的格式与判题。题库、附加题和独立的内容检查共用。"""
from __future__ import annotations

import csv
import io
import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

KINDS = ("table", "csv", "json", "schema", "values")
NORMALIZE = ("strip", "fullwidth", "casefold")
WIDTH_MAP = {i: i - 0xFEE0 for i in range(0xFF01, 0xFF5F)} | {0x3000: 32}
# 与零基础教学大纲里的 DM 编号对应，作者也可以在题里给出解释。
MISCONCEPTIONS = {
    "DM01": ("带引号的数字也是数", "引号里的数字是文字，保留的是字符。"),
    "DM02": ("写着真就是布尔值", "文字可以写成任何样子，布尔值只有真和假两种。"),
    "DM03": ("空就是零", "零是已知的数量，缺失表示这个位置没有记录值。"),
    "DM04": ("由数字组成就能算", "编号用来辨认对象，对编号求平均没有数量上的意义。"),
    "DM05": ("名字能当标识", "不同记录可能同名，主键要能唯一标识一条记录。"),
    "DM06": ("CSV 会保留类型", "CSV 记录的是字符，读入后需要按列解释类型。"),
    "DM07": ("一列里可以混着写", "同一列按同一种类型记录，比较和计算才有一致的含义。"),
    "DM08": ("数据只有一种存法", "同一批记录可以按行或按列组织，也可以写成嵌套结构。"),
}


def nonblank(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def reject_constant(value: str) -> None:
    raise ValueError(f"JSON 数字不合法：{value}")


def data_block(raw: Any, directory: Path | None = None) -> dict:
    """展开 file 并检查内容。出附加题时没有目录，只允许内联文本。"""
    if not isinstance(raw, dict) or raw.get("kind") not in KINDS:
        raise ValueError(f"数据块的 kind 应为 {' / '.join(KINDS)}")
    kind = raw["kind"]
    if ("file" in raw) == ("content" in raw):
        raise ValueError("数据块的 file 和 content 必须二选一")
    if "file" in raw:
        if directory is None or not nonblank(raw["file"]):
            raise ValueError("数据块需要内联 content")
        path = (directory / raw["file"]).resolve()
        if Path(raw["file"]).is_absolute() or not path.is_relative_to(directory.resolve()) or not path.is_file():
            raise ValueError(f"数据文件必须位于当前目录内且存在：{raw['file']}")
        content = path.read_text(encoding="utf-8")
    else:
        content = raw["content"]
    if not nonblank(content) or not isinstance(raw.get("title", ""), str):
        raise ValueError("数据块需要文本内容，title 应为文字")
    block = {"kind": kind, "title": raw.get("title", ""), "content": content}
    if kind in ("table", "csv"):
        try:
            rows = list(csv.reader(io.StringIO(content, newline=""), strict=True))
        except csv.Error as exc:
            raise ValueError(f"CSV 格式错误：{exc}") from exc
        # csv.reader 把完全空的一行读成 []；在单列表里它就是一个缺失字段。
        if not rows or not rows[0] or any((len(row) or 1) != len(rows[0]) for row in rows):
            raise ValueError("CSV 表头和各行的列数应一致")
    elif kind == "schema":
        try:
            schema = yaml.safe_load(content)
        except yaml.YAMLError as exc:
            raise ValueError(f"表结构 YAML 格式错误：{exc}") from exc
        columns = schema.get("columns") if isinstance(schema, dict) else None
        if not isinstance(columns, list) or not columns:
            raise ValueError("表结构需要非空的 columns 列表")
        for col in columns:
            if (not isinstance(col, dict) or not all(nonblank(col.get(k)) for k in ("name", "type"))
                    or not all(isinstance(col.get(k), bool) for k in ("nullable", "primary_key"))):
                raise ValueError("每列需要 name、type 和布尔值 nullable、primary_key")
        block["columns"] = [{k: c[k] for k in ("name", "type", "nullable", "primary_key")} for c in columns]
    else:
        value = json.loads(content, parse_constant=reject_constant)
        if kind == "values" and (not isinstance(value, list) or not value):
            raise ValueError("values 需要非空的 JSON 数组")
    return block


def normalize(value: str, rules: Sequence[str]) -> str:
    for rule in rules:
        if rule == "strip":
            value = value.strip()
        elif rule == "fullwidth":
            value = value.translate(WIDTH_MAP)
        elif rule == "casefold":
            value = value.casefold()
    return value


@dataclass
class InspectExercise:
    data: list[dict]
    answer: dict
    explain: str
    feedback: dict[str, dict[str, str]]
    rules: Sequence[str]
    accepted: set[str]

    @classmethod
    def load(cls, spec: dict, directory: Path | None = None) -> InspectExercise:
        if spec.get("mode") != "inspect":
            raise ValueError("inspect 题需要 mode: inspect")
        if not isinstance(spec.get("data"), list) or not spec["data"]:
            raise ValueError("inspect 题需要至少一个数据块")
        blocks = [data_block(b, directory) for b in spec["data"]]
        if not nonblank(spec.get("explain")):
            raise ValueError("inspect 题需要 explain")
        answer = spec.get("answer")
        if not isinstance(answer, dict) or answer.get("type") not in ("choice", "short"):
            raise ValueError("answer.type 应为 choice 或 short")
        rules = []
        valid_choices = set()
        if answer["type"] == "choice":
            options, correct = answer.get("options"), answer.get("correct")
            if not isinstance(options, list) or len(options) < 2 or not all(map(nonblank, options)):
                raise ValueError("choice 需要至少两个文字选项")
            if type(correct) is not int or not 0 <= correct < len(options):
                raise ValueError("choice 的 correct 超出选项范围")
            accepted = {str(correct)}
            valid_choices = {str(i) for i in range(len(options))}
        else:
            rules = answer.get("normalize", list(NORMALIZE))
            if not isinstance(rules, list) or any(r not in NORMALIZE for r in rules):
                raise ValueError("normalize 应为 strip、fullwidth、casefold 组成的列表")
            accept = answer.get("accept")
            if not isinstance(accept, list) or not accept or not all(map(nonblank, accept)):
                raise ValueError("short 的 accept 需要非空的答案文字列表")
            accepted = {normalize(v, rules) for v in accept}
            if "" in accepted or len(accepted) != len(accept):
                raise ValueError("accept 规范化后不能有空值或重复答案")
        feedback = {}
        mappings = answer.get("misconceptions", {})
        if not isinstance(mappings, dict):
            raise ValueError("misconceptions 应为错误答案到误解的映射")
        for raw, info in mappings.items():
            key = normalize(str(raw), rules)
            if key in accepted or key in feedback or (valid_choices and key not in valid_choices):
                raise ValueError(f"misconceptions 中的错误答案无效或重复：{raw}")
            if isinstance(info, str) and info in MISCONCEPTIONS:
                name, line = MISCONCEPTIONS[info]
                info = {"id": info, "name": name, "line": line}
            if not isinstance(info, dict) or not all(nonblank(info.get(k)) for k in ("id", "name", "line")):
                raise ValueError("误解需要已知编号或 {id, name, line}")
            feedback[key] = {k: info[k] for k in ("id", "name", "line")}
        return cls(blocks, answer, spec["explain"], feedback, rules, accepted)

    def grade(self, submitted: str) -> dict:
        key = normalize(submitted, self.rules)
        right = key in self.accepted
        result = {"verdict": "accepted" if right else "wrong_answer", "passed": int(right),
                  "total": 1, "cases": [], "explain": self.explain}
        if not right and key in self.feedback:
            result["misconception"] = self.feedback[key]
        return result
