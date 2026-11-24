// 在全新数据目录中实跑 AppImage，所有发布与同步请求都只访问这个回环服务。
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
const root = path.join(__dirname, '../..')
const work = fs.mkdtempSync(path.join(require('node:os').tmpdir(), 'dojo-smoke-'))
const tmp = path.join(work, 'tmp')
const bin = path.join(work, 'bin')
for (const dir of [tmp, bin]) fs.mkdirSync(dir)
const contents = new Map()
let closing = false, stall = false, finalReads = 0
let connected = false
const blob = bytes => createHash('sha1').update('blob ' + bytes.length + '\0').update(bytes).digest('hex')

const hub = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://127.0.0.1').pathname
  const sync = url.includes('/code_dojo_sync/')
  assert.equal(req.headers.authorization, sync ? 'Bearer test-write' : connected ? 'Bearer test-read' : undefined)
  const reply = obj => res.end(JSON.stringify(obj))
  if (url.endsWith('payload-latest')) {
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
  await page.keyboard.press('Control+a')
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

// 仅从本次 Electron 主进程的直接子树选取正在测试的 Python 服务。
function childMatching(parent, matches) {
  for (const task of fs.readdirSync('/proc/' + parent + '/task')) {
    let children
    try { children = fs.readFileSync('/proc/' + parent + '/task/' + task + '/children', 'utf8').trim() } catch { continue }
    for (const pid of children.split(' ').filter(Boolean)) {
      let args
      try { args = fs.readFileSync('/proc/' + pid + '/cmdline', 'utf8').split('\0') } catch { continue }
      if (matches(args)) return Number(pid)
    }
  }
  assert.fail('未找到本轮启动的子进程')
}

async function main() {
  // Playwright 的调试参数由包装脚本转交给 Electron，AppImage 运行时参数必须排在首位。
  const launcher = path.join(bin, 'launch')
  fs.writeFileSync(launcher, '#!/bin/sh\nexec "$DOJO_SMOKE_IMAGE" --appimage-extract-and-run "$@"\n', { mode: 0o755 })
  // 隔离用户的 Git、gh、助教和钥匙串。仅为本次测试提供凭据存储。
  fs.writeFileSync(path.join(bin, 'secret-tool'), '#!/bin/sh\nfile="$CODE_DOJO_DATA/test-keyring"\ncase "$1" in store) /bin/cat > "$file";; lookup) [ -f "$file" ] && /bin/cat "$file";; clear) /bin/rm -f "$file";; esac\n', { mode: 0o755 })
  hub.listen(0, '127.0.0.1')
  await once(hub, 'listening')
  let app
  try {
    const env = Object.fromEntries(Object.entries(process.env).filter(([k]) => !k.startsWith('CODE_DOJO_')))
    delete env.ELECTRON_RUN_AS_NODE
    Object.assign(env, { PATH: bin, TMPDIR: tmp, XDG_CACHE_HOME: path.join(work, 'cache'),
      XDG_CONFIG_HOME: path.join(work, 'config'), CODE_DOJO_DATA: path.join(work, 'data'),
      CODE_DOJO_AI_PROVIDER: 'off', CODE_DOJO_PORT: '8001', CODE_DOJO_GITHUB_API: 'http://127.0.0.1:' + hub.address().port,
      DOJO_SMOKE_IMAGE: image, NO_CLEANUP: '1' })
    app = await _electron.launch({ executablePath: launcher, chromiumSandbox: true, env, timeout: 120000,
      args: ['--ozone-platform=x11', '--password-store=basic', '--disable-dev-shm-usage'], artifactsDir: work })
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
    // 网页仍是隔离的沙箱页面；AppImage 的 AppRun 一律带 --no-sandbox（见 scripts/desktop/build.py），这里确认没丢。
    assert.ok(main.sandbox && main.isolated && !main.node && main.noSandbox)
    execFileSync(main.executable, ['--ozone-platform=x11'], { env, timeout: 10000, stdio: 'ignore' })
    assert.equal(await app.evaluate(() => globalThis.secondLaunches), 1)
    const supervisor = childMatching(main.pid, args => args.includes('bootstrap') && args.includes('jsonl'))
    const backend = childMatching(supervisor, args => args.some(arg => arg.endsWith('/runtime/start.py')))
    process.kill(backend, 'SIGKILL')
    await page.getByText('本机服务意外退出，请重启').waitFor()
    await shot('restart')
    await page.getByRole('button', { name: '重启', exact: true }).click()
    await page.waitForURL(/^http:\/\/127\.0\.0\.1:\d+\/$/, { timeout: 90000 })
    origin = new URL(page.url()).origin
    await page.getByRole('tab').first().waitFor()
    console.log('已验证渲染器隔离、第二实例聚焦与后端崩溃重启')
    await page.getByText('本机保存', { exact: true }).waitFor()
    await page.locator('summary', { hasText: '桌面' }).click()
    const opened = app.waitForEvent('window')
    await page.getByRole('button', { name: '设置', exact: true }).click()
    const settings = await opened
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
    assert.ok(!fs.existsSync(path.join(env.CODE_DOJO_DATA, 'test-keyring')))
    await enable()
    await settings.close()
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
    const expectedBounds = await app.evaluate(({ BrowserWindow }) => {
      const win = BrowserWindow.getAllWindows()[0]
      win.setBounds({ x: 40, y: 50, width: 1200, height: 760 })
      return win.getNormalBounds()
    })
    closing = true
    const closed = app.waitForEvent('close', { timeout: 13000 })
    await app.evaluate(({ BrowserWindow }) => BrowserWindow.getAllWindows()[0].close())
    await page.getByRole('heading', { name: '正在同步…' }).waitFor()
    await shot('closing')
    await closed
    app = null
    assert.ok(finalReads > 0 && contents.size > 0)
    const events = [...contents.values()].map(bytes => bytes.toString()).join('\n')
    assert.ok(events.includes('py-0a-003-rectangle-perimeter') && events.includes('sql-3-020-duplicate-rating-preview'))
    await assert.rejects(fetch(origin + '/api/health'))
    console.log('外部链接 2 个，退出推送完成，端口已释放。', work)

    // 再开一次已提取的同一成品，验证窗口记忆和远端无响应时的退出上限。
    closing = false
    app = await _electron.launch({ executablePath: main.executable, chromiumSandbox: true, env,
      args: ['--ozone-platform=x11', '--password-store=basic', '--disable-dev-shm-usage'], artifactsDir: work })
    const reopened = await app.firstWindow()
    await reopened.getByRole('tab').first().waitFor({ timeout: 90000 })
    assert.deepEqual(await app.evaluate(({ BrowserWindow }) => BrowserWindow.getAllWindows()[0].getNormalBounds()), expectedBounds)
    const reopenedOrigin = new URL(reopened.url()).origin
    stall = true
    const started = Date.now()
    const stopped = app.waitForEvent('close', { timeout: 12000 })
    await app.evaluate(({ BrowserWindow }) => BrowserWindow.getAllWindows()[0].close())
    await stopped
    app = null
    const elapsed = Date.now() - started
    assert.ok(elapsed >= 8000 && elapsed < 11000, '退出耗时 ' + elapsed + ' 毫秒')
    await assert.rejects(fetch(reopenedOrigin + '/api/health'))
    console.log('窗口位置与大小已恢复。远端不响应时退出耗时', elapsed, '毫秒，端口已释放。')
  } finally {
    if (app) await app.close()
    hub.closeAllConnections()
    hub.close()
  }
}

main().catch(error => { console.error(error); process.exitCode = 1 })
