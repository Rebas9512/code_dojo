// 在全新数据目录中实跑 AppImage 或 macOS .app，所有发布与同步请求都只访问这个回环服务。
const assert = require('node:assert/strict')
const { execFileSync } = require('node:child_process')
const { createHash } = require('node:crypto')
const { once } = require('node:events')
const fs = require('node:fs')
const path = require('node:path')
const http = require('node:http')
const { setTimeout: delay } = require('node:timers/promises')
const { _electron } = require('playwright-core')

const [image, payload, output] = process.argv.slice(2).map(p => path.resolve(p))
const mac = process.platform === 'darwin'
const root = path.join(__dirname, '../..')
const work = fs.mkdtempSync(path.join(require('node:os').tmpdir(), 'dojo-smoke-'))
const tmp = path.join(work, 'tmp')
const bin = path.join(work, 'bin')
for (const dir of [tmp, bin]) fs.mkdirSync(dir)
const contents = new Map()
let closing = false, stall = false, finalReads = 0
let stallRelease = false, releaseRequestedAt
let connected = false
const blob = bytes => createHash('sha1').update('blob ' + bytes.length + '\0').update(bytes).digest('hex')

const hub = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://127.0.0.1').pathname
  const sync = url.includes('/code_dojo_sync/')
  assert.equal(req.headers.authorization, sync ? 'Bearer test-write' : connected ? 'Bearer test-read' : undefined)
  const reply = obj => res.end(JSON.stringify(obj))
  if (url.endsWith('payload-latest')) {
    if (stallRelease) { releaseRequestedAt = Date.now(); return }
    reply({ assets: [{ id: 1, name: 'manifest.json' }, { id: 2, name: 'payload.zip' }] })
  } else if (url.endsWith('/assets/1')) {
    res.end(fs.readFileSync(path.join(payload, 'manifest.json')))
  } else if (url.endsWith('/assets/2')) {
    const archive = path.join(payload, 'payload.zip')
    res.setHeader('content-length', fs.statSync(archive).size)
    for await (const chunk of fs.createReadStream(archive, { highWaterMark: 1024 * 1024 })) {
      res.write(chunk)
      await delay(100)
    }
    res.end()
  } else if (sync && url.endsWith('/git/trees/main')) {
    if (stall) return
    if (closing) { finalReads++; await delay(700) }
    reply({ sha: String(contents.size), tree: Array.from(contents, ([key, bytes]) => ({ path: key, sha: blob(bytes), type: 'blob' })) })
  } else if (sync && url.includes('/contents/')) {
    const key = url.split('/contents/')[1]
    if (req.method === 'PUT') {
      if (!closing) { res.writeHead(503).end(); return }
      const chunks = []
      for await (const part of req) chunks.push(part)
      const bytes = Buffer.from(JSON.parse(Buffer.concat(chunks)).content, 'base64')
      contents.set(key, bytes)
      reply({ content: { sha: blob(bytes) } })
    } else {
      res.end(contents.get(key))
    }
  } else {
    res.writeHead(404).end()
  }
})

async function submit(page, origin, track, stage, id, file) {
  await page.goto(origin + '/p/' + id)
  const source = fs.readFileSync(path.join(root, 'problems', track, stage, id, file), 'utf8').trimEnd()
  await page.locator('.monaco-editor .view-lines').first().click({ position: { x: 30, y: 12 } })
  await page.keyboard.press('ControlOrMeta+a')
  await page.keyboard.insertText(source)
  const result = page.waitForResponse(r => r.url().endsWith('/' + id + '/submit'))
  await page.getByRole('button', { name: '提交', exact: true }).click()
  const body = await (await result).json()
  assert.equal(body.verdict, 'accepted', JSON.stringify(body))
  assert.equal(body.passed, body.total)
  await page.locator('.tone-pass').first().waitFor()
  await page.screenshot({ path: path.join(output, track + '.png') })
  console.log(track, body.passed + '/' + body.total)
}

// 只在指定父进程的直接子进程中找本次测试的启动器和后端。
function childMatching(parent, pattern) {
  return Number(execFileSync('/usr/bin/pgrep', ['-P', String(parent), '-f', pattern], { encoding: 'utf8' }).trim())
}

async function openSettings(app, page) {
  await page.locator('summary', { hasText: '桌面' }).click()
  const opened = app.waitForEvent('window', { timeout: 10000 })
  await page.getByRole('button', { name: '设置', exact: true }).click()
  const settings = await opened
  await settings.getByRole('button', { name: '完成' }).waitFor()
  return settings
}

// "完成"会关掉自己所在的窗口；窗口关得比点击收尾快时 Playwright 报页面已关闭，这种情况算成功。
async function closeSettings(settings) {
  const closed = settings.waitForEvent('close', { timeout: 5000 })
  await settings.getByRole('button', { name: '完成' }).click().catch(error => { if (!settings.isClosed()) throw error })
  await closed
}

async function checkAgentPath(app, page, origin) {
  const binary = path.join(work, '手动 命令', 'claude')
  fs.mkdirSync(path.dirname(binary))
  fs.writeFileSync(binary, '#!/bin/sh\n[ "$#" = 1 ] && [ "$1" = --version ] || exit 9\necho "2.0.0 (Claude Code)"\n', { mode: 0o755 })
  const settings = await openSettings(app, page)
  const row = settings.getByRole('form', { name: 'Claude Code' })
  const ids = async () => (await (await fetch(origin + '/api/status')).json()).ai_agents.map(a => a.id)
  await settings.getByText(/AI 助教已关闭/).waitFor()
  await row.getByText('未找到', { exact: true }).waitFor()
  assert.deepEqual(await ids(), [])
  await row.getByRole('textbox').fill(binary)
  await row.getByRole('button', { name: '保存' }).click()
  await settings.getByText('AI 助教已启用', { exact: true }).waitFor()
  await row.getByText('手动指定 · ' + binary, { exact: true }).waitFor()
  assert.deepEqual(await ids(), ['claude'])
  await row.getByRole('button', { name: '改回自动查找' }).click()
  await row.getByText('未找到', { exact: true }).waitFor()
  await settings.getByText(/AI 助教已关闭/).waitFor()
  assert.deepEqual(await ids(), [])
  await closeSettings(settings)
  await page.getByRole('tab').first().waitFor()
  console.log('设置保存与改回自动后，后端助教列表分别为 [claude] 和 []')
}

async function main() {
  const args = mac ? ['--use-mock-keychain'] : ['--ozone-platform=x11', '--password-store=basic', '--disable-dev-shm-usage']
  let launcher = path.join(image, 'Contents/MacOS/code-dojo')
  if (!mac) {
    // 包装脚本把 AppImage 的解包参数放在 Playwright 调试参数之前。
    launcher = path.join(bin, 'launch')
    fs.writeFileSync(launcher, '#!/bin/sh\nexec "$DOJO_SMOKE_IMAGE" --appimage-extract-and-run "$@"\n', { mode: 0o755 })
    fs.writeFileSync(path.join(bin, 'secret-tool'), '#!/bin/sh\nfile="$CODE_DOJO_DATA/test-keyring"\ncase "$1" in store) /bin/cat > "$file";; lookup) [ -f "$file" ] && /bin/cat "$file";; clear) /bin/rm -f "$file";; esac\n', { mode: 0o755 })
  }
  hub.listen(0, '127.0.0.1')
  await once(hub, 'listening')
  let app
  try {
    const env = Object.fromEntries(Object.entries(process.env).filter(([k]) => !k.startsWith('CODE_DOJO_')))
    delete env.ELECTRON_RUN_AS_NODE
    // 登录 shell 也与系统 PATH 隔离。macOS 找不到 security 时走测试数据目录的凭据文件。
    Object.assign(env, { PATH: bin, SHELL: '/usr/bin/false', TMPDIR: tmp, XDG_CACHE_HOME: path.join(work, 'cache'),
      XDG_CONFIG_HOME: path.join(work, 'config'), CODE_DOJO_DATA: path.join(work, 'data'),
      CODE_DOJO_AI_PROVIDER: 'off', CODE_DOJO_PORT: '8019', CODE_DOJO_GITHUB_API: 'http://127.0.0.1:' + hub.address().port,
      DOJO_SMOKE_IMAGE: image, NO_CLEANUP: '1' })
    app = await _electron.launch({ executablePath: launcher, chromiumSandbox: true, env, args, timeout: 120000, artifactsDir: work })
    const page = await app.firstWindow()
    page.setDefaultTimeout(90000)
    page.on('framenavigated', frame => { if (frame === page.mainFrame()) console.log('窗口导航', frame.url()) })
    const shot = name => page.screenshot({ path: path.join(output, name + '.png') })
    await page.getByRole('progressbar').waitFor()
    await shot('download')
    await page.waitForURL(/^http:\/\/127\.0\.0\.1:\d+\/$/, { timeout: 120000 })
    let origin = new URL(page.url()).origin
    await page.getByRole('tab').first().waitFor()
    assert.equal(await page.title(), 'code-dojo')
    const version = await page.evaluate(() => window.dojoDesktop.version())
    assert.equal(version.launcher, require('../package.json').version)
    assert.equal(await page.evaluate(() => typeof window.dojoStartup), 'undefined')
    await shot('map')
    const main = await app.evaluate(({ app, BrowserWindow }) => {
      globalThis.secondLaunches = 0
      app.on('second-instance', () => globalThis.secondLaunches++)
      const prefs = BrowserWindow.getAllWindows()[0].webContents.getLastWebPreferences()
      return { pid: process.pid, executable: process.execPath, sandbox: prefs.sandbox,
        isolated: prefs.contextIsolation, node: prefs.nodeIntegration, noSandbox: app.commandLine.hasSwitch('no-sandbox') }
    })
    assert.ok(main.sandbox && main.isolated && !main.node)
    assert.equal(main.noSandbox, !mac)
    execFileSync(main.executable, args, { env, timeout: 10000, stdio: 'ignore' })
    assert.equal(await app.evaluate(() => globalThis.secondLaunches), 1)
    const supervisor = childMatching(main.pid, ' -m bootstrap serve --protocol jsonl$')
    const backend = childMatching(supervisor, '/runtime/start[.]py$')
    process.kill(backend, 'SIGKILL')
    await page.getByText('本机服务意外退出，请重启').waitFor()
    await shot('restart')
    await page.getByRole('button', { name: '重启', exact: true }).click()
    await page.waitForURL(/^http:\/\/127\.0\.0\.1:\d+\/$/, { timeout: 90000 })
    origin = new URL(page.url()).origin
    await page.getByRole('tab').first().waitFor()
    console.log('已验证渲染器隔离、第二实例聚焦与后端崩溃重启')
    await page.getByText('本机保存', { exact: true }).waitFor()
    const localSettings = await openSettings(app, page)
    const nativeSettings = await app.browserWindow(localSettings)
    assert.equal(await nativeSettings.evaluate(win => win.isModal()), !mac)
    await Promise.all([localSettings.waitForEvent('close', { timeout: 5000 }), localSettings.keyboard.down('Escape')])
    assert.ok(localSettings.isClosed() && !page.isClosed())
    const settings = await openSettings(app, page)
    await settings.getByText(/AI 助教已关闭/).waitFor()
    await settings.screenshot({ path: path.join(output, 'settings.png') })
    await settings.getByLabel('同步码').fill('incorrect-smoke-password')
    await settings.getByRole('button', { name: '开启同步' }).click()
    await settings.getByText('同步码不对，还可尝试 4 次').waitFor()
    await settings.screenshot({ path: path.join(output, 'settings-failed.png') })
    async function enable() {
      await settings.getByLabel('同步码').fill('dojo-smoke-unlock')
      await settings.getByRole('button', { name: '开启同步' }).click()
      await settings.getByText('已开启进度同步').waitFor()
      connected = true
    }
    await enable()
    await settings.screenshot({ path: path.join(output, 'settings-connected.png') })
    await settings.getByRole('button', { name: '关闭同步' }).click()
    await settings.getByRole('button', { name: '确认关闭' }).click()
    await settings.getByLabel('同步码').waitFor()
    connected = false
    assert.ok(!fs.existsSync(path.join(env.CODE_DOJO_DATA, mac ? 'github-tokens.json' : 'test-keyring')))
    await enable()
    await closeSettings(settings)
    assert.ok(settings.isClosed() && !page.isClosed())
    origin = new URL(page.url()).origin
    await page.getByRole('tab').first().waitFor()
    await submit(page, origin, 'python', '0A', 'py-0a-003-rectangle-perimeter', 'solution.py')
    await submit(page, origin, 'sql', '3', 'sql-3-020-duplicate-rating-preview', 'solution.sql')
    await app.evaluate(({ shell }) => { globalThis.openedLinks = []; shell.openExternal = async url => { globalThis.openedLinks.push(url) } })
    const link = page.locator('a[href*="leetcode.com"]').first()
    const url = await link.getAttribute('href')
    await link.click()
    assert.deepEqual(await app.evaluate(() => globalThis.openedLinks), [url])
    assert.equal(new URL(page.url()).origin, origin)
    await page.evaluate(() => { location.href = 'https://github.com/' })
    const deadline = Date.now() + 5000
    while (await app.evaluate(() => globalThis.openedLinks.length) < 2 && Date.now() < deadline) await delay(50)
    assert.deepEqual(await app.evaluate(() => globalThis.openedLinks), [url, 'https://github.com/'])
    assert.equal(new URL(page.url()).origin, origin)
    assert.equal(app.windows().length, 1)
    const expectedBounds = await app.evaluate(({ BrowserWindow, screen }) => {
      const win = BrowserWindow.getAllWindows()[0]
      const area = screen.getPrimaryDisplay().workArea
      win.setBounds({ x: area.x, y: area.y, width: Math.min(1200, area.width), height: Math.min(760, area.height) })
      return win.getNormalBounds()
    })
    // 应用拦下的外链跳转在 Playwright 看来一直没结束，再点页面会一直等；先回首页。
    await page.goto(origin + '/')
    await page.getByRole('tab').first().waitFor()
    const desktopData = path.join(env.CODE_DOJO_DATA, 'desktop')
    const installed = JSON.parse(fs.readFileSync(path.join(desktopData, 'current.json'), 'utf8'))
    const probeName = '/assets/smoke-ab12CD34.txt'
    const probeFile = path.join(desktopData, installed.digest, 'web/dist', probeName)
    fs.writeFileSync(probeFile, 'old')
    const readProbe = name => fetch(name).then(reply => reply.text())
    assert.equal(await page.evaluate(readProbe, probeName), 'old')
    fs.writeFileSync(probeFile, 'new')
    assert.equal(await page.evaluate(readProbe, probeName), 'old')
    await page.evaluate(() => localStorage.setItem('smoke-draft', 'draft'))
    const settingsAtQuit = await openSettings(app, page)
    await settingsAtQuit.getByText('已开启进度同步').waitFor()
    const appProcess = app.process()
    closing = true
    const closed = app.waitForEvent('close', { timeout: 13000 })
    await app.evaluate(({ app }) => app.quit())
    await page.getByRole('heading', { name: '正在同步…' }).waitFor()
    await shot('closing')
    await closed
    assert.ok(settingsAtQuit.isClosed())
    assert.equal(appProcess.exitCode, 0)
    app = null
    assert.ok(finalReads > 0 && contents.size > 0)
    const events = [...contents.values()].map(bytes => bytes.toString()).join('\n')
    assert.ok(events.includes('py-0a-003-rectangle-perimeter') && events.includes('sql-3-020-duplicate-rating-preview'))
    await assert.rejects(fetch(origin + '/api/health'))
    console.log('外部链接 2 个，退出推送完成，端口已释放。', work)

    // 模拟上次载入过旧网页。重开时题库远端挂起，退出时再单独挂起进度远端。
    closing = false
    fs.writeFileSync(path.join(desktopData, 'loaded-payload-version'), 'previous-smoke-version')
    stallRelease = true
    // 此轮的 PATH、登录 shell 和扩展目录都隔离，只能选到接受 --version 的假命令。
    const agentEnv = { ...env, HOME: work, CODE_DOJO_AI_PROVIDER: 'claude' }
    app = await _electron.launch({ executablePath: main.executable, chromiumSandbox: true, env: agentEnv, args, artifactsDir: work })
    const reopened = await app.firstWindow()
    await reopened.getByRole('heading', { name: '正在检查更新…' }).waitFor({ timeout: 15000 })
    await reopened.getByRole('tab').first().waitFor({ timeout: 18000 })
    const launchMs = Date.now() - releaseRequestedAt
    assert.ok(launchMs >= 4500 && launchMs < 18000, '挂起的更新请求到地图可用 ' + launchMs + ' 毫秒')
    assert.equal(await reopened.evaluate(() => window.dojoDesktop.version().then(v => v.payload)), version.payload)
    assert.equal(await reopened.evaluate(readProbe, probeName), 'new')
    assert.equal(await reopened.evaluate(() => localStorage.getItem('smoke-draft')), 'draft')
    assert.deepEqual(await app.evaluate(({ BrowserWindow }) => BrowserWindow.getAllWindows()[0].getNormalBounds()), expectedBounds)
    const reopenedOrigin = new URL(reopened.url()).origin
    await checkAgentPath(app, reopened, reopenedOrigin)
    stall = true
    const started = Date.now()
    const stopped = app.waitForEvent('close', { timeout: 12000 })
    await app.evaluate(({ BrowserWindow }) => BrowserWindow.getAllWindows()[0].close())
    await stopped
    app = null
    const elapsed = Date.now() - started
    assert.ok(elapsed >= 8000 && elapsed < 11000, '退出耗时 ' + elapsed + ' 毫秒')
    await assert.rejects(fetch(reopenedOrigin + '/api/health'))
    console.log('题库远端挂起后', launchMs, '毫秒进入地图，HTTP 缓存已刷新，草稿和窗口位置已保留。进度远端挂起时退出耗时', elapsed, '毫秒，端口已释放。')
  } finally {
    if (app) await app.close()
    hub.closeAllConnections()
    hub.close()
  }
}

main().catch(error => { console.error(error); process.exitCode = 1 })
