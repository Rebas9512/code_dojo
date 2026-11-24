"""整跑与判定。Python 逐行读判题子进程的输出，SQL 与浏览器共用 PGlite 检查。"""

import json
import math
import operator
import time
from collections.abc import Callable, Iterator
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from tempfile import TemporaryDirectory
from pathlib import Path

from .judge import Judge
from .problems import shared_db
from .projects import Project
from .sql_judge import run_node

COMPARE = {"<": operator.lt, "<=": operator.le, "==": operator.eq, ">=": operator.ge, ">": operator.gt}


def evaluate_metrics(line: str, thresholds: dict) -> dict:
    try:
        metrics = json.loads(line)
    except ValueError:
        metrics = None
    if not isinstance(metrics, dict):
        return {"verdict": "wrong_answer", "error": "最后一行需要输出 JSON 指标对象"}
    selected = {key: metrics.get(key) for key in thresholds}
    for key, targets in thresholds.items():
        value = metrics.get(key)
        if type(value) not in (int, float) or (isinstance(value, float) and not math.isfinite(value)):
            return {"verdict": "wrong_answer", "error": f"指标 {key} 缺失或不是有限数值"}
        for op, target in targets.items():
            if not COMPARE[op](value, target):
                return {"verdict": "wrong_answer", "metrics": selected, "error": f"{key} = {value}，要求 {op} {target}"}
    return {"verdict": "accepted", "metrics": selected}


def python_run(judge: Judge, project: Project, code: str,
               on_complete: Callable[[str], None] | None = None) -> Iterator[dict]:
    meta = project.meta
    judge.tmp_root.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=judge.tmp_root) as directory, ThreadPoolExecutor(max_workers=1) as pool:
        log = Path(directory) / "output"
        log.touch()
        def execute():
            result = judge.run(mode="project", runtime="ds", cases=[], code=code,
                               time_limit_ms=meta.run.timeout * 1000, args=meta.run.args,
                               data=project.directory / meta.data, log=log)
            if result["verdict"] == "accepted":
                last = ""
                with log.open(encoding="utf-8") as lines:
                    for line in lines:
                        if line.strip():
                            last = line
                result = evaluate_metrics(last, meta.success)
                if on_complete and result["verdict"] == "accepted":
                    on_complete(meta.id)
            return result

        future = pool.submit(execute)
        with log.open("rb") as reader:
            pending = b""
            while True:
                done = future.done()
                chunks = (pending + reader.read()).split(b"\n")
                pending = chunks.pop()
                if done and pending:
                    chunks.append(pending)
                for raw in chunks:
                    yield {"line": raw.decode("utf-8", errors="replace").rstrip("\r")}
                if done:
                    break
                time.sleep(0.15)
        yield {"result": future.result()}


@lru_cache(maxsize=16)
def sql_plan(project: Project) -> dict:
    """参考脚本的期望结果只取决于题库里的项目，按项目对象缓存（题库重载会换新对象）；每次 PGlite 跑一遍约 1 秒。"""
    meta = project.meta
    setup = shared_db(project.directory.parents[1], meta.data)
    checks = [c.model_dump() for c in meta.run.checks]
    timeout = meta.run.timeout * 1000
    expected, = run_node(mode="script", datasets=[setup], solution=project.reference, checks=checks, timeoutMs=timeout)
    return {"mode": "script", "setup": setup, "checks": checks, "expected": expected, "timeoutMs": timeout}
