"""SQL 数据集、服务器参考结果与内容寻址缓存。用户查询由浏览器执行。"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from functools import lru_cache
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .problems import Problem

RUNNER = Path(__file__).with_name("sql_runner.mjs")


def dataset(p: Problem, spec: str) -> list[str]:
    from .problems import shared_db

    scripts = []
    for part in map(str.strip, spec.split("+")):
        if part.startswith("db:"):
            scripts.extend(shared_db(p.path.parents[1], part[3:]))
        else:
            content = p.read(part)
            if content is None:
                raise ValueError(f"找不到数据集 {part}")
            scripts.append(content)
    return scripts


def run_node(**job: Any) -> list:
    env = {key: os.environ[key] for key in ("PATH", "SystemRoot", "TEMP", "TMP") if key in os.environ}
    try:
        proc = subprocess.run(
            ["node", "--experimental-strip-types", str(RUNNER)], input=json.dumps(job),
            capture_output=True, encoding="utf-8", timeout=30, env={**env, "TZ": "UTC"},
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError(f"无法运行 SQL 校验或运行超时：{exc}") from exc
    if proc.returncode:
        raise ValueError(f"Node PGlite 运行失败，请检查 scripts/curriculum 的 npm 依赖：{proc.stderr[-1200:]}")
    result = json.loads(proc.stdout)
    if "error" in result:
        raise ValueError(result["error"])
    return result["tables"]


def verify_sql_files(directory: Path, meta: dict, datasets: list[list[str]]) -> list:
    """两个题库脚本共用固定题的判定规则，内容侧只需 PyYAML 和 Node。"""
    wrong = [w["sql"] for w in meta.get("wrong_examples") or []]
    if meta.get("mode") == "dml" and not wrong:
        raise ValueError("修改类题至少要有一段 wrong_examples")
    if not datasets:
        raise ValueError("SQL 题必须至少有一个数据集")
    starter = {"starter": (directory / "starter.sql").read_text(encoding="utf-8")} if meta["format"] == "fix" else {}
    return run_node(datasets=datasets, solution=(directory / "solution.sql").read_text(encoding="utf-8"),
                    ordered=meta.get("ordered", False), wrong=wrong, mode=meta.get("mode"),
                    check_query=meta.get("check_query"), **starter)


def sql_cases(p: Problem, data_dir: Path, *, all_cases: bool) -> dict:
    solution = p.read("solution.sql")
    if not solution:
        raise ValueError("缺少参考解 solution.sql")
    cache = data_dir / "sql-cache"
    cache.mkdir(parents=True, exist_ok=True)
    cases, missing = [], {}
    exercise = {"mode": "dml", "check_query": p.meta.check_query} if p.meta.mode == "dml" else {}
    options = {**exercise, "ordered": p.meta.ordered} if exercise else {}
    for i, spec in enumerate(p.meta.datasets if all_cases else p.meta.datasets[:1]):
        setup = dataset(p, spec)
        key_parts = [solution, setup, options] if options else [solution, setup]
        key = hashlib.sha256(json.dumps(key_parts).encode()).hexdigest()
        path = cache / f"{key}.json"
        case = {"setup": setup, "hidden": i > 0}
        cases.append(case)
        if path.exists():
            case["expected"] = json.loads(path.read_text(encoding="utf-8"))
        else:
            missing.setdefault(path, []).append(case)
    if missing:
        tables = run_node(datasets=[items[0]["setup"] for items in missing.values()], solution=solution, **options)
        for (path, items), table in zip(missing.items(), tables, strict=True):
            for item in items:
                item["expected"] = table
            # 并发首次加载时，读者总是看到完整写入的结果。
            with NamedTemporaryFile(mode="w", dir=cache, delete=False, encoding="utf-8") as tmp:
                json.dump(table, tmp, ensure_ascii=False)
            os.replace(tmp.name, path)
    return {"ordered": p.meta.ordered, "tolerance": 1e-6, "datasets": cases, **exercise}


def sample_context(p: Problem) -> str:
    return _sample_context(tuple(dataset(p, p.meta.datasets[0])))


@lru_cache(maxsize=16)
def _sample_context(setup: tuple[str, ...]) -> str:
    tables, = run_node(datasets=[setup], preview=True)
    return "表结构和样例数据（每表最多三行）：\n" + json.dumps(tables, ensure_ascii=False)
