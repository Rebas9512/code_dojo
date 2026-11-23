"""地图、题目列表和知识点页共用的单元归属。"""

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any

from .mastery import Progress
from .problems import Problem, Skill
from .tracks import Track


@dataclass
class Unit:
    id: str
    name: str
    skills: list[Skill] = field(default_factory=list)
    problems: list[Problem] = field(default_factory=list)


def group_units(track: Track, skills: dict[str, Skill], ordered: list[Problem]) -> dict[str, list[Unit]]:
    """ordered 是题库的学习顺序。跟随前题的归属只在同一阶段内有效。"""
    stages: dict[str, list[Unit]] = {sid: [] for sid in track.stages}
    if track.status == "planned":
        return stages
    by_stage: dict[str, list[Problem]] = defaultdict(list)
    for problem in ordered:
        by_stage[problem.meta.stage].append(problem)
    for sid, name in track.stages.items():
        local = [s for s in skills.values() if s.track == track.id and s.stage == sid]
        groups = {s.id: s.group for s in local if s.group is not None}
        if not groups:
            stages[sid] = [Unit(sid, name, local, by_stage[sid])]
            continue
        names = track.units.get(sid, {})
        numbers = sorted(set(groups.values()).union(names))
        units = {g: Unit(str(g), names.get(g, f"第 {g} 组")) for g in numbers}
        first = min(units)
        for skill in local:
            units[groups.get(skill.id, first)].skills.append(skill)
        previous = first
        for problem in by_stage[sid]:
            refs = problem.meta.skills
            # problem.yaml 可以写 unit: N 直接指定单元（推算不对时用，例如只用到前置线技能的练习题）；
            # 指定后，后面没有本阶段技能的题也跟着它走
            if problem.meta.unit in units:
                previous = problem.meta.unit
            else:
                previous = max(
                    (groups[sk] for sk in [*refs.requires, refs.introduces] if sk is not None and sk in groups),
                    default=previous,
                )
            units[previous].problems.append(problem)
        stages[sid] = list(units.values())
    return stages


def progress_frontier(stages: dict[str, list[Unit]], status: dict[str, str]) -> dict[str, str] | None:
    """按地图顺序，从最靠后的已做题开始找下一道未做的必修题。"""
    units = [unit for stage in stages.values() for unit in stage]
    start_unit, after_last = 0, 0
    for i, unit in enumerate(units):
        for j, problem in enumerate(unit.problems):
            if problem.id in status:
                start_unit, after_last = i, j + 1

    for i in range(start_unit, len(units)):
        problems = units[i].problems
        if i == start_unit and after_last:
            # 当前单元先往后走，再从头补漏；后续单元直接从头找。
            problems = problems[after_last:] + problems[:after_last]
        for problem in problems:
            if problem.id not in status and not problem.meta.optional:
                return {"id": problem.id, "title": problem.meta.title}
    return None


def introduction_status(ordered: list[Problem], statuses: dict[str, dict[str, str]]) -> dict[str, str]:
    """技能小点取引入它的题中最好的提交状态。"""
    rank = {"attempted": 1, "assisted": 2, "solved": 3}
    best: dict[str, str] = {}
    for p in ordered:
        skill = p.meta.skills.introduces
        result = statuses[p.meta.track].get(p.id)
        if skill and result and (skill not in best or rank[result] > rank[best[skill]]):
            best[skill] = result
    return best


def stage_progress(track: Track, stages: dict[str, list[Unit]], status: dict[str, str],
                   skill_status: dict[str, str], progress: Progress) -> list[dict[str, Any]]:
    rows = []
    for sid, units in stages.items():
        summaries = []
        for unit in units:
            counts = Counter(status.get(p.id) for p in unit.problems)
            upcoming = progress.next_item([p.id for p in unit.problems])
            summaries.append({
                "id": unit.id, "name": unit.name, "total": len(unit.problems),
                "solved": counts["solved"] + counts["assisted"], "assisted": counts["assisted"],
                "attempted": counts["attempted"],
                "mastered": sum(progress.state(s.id) == "mastered" for s in unit.skills),
                "skills": [{"id": s.id, "name": s.name, "status": skill_status.get(s.id)} for s in unit.skills],
                "next": upcoming,
            })
        rows.append({"id": sid, "name": track.stages[sid], "units": summaries,
                     "total": sum(u["total"] for u in summaries), "solved": sum(u["solved"] for u in summaries)})
    return rows
