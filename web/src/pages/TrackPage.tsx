import { Link, useLoaderData, useParams } from 'react-router-dom'
import { practicePath, type ServerStatus, type TrackProblem, type Skill } from '../api'
import { FORMAT_GLYPH, FORMAT_NAME } from '../labels'
import { useTracks } from '../tracks'
import { ProblemStatus } from '../components/ProblemStatus'
import { StageList } from '../components/StageList'
import { unitAnchor, useUnitAnchor } from './unitAnchor'

export function TrackPage() {
  const { track } = useParams()
  const current = useTracks().find((t) => t.id === track)!
  const [problems, skillList, health] = useLoaderData() as [TrackProblem[], Skill[], ServerStatus]
  const skills = new Map(skillList.map((s) => [s.id, s]))
  useUnitAnchor()
  const lists = new Map<string, { problem: TrackProblem; index: number }[]>()
  const counts = new Map<string, number>()
  for (const problem of problems) {
    const key = unitAnchor(problem.stage, problem.unit)
    const index = (counts.get(problem.stage) ?? 0) + 1
    counts.set(problem.stage, index)
    if (!lists.has(key)) lists.set(key, [])
    lists.get(key)!.push({ problem, index })
  }

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

      {current.status === 'active' && current.stages.map(({ id: stage, name, solved, total, units }) => (
        <section key={stage} className="stage">
          <header className="stage-head">
            <span className="stage-code">{stage}</span>
            <span className="stage-name">{name}</span>
            <span className="faint">{solved}/{total}</span>
          </header>
          <div className="skill-groups">
            {units.map((unit) => {
              const anchor = unitAnchor(stage, unit.id)
              const list = lists.get(anchor) ?? []
              return <div key={unit.id} id={anchor} className="skill-group">
                {(units.length > 1 || unit.name !== name) && <h2>{unit.name}</h2>}
                {!list.length && <p className="muted">暂无题目</p>}
                <ol className="problem-list">
                  {list.map(({ problem: p, index }) => {
                    const intro = p.skills.introduces
                    return <li key={p.id}>
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
            })}
          </div>
        </section>
      ))}
    </main>
  )
}
