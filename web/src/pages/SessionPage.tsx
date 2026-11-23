import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api } from '../api'
import { beginSession, enableFocus, sessionItemPath, usePracticeSession } from '../practiceSession'
import { readPref, writePref } from '../theme'
import type { MapTab } from './mapTree'
import './plan.css'

export function SessionStart({ tab, again = false }: { tab: MapTab; again?: boolean }) {
  const session = usePracticeSession()
  const navigate = useNavigate()
  const [size, setSize] = useState(() => Number(readPref('dojo-session-size', '5')))
  const [minutes, setMinutes] = useState(() => Number(readPref('dojo-session-minutes', '0')))
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState('')

  async function start() {
    setBusy(true)
    setMessage('')
    try {
      const items = await api.sessionPlan(tab, size)
      if (!items.length) {
        setMessage('这条线暂时没有可排的题。')
        return
      }
      const group = beginSession(tab, items, minutes)
      enableFocus(true)
      await navigate(sessionItemPath(group.items[0]))
    } catch (e) {
      setMessage((e as Error).message)
    } finally { setBusy(false) }
  }

  if (session && !session.ended) return <Link className="session-resume" to={sessionItemPath(session.items[session.current])}>
    继续这组 {session.current + 1}/{session.items.length}</Link>
  return <div className="session-start">
    <button disabled={busy} onClick={start}>{busy ? '排题中…' : again ? '再来一组' : '开始一组'}</button>
    {!again && <details onBlur={e => {
      if (!e.currentTarget.contains(e.relatedTarget)) e.currentTarget.open = false
    }} onKeyDown={e => {
      if (e.key === 'Escape') {
        e.currentTarget.open = false
        e.currentTarget.querySelector('summary')?.focus()
      }
    }}>
      <summary aria-label="一组练习选项" title="一组练习选项">⌄</summary>
      <div className="session-options">
        <label htmlFor="session-size">题数</label><select id="session-size" value={size} onChange={e => {
          setSize(Number(e.target.value)); writePref('dojo-session-size', e.target.value)
        }}>{[3, 5, 8].map(n => <option key={n} value={n}>{n} 题</option>)}</select>
        <label htmlFor="session-minutes">时间盒</label><select id="session-minutes" value={minutes} onChange={e => {
          setMinutes(Number(e.target.value)); writePref('dojo-session-minutes', e.target.value)
        }}>{[0, 25, 45].map(n => <option key={n} value={n}>{n ? n + ' 分钟' : '不限时'}</option>)}</select>
      </div>
    </details>}
    {message && <span className="session-message" role="status">{message}</span>}
  </div>
}

export function SessionPage() {
  const s = usePracticeSession()
  if (!s || !s.ended) return <main className="study-page"><h1>一组练习</h1>
    <p>{s ? <Link to={sessionItemPath(s.items[s.current])}>继续这组</Link> : '暂无练习小结。'}</p><Link to="/">回地图</Link></main>
  const seconds = Math.floor((s.ended - s.started) / 1000)
  const metrics = [
    ['题数', s.items.length], ['首次通过', s.items.filter(p => p.firstPass).length],
    ['跳过', s.items.filter(p => p.status === 'skipped').length], ['用到提示或 AI', s.items.filter(p => p.hints || p.ai).length],
    ['总用时', seconds < 60 ? seconds + ' 秒' : Math.floor(seconds / 60) + ' 分钟'], ['最高连续首次通过', s.best],
  ]
  return <main className="study-page session-summary">
    <header><h1>本组小结</h1></header>
    <dl>{metrics.map(([label, value]) => <div key={label}><dt>{label}</dt><dd>{value}</dd></div>)}</dl>
    <ol>{s.items.map(p => <li key={p.id}>
      <Link to={sessionItemPath(p, true)}>{p.title}</Link>
      <span className={p.status === 'passed' ? 'tone-pass' : 'muted'}>
        {p.status === 'skipped' ? '已跳过' : p.firstPass ? '首次通过' : p.status === 'passed' ? '重试通过' : p.firstPass === false ? '未通过' : '未做'}
      </span>
    </li>)}</ol>
    <nav><SessionStart tab={s.tab} again /><Link to={'/?tab=' + s.tab}>回地图</Link></nav>
  </main>
}
