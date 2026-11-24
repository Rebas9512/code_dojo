import { Link, useLoaderData, useParams } from 'react-router-dom'
import { practicePath, type ServerStatus, type TrackProblem, type TrackStage, type Skill } from '../api'
import { FORMAT_GLYPH, FORMAT_NAME } from '../labels'
import { useTracks } from '../tracks'
import { ProblemStatus } from '../components/ProblemStatus'
import { StageList } from '../components/StageList'
import { unitAnchor, useUnitAnchor } from './unitAnchor'

interface ProblemRow {
  problem: TrackProblem
  index: number
  anchor?: string
}

interface ProblemGroup {
  key: string
  title?: string
  anchor?: string
  project?: string
  rows: ProblemRow[]
}

function stageGroups(stage: TrackStage, problems: TrackProblem[]): ProblemGroup[] {
  const rows = problems.filter(p => p.stage === stage.id).map((problem, i) => ({ problem, index: i + 1 }))
  const units = stage.units.map(unit => ({
    key: unit.id, project: unit.project, anchor: unitAnchor(stage.id, unit.id),
    title: stage.units.length > 1 || unit.name !== stage.name ? unit.name : undefined,
    rows: rows.filter(row => row.problem.unit === unit.id),
  }))
  if (!rows.some(row => row.problem.week != null)) return units

  const byWeek = new Map<number, ProblemRow[]>()
  for (const row of rows) {
    const week = row.problem.week ?? Infinity
    if (!byWeek.has(week)) byWeek.set(week, [])
    byWeek.get(week)!.push(row)
  }
  // 地图仍按单元链接；周次混排时，定位到该单元第一次出现的位置。
  const seen = new Set<string>()
  const weeks = Array.from(byWeek).sort(([a], [b]) => a - b).map(([week, list]) => {
    const group: ProblemGroup = { key: 'week-' + week, title: Number.isFinite(week) ? `第 ${week} 周` : '未分周', rows: list }
    for (const [i, row] of list.entries()) {
      const unit = row.problem.unit
      if (seen.has(unit)) continue
      seen.add(unit)
      if (i === 0) group.anchor = unitAnchor(stage.id, unit)
      else row.anchor = unitAnchor(stage.id, unit)
    }
    return group
  })
  return [...weeks, ...units.filter(unit => !unit.rows.length)]
}

export function TrackPage() {
  const { track } = useParams()
  const current = useTracks().find((t) => t.id === track)!
  const [problems, skillList, health] = useLoaderData() as [TrackProblem[], Skill[], ServerStatus]
  const skills = new Map(skillList.map((s) => [s.id, s]))
  useUnitAnchor()
  const next = current.next

  return (
    <main className="track">
      {current.status === 'active' && current.language === 'python' && health.judge_mode === 'docker' && !health.judge_image_present && (
        <p className="notice tone-fail">判题镜像不存在：docker build -t code-dojo-judge-py:3.14 judge/python</p>
      )}
      {health.load_errors.length > 0 && (
        <details className="notice">
          <summary className="tone-fail">{health.load_errors.length} 个文件加载失败</summary>
          <ul>
            {health.load_errors.map((e) => (
              <li key={e.path}>
                <code>{e.path}</code> {e.message}
              </li>
            ))}
          </ul>
        </details>
      )}

      {current.status === 'planned' && <StageList track={current} />}
      {next && (
        <Link to={practicePath(next)} className="continue">
          <span className="faint">继续</span>
          <span className="continue-title">{next.title}</span>
          <span className="faint">{next.source ? '复习' : '新题'}</span>
        </Link>
      )}

      {current.status === 'active' && current.stages.map(stage => (
        <section key={stage.id} className="stage">
          <header className="stage-head">
            <span className="stage-code">{stage.id}</span>
            <span className="stage-name">{stage.name}</span>
            <span className="faint">{stage.solved}/{stage.total}</span>
          </header>
          <div className="skill-groups">
            {stageGroups(stage, problems).map(group => (
              <div key={group.key} id={group.anchor} className="skill-group">
                {group.title && <h2>{group.title}</h2>}
                {group.project && <Link to={'/project/' + group.project}>打开项目</Link>}
                {!group.rows.length && <p className="muted">暂无题目</p>}
                <ol className="problem-list">
                  {group.rows.map(({ problem: p, index, anchor }) => {
                    const intro = p.skills.introduces
                    return <li key={p.id} id={anchor}>
                      <Link to={`/p/${p.id}`} className={`problem-row ${p.status ?? 'todo'}`}>
                        <ProblemStatus status={p.status} />
                        <span className="idx faint">{index}</span>
                        <span className="title">{p.title}{p.optional && <span className="optional"> 选修</span>}</span>
                        <span className="glyph" title={FORMAT_NAME[p.format]}>{FORMAT_GLYPH[p.format]}</span>
                        <span className="new-skill">{intro && `+ ${skills.get(intro)?.name ?? intro}`}</span>
                        <span className="difficulty faint" title="难度 1–100">{p.difficulty}</span>
                      </Link>
                    </li>
                  })}
                </ol>
              </div>
            ))}
          </div>
        </section>
      ))}
    </main>
  )
}
