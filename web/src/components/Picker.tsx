import { useEffect, useMemo, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api, type TrackInfo, type TrackProblem } from '../api'
import './picker.css'

export interface PickerItem {
  id: string
  title: string
  detail?: string
  shortcut?: string
  disabled?: boolean
  run: () => void
}

// 优先完整前缀和连续子串，再匹配按顺序输入的字符。
function score(field: string, query: string) {
  const text = field.toLowerCase()
  const at = text.indexOf(query)
  if (at >= 0) return at === 0 ? 0 : 1 + at / (text.length + 1)
  let cursor = -1
  let first = -1
  for (const c of query) {
    cursor = text.indexOf(c, cursor + 1)
    if (cursor < 0) return Infinity
    if (first < 0) first = cursor
  }
  return 2 + cursor - first
}

export function Picker({ label, items, close, message }: {
  label: string; items: PickerItem[]; close: () => void; message?: string
}) {
  const dialog = useRef<HTMLDialogElement>(null)
  const list = useRef<HTMLDivElement>(null)
  const [query, setQuery] = useState('')
  const [selected, setSelected] = useState(0)
  useEffect(() => {
    const el = dialog.current!
    el.showModal()
    return () => el.close()
  }, [])
  const matches = useMemo(() => {
    const term = query.trim().toLowerCase()
    if (!term) return items.slice(0, 40)
    return items.map(item => ({ item, rank: Math.min(score(item.title, term), score(item.id, term),
      item.detail ? score(item.detail, term) : Infinity) }))
      .filter(row => Number.isFinite(row.rank)).sort((a, b) => a.rank - b.rank).map(row => row.item)
  }, [items, query])
  useEffect(() => {
    list.current?.children[selected]?.scrollIntoView({ block: 'nearest' })
  }, [selected])
  function choose(item?: PickerItem) {
    if (!item || item.disabled) return
    close()
    item.run()
  }
  return <dialog ref={dialog} className="picker" aria-label={label} onCancel={close}
    onClick={e => { if (e.target === dialog.current) close() }}>
    <div className="picker-box">
      <input autoFocus role="combobox" aria-label={label} aria-expanded="true" aria-controls="picker-list"
        aria-activedescendant={matches[selected] ? 'picker-' + selected : undefined}
        placeholder={label} value={query} onChange={e => { setQuery(e.target.value); setSelected(0) }}
        onKeyDown={e => {
          if (e.nativeEvent.isComposing) return
          if (e.key === 'Enter') { e.preventDefault(); e.stopPropagation(); choose(matches[selected]) }
          if (matches.length && (e.key === 'ArrowDown' || e.key === 'ArrowUp')) {
            e.preventDefault()
            setSelected(i => (i + (e.key === 'ArrowDown' ? 1 : -1) + matches.length) % matches.length)
          }
        }} />
      <div ref={list} role="listbox" aria-label={label} id="picker-list" className="picker-list">
        {matches.map((item, i) => <button role="option" aria-selected={i === selected}
          id={'picker-' + i} key={item.id} tabIndex={-1} disabled={item.disabled}
          onClick={() => choose(item)}>
          <span>{item.title}</span>{item.detail && <small>{item.detail}</small>}
          {item.shortcut && <kbd>{item.shortcut}</kbd>}
        </button>)}
      </div>
      {!matches.length && <p role="status">{message || '没有匹配项'}</p>}
    </div>
  </dialog>
}

// 全站共用题名索引。切题时复用进行中的请求，题量变化后重新读取。
let catalog: { signature: string; rows: Promise<TrackProblem[]> } | null = null
function problemCatalog(tracks: TrackInfo[]) {
  const active = tracks.filter(track => track.total)
  const signature = active.map(track => track.id + ':' + track.total).join(',')
  if (catalog?.signature === signature) return catalog.rows
  const rows = Promise.all(active.map(track => api.problems(track.id))).then(groups => groups.flat())
  catalog = { signature, rows }
  rows.catch(() => { if (catalog?.rows === rows) catalog = null })
  return rows
}

export function QuickOpen({ tracks, close }: { tracks: TrackInfo[]; close: () => void }) {
  const navigate = useNavigate()
  const [rows, setRows] = useState<TrackProblem[]>([])
  const [message, setMessage] = useState('正在读取题库…')
  useEffect(() => {
    let current = true
    problemCatalog(tracks)
      .then(list => { if (current) { setRows(list); setMessage('') } })
      .catch(e => { if (current) setMessage(e.message) })
    return () => { current = false }
  }, [tracks])
  const items = useMemo(() => rows.map(p => ({
    id: p.id, title: p.title, detail: [p.id, p.leetcode].filter(Boolean).join(' · '),
    run: () => navigate('/p/' + p.id),
  })), [rows, navigate])
  return <Picker label="按题名、题号或 LeetCode slug 搜索" items={items} close={close} message={message} />
}

export function usePickerShortcut(shift: boolean, open: () => void) {
  useEffect(() => {
    function key(e: KeyboardEvent) {
      if (e.isComposing || !(e.ctrlKey || e.metaKey) || e.altKey || e.shiftKey !== shift || e.code !== 'KeyP') return
      e.preventDefault()
      e.stopPropagation()
      if (!document.querySelector('dialog[open]')) open()
    }
    window.addEventListener('keydown', key, true)
    return () => window.removeEventListener('keydown', key, true)
  }, [shift, open])
}
