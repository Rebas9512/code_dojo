const ui = window.dojoStartup
const el = id => document.getElementById(id)
let cooldown

function show(state) {
  clearInterval(cooldown)
  for (const id of ['note', 'progress', 'tokens', 'unlock', 'recovery', 'installer', 'ai']) el(id).hidden = true
  const prompt = state.type === 'need_unlock' || state.type === 'unlock_failed'
  const manual = state.type === 'need_tokens' || state.type === 'settings'
  el('heading').textContent = prompt ? '解锁安装包' : manual ? (state.type === 'settings' ? '设置' : '设置 GitHub 令牌') :
    state.type === 'error' ? '无法打开练习' : state.message
  if (state.message && state.type !== 'status') {
    el('note').hidden = false
    el('note').textContent = state.message
  }
  const percent = /下载题库 (\d+)%/.exec(state.message || '')
  if (percent) {
    el('progress').hidden = false
    el('progress').value = Number(percent[1])
  }
  if (prompt) {
    el('unlock').hidden = false
    el('unlockButton').disabled = false
    el('password').focus()
    if (state.type === 'unlock_failed') {
      const until = Date.now() + state.wait * 1000
      function update() {
        const seconds = Math.max(0, Math.ceil((until - Date.now()) / 1000))
        el('note').hidden = false
        el('note').textContent = seconds ? '密码不对，请在 ' + seconds + ' 秒后重试' :
          state.remaining ? '密码不对，还可尝试 ' + state.remaining + ' 次' : '可以重新输入密码'
        el('unlockButton').disabled = seconds > 0
        if (!seconds) clearInterval(cooldown)
      }
      cooldown = setInterval(update, 250)
      update()
    }
  } else if (manual) {
    el('tokens').hidden = false
    el('save').disabled = false
    el('code').focus()
    if (state.type === 'settings') {
      el('ai').hidden = false
      el('ai').textContent = state.ai ? 'AI 助教已启用' : 'AI 助教已关闭。需要时请安装并登录 Claude Code，再重新打开应用。'
    }
  } else if (state.type === 'error') {
    el('recovery').hidden = false
    el('retry').focus()
  }
  if (state.installer) {
    el('installer').hidden = false
    el('installer').href = state.installer
  }
}

for (const button of document.querySelectorAll('.manual')) {
  button.onclick = () => { el('password').value = ''; show({ type: 'need_tokens' }) }
}
el('unlock').onsubmit = e => {
  e.preventDefault()
  el('unlockButton').disabled = true
  void ui.unlock(el('password').value)
  el('password').value = ''
}
el('tokens').onsubmit = e => {
  e.preventDefault()
  el('save').disabled = true
  el('note').hidden = false
  el('note').textContent = '正在保存令牌…'
  void ui.tokens(el('code').value, el('sync').value)
  el('tokens').reset()
}
el('retry').onclick = () => ui.retry()
let received = false
ui.subscribe(state => { received = true; show(state) })
ui.read().then(state => { if (!received && state) show(state) })
