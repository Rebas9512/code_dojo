import { useEffect, useState } from 'react'
import { useRevalidator } from 'react-router-dom'
import { api, invalidate, type SyncState } from '../api'

// 做题页切题时状态栏会重新挂载，先显示上次读到的状态，不闪空。
let known: SyncState | null = null
let deferredError = ''
// 服务启动时的第一次同步在后台进行，地图不等它。页面打开后才完成的那次可能合并了别的机器的记录，完成时刷新一次数据。
let startup = true

export function SyncStatus({ silent = false }: { silent?: boolean }) {
  const [state, setState] = useState<SyncState | null>(known)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')
  const { revalidate } = useRevalidator()

  useEffect(() => {
    const failure = error || state?.error
    if (silent && failure) deferredError = failure
    if (!silent && deferredError) {
      setNotice(deferredError)
      deferredError = ''
    }
  }, [silent, state, error])

  useEffect(() => {
    if (busy) return
    let active = true
    let soon = 0
    async function refresh() {
      try {
        const next = known = await api.syncStatus()
        if (!active) return
        setState(next)
        setError('')
        setNotice('')
        if (startup && next.syncing) {
          window.clearTimeout(soon)
          soon = window.setTimeout(refresh, 1000)
        } else if (startup) {
          startup = false
          if (next.last_sync && Date.parse(next.last_sync) >= performance.timeOrigin) {
            invalidate()
            void revalidate()
          }
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
      window.clearTimeout(soon)
      window.removeEventListener('focus', refresh)
    }
  }, [busy])

  async function sync() {
    setBusy(true)
    setError('')
    setNotice('')
    try {
      const next = known = await api.syncNow()
      setState(next)
      if (!next.error) await revalidate()
    } catch {
      setError('无法连接本机服务')
    } finally {
      setBusy(false)
    }
  }

  const failure = error || state?.error || notice
  if (silent || (!state && !failure)) return null
  if (state && !state.enabled && !failure) return <span className="sync-status">未开启同步</span>
  const date = state?.last_sync ? new Date(state.last_sync) : null
  const time = date?.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  const last = time ? `已同步 ${date?.toDateString() === new Date().toDateString() ? '' : date?.toLocaleDateString('zh-CN') + ' '}${time}` : '尚未同步'
  const pending = state?.pending ? ` · ${state.pending} 条待推送` : ''
  const detail = [date ? `上次同步 ${date.toLocaleString('zh-CN')}` : last,
    `待推送 ${state?.pending ?? 0} 条`, failure, '立即同步'].filter(Boolean).join(' · ')
  return <button className="ghost sync-status" onClick={sync} disabled={busy || state?.syncing}
    title={detail} aria-label={detail}>
    {busy || state?.syncing ? '正在同步' : failure ? <span className="tone-fail">{failure}</span> : last}{pending}
  </button>
}
