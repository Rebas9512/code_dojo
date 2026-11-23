const { app, BrowserWindow, dialog, ipcMain, Menu, screen, shell } = require('electron')
const { spawn } = require('node:child_process')
const fs = require('node:fs')
const os = require('node:os')
const path = require('node:path')
const readline = require('node:readline')
const { pathToFileURL } = require('node:url')

const base = process.platform === 'linux' ? process.env.XDG_DATA_HOME || path.join(os.homedir(), '.local/share') : app.getPath('appData')
const data = path.resolve(process.env.CODE_DOJO_DATA || path.join(base, 'code-dojo'))
const profile = path.join(data, 'desktop', 'chromium')
fs.mkdirSync(profile, { recursive: true })
app.setPath('userData', profile)
if (process.platform === 'linux') app.commandLine.appendSwitch('class', 'Code-dojo')
const boundsFile = path.join(data, 'desktop', 'window.json')
const startup = pathToFileURL(path.join(__dirname, 'startup.html')).href
const preferences = { preload: path.join(__dirname, 'preload.cjs'), sandbox: true, contextIsolation: true, nodeIntegration: false }
let win, settingsWindow, child, origin, ready, quitting = false
let state = { type: 'status', message: '正在打开…' }

function publish(next) {
  state = next
  if (win && !win.isDestroyed() && win.webContents.getURL() === startup) win.webContents.send('startup:state', next)
}

function localPage(next) {
  publish(next)
  if (win.webContents.getURL() !== startup) void win.loadURL(startup).catch(() => {})
}

function send(command, fields = {}) {
  if (child?.stdin.writable) child.stdin.write(JSON.stringify({ command, ...fields }) + '\n')
}

function showInfo(message, detail, installer) {
  const buttons = installer ? ['下载新版安装包', '关闭'] : ['关闭']
  void dialog.showMessageBox(win, { type: 'info', title: 'code-dojo', message, detail: detail || '', buttons,
    cancelId: buttons.length - 1 }).then(({ response }) => {
    if (installer && response === 0) openExternal(installer)
  })
}

function onEvent(event) {
  if (quitting) return
  switch (event.type) {
    case 'ready': {
      if (!Number.isInteger(event.port) || event.port < 1 || event.port > 65535) break
      ready = event
      origin = 'http://127.0.0.1:' + event.port
      settingsWindow?.close()
      void win.loadURL(origin + '/').then(() => {
        if (event.message && !quitting) showInfo(event.message, '', event.installer)
      }).catch(() => {
        if (!quitting) localPage({ type: 'error', message: '学习地图加载失败，请重试' })
      })
      break
    }
    case 'sync':
      break // 网页顶栏从同一后端读取最新同步状态。
    case 'status':
      if (event.checked && ready) {
        if (win.webContents.getURL() === startup) void win.loadURL(origin)
        showInfo(event.message, '', event.installer)
      } else {
        publish(event)
      }
      break
    case 'error':
    case 'need_tokens':
    case 'need_unlock':
    case 'unlock_failed':
      ready = null
      origin = null
      settingsWindow?.close()
      localPage(event)
      break
  }
}

function start() {
  if (child || quitting) return
  const runtime = path.join(process.resourcesPath, 'runtime')
  const executable = path.join(runtime, process.platform === 'win32' ? 'python/python.exe' : 'python/bin/python3')
  const env = { ...process.env, CODE_DOJO_DATA: data }
  // -E 忽略用户 Python 环境；凭据通过控制管道交给后端。
  delete env.CODE_DOJO_GITHUB_TOKEN
  delete env.CODE_DOJO_SYNC_TOKEN
  delete env.CODE_DOJO_SEALED_TOKENS
  const proc = spawn(executable, ['-E', '-s', '-B', '-X', 'utf8', '-m', 'bootstrap', 'serve', '--protocol', 'jsonl'],
    { cwd: runtime, env, windowsHide: true, detached: process.platform !== 'win32', stdio: ['pipe', 'pipe', 'ignore'] })
  child = proc
  proc.stdin.on('error', () => {}) // 子进程退出与最后一条指令可能同时发生。
  readline.createInterface({ input: proc.stdout }).on('line', line => {
    if (child !== proc) return
    try { onEvent(JSON.parse(line)) }
    catch { onEvent({ type: 'error', message: '无法读取启动器状态，请重启' }) }
  })
  proc.on('error', () => onEvent({ type: 'error', message: '无法启动内置 Python，请检查安装包' }))
  proc.once('close', () => {
    if (child !== proc) return
    child = null
    if (!quitting && state.type !== 'error') onEvent({ type: 'error', message: '本机服务意外退出，请重启' })
  })
}

function openExternal(raw) {
  let url
  try { url = new URL(raw) } catch { return }
  if (!['https:', 'http:'].includes(url.protocol) || url.username || url.password ||
      ['127.0.0.1', '[::1]', 'localhost'].includes(url.hostname)) return
  void shell.openExternal(url.href).catch(() => showInfo('系统浏览器未能打开链接'))
}

function appPage(raw) {
  if (!origin || !URL.canParse(raw)) return false
  const url = new URL(raw)
  return url.protocol === 'http:' && url.origin === origin && !url.username && !url.password
}

function protect(window) {
  const contents = window.webContents
  const allowed = raw => window === win && appPage(raw)
  contents.setWindowOpenHandler(({ url }) => {
    if (allowed(url)) void win.loadURL(url)
    else openExternal(url)
    return { action: 'deny' }
  })
  contents.on('will-frame-navigate', event => {
    if (!allowed(event.url)) {
      event.preventDefault()
      if (event.isMainFrame) openExternal(event.url)
    }
  })
  contents.on('will-redirect', event => {
    if (!allowed(event.url)) event.preventDefault()
  })
  contents.on('will-attach-webview', event => event.preventDefault())
  window.on('page-title-updated', event => event.preventDefault())
}

function settings() {
  if (quitting) return
  if (!ready) {
    if (child) localPage({ type: 'need_tokens' })
    return
  }
  if (settingsWindow) return settingsWindow.focus()
  settingsWindow = new BrowserWindow({ parent: win, modal: true, width: 540, height: 500,
    title: '设置', autoHideMenuBar: true, webPreferences: preferences })
  settingsWindow.removeMenu()
  protect(settingsWindow)
  settingsWindow.once('closed', () => { settingsWindow = null })
  void settingsWindow.loadURL(startup)
}

function about() {
  showInfo('code-dojo ' + app.getVersion(), '题库版本　' + (ready?.payload_version || '尚未载入'))
}

function menu() {
  const controls = [
    { label: '立即同步', accelerator: 'CmdOrCtrl+Shift+S', click: () => send('sync') },
    { label: '检查更新', click: () => { if (ready) send('check_update') } },
    { label: '设置…', accelerator: 'CmdOrCtrl+,', click: settings },
    { label: '关于 code-dojo', click: about },
    { type: 'separator' }, { label: '退出', accelerator: 'CmdOrCtrl+Q', click: () => app.quit() },
  ]
  Menu.setApplicationMenu(Menu.buildFromTemplate([
    { label: process.platform === 'darwin' ? app.name : '应用', submenu: controls },
    { label: '编辑', submenu: ['undo', 'redo', 'cut', 'copy', 'paste', 'selectAll'].map((role, i) =>
      ({ role, label: ['撤销', '重做', '剪切', '复制', '粘贴', '全选'][i] })) },
  ]))
}

function listen(name, permission, action) {
  ipcMain.handle(name, (event, ...args) => {
    const frame = event.senderFrame
    if (!frame || frame !== event.sender.mainFrame) return
    const isMain = event.sender === win?.webContents
    const isSettings = event.sender === settingsWindow?.webContents
    const local = (isMain || isSettings) && frame.url === startup
    const page = isMain && appPage(frame.url)
    if (permission === 'local' ? local : local || page) return action(isSettings, ...args)
  })
}

function ipc() {
  listen('dojo:sync', 'page', () => send('sync'))
  listen('dojo:settings', 'page', settings)
  listen('dojo:about', 'page', about)
  listen('dojo:quit', 'page', () => app.quit())
  listen('dojo:version', 'page', () => ({ launcher: app.getVersion(), payload: ready?.payload_version || '' }))
  listen('startup:read', 'local', isSettings => isSettings ? { type: 'settings', ai: ready?.ai } : state)
  listen('startup:unlock', 'local', (_, password) => {
    if (typeof password === 'string' && !ready) send('unlock', { password })
  })
  listen('startup:tokens', 'local', (_, code, sync) => {
    if (typeof code !== 'string' || typeof sync !== 'string' || !code.trim()) return
    if (!child) start()
    send('set_tokens', { code, sync })
  })
  listen('startup:retry', 'local', () => {
    publish({ type: 'status', message: '正在重新启动…' })
    if (child) send('check_update')
    else start()
  })
}

function bounds() {
  try {
    const b = JSON.parse(fs.readFileSync(boundsFile, 'utf8'))
    if (['x', 'y', 'width', 'height'].every(k => Number.isInteger(b[k])) && b.width >= 1024 && b.height >= 700 &&
        screen.getAllDisplays().some(({ workArea: a }) => b.x < a.x + a.width && b.y < a.y + a.height &&
          b.x + b.width > a.x && b.y + 50 > a.y)) return b
  } catch { /* 首次使用或显示器变更时采用默认值。 */ }
  return { width: 1440, height: 900 }
}

function shutdown() {
  if (quitting) return
  quitting = true
  try { fs.writeFileSync(boundsFile, JSON.stringify(win.getNormalBounds())) } catch { /* 仍然推送进度。 */ }
  settingsWindow?.destroy()
  localPage({ type: 'status', message: '正在同步…' })
  const proc = child
  if (!proc) return app.exit(0)
  const timer = setTimeout(() => {
    if (process.platform === 'win32') {
      const killer = spawn(path.join(process.env.SystemRoot, 'System32/taskkill.exe'), ['/PID', String(proc.pid), '/T', '/F'], { windowsHide: true, stdio: 'ignore' })
      killer.unref()
    } else {
      try { process.kill(-proc.pid, 'SIGKILL') } catch { /* 进程已退出。 */ }
    }
    app.exit(0)
  }, 10000)
  proc.once('close', () => { clearTimeout(timer); app.exit(0) })
  send('sync')
  send('quit')
  proc.stdin.end()
}

if (!app.requestSingleInstanceLock()) {
  app.quit()
} else {
  app.on('second-instance', () => {
    if (win?.isMinimized()) win.restore()
    win?.show()
    const active = settingsWindow || win
    active?.focus()
  })
  app.on('before-quit', event => { if (win) { event.preventDefault(); shutdown() } })
  app.whenReady().then(async () => {
    ipc()
    win = new BrowserWindow({ ...bounds(), minWidth: 1024, minHeight: 700, title: 'code-dojo',
      icon: path.join(process.resourcesPath, 'code-dojo.png'), backgroundColor: '#25241f', webPreferences: preferences })
    win.webContents.session.setPermissionRequestHandler((_wc, _perm, callback) => callback(false))
    protect(win)
    menu()
    win.on('close', event => { event.preventDefault(); shutdown() })
    await win.loadURL(startup)
    start()
  })
}
