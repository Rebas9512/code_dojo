const ui = window.dojoStartup
const el = id => document.getElementById(id)
let cooldown

function note(message) {
  el('note').hidden = !message
  el('note').textContent = message || ''
}

function show(state) {
  clearInterval(cooldown)
  const settings = state.type === 'settings'
  const error = state.type === 'error'
  el('heading').textContent = settings ? '设置' : error ? '无法打开练习' : state.message
  el('retry').hidden = !error
  if (error) el('retry').focus()
  el('installer').hidden = !state.installer
  if (state.installer) el('installer').href = state.installer
  const percent = /下载题库 (\d+)%/.exec(state.message || '')
  el('progress').hidden = !percent
  if (percent) el('progress').value = Number(percent[1])
  note(settings || error ? state.message : '')
  el('connect').hidden = !settings || state.sync
  el('connected').hidden = !settings || !state.sync
  el('ai').hidden = !settings
  if (!settings) return

  el('ai').textContent = state.ai ? 'AI 助教已启用' : 'AI 助教已关闭。需要时请安装并登录 Claude Code 或 Codex，再重新打开应用。'
  el('disable').disabled = !!state.busy
  el('disable').hidden = false
  el('confirm').hidden = true
  el('enable').disabled = !!state.busy
  if (!state.sync && !state.busy) el('code').focus()
  if (state.retryAt !== undefined) {
    function update() {
      const seconds = Math.max(0, Math.ceil((state.retryAt - Date.now()) / 1000))
      el('enable').disabled = seconds > 0
      note(seconds ? '同步码不对，请在 ' + seconds + ' 秒后重试' :
        state.remaining ? '同步码不对，还可尝试 ' + state.remaining + ' 次' : '可以重新输入同步码')
      if (!seconds) clearInterval(cooldown)
    }
    cooldown = setInterval(update, 250)
    update()
  }
}

el('connect').onsubmit = event => {
  event.preventDefault()
  if (el('enable').disabled) return
  el('enable').disabled = true
  void ui.connectSync(el('code').value)
  el('connect').reset()
}
el('disable').onclick = () => {
  el('disable').hidden = true
  el('confirm').hidden = false
  el('cancel').focus()
}
el('cancel').onclick = () => {
  el('confirm').hidden = true
  el('disable').hidden = false
  el('disable').focus()
}
el('confirmDisable').onclick = () => {
  el('confirm').hidden = true
  el('disable').hidden = false
  el('disable').disabled = true
  void ui.disconnectSync()
}
el('retry').onclick = () => ui.retry()
let received = false
ui.subscribe(state => { received = true; show(state) })
ui.read().then(state => { if (!received && state) show(state) })
