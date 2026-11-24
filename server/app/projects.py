"""项目合同与拼装。部分题和普通题共用目录与题号，项目目录名是单元编号。"""

from __future__ import annotations

import re
import shlex
from collections.abc import Iterator
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, ConfigDict, Field

from .tracks import Track, read_yaml

if TYPE_CHECKING:
    from .problems import Problem


class QueryCheck(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str = Field(min_length=1)
    query: str = Field(min_length=1)
    ordered: bool = False


class ProbeCheck(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str = Field(min_length=1)
    probe: str = Field(min_length=1)
    expect: Literal["error", "ok"]


class ResultCheck(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str = Field(min_length=1)
    result: Literal[True]
    ordered: bool = False


SqlCheck = QueryCheck | ProbeCheck | ResultCheck


class ProjectRun(BaseModel):
    entry: str = "main"
    args: list[str] = Field(default_factory=list)
    timeout: int = Field(default=300, gt=0)
    checks: list[SqlCheck] = Field(default_factory=list)


class ProjectMeta(BaseModel):
    id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    title: str
    summary: str
    language: Literal["python", "sql"]
    scaffold: str
    reference: Literal["assembled"]
    data: str
    parts: list[str] = Field(min_length=1)
    run: ProjectRun
    success: dict[str, dict[Literal["<", "<=", "==", ">=", ">"], float]] | Literal["all_checks"]


@dataclass(eq=False)  # 按对象比较和哈希，sql_plan 可以按项目对象缓存
class Project:
    meta: ProjectMeta
    directory: Path
    parts: list[Problem]
    # 每个占位之前的原文，加最后一个占位之后的原文。
    sections: list[str]
    solutions: dict[str, str]

    @classmethod
    def load(cls, path: Path, track: Track, problems: dict[str, Problem]) -> Project:
        meta = ProjectMeta.model_validate(read_yaml(path))
        directory = path.parent
        # 题库只按 track.yaml 列出的 <项目阶段>/<单元编号>/project.yaml 来找，阶段和单元已经对得上。
        stage, unit = directory.parent.name, int(directory.name)
        if meta.language != track.language:
            raise ValueError("项目语言应与学习线相同")
        if meta.language == "python":
            if not meta.run.entry.isidentifier() or not (directory / meta.data).is_dir():
                raise ValueError("Python 项目需要入口和数据目录")
            if not isinstance(meta.success, dict) or not meta.success or not all(meta.success.values()):
                raise ValueError("Python 项目需要非空的指标阈值")
        elif meta.success != "all_checks" or not meta.run.checks:
            raise ValueError("SQL 项目需要最终检查和 all_checks")
        parts = sorted((p for p in problems.values() if p.meta.track == track.id and p.meta.stage == stage
                        and p.meta.unit == unit), key=lambda p: p.meta.order)
        if [p.id for p in parts] != meta.parts:
            raise ValueError("parts 必须按 order 列全本单元的题目")
        extension = "py" if meta.language == "python" else "sql"
        for i, p in enumerate(parts, 1):
            if p.meta.project != meta.id or p.meta.part != i:
                raise ValueError(f"{p.id} 应标记 project: {meta.id}、part: {i}")
            if meta.language == "sql" and any(s.split("+")[0].strip() != "db:" + meta.data for s in p.meta.datasets):
                raise ValueError(f"{p.id} 的数据集应从项目库 db:{meta.data} 开始")
        marker = "#" if meta.language == "python" else "--"
        scaffold = (directory / meta.scaffold).read_text(encoding="utf-8")
        chunks = re.split(rf"^{marker} @part (\S+)[ \t]*$", scaffold, flags=re.MULTILINE)
        if chunks[1::2] != meta.parts:
            raise ValueError("骨架占位应按 parts 顺序出现，每题一行")
        solutions = {p.id: p.file("solution." + extension).read_text(encoding="utf-8") for p in parts}
        return cls(meta, directory, parts, chunks[::2], solutions)

    @cached_property
    def reference(self) -> str:
        return self.assemble(self.solutions)

    def blocks(self, answers: dict[str, str], *, notebook: bool = False) -> Iterator[str]:
        python = self.meta.language == "python"
        prefix = self.sections[0]
        if python:
            base = "Path.cwd()" if notebook else "Path(__file__).resolve().parent"
            prefix += f'\nfrom pathlib import Path\nDATA_DIR = {base} / "data"\n\n'
            if not notebook:
                command = shlex.join(["python", self.meta.id + ".py", *self.meta.run.args])
                prefix = f"# 运行：{command}\n" + prefix
        yield prefix
        for i, p in enumerate(self.parts, 1):
            todo = f"第 {i} 部分还没完成"
            stub = f'raise NotImplementedError("{todo}")' if python else "-- TODO " + todo
            code = answers.get(p.id, stub).rstrip("\n")
            yield code + self.sections[i]
        if python:
            entry = self.meta.run.entry
            if notebook:
                yield f"import sys\nsys.argv = {[self.meta.id, *self.meta.run.args]!r}\n{entry}()\n"
            else:
                yield f'\nif __name__ == "__main__":\n    {entry}()\n'

    def assemble(self, answers: dict[str, str]) -> str:
        return "".join(self.blocks(answers))

    def notebook(self, answers: dict[str, str]) -> dict:
        blocks = iter(self.blocks(answers, notebook=True))
        cells = []

        def cell(kind: str, source: str):
            fields = {"outputs": [], "execution_count": None} if kind == "code" else {}
            cells.append({"cell_type": kind, "metadata": {}, "source": source.strip("\n"), **fields})

        cell("code", next(blocks))
        for part in self.parts:
            paragraphs = part.statement.strip().split("\n\n")
            description = next((text for text in paragraphs if not text.startswith("#")), "")
            cell("markdown", f"## {part.meta.title}\n\n{description}")
            cell("code", next(blocks))
        cell("code", next(blocks))
        return {"nbformat": 4, "nbformat_minor": 4, "cells": cells,
                "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}}}
