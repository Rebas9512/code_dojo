import { useEffect, useMemo, useSyncExternalStore } from 'react'
import { practicePath, type PracticeLink } from './api'
import type { MapTab } from './pages/mapTree'
import { readPref, writePref } from './theme'

const key = 'dojo-practice-session'
const lifetime = 12 * 60 * 60 * 1000

export interface SessionItem extends PracticeLink {
  firstPass: boolean | null
  status: 'open' | 'passed' | 'skipped'
  hints: number
  ai: number
  reviewClosed: boolean
}

export interface PracticeSession {
  id: string
  tab: MapTab
  items: SessionItem[]
  current: number
  started: number
  ended: number | null
  minutes: number
  streak: number
  best: number
}

function save(session: PracticeSession | null) {
  writePref(key, session && JSON.stringify(session))
  window.dispatchEvent(new Event(key))
}

function snapshot() {
  return localStorage.getItem(key)
}

function read(raw: string | null): PracticeSession | null {
  const session: PracticeSession | null = raw === null ? null : JSON.parse(raw)
  return session && !session.ended && Date.now() >= session.started + lifetime ? null : session
}

function subscribe(notify: () => void) {
  const changed = (e: StorageEvent) => { if (e.key === key || e.key === null) notify() }
  window.addEventListener(key, notify)
  window.addEventListener('storage', changed)
  return () => {
    window.removeEventListener(key, notify)
    window.removeEventListener('storage', changed)
  }
}

export function usePracticeSession() {
  const raw = useSyncExternalStore(subscribe, snapshot)
  const session = useMemo(() => read(raw), [raw])
  useEffect(() => {
    if (!session || session.ended) return
    const timer = window.setTimeout(() => {
      if (!read(snapshot())) save(null)
    }, session.started + lifetime - Date.now())
    return () => clearTimeout(timer)
  }, [session])
  return session
}

export function beginSession(tab: MapTab, links: PracticeLink[], minutes: number) {
  const session: PracticeSession = {
    id: crypto.randomUUID(), tab, started: Date.now(), ended: null, minutes, current: 0, streak: 0, best: 0,
    items: links.map(link => ({ ...link, firstPass: null, status: 'open', hints: 0, ai: 0, reviewClosed: false })),
  }
  save(session)
  return session
}

// 判题或助教可能在切题后返回。只更新发起操作的那一组，并保留期间的其他操作。
function update(id: string, change: (s: PracticeSession) => void | false) {
  const session = read(snapshot())
  if (!session || session.ended || session.id !== id) return null
  if (change(session) === false) return null
  save(session)
  return session
}

export function recordSubmission(id: string, index: number, passed: boolean) {
  return update(id, s => {
    const item = s.items[index]
    if (item.status !== 'open') return false
    if (item.firstPass === null) {
      item.firstPass = passed
      s.streak = passed ? s.streak + 1 : 0
      s.best = Math.max(s.best, s.streak)
    }
    if (passed) item.status = 'passed'
    if (item.source) item.reviewClosed = true
  })
}

export function recordHelp(id: string, index: number, kind: 'ai' | 'hints', closedReview = false) {
  update(id, s => {
    const item = s.items[index]
    if (item.status !== 'open') return false
    item[kind]++
    if (closedReview && item.source) item.reviewClosed = true
  })
}

export function visitItem(id: string, index: number) {
  update(id, s => {
    if (s.current === index) return false
    s.current = index
  })
}

export function endSession(id: string) {
  return update(id, s => { s.ended = Date.now() })
}

export function deadline(s: PracticeSession) {
  return s.minutes ? s.started + s.minutes * 60_000 : Infinity
}

export function advanceSession(id: string, index: number, skip: boolean) {
  return update(id, s => {
    const item = s.items[index]
    if (skip && item.status === 'open') {
      item.status = 'skipped'
      s.streak = 0
    }
    let next = s.items.findIndex((p, i) => i > index && p.status === 'open')
    if (next < 0) next = s.items.findIndex(p => p.status === 'open')
    if (next < 0 || Date.now() >= deadline(s)) s.ended = Date.now()
    else s.current = next
  })
}

// 一轮复习只交一次；再练和小结回看走普通题面，保留附加题地址。
export function sessionItemPath(item: SessionItem, revisit = false) {
  return practicePath(item.reviewClosed || revisit ? { ...item, source: undefined } : item)
}

export function enableFocus(enabled: boolean) {
  writePref('dojo-focus', enabled ? '1' : '0')
  // 用户可以拒绝全屏或按 Esc 离开全屏，工作台仍保留专注布局。
  if (enabled && !document.fullscreenElement && document.fullscreenEnabled) {
    void document.documentElement.requestFullscreen().catch(() => {})
  } else if (!enabled && document.fullscreenElement) {
    void document.exitFullscreen()
  }
}

// 通过提示音：G5 → D6 两声轻敲（上行五度）。每声是基音加两个泛音，泛音比基音衰减得快，听起来像敲玻璃。
const NOTES = [[783.99, 0], [1174.66, .09]]
const PARTIALS = [[1, 1, 1.1], [2, .22, .4], [3, .06, .2]] // 倍频、相对音量、衰减秒数

let audio: AudioContext | undefined
export function playPassSound(preview = false) {
  if (!preview && readPref('dojo-sound', '0') !== '1') return
  const ctx = audio ??= new AudioContext()
  if (ctx.state === 'suspended') void ctx.resume()
  const out = ctx.createGain()
  out.gain.value = .04
  out.connect(ctx.destination)
  for (const [frequency, delay] of NOTES) {
    const start = ctx.currentTime + .01 + delay
    for (const [ratio, level, decay] of PARTIALS) {
      const tone = ctx.createOscillator()
      const volume = ctx.createGain()
      tone.frequency.value = frequency * ratio
      volume.gain.setValueAtTime(0, start)
      volume.gain.linearRampToValueAtTime(level, start + .005)
      volume.gain.exponentialRampToValueAtTime(.0001, start + decay)
      tone.connect(volume).connect(out)
      tone.start(start)
      tone.stop(start + decay)
    }
  }
}
