#!/usr/bin/env python3
"""在 PGlite（PostgreSQL 18，Node 22）上跑每道 SQL 题的参考解和"典型错误写法"。

检查项：
  - 查询题的参考解结果非空；修改题的参考解必须改变每个数据集的检查结果。要求行序时结果查询必须有 ORDER BY。
  - 查询题和修改题的 wrong_examples 每一条都能运行，
    并且至少在一个**隐藏**数据集上和参考解结果不同——保证隐藏数据真能抓住这个错误。
  - 脚本题逐项比较查询与探针，保证参考脚本全过，每段错误脚本至少在一个数据集上判错。
  - fix 题：starter.sql 在样例数据集（datasets 第一项）上就和参考解不同（学习者点"运行"能看到 bug）。
  - 打印每个数据集上参考解的结果（默认最多 12 行），方便人工核对期望答案。
  - 课（problems/<学习线>/lessons/*/lesson.yaml）里的每个 example：在它写的 db（+ patch）上能运行。
结果比较规则和 docs/problem-format.md 一致：列数相同；数字容差 1e-6；NULL 等于 NULL；
日期按 ISO 字符串；ordered: false 时忽略行序；不比较列名。

依赖：在 scripts/curriculum/ 下 `npm install` 过（@electric-sql/pglite），以及 PyYAML。
用法：python3 scripts/curriculum/verify_sql.py [--only sql-0-01] [-q] [--rows 12]
"""
from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("需要 PyYAML：uv run --with pyyaml python3 scripts/curriculum/verify_sql.py", file=sys.stderr)
    sys.exit(2)

HERE = Path(__file__).resolve().parent
from track_files import Track, active_tracks, lesson_files, stage_dirs
from app.sql_judge import validation_job

NUMERIC_TYPES = {20, 21, 23, 700, 701, 1700}


# ---------------------------------------------------------------------------
# 数据集与执行
# ---------------------------------------------------------------------------

def dataset_scripts(problem_dir: Path, spec: str) -> list[str]:
    """把 datasets 里的一项（db:bookstore / db:bookstore + datasets/x.sql / datasets/own.sql）展开成脚本列表。"""
    scripts = []
    for part in [p.strip() for p in spec.split("+")]:
        if part.startswith("db:"):
            db = problem_dir.parents[1] / "_db" / part[3:]
            scripts += [(db / "schema.sql").read_text(encoding="utf-8"), (db / "seed.sql").read_text(encoding="utf-8")]
        else:
            scripts.append((problem_dir / part).read_text(encoding="utf-8"))
    return scripts


def run_jobs(jobs: list[dict]) -> dict[str, dict]:
    """jobs: [{key, setup: [...], queries: {name: sql}}] → {key: {setupError, results}}"""
    if not (HERE / "node_modules" / "@electric-sql" / "pglite").exists():
        raise SystemExit("缺少 PGlite：先在 scripts/curriculum/ 下运行 npm install")
    proc = subprocess.run(
        ["node", "--experimental-strip-types", str(HERE / "pglite_runner.mjs")], input=json.dumps(jobs), capture_output=True,
        text=True, cwd=HERE, env={"TZ": "UTC", "PATH": __import__("os").environ.get("PATH", "")},
    )
    if proc.returncode != 0:
        raise SystemExit(f"pglite_runner 失败：\n{proc.stderr}")
    return {r["key"]: r for r in json.loads(proc.stdout)}


# ---------------------------------------------------------------------------
# 结果比较
# ---------------------------------------------------------------------------

def norm_cell(v, type_id: int):
    if v is None:
        return None
    if type_id in NUMERIC_TYPES and isinstance(v, str):
        try:
            return float(v)
        except ValueError:
            return v
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return float(v)
    if type_id in (1114, 1184) and isinstance(v, str):
        return v.replace(" ", "T")
    return v


def norm_result(r: dict) -> list[list]:
    return [[norm_cell(v, t) for v, t in zip(row, r["types"])] for row in r["rows"]]


def _cell_eq(a, b) -> bool:
    if isinstance(a, float) and isinstance(b, float):
        return math.isclose(a, b, rel_tol=1e-6, abs_tol=1e-6)
    return a == b


def _sort_key(row):
    return [(0, "") if v is None else (1, round(v, 6)) if isinstance(v, float) else (2, str(v)) for v in row]


def same_result(a: list[list], b: list[list], ordered: bool) -> bool:
    if len(a) != len(b):
        return False
    if a and b and len(a[0]) != len(b[0]):
        return False
    if not ordered:
        a, b = sorted(a, key=_sort_key), sorted(b, key=_sort_key)
    return all(len(x) == len(y) and all(_cell_eq(p, q) for p, q in zip(x, y)) for x, y in zip(a, b))


def fmt_cell(v) -> str:
    if v is None:
        return "NULL"
    if isinstance(v, float) and v.is_integer() and abs(v) < 1e15:
        return str(int(v))
    return str(v)


def markdown_table(columns: list[str], rows: list[list], limit: int) -> str:
    lines = ["| " + " | ".join(columns) + " |", "|" + "---|" * len(columns)]
    for row in rows[:limit]:
        lines.append("| " + " | ".join("NULL" if v is None else str(v) for v in row) + " |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 校验
# ---------------------------------------------------------------------------

def load_problems(tracks: list[Track], only: str) -> list[tuple[Path, dict]]:
    out = []
    for sd in stage_dirs(tracks):
        if not sd.exists():
            continue
        items = []
        for d in sd.iterdir():
            if (d / "problem.yaml").exists() and d.name.startswith(only):
                meta = yaml.safe_load((d / "problem.yaml").read_text(encoding="utf-8"))
                if meta.get("format") == "inspect":
                    continue
                items.append((meta.get("order", 0), d, meta))
        out += [(d, m) for _, d, m in sorted(items, key=lambda x: (x[0], x[1].name))]
    return out


def build_jobs(problems: list[tuple[Path, dict]]) -> list[dict]:
    jobs = []
    for d, meta in problems:
        queries = {"solution": (d / "solution.sql").read_text(encoding="utf-8")}
        for i, w in enumerate(meta.get("wrong_examples") or []):
            queries[f"wrong{i}"] = w["sql"]
        if (d / "starter.sql").exists():
            queries["starter"] = (d / "starter.sql").read_text(encoding="utf-8")
        for k, spec in enumerate(meta["datasets"]):
            jobs.append({"key": f"{d.name}#{k}", "setup": dataset_scripts(d, spec), "queries": queries})
    return jobs


def verify(problems, results, quiet: bool, rows_limit: int) -> int:
    failed = 0
    for d, meta in problems:
        issues: list[str] = []
        ordered = bool(meta.get("ordered"))
        datasets = meta["datasets"]
        sol_sql = (d / "solution.sql").read_text(encoding="utf-8")
        if ordered and not re.search(r"\border\s+by\b", sol_sql, re.I):
            issues.append("ordered: true，但参考解没有 ORDER BY")
        sol_rows = []
        detail = []
        for k, spec in enumerate(datasets):
            res = results[f"{d.name}#{k}"]
            if res["setupError"]:
                issues.append(f"数据集 {spec} 建库失败：{res['setupError']}")
                sol_rows.append(None)
                continue
            sol = res["results"]["solution"]
            if not sol["ok"]:
                issues.append(f"参考解在 {spec} 上报错：{sol['error']}")
                sol_rows.append(None)
                continue
            rows = norm_result(sol)
            sol_rows.append(rows)
            if not rows:
                issues.append(f"参考解在 {spec} 上结果为空")
            label = "样例" if k == 0 else "隐藏"
            detail.append(f"    [{label}] {spec} → {len(rows)} 行，列 {sol['columns']}")
            for row in sol["rows"][:rows_limit]:   # 打印 PostgreSQL 的原始文本（33.00、2025-03-01）
                detail.append("        " + " | ".join("NULL" if v is None else str(v) for v in row))
            if len(rows) > rows_limit:
                detail.append(f"        …（还有 {len(rows) - rows_limit} 行）")

        def differs_on(name: str) -> tuple[list[int], list[str]]:
            diff, errors = [], []
            for k, spec in enumerate(datasets):
                res = results[f"{d.name}#{k}"]
                if res["setupError"] or sol_rows[k] is None:
                    continue
                r = res["results"][name]
                if not r["ok"]:
                    errors.append(f"{spec}: {r['error']}")
                    continue
                if not same_result(sol_rows[k], norm_result(r), ordered):
                    diff.append(k)
            return diff, errors

        for i, w in enumerate(meta.get("wrong_examples") or []):
            diff, errors = differs_on(f"wrong{i}")
            hidden_diff = [k for k in diff if k > 0]
            why = w.get("why", "")
            if errors:
                issues.append(f"错误写法 #{i + 1}（{why}）运行报错：{errors[0]}")
            elif not hidden_diff:
                issues.append(f"错误写法 #{i + 1}（{why}）在所有隐藏数据集上都和参考解相同——隐藏数据抓不住它")
            else:
                where = ", ".join("样例" if k == 0 else f"隐藏#{k}" for k in diff)
                detail.append(f"    ✓ 错误写法 #{i + 1}（{why}）被抓住：{where}")
        if (d / "starter.sql").exists() and meta.get("format") == "fix":
            diff, errors = differs_on("starter")
            if errors:
                issues.append(f"starter.sql 运行报错：{errors[0]}")
            elif 0 not in diff:
                issues.append("fix 题的 starter.sql 在样例数据集上和参考解一样——学习者看不到 bug")
            else:
                detail.append("    ✓ starter.sql 在样例数据上就与参考解不同")
        if not meta.get("wrong_examples"):
            issues.append("没有 wrong_examples（至少写一条典型错误写法）")

        mark = "✗" if issues else "✓"
        if issues or not quiet:
            print(f"{mark} {d.name}  （{len(datasets)} 个数据集，ordered={ordered}）")
        if not quiet:
            print("\n".join(detail))
        for msg in issues:
            print(f"    ✗ {msg}")
        failed += bool(issues)
    return failed


def lesson_examples(tracks: list[Track]) -> list[tuple[Path, int, dict]]:
    out = []
    for yml in lesson_files(tracks):
        lesson = yaml.safe_load(yml.read_text(encoding="utf-8")) or {}
        for i, st in enumerate(lesson.get("steps") or [], 1):
            if (st or {}).get("type") == "example" and "data" not in st:
                out.append((yml.parent, i, st))
    return out


def verify_lessons(tracks: list[Track], quiet: bool) -> tuple[int, int]:
    examples = lesson_examples(tracks)
    jobs = []
    for lesson_dir, i, st in examples:
        lid = lesson_dir.name
        db = lesson_dir.parents[1] / "_db" / str(st.get("db"))
        setup = [(db / "schema.sql").read_text(encoding="utf-8"), (db / "seed.sql").read_text(encoding="utf-8")]
        if st.get("patch"):
            setup.append(st["patch"])
        jobs.append({"key": f"{lid}#{i}", "setup": setup, "queries": {"example": st.get("code") or ""}})
    results = run_jobs(jobs) if jobs else {}
    failed = 0
    for lesson_dir, i, st in examples:
        lid = lesson_dir.name
        res = results[f"{lid}#{i}"]
        r = res["results"].get("example") if not res["setupError"] else None
        if not r or not r["ok"]:
            failed += 1
            print(f"✗ {lid} 第 {i} 步（{st.get('skill')}）运行出错：{res['setupError'] or (r or {}).get('error')}")
        elif not quiet:
            print(f"  {lid} 第 {i:>2} 步 {st.get('skill'):<20} → {len(r['rows'])} 行，列 {r['columns']}")
    return len(examples), failed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", default="", help="只校验 id 以此开头的题")
    ap.add_argument("-q", "--quiet", action="store_true", help="只打印有问题的题")
    ap.add_argument("--rows", type=int, default=12, help="每个数据集最多打印几行结果")
    args = ap.parse_args()
    tracks = active_tracks("sql")
    problems = load_problems(tracks, args.only)
    queries = [(d, m) for d, m in problems if m.get("mode") not in ("dml", "script")]
    jobs = build_jobs(queries)
    failed = 0
    for directory, meta in problems:
        if meta.get("mode") in ("dml", "script"):
            try:
                datasets = [dataset_scripts(directory, spec) for spec in meta["datasets"]]
                jobs.append({"key": directory.name, "validation": validation_job(directory, meta, datasets)})
            except (ValueError, OSError) as exc:
                print(f"✗ {directory.name}：{exc}")
                failed += 1
    results = run_jobs(jobs) if jobs else {}
    failed += verify(queries, results, args.quiet, args.rows)
    for job in jobs:
        if "validation" in job:
            result = results[job["key"]]
            if "error" in result:
                print(f"✗ {job['key']}：{result['error']}")
                failed += 1
            elif not args.quiet:
                print(f"✓ {job['key']}  （{len(result['tables'])} 个数据集）")
                for i, table in enumerate(result["tables"], 1):
                    print(f"    数据集 {i}")
                    if "checks" in table:
                        for check, value in zip(job["validation"]["checks"], table["checks"], strict=True):
                            print(f"    {check['label']} → {value.get('outcome', '通过')}")
                            if "rows" in value:
                                print(markdown_table(value["columns"], value["rows"], args.rows))
                    else:
                        print(markdown_table(table["columns"], table["rows"], args.rows))
    print(f"\n{len(problems) - failed}/{len(problems)} 道 SQL 题通过")
    lesson_tracks = [t for t in tracks if args.only.startswith(t.skill_prefix + "-")] or tracks
    n_ex, bad_ex = verify_lessons(lesson_tracks, args.quiet)
    print(f"课的示例：{n_ex - bad_ex}/{n_ex} 个能在 PGlite 上运行")
    return 1 if failed or bad_ex else 0


if __name__ == "__main__":
    sys.exit(main())
