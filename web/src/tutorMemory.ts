import { useEffect, useState } from 'react'
import { api } from './api'

// 保存时切页或重开命令面板，新入口等同一次写入完成再显示状态。
let pendingSave: ReturnType<typeof api.setMemoryEnabled> | null = null

export function useTutorMemory(visible: boolean) {
  const [enabled, setEnabled] = useState<boolean | null>(null)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!visible) return
    let current = true
    setEnabled(null)
    setError('')
    const settings = pendingSave ?? api.memorySettings()
    settings.then(value => { if (current) setEnabled(value.enabled) })
      .catch((err: Error) => { if (current) setError(err.message) })
    return () => { current = false }
  }, [visible])

  async function toggle() {
    if (enabled === null || saving) return
    setSaving(true)
    setError('')
    try {
      pendingSave = api.setMemoryEnabled(!enabled)
      setEnabled((await pendingSave).enabled)
    } catch (err) {
      setError((err as Error).message)
    } finally {
      pendingSave = null
      setSaving(false)
    }
  }

  return { enabled, busy: enabled === null || saving, toggle, error }
}
