#!/usr/bin/env python3
"""用平台判题器逐题验证标准写法、说明和进阶代码。"""

from __future__ import annotations

import argparse
import sys
from functools import cache
from glob import escape
from pathlib import Path

from check_curve import PROBLEMS, Report, closure, load_skills, load_tracks, project_names, standard_skill_errors
from app.config import load_settings
from app.judge import Judge
from app.problems import Problem, ProblemBank, load_problem
from app.sql_judge import dataset, verify_sql_files
from app.standard import MARKDOWN_PART, note_sections
from app.tracks import load_track


def note_errors(markdown: str, problem: Problem) -> tuple[list[str], str | None]:
    sections = note_sections(markdown)
    titles = [title for title, _ in sections]
    required = ["思路", "写法要点"]
    if problem.track.id in ("python", "algo") or "复杂度" in titles:
        required.insert(1, "复杂度")
    if "进阶写法" in titles:
        required.append("进阶写法")
    errors = []
    if titles != required:
        errors.append(f"standard.md 小节应依次为{'、'.join(required)}")
    advanced = None
    for title, body in sections:
        if not body:
            errors.append(f"standard.md 的「{title}」缺少内容")
        if title == "复杂度" and problem.meta.track == "algo" and not all(word in body for word in ("时间", "空间")):
            errors.append("算法题需要说明时间和空间复杂度")
        if title == "进阶写法":
            blocks = [m for m in MARKDOWN_PART.finditer(body) if m["language"] is not None]
            if len(blocks) != 1 or blocks[0]["language"].strip() != problem.track.language or not blocks[0]["code"].strip():
                errors.append(f"进阶写法需要一个 {problem.track.language} 代码块")
            else:
                block = blocks[0]
                advanced = block["code"]
                if not (body[:block.start()] + body[block.end():]).strip():
                    errors.append("进阶写法需要简短说明")
    return errors, advanced


@cache
def skill_graph() -> dict[str, dict]:
    """全部学习线的技能图（含跨线前置），用来展开 requires 的前置，规则和参考解一致。"""
    tracks, _ = load_tracks(PROBLEMS)
    graph: dict[str, dict] = {}
    for track in tracks.values():
        graph.update(load_skills(track, Report()))
    return graph


def standard_sources(p: Problem) -> tuple[list[str], dict[str, str]]:
    files = {f.name for f in p.path.glob("standard.*")}
    if not files:
        return [], {}
    if p.meta.format in ("predict", "inspect"):
        return ["预测题和看数据题不提供参考答案"], {}
    filename = "standard.sql" if p.track.language == "sql" else "standard.py"
    expected = {filename, "standard.md"}
    errors = [f"缺少 {name}" for name in sorted(expected - files)]
    errors += [f"该题不使用 {name}" for name in sorted(files - expected)]
    sources = {}
    if filename in files:
        code = p.file(filename).read_text(encoding="utf-8")
        sources["标准写法"] = code
        skills = p.meta.skills
        declared = set(skills.requires)
        if skills.introduces:
            declared.add(skills.introduces)
        allowed = closure(skill_graph(), declared)
        errors.extend(standard_skill_errors(code, p.track.language, p.meta.mode, p.meta.entry, allowed,
                                            project_names(p.path, p.meta.project)))
    if "standard.md" in files:
        issues, advanced = note_errors(p.file("standard.md").read_text(encoding="utf-8"), p)
        errors.extend(issues)
        if advanced is not None:
            sources["进阶写法"] = advanced
    return errors, sources


def check_answers(judge: Judge, p: Problem) -> list[str]:
    """全库校验也从这里运行 SQL 验题，各种写法共用一次 PGlite 启动。"""
    errors, sources = standard_sources(p)
    if p.track.language == "sql" and not p.inspect:
        try:
            verify_sql_files(p.path, p.meta.model_dump(), [dataset(p, spec) for spec in p.meta.datasets], answers=sources)
        except (ValueError, OSError) as exc:
            errors.append(str(exc))
    else:
        for label, code in sources.items():
            cases = p.cases("all")
            result = judge.run(mode=p.meta.mode or "function", code=code, cases=cases, **p.judge_options())
            if result["verdict"] != "accepted":
                bad = next((case for case in result["cases"] if case["status"] != "passed"), {})
                detail = result.get("error") or bad.get("error") or ""
                errors.append(f"{label}没通过：{result['verdict']}（{result.get('passed', 0)}/{len(cases)}）{detail}")
    return errors


def selected_directories(root: Path, only: str, track: str | None) -> list[Path]:
    # 先按题号筛目录；只有命中并且带 standard 文件的题才需要读取 YAML。
    base = root / track if track else root
    pattern = f"*/{escape(only)}*/standard.*"
    paths = base.glob(pattern if track else "*/" + pattern)
    return sorted({path.parent for path in paths})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", default="", help="题号前缀")
    parser.add_argument("--track", help="学习线目录名")
    args = parser.parse_args()
    settings = load_settings()
    if args.track and not (settings.problems_dir / args.track / "track.yaml").is_file():
        parser.error(f"没有这条学习线：{args.track}")
    directories = selected_directories(settings.problems_dir, args.only, args.track)
    judge = Judge.from_settings(settings)
    tracks = {}
    bank = ProblemBank(settings.problems_dir)
    failed = 0
    for directory in directories:
        track = directory.parents[1]
        try:
            if track not in tracks:
                tracks[track] = load_track(track / "track.yaml")
            problem = load_problem(directory, tracks[track])
            if problem.meta.project:
                if not bank.projects:
                    bank.refresh(stamp=0)
                problem = bank.problems[problem.id]
            issues = check_answers(judge, problem)
        except Exception as exc:  # 单题文件损坏时继续检查下一题。
            issues = [str(exc)]
        if issues:
            failed += 1
            print(f"✗ {directory.name}\n    " + "\n    ".join(issues))
        else:
            print(f"✓ {directory.name}")
    print(f"有参考答案 {len(directories)} 道，通过 {len(directories) - failed}，失败 {failed}")
    return int(failed > 0)


if __name__ == "__main__":
    sys.exit(main())
