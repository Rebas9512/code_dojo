import { useState } from 'react'
import { Link, useLoaderData, useNavigate, useRevalidator } from 'react-router-dom'
import { api, practicePath, type PracticeLink, type TodayPlan, type Week } from '../api'
import { useTracks } from '../tracks'
import { useTutorMemory } from '../tutorMemory'
import { unitAnchor } from './unitAnchor'
import './plan.css'

const percent = (n: number) => Math.round(n * 100) + '%'
const shortDate = (iso: string) => iso.slice(5).replace('-', '/')
export const variantRequest = '请出一道同套路的新题，使用原题的焦点技能，换一个场景，难度相近。'

function ReviewRow({ item }: { item: PracticeLink }) {
  const navigate = useNavigate()
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  async function generate() {
    setBusy(true)
    try {
      const parent = item.parent ?? item.id
      const extra = await api.createExtra(parent, variantRequest, undefined, { review_source: item.source, review_due: item.due })
      navigate(practicePath({ ...item, id: extra.id, parent, generate: false }))
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setBusy(false)
    }
  }
  return <li><small>{item.rewrite ? '重写' : '复习'} · {shortDate(item.due!)}</small>
    {item.generate ? <span>{item.title} <button className="link" disabled={busy} onClick={generate}>
      {busy ? '正在出题…' : '让助教出一道同套路的'}</button></span> :
      <Link to={practicePath(item)}>{item.title} →</Link>}
    {error && <span role="alert" className="tone-fail">{error}</span>}</li>
}

export function TodayPage() {
  const plan = useLoaderData() as TodayPlan
  const { revalidate } = useRevalidator()
  const [limit, setLimit] = useState(String(plan.daily_limit))
  const [busy, setBusy] = useState(false)
  const memory = useTutorMemory(true)
  const [clearing, setClearing] = useState(false)
  const [error, setError] = useState('')
  async function clearMemory() {
    if (!window.confirm('清空本机现有的笔记？删除会同步，离线新增或更新的笔记可能再次出现。历史记录会保留。')) return
    setClearing(true)
    setError('')
    try { await api.clearMemory() }
    catch (err) { setError((err as Error).message) }
    finally { setClearing(false) }
  }
  return <main className="study-page">
    <header><h1>今日计划</h1><time dateTime={plan.date}>{plan.date.replaceAll('-', '.')}</time></header>
    <section>
      <div className="plan-heading"><h2>到期复习</h2>
        <div className="plan-settings">
          <form onSubmit={async e => {
            e.preventDefault()
            setBusy(true)
            setError('')
            try { await api.dailyLimit(Number(limit)); await revalidate() }
            catch (err) { setError((err as Error).message) }
            finally { setBusy(false) }
          }}><label>每日上限 <input type="number" min="0" required value={limit}
            onChange={e => setLimit(e.target.value)} /></label>
            {limit !== String(plan.daily_limit) && <button className="secondary" disabled={busy}>保存</button>}
          </form>
          <div className="memory-controls">
            <label><input type="checkbox" role="switch" checked={memory.enabled === true}
              disabled={memory.enabled === null} aria-disabled={memory.busy} onChange={memory.toggle} />允许助教记忆</label>
            <button className="ghost" onClick={clearing ? undefined : clearMemory} aria-disabled={clearing}>清空记忆</button>
          </div>
        </div>
      </div>
      {(error || memory.error) && <p role="alert">{error || memory.error}</p>}
      {plan.reviews.length ? <ul>{plan.reviews.map(item => <ReviewRow key={item.source} item={item} />)}</ul> :
        <p className="muted">今天没有待做的复习。</p>}
    </section>
    <section><h2>下一道新题</h2><ul>{plan.tracks.map(track => <li key={track.id}><small>{track.name}</small>
      {track.next ? <Link to={practicePath(track.next)}>{track.next.title} →</Link> :
        <span className="muted">暂无可选新题</span>}</li>)}</ul></section>
    <section className="plan-rate"><h2>首次提交通过率</h2><strong>{plan.first_rate == null ? '—' : percent(plan.first_rate)}</strong>
      <small>最近 {plan.first_count} 题</small><Link to="/stats">按周查看 →</Link></section>
  </main>
}

type Metric = Exclude<keyof Week, 'week'>
const metrics: { key: Metric; title: string; unit: string }[] = [
  { key: 'first_rate', title: '首次提交通过率', unit: '%' },
  { key: 'syntax_errors', title: '语法错误', unit: '次' },
  { key: 'elapsed_ms', title: '首次通过平均用时', unit: '分钟' },
  { key: 'hints', title: '使用提示', unit: '条' },
  { key: 'ai_rate', title: '通过中的 AI 协助', unit: '%' },
]

function display(n: number | null, unit: string) {
  if (n == null) return '—'
  if (unit === '%') return percent(n)
  return (unit === '分钟' ? Number((n / 60000).toFixed(1)) : n) + ' ' + unit
}

export function StatsPage() {
  const { weeks } = useLoaderData() as { weeks: Week[] }
  const tracks = useTracks()
  const [selected, setSelected] = useState(weeks.length - 1)
  return <main className="study-page stats-page">
    <header><h1>手感统计</h1><span>最近八周 · 普通提交</span></header>
    <div className="week-select"><label>查看周次 <select value={selected} onChange={e => setSelected(Number(e.target.value))}>
      {weeks.map((w, i) => <option key={w.week} value={i}>{w.week} 起</option>)}</select></label></div>
    {metrics.map(({ key, title, unit }) => {
      const values = weeks.map(w => w[key])
      const max = unit === '%' ? 1 : Math.max(1, ...values.map(n => n ?? 0))
      return <section className="trend" key={key}><div><h2>{title}</h2>
        <output>{display(values[selected], unit)}</output></div>
        <svg viewBox="0 0 480 76" role="img" aria-label={title + '，' + weeks.map((w, i) =>
          shortDate(w.week) + ' ' + display(values[i], unit)).join('，')}>
          {weeks.map((w, i) => {
            const x = 30 + i * 60
            const n = values[i]
            const height = n === null ? 0 : n / max * 47
            return <g key={w.week} className={selected === i ? 'selected-week' : ''}>
              <title>{w.week} · {display(n, unit)}</title>
              <line x1={x-17} x2={x+17} y1="51" y2="51" />
              {n !== null && <rect x={x-9} y={50-height} width="18" height={Math.max(1,height)} />}
              <text x={x} y="70" textAnchor="middle">{shortDate(w.week)}</text></g>
          })}</svg></section>
    })}
    <section className="stats-mastery"><h2>知识点掌握</h2>
      {tracks.filter(t => t.status === 'active').map(t => <details key={t.id}>
        <summary>{t.name}<span>{t.mastered} / {t.skills}</span></summary>
        <ul>{t.stages.flatMap(stage => stage.units.map(unit => <li key={stage.id + '/' + unit.id}>
          <small>{stage.name}</small><Link to={'/t/' + t.id + '/skills#' + unitAnchor(stage.id, unit.id)}>
            {unit.name} · {unit.mastered} / {unit.skills.length}</Link></li>))}</ul>
      </details>)}</section>
  </main>
}
