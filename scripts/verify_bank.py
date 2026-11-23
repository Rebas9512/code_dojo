#!/usr/bin/env python3
"""题库校验（平台侧）：格式能否加载 + 用真正的判题沙箱跑每道 Python 题的参考解。

检查项：
  1. problems/ 下所有题目都能按 docs/problem-format.md 加载（没有 load_errors）；
  2. function / class / stdio 题：solution.py 跑全部用例（examples + hidden）必须 accepted；
  3. predict 题：solution.py 能正常运行、有输出；
  4. fix 题：starter.py（带 bug 的代码）必须至少挂一个用例。
  5. 标准写法与进阶写法使用相同判题规则；标准写法还要通过显式技能和说明检查。
  6. SQL 题：Node PGlite 实跑各数据集，检查参考解、典型错误写法和改错题初始代码。

用法：
  cd server && uv run python ../scripts/verify_bank.py [--judge local|docker] [--only <题目 id 前缀>] [--jobs 4]
"""

from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "server"))
sys.path.insert(0, str(Path(__file__).resolve().parent / "curriculum"))
from verify_standard import check_answers  # noqa: E402
from app.config import load_settings  # noqa: E402
from app.judge import Judge  # noqa: E402
from app.local_judge import PreparationError  # noqa: E402
from app.problems import Problem, ProblemBank  # noqa: E402


def check_problem(judge: Judge, p: Problem) -> list[str]:
    m = p.meta
    problems = check_answers(judge, p)
    if p.track.language == "sql" or p.inspect:
        return problems
    solution = p.read("solution.py")
    if solution is None:
        return [*problems, "缺少 solution.py"]

    if m.mode == "predict":
        r = judge.run(mode="stdio", code=solution, cases=[{"stdin": "", "expected": ""}], **p.judge_options())
        case = (r.get("cases") or [{}])[0]
        if r["verdict"] not in ("accepted", "wrong_answer"):
            problems.append(f"展示的程序运行出错：{r.get('error') or case.get('error')}")
        elif not (case.get("actual") or "").strip():
            problems.append("展示的程序没有输出")
        return problems

    common = dict(
        mode=m.mode or "function",
        cases=p.cases("all"),
        **p.judge_options(),
    )
    n_cases = len(common["cases"])
    n_examples = len(p.cases("examples"))
    if n_examples < 2 or n_cases - n_examples < 3:
        problems.append(f"用例不够：examples {n_examples}（至少 2），hidden {n_cases - n_examples}（至少 3）")

    r = judge.run(code=solution, **common)
    if r["verdict"] != "accepted":
        bad = next((c for c in r.get("cases", []) if c["status"] != "passed"), {})
        problems.append(
            f"参考解没通过：{r['verdict']} {r.get('passed')}/{r.get('total')} "
            f"{r.get('error') or ''} 输入={bad.get('input')} 期望={bad.get('expected')} 实际={bad.get('actual')} "
            f"{bad.get('error') or ''}".strip()
        )

    if m.format == "fix":
        starter = p.read("starter.py")
        if starter is None:
            problems.append("fix 题缺少 starter.py")
        else:
            r2 = judge.run(code=starter, **common)
            if r2["verdict"] == "accepted":
                problems.append("fix 题的 starter.py（带 bug 的代码）居然全部通过，bug 没被测试抓住")
            elif r2["verdict"] == "system_error":
                problems.append(f"无法运行改错题的初始代码：{r2.get('error')}")
    if p.track.runtime == "ds":
        for wrong in getattr(m, "wrong_examples", []):
            r = judge.run(code=wrong["code"], **common)
            if r["verdict"] in ("accepted", "system_error"):
                problems.append(f"典型错误写法未验证：{wrong['why']}（{r['verdict']}）")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", default="", help="只校验 id 以此开头的题")
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--judge", choices=("local", "docker"), help="指定 Python 判题方式")
    args = parser.parse_args()

    settings = load_settings()
    if args.judge:
        settings = replace(settings, judge_mode=args.judge)
    bank = ProblemBank(settings.problems_dir)
    bank.refresh(force=True)
    judge = Judge.from_settings(settings, concurrency=args.jobs)
    selected = [p for p in bank.ordered() if p.id.startswith(args.only)]
    # 加载时已用共用的格式检查解析每个数据块，校验正确答案和误解映射。
    inspect = [p for p in selected if p.inspect]
    python = [p for p in selected if not p.inspect and p.track.language == "python"]
    sql = [p for p in selected if not p.inspect and p.track.language == "sql"]
    for runtime in sorted({p.track.runtime for p in python}):
        if judge.backends[runtime] == "docker" and not judge.image_present(runtime):
            image = judge.image_for(runtime)
            print(f"判题镜像 {image} 不存在，先运行：docker build -t {image} judge/{runtime}")
            return 2
        if judge.backends[runtime] == "local":
            # 先准备一次，安装失败时整批只报一次原因。
            try:
                judge.local.interpreter(runtime)
            except PreparationError as exc:
                print(exc)
                return 2

    failed = 0
    for err in bank.errors:
        failed += 1
        print(f"✗ 加载失败 {err.path}\n    {err.message}")

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda p: (p, check_problem(judge, p)), python + sql + inspect))
    passed = {"python": 0, "sql": 0}
    for p, issues in results:
        if issues:
            failed += 1
            print(f"✗ {p.id}")
            for issue in issues:
                print(f"    {issue}")
        elif not p.inspect:
            passed[p.track.language] += 1
    print(f"\nPython：{passed['python']}/{len(python)} 通过；"
          f"看数据作答：{len(inspect)} 道已验证；SQL：{passed['sql']}/{len(sql)} 通过；加载错误 {len(bank.errors)} 个")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
