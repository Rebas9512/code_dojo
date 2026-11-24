// 只有桌面更新包会标记入口页面。多窗口各自领取任务，由服务端保证一次只交给一个窗口。
async function listen() {
  for (;;) {
    try {
      const res = await fetch('/api/desktop/sql/next', { method: 'POST', headers: { 'Content-Type': 'application/json' } })
      if (res.ok) {
        const task = await res.json()
        if (task) {
          const worker = new Worker(new URL('./validationWorker.ts', import.meta.url), { type: 'module' })
          try {
            const reply = await new Promise(resolve => {
              const timer = setTimeout(() => resolve({ error: '浏览器验证 SQL 超时' }), 30000 + (task.job.timeoutMs ?? 0))
              worker.onmessage = e => { clearTimeout(timer); resolve(e.data) }
              worker.onerror = () => { clearTimeout(timer); resolve({ error: 'SQL 校验器加载失败' }) }
              worker.postMessage(task.job)
            })
            await fetch('/api/desktop/sql/' + task.id, { method: 'POST',
              headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(reply) })
          } finally {
            worker.terminate()
          }
        }
      }
    } catch {
      // 服务关闭或暂时断开后，页面可在下次轮询时恢复。
    }
    await new Promise(resolve => setTimeout(resolve, 1800))
  }
}
void listen()
