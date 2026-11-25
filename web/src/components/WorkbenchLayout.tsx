import { useEffect, useRef, useState, useSyncExternalStore, type CSSProperties } from 'react'
import { Link } from 'react-router-dom'
import { prefetchProblem, type ProblemDetail, type TrackProblem } from '../api'
import { FORMAT_NAME } from '../labels'
import { readPref, writePref } from '../theme'
import { enableFocus } from '../practiceSession'
import { ProblemStatus } from './ProblemStatus'
import '@vscode/codicons/dist/codicon.css'
import './workbench.css'

export function Icon({ name }: { name: string }) {
  return <span aria-hidden="true" className={'codicon codicon-' + name} />
}

const media = window.matchMedia('(width < 900px)')
const subscribe = (change: () => void) => {
  media.addEventListener('change', change)
  return () => media.removeEventListener('change', change)
}

function useFlag(key: string, fallback: boolean) {
  const [value, set] = useState(() => readPref(key, fallback ? '1' : '0') === '1')
  useEffect(() => writePref(key, value ? '1' : '0'), [key, value])
  return [value, set] as const
}

function useSize(key: string, fallback: number, min: number, max: number) {
  const clamp = (n: number) => Math.max(min, Math.min(max, n))
  const [value, set] = useState(() => clamp(Number(readPref(key, String(fallback)))))
  useEffect(() => writePref(key, String(value)), [key, value])
  // 窗口尺寸变化时只限制显示值，保留上次手动设置的偏好。
  return { value: clamp(value), min, max, set: (n: number) => set(clamp(n)) }
}

export function useWorkbenchLayout() {
  const narrow = useSyncExternalStore(subscribe, () => media.matches)
  const [files, setFiles] = useFlag('dojo-files', true)
  const [chat, setChat] = useFlag('dojo-chat', true)
  const [panel, setPanel] = useFlag('dojo-panel', false)
  const [focus, setFocus] = useState(() => readPref('dojo-focus', '0') === '1')
  const [focusChat, setFocusChat] = useState(false)
  const [drawer, setDrawer] = useState(() => readPref('dojo-drawer', ''))
  useEffect(() => writePref('dojo-drawer', drawer), [drawer])
  const sidebar = useSize('dojo-files-width', 224, 150, 480)
  const tutor = useSize('dojo-chat-width', 284, 190, 540)
  const chatRef = useRef<HTMLElement>(null)
  const chatQuickRef = useRef<HTMLDivElement>(null)
  const [chatInputMax, setChatInputMax] = useState(400)
  const [quickHeight, setQuickHeight] = useState(0)
  useEffect(() => {
    const chat = chatRef.current!
    const quick = chatQuickRef.current!
    const observer = new ResizeObserver(() => {
      if (!chat.clientHeight) return
      setChatInputMax(Math.min(400, Math.floor(chat.clientHeight / 2)))
      setQuickHeight(quick.offsetHeight)
    })
    observer.observe(chat)
    observer.observe(quick)
    return () => observer.disconnect()
  }, [])
  // 按钮换行后，仍给文本框留一行字和内外边距。
  const chatInputMin = Math.min(chatInputMax, quickHeight + 60)
  const chatInput = useSize('dojo-chat-input-height', 160, chatInputMin, chatInputMax)
  const bottom = useSize('dojo-panel-height', 236, 92, 650)
  const split = useSize('dojo-editor-split', 46, 22, 78)
  const vertical = useSize('dojo-mobile-split', 48, 20, 75)
  const filesOpen = !focus && (narrow ? drawer === 'files' : files)
  const chatOpen = focus ? focusChat : narrow ? drawer === 'chat' : chat
  return { narrow, filesOpen, chatOpen, panel, setPanel, sidebar, tutor, bottom, split: narrow ? vertical : split,
    chatInput, chatRef, chatQuickRef,
    focus, toggleFocus: () => {
      enableFocus(!focus)
      setFocus(!focus)
      setFocusChat(false)
    },
    toggleFiles: () => narrow ? setDrawer(filesOpen ? '' : 'files') : setFiles(!files),
    toggleChat: () => focus ? setFocusChat(!focusChat) : narrow ? setDrawer(chatOpen ? '' : 'chat') : setChat(!chat),
    closeDrawer: () => focus ? setFocusChat(false) : setDrawer(''),
    style: { '--files-w': filesOpen ? `min(${sidebar.value}px, 20vw)` : '0px',
      '--chat-w': chatOpen ? `min(${tutor.value}px, 25vw)` : '0px',
      '--chat-input-h': chatInput.value + 'px',
      '--split': (narrow ? vertical.value : split.value) + '%',
      '--panel-h': panel ? `min(${bottom.value}px, 44%)` : '0px',
    } as CSSProperties,
  }
}
export type WorkbenchLayout = ReturnType<typeof useWorkbenchLayout>

export function Separator({ label, side, size, percent = false }: {
  label: string; side: 'left' | 'right' | 'bottom' | 'top'; size: ReturnType<typeof useSize>; percent?: boolean
}) {
  const horizontal = side === 'top' || side === 'bottom'
  const drag = useRef<{ origin: number; initial: number; scale: number } | null>(null)
  const sign = side === 'bottom' || side === 'right' ? -1 : 1
  return <div role="separator" aria-label={label} aria-orientation={horizontal ? 'horizontal' : 'vertical'}
    aria-valuenow={Math.round(size.value)} aria-valuemin={size.min} aria-valuemax={size.max}
    tabIndex={0} className={'sash sash-' + side}
    onPointerDown={e => {
      if (e.button !== 0) return
      const rect = e.currentTarget.parentElement!.getBoundingClientRect()
      const length = horizontal ? rect.height : rect.width
      const group = e.currentTarget.parentElement!.parentElement!.getBoundingClientRect()
      const scale = percent ? 100 / (horizontal ? group.height : group.width) : 1
      drag.current = { origin: horizontal ? e.clientY : e.clientX, initial: length * scale, scale }
      e.currentTarget.setPointerCapture(e.pointerId)
      e.preventDefault()
    }}
    onPointerMove={e => {
      const d = drag.current
      if (d) size.set(d.initial + ((horizontal ? e.clientY : e.clientX) - d.origin) * sign * d.scale)
    }}
    onLostPointerCapture={() => { drag.current = null }}
    onKeyDown={e => {
      const arrows = horizontal ? ['ArrowUp', 'ArrowDown'] : ['ArrowLeft', 'ArrowRight']
      if (!arrows.includes(e.key)) return
      e.preventDefault()
      size.set(size.value + (e.key === arrows[0] ? -1 : 1) * sign * (percent ? 2 : 16))
    }} />
}

const icons = { predict: 'eye', inspect: 'table', write: 'code', fix: 'debug-alt', complete: 'edit',
  combine: 'layers', variant: 'symbol-method' }

export function Explorer({ rows, parent, unit, due, layout }: {
  rows: TrackProblem[]; parent: ProblemDetail; unit: string; due: Set<string>; layout: WorkbenchLayout
}) {
  const current = useRef<HTMLAnchorElement>(null)
  useEffect(() => { current.current?.scrollIntoView({ block: 'nearest' }) }, [parent.id, layout.filesOpen])
  return <aside className="wb-explorer" aria-label="本单元题目">
    <header className="side-head"><Icon name="folder-opened" /><strong title={unit}>{unit}</strong>
      <Link to={parent.language === 'sql' ? '/?tab=sql' : '/'} title="返回地图">返回地图</Link></header>
    <nav>{rows.map(p => <Link key={p.id} ref={p.id === parent.id ? current : undefined}
      to={'/p/' + p.id} aria-current={p.id === parent.id ? 'page' : undefined}
      title={p.title + ' · ' + FORMAT_NAME[p.format]} onPointerEnter={() => prefetchProblem(p.id)} onClick={() => { if (layout.narrow) layout.closeDrawer() }}>
      <Icon name={icons[p.format]} /><span className="file-title">{p.title}</span>
      {due.has(p.id) && <span className="review-dot" aria-label="复习到期" title="复习到期" />}
      <ProblemStatus status={p.status} />
    </Link>)}</nav>
    {!layout.narrow && <Separator label="调整题目列表宽度" side="left" size={layout.sidebar} />}
  </aside>
}
