import { useEffect, useState } from 'react'
import { useRevalidator } from 'react-router-dom'
import { api, type SyncState } from '../api'

export function SyncStatus() {
  const [state, setState] = useState<SyncState | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const { revalidate } = useRevalidator()

  useEffect(() => {
    if (busy) return
    let active = true
    async function refresh() {
      try {
        const next = await api.syncStatus()
        if (active) {
          setState(next)
          setError('')
        }
      } catch {
        if (active) setError('无法读取同步状态')
      }
    }
    void refresh()
    const timer = window.setInterval(refresh, 15000)
    window.addEventListener('focus', refresh)
    return () => {
      active = false
      window.clearInterval(timer)
      window.removeEventListener('focus', refresh)
    }
  }, [busy])

  async function sync() {
    setBusy(true)
    setError('')
    try {
      const next = await api.syncNow()
      setState(next)
      if (!next.error) await revalidate()
    } catch {
      setError('无法连接本机服务')
    } finally {
      setBusy(false)
    }
  }

  if (!state && !error) return null
  if (state && !state.enabled && !error) return <span className="sync-status">未开启同步</span>
  const date = state?.last_sync ? new Date(state.last_sync) : null
  const time = date?.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  const last = time ? `已同步 ${date?.toDateString() === new Date().toDateString() ? '' : date?.toLocaleDateString('zh-CN') + ' '}${time}` : '尚未同步'
  const pending = state?.pending ? ` · ${state.pending} 条待推送` : ''
  const failure = error || state?.error
  const detail = [date ? `上次同步 ${date.toLocaleString('zh-CN')}` : last,
    `待推送 ${state?.pending ?? 0} 条`, failure, '立即同步'].filter(Boolean).join(' · ')
  return <button className="ghost sync-status" onClick={sync} disabled={busy || state?.syncing}
    title={detail} aria-label={detail}>
    {busy || state?.syncing ? '正在同步' : failure ? <span className="tone-fail">{failure}</span> : last}{pending}
  </button>
}
