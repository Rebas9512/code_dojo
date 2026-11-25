const ui = window.dojoStartup
const el = id => document.getElementById(id)
let cooldown

function agentRow(name, title) {
  const form = el('agent-row').content.firstElementChild.cloneNode(true)
  const label = form.querySelector('label')
  const input = form.querySelector('input')
  const status = form.querySelector('.agent-state')
  const feedback = form.querySelector('.agent-note')
  const browse = form.querySelector('.browse')
  const reset = form.querySelector('.auto')
  label.textContent = title
  label.htmlFor = input.id = name + '-path'
  label.id = name + '-label'
  form.setAttribute('aria-labelledby', label.id)
  feedback.id = name + '-note'
  input.setAttribute('aria-describedby', 'path-help ' + feedback.id)
  browse.onclick = async () => {
    const path = await ui.browseAgent()
    if (path) {
      input.value = path
      input.focus()
    }
  }
  form.onsubmit = event => { event.preventDefault(); void ui.setAgentPath(name, input.value) }
  reset.onclick = () => ui.setAgentPath(name, null)
  el('agents').append(form)
  let lastManual
  return state => {
    const { source, path, manual } = state.agents[name]
    const found = !path ? '未找到' : source === 'manual' ? '手动指定' : '已找到'
    status.textContent = found + (source === 'env' ? '（环境变量）' : '') + (path ? ' · ' + path : '')
    if (manual !== lastManual) input.value = manual || ''
    lastManual = manual
    reset.hidden = !manual
    for (const control of form.elements) control.disabled = !!state.busy
    feedback.textContent = state.agent === name ? state.message : ''
    feedback.hidden = !feedback.textContent
    input.setAttribute('aria-invalid', String(!state.busy && !!feedback.textContent))
  }
}

if (navigator.platform.startsWith('Win')) {
  el('path-help').textContent = '在终端运行 where.exe claude 或 where.exe codex 可查看路径。'
}
const agentRows = [agentRow('claude', 'Claude Code'), agentRow('codex', 'Codex')]

function note(message) {
  el('note').hidden = !message
  el('note').textContent = message || ''
}

function show(state) {
  clearInterval(cooldown)
  const settings = state.type === 'settings'
  const showCode = el('connect').hidden && settings && !state.sync
  const error = state.type === 'error'
  el('heading').textContent = settings ? '设置' : error ? '无法打开练习' : state.message
  el('retry').hidden = !error
  if (error) el('retry').focus()
  el('installer').hidden = !state.installer
  if (state.installer) el('installer').href = state.installer
  const percent = /下载题库 (\d+)%/.exec(state.message || '')
  el('progress').hidden = !percent
  if (percent) el('progress').value = Number(percent[1])
  note((settings || error) && !state.agent ? state.message : '')
  el('connect').hidden = !settings || state.sync
  el('connected').hidden = !settings || !state.sync
  el('agents').hidden = !settings
  el('done').hidden = !settings
  if (!settings) return

  el('ai').textContent = state.ai ? 'AI 助教已启用' : Object.values(state.agents).some(agent => agent.path)
    ? 'AI 助教已关闭（环境变量）' : 'AI 助教已关闭，可在下方指定命令位置'
  for (const update of agentRows) update(state)
  el('disable').disabled = !!state.busy
  el('disable').hidden = false
  el('confirm').hidden = true
  el('enable').disabled = !!state.busy
  if (!state.busy && !state.agent && (showCode || state.retryAt !== undefined)) el('code').focus()
  if (state.retryAt !== undefined) {
    function update() {
      const seconds = Math.max(0, Math.ceil((state.retryAt - Date.now()) / 1000))
      el('enable').disabled = !!state.busy || seconds > 0
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
el('done').onclick = () => ui.close()
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && !el('done').hidden) {
    event.preventDefault()
    void ui.close()
  }
})
let received = false
ui.subscribe(state => { received = true; show(state) })
ui.read().then(state => { if (!received && state) show(state) })
