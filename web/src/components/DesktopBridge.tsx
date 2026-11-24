import { useEffect, useRef, useState } from 'react'
import { api } from '../api'

declare global {
  interface Window {
    dojoDesktop?: {
      sync(): Promise<void>
      settings(): Promise<void>
      about(): Promise<void>
      quit(): Promise<void>
      version(): Promise<{ launcher: string; payload: string }>
    }
  }
}

export function DesktopBridge() {
  const desktop = window.dojoDesktop
  const menu = useRef<HTMLDetailsElement>(null)
  const [syncEnabled, setSyncEnabled] = useState(false)
  useEffect(() => {
    if (!desktop) return
    function close(event: PointerEvent) {
      if (menu.current && !menu.current.contains(event.target as Node)) menu.current.open = false
    }
    document.addEventListener('pointerdown', close)
    return () => document.removeEventListener('pointerdown', close)
  }, [desktop])
  if (!desktop) return null
  const actions: [string, () => Promise<void>][] = [['设置', desktop.settings], ['关于', desktop.about]]
  if (syncEnabled) actions.unshift(['立即同步', desktop.sync])
  return <details ref={menu} style={{ position: 'relative' }} onToggle={e => {
    if (e.currentTarget.open) void api.syncStatus().then(state => setSyncEnabled(state.enabled), () => setSyncEnabled(false))
  }} onKeyDown={e => {
    if (e.key === 'Escape' && menu.current) {
      menu.current.open = false
      menu.current.querySelector('summary')?.focus()
    }
  }}>
    <summary className="ghost" style={{ cursor: 'pointer' }}>桌面</summary>
    <div style={{ position: 'absolute', right: 0, top: '100%', zIndex: 20, display: 'grid',
      minWidth: '7em', padding: 4, background: 'var(--panel)', border: '1px solid var(--line)' }}>
      {actions.map(([label, act]) =>
        <button key={label} className="ghost" onClick={() => {
          if (menu.current) menu.current.open = false
          void act()
        }}>{label}</button>)}
    </div>
  </details>
}
