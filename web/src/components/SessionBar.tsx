import { useEffect, useState } from 'react'
import { Link, useNavigate, useNavigation } from 'react-router-dom'
import { advanceSession, deadline, endSession, sessionItemPath, type PracticeSession } from '../practiceSession'

function TimeBox({ session }: { session: PracticeSession }) {
  const end = deadline(session)
  const [now, setNow] = useState(Date.now)
  useEffect(() => {
    if (now >= end) return
    // 只更新这条细线，最后一次准时显示到点提示。
    const timer = setTimeout(() => setNow(Date.now()), Math.min(60_000, end - Date.now()))
    return () => clearTimeout(timer)
  }, [now, end])
  if (now >= end) return <span role="status">时间到，做完这题就收</span>
  return <progress aria-label="本组时间盒" max={end - session.started} value={now - session.started} />
}

function advance(id: string, index: number, skip: boolean) {
  const next = advanceSession(id, index, skip)
  return next && (next.ended ? '/session' : sessionItemPath(next.items[next.current]))
}

export function SessionBar({ session, index, busy, autoAt, setAutoAt, review }: {
  session: PracticeSession; index: number; busy: boolean; autoAt: number | null
  setAutoAt: (time: number | null) => void; review: boolean
}) {
  const { items, id, current } = session
  const item = items[index]
  const navigate = useNavigate()
  const leaving = !!useNavigation().location

  useEffect(() => {
    if (!autoAt) return
    if (leaving) { setAutoAt(null); return }
    const timer = setTimeout(() => {
      const path = advance(id, index, false)
      if (path) void navigate(path)
    }, autoAt - Date.now())
    const cancel = (e: KeyboardEvent) => {
      if (e.key !== 'Escape') return
      clearTimeout(timer)
      setAutoAt(null)
      e.preventDefault()
      e.stopPropagation()
    }
    // 某些浏览器先用 Esc 退出原生全屏，不把这次按键传给页面。
    const onFullscreen = () => {
      if (!document.fullscreenElement) { clearTimeout(timer); setAutoAt(null) }
    }
    window.addEventListener('keydown', cancel, true)
    document.addEventListener('fullscreenchange', onFullscreen)
    return () => {
      clearTimeout(timer)
      window.removeEventListener('keydown', cancel, true)
      document.removeEventListener('fullscreenchange', onFullscreen)
    }
  }, [autoAt, setAutoAt, leaving, navigate, id, index])

  const go = (skip: boolean) => {
    const path = advance(id, index, skip)
    if (path) void navigate(path)
  }
  return <div className="session-bar" aria-label="本组练习">
    <span className="session-position"><span aria-hidden="true">{items.map((p, i) => p.status !== 'open' || i === index ? '●' : '○').join('')}</span> {index + 1}/{items.length}</span>
    <span>连续首次通过 {session.streak}</span>
    {session.minutes > 0 && <TimeBox session={session} />}
    <span className="bar-spacer" />
    {autoAt ? <span className="session-accepted" role="status">通过 ✓ · 1.5 秒后进入{items.some(p => p.status === 'open') && Date.now() < deadline(session) ? '下一题' : '小结'}（Esc 留下）</span> :
      index !== current && item.status !== 'open' ? <Link to={sessionItemPath(items[current])}>继续这组 →</Link> :
      item.status === 'passed' ? <button onClick={() => go(false)}>下一题 →</button> :
      <>{review && item.reviewClosed && <Link to={sessionItemPath(item)}>再练这题</Link>}
        <button disabled={busy} onClick={() => go(true)}>跳过</button></>}
    <button disabled={busy} onClick={() => { endSession(id); void navigate('/session') }}>结束这组</button>
  </div>
}
