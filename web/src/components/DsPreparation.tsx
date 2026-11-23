import { useEffect, useState } from 'react'
import { api } from '../api'

/** 只在数据科学题有操作进行时等待首次安装。 */
export function DsPreparation() {
  const [preparing, setPreparing] = useState(false)
  useEffect(() => {
    let active = true
    let timer: ReturnType<typeof setTimeout>
    const check = async () => {
      const { ds_state } = await api.judgeStatus()
      if (!active) return
      setPreparing(ds_state === 'preparing')
      if (ds_state === 'unprepared' || ds_state === 'preparing') timer = setTimeout(check, 1000)
    }
    void check()
    return () => { active = false; clearTimeout(timer) }
  }, [])
  return preparing ? <span className="faint" role="status">正在准备数据科学环境（约 1–5 分钟，只需一次）</span> : null
}
