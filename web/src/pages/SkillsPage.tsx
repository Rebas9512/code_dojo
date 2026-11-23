import { Link, useLoaderData, useParams } from 'react-router-dom'
import type { Skill } from '../api'
import { Markdown } from '../components/Markdown'
import { ProblemStatus } from '../components/ProblemStatus'
import { StageList } from '../components/StageList'
import { FORMAT_NAME } from '../labels'
import { useTracks } from '../tracks'
import { unitAnchor, useUnitAnchor } from './unitAnchor'

export function SkillsPage() {
  const { track } = useParams()
  const tracks = useTracks()
  const current = tracks.find((t) => t.id === track)!
  const skills = useLoaderData() as Skill[]
  useUnitAnchor()
  const byId = new Map(skills.map((s) => [s.id, s]))
  if (current.status === 'planned') return <main className="track"><StageList track={current} /></main>
  return <main className="track skill-page">
    <h1>知识点 <small>{skills.length}</small></h1>
    {current.stages.map((stage) => {
      return <section className="stage" key={stage.id}>
        <header className="stage-head"><span className="stage-code">{stage.id}</span>
          <span className="stage-name">{stage.name}</span></header>
        <div className="skill-groups">
          {stage.units.map((unit) => <div className="skill-group" key={unit.id} id={unitAnchor(stage.id, unit.id)}>
            {(stage.units.length > 1 || unit.name !== stage.name) && <h2>{unit.name}</h2>}
            {!unit.skills.length && <p className="muted">暂无知识点</p>}
            {unit.skills.map((ref) => byId.get(ref.id)).filter((s) => s !== undefined).map((s) =>
            <details className="skill" key={s.id} id={s.id}>
              <summary>
                <span className="skill-name">{s.name}</span>
                <small className={s.state === 'mastered' ? 'tone-pass' : 'muted'}>
                  {{ unlearned: '未学', learning: '学习中', mastered: '掌握', review: '需复习' }[s.state]}
                </small>
                {s.lesson && <small className="lesson-mark" title={s.lesson.title}>课</small>}
                {s.problems.map((p) => <ProblemStatus key={p.id} status={p.status} />)}
                {s.prereqs.length > 0 && <span className="skill-prereqs">先学：{s.prereqs.map((pre) =>
                  pre.track === track ? pre.name : `${tracks.find((t) => t.id === pre.track)?.name ?? pre.track} · ${pre.name}`
                ).join('、')}</span>}
              </summary>
              <div className="skill-detail"><p className="muted">独立写对 {s.counted_solves} 道
                {s.last_used && ' · 最近练习 ' + new Date(s.last_used).toLocaleDateString('zh-CN')}</p><Markdown>{s.card}</Markdown>
                {s.problems.map((p) => <Link key={p.id} to={`/p/${p.id}`}>
                  <ProblemStatus status={p.status} /> {FORMAT_NAME[p.format]} · {p.title} →
                </Link>)}
              </div>
            </details>)}
          </div>)}
        </div>
      </section>
    })}
  </main>
}
