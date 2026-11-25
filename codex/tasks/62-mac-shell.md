# 62-mac-shell：macOS 安装包签名，设置窗口能关、能退出（issue #1、#2）

## 背景
用户 2026-11-24 在 Mac（Apple Silicon，app-v1.3.0）上实测后开了 6 个 issue，今天说："现在我想 把这6条解决一下，分别先做一下能修的部分，然后其他conflict的问题的话看看出一个推荐方案这样 …… 可以并行做"。

本任务负责两条，先用 `gh issue view 1` 和 `gh issue view 2` 读全文（只读，不要评论、不要改 issue）：
- **#1**：macOS 包没有签名（`desktop/builder.cjs` 里 `identity: null`，`scripts/desktop/build.py` 里 `CSC_IDENTITY_AUTO_DISCOVERY=false`）。整个 .app 只剩 Electron 二进制自带的签名，和改过的 bundle 对不上，加上浏览器下载带的隔离标记，Apple Silicon 直接提示"已损坏"。
- **#2**：设置窗口是 `parent: win, modal: true`，在 macOS 上会显示成 sheet：没有标题栏和关闭按钮，Esc 也关不掉，主窗口被挡住；这时用 AppleScript 退出返回 -128，等了约 10 秒进程都还在。

同时在跑的其他任务：61 改 `bootstrap/agents.py`、`server/app/ai/provider.py`，以及 deploy/README.md 里"AI 助教已关闭"那一节；63 改 `web/`；64 只写 `docs/tutor-memory.md`。这些你都不要碰。

## 要做的事
1. **#1 ad-hoc 签名**（Apple 开发者账号签名和公证这次不做）：
   - `builder.cjs` 改成让 electron-builder 对整个 bundle 做 ad-hoc 签名（`identity: '-'` 或 26.x 里等效的写法）。去 `desktop/node_modules/app-builder-lib` 的源码里确认这个版本确实支持、确实会签 `Resources/runtime` 里随包 Python 的 `.so` / `.dylib` / 可执行文件。`build.py` 里的 `CSC_IDENTITY_AUTO_DISCOVERY` 按需要调整。
   - `release-app.yml` 的 macOS 任务里，构建完加一步 `codesign --verify --deep --strict --verbose=2 <app 路径>`，签名不对构建就失败。
   - 检查运行时有没有东西往 .app 里写文件（`.pyc`、缓存、日志等）。现在随包 `.pyc` 是构建时生成的 unchecked-hash，后端带 `-B`，应该没有。确认一遍；如果有写入，会破坏签名，还可能触发 macOS 的"想要修改其他应用"提示，要改到用户数据目录。
2. **能在发版前试跑**：给 `release-app.yml` 加 `workflow_dispatch`。手动触发时三系统照常构建、跑检查和冒烟，但跳过"标签和版本号一致"的校验，也不跑 `publish-app`（发布只在推 `app-v*` 标签时做）。这样主控可以在分支上先跑一遍再打标签。
3. **#2 设置窗口能关**：
   - `startup.html` / `startup.js`：设置模式下加一个"完成"按钮，按 Esc 也能关闭。
   - `preload.cjs` 的 `dojoStartup` 加 `close`，`main.cjs` 用 `listen('startup:close', 'local', …)` 只关设置窗口。
   - macOS 上不要再用 sheet：`modal` 只在 macOS 以外打开（或者你有更好的写法），macOS 上设置窗口是带红绿灯的普通子窗口，不挡住应用退出。Windows / Linux 保持模态。
   - 不要加会关掉主窗口的全局 `CmdOrCtrl+W`：主窗口关闭就等于退出，在编辑器里误按会直接退出程序。
4. **#2 退出一定能走完**：`shutdown()` 一开头就把 `quitting` 设成 true，后面任何一步抛异常，退出计时器就设不上，之后的退出请求全被吞掉。改成先设好计时器（或者用 try/finally 保证设上），再做写窗口位置、销毁设置窗口、切换页面、发 sync/quit 这些步骤。不加别的兜底。
5. **冒烟测试**（`desktop/tests/smoke.cjs`）：把现在直接 `await settings.close()` 的地方改成点"完成"按钮，并断言设置窗口确实关了；再加一个用例：设置窗口开着时退出，断言程序会退出。
6. **macOS 也跑冒烟**（可选）：如果 `smoke.cjs` 只要小改就能接受 macOS 的 `.app`（Playwright `_electron.launch` 用 `Contents/MacOS/code-dojo`），就在 `release-app.yml` 的 macOS 任务里也跑一遍；改动大就不做，写进报告。仓库是公开的，标准 runner 不计费。
7. **文档**：
   - `deploy/README.md` 只改 macOS 下载和首次打开那几节（约 35–45 行），不要动"AI 助教已关闭"那一节，那一节归 61。签名后提示应该从"已损坏"变成"无法验证开发者"，写"系统设置 → 隐私与安全性 → 仍要打开"的步骤；`xattr` 那行命令留作旧版本或仍提示已损坏时的办法。macOS 15 起按住 Control 点"打开"已经不能绕过，不要写这个办法。
   - `docs/README.md` 只改"桌面应用"一节里相关的描述。
   - 不要改版本号（`bootstrap/__init__.py` 的 VERSION、`desktop/package.json`），发版由主控统一改。

## 这次不做
- Apple Developer ID 签名和公证（$99/年）。报告里写一段"什么情况下值得做、要准备什么"，主控转给用户。
- 不改 `bootstrap/`、`server/`、`web/`、`ci.yml`、`release-payload.yml`。

## 验收标准
- `for f in desktop/*.cjs desktop/*.js desktop/tests/smoke.cjs; do node --check "$f" || exit 1; done` 通过。
- `release-app.yml` 用 `python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))"` 能解析；推标签时的行为和现在一致（构建 → 检查 → 发布），手动触发时不发布。
- **不要在本机启动 Electron 窗口**：本机没有 xvfb，窗口会弹在用户正在用的桌面上。Electron 冒烟和 macOS 签名检查由主控在分支上手动触发 `release-app.yml` 来跑。报告里写清你预期 CI 上每一步会怎样，有拿不准的地方标出来。
- 报告单独一节"需要在 Mac 上实测的点"：主控会请用户在 Mac 上照着验。
