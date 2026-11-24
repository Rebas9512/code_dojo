# 59-local-first-sync-code：下载即本机用，设置里输入同步码才接进度仓库

## 背景

用户 2026-11-23 先提出"第二套密码 = 访客模式"，随后改成更简单的做法：
> "我想干脆可以直接做成这样 大家可以下载来直接就是本地用，然后在设置里就直接放给我输入同步码的地方，输入了以后我就接到同步仓库了，没有输入的就是默认本地使用 也不需要游客码了"

旧的 59（访客密码、多槽加密文件）已经作废，改动已撤销，不要再做。

现状（读 `docs/README.md` 的「桌面应用」和 `deploy/README.md` 的「在一台新电脑上用」）：
- 第一次打开要在启动页输入解锁密码。`bootstrap/protocol.py` 的 `Controller.begin()` 按 `credential_source()` 的结果走：
  - 有本机凭据或 `gh` 登录：直接启动；
  - 有随包的 `sealed-tokens.json`：`need_unlock`；
  - 都没有：`need_tokens`，手动填令牌。
- 解锁后两个令牌（`code`、`sync`）存进钥匙串或 `github-tokens.json`（`bootstrap/credentials.py`）。
- `bootstrap/github.py` 的 `GitHub.open` 每次都带 `Authorization`；查更新、下载更新包都用 `code` 令牌。
- `bootstrap/service.py` 在令牌为空时已经把 `CODE_DOJO_SYNC_REPO` 置空，后端不同步。
- 后端的 `store.pending_events()` 是所有还没推上去的事件。
- **仓库 `Rebas9512/code_dojo` 已经公开**，`payload-latest` Release 不用令牌就能读和下载。进度仓库 `code_dojo_sync` 仍是私有的。

## 要做的事

1. **打开就能用，不再要密码**
   - 有已存凭据（钥匙串或 `github-tokens.json`）：和现在一样，带同步启动。1.2.0 已经解锁过的机器升级后照旧同步，不用重新输入。
   - 没有已存凭据：直接以**本机模式**启动，令牌为空、不同步，做题记录写本机数据目录。
   - 删掉这些：
     - 启动页的解锁表单、令牌表单和"改用令牌"；
     - 协议里的 `unlock`、`set_tokens`、`need_unlock`、`need_tokens`；
     - 启动时的 `gh auth token` 自动探测。本机模式每次启动都要多一次 `gh` 调用和两次网络往返，换来的只是主人少输一次同步码。
2. **查更新不要令牌**
   - `GitHub.open` 只在有令牌时才带 `Authorization`，查更新、下载更新包一律可以匿名。
   - 主人有 `code` 令牌时照旧带上，额度更高。
3. **同步码**：就是现在的解锁密码，`sealed-tokens.json` 的格式和 `scripts/desktop/seal_tokens.py` 都不改。
   - 协议新增 `connect_sync`（参数 `code`）：
     - 用它解开随包的 `sealed-tokens.json`。解开后存凭据，用当前题库直接重启本机服务（带同步，不用再查一次更新），再发 `ready`。
     - 输错沿用 `UnlockAttempts`：最多 5 次，之后等 30 秒，发 `sync_code_failed`（`remaining`、`wait`）。
     - 安装包里没有加密文件（比如开发环境）时，发一条错误："这个安装包不支持同步码"。
   - 协议新增 `disconnect_sync`：清掉已存凭据，钥匙串和备用文件都要清；然后重启服务，不再同步。本机的记录和还没推上去的事件都保留。
   - `ready` 加字段 `sync`（布尔），表示进度同步是否开着。
   - 先在本机模式下做的题，输入同步码以后，第一次同步要一起推上去。`pending_events` 应该已经是这样，写测试确认。
4. **界面**
   - **设置窗口**（桌面 → 设置、Ctrl+,）：
     - 没开同步时显示一句"做题记录保存在本机。输入同步码，可以把记录同步到进度仓库，换电脑接着练。"，下面是同步码输入框和「开启同步」按钮。输错时显示剩余次数或倒计时，和现在的解锁页一样。
     - 已开同步时显示"已开启进度同步"和「关闭同步」按钮，点了先确认一次。
     - 助教状态照旧显示。
   - **启动页**只留状态、下载进度、出错重试和新版安装包链接。
   - **做题页状态栏**：没开同步时显示"本机保存"，悬停提示"在 桌面 → 设置 输入同步码可以开启同步"。不再显示"未开启同步"。
   - 顶栏"桌面"菜单里的"立即同步"，没开同步时不显示。
   - 网页靠 `GET /api/sync/status` 的 `enabled` 判断，不需要改 `api.ts`。
5. **文档**
   - `deploy/README.md`：
     - 「在一台新电脑上用」改成三步：下载安装包 → 打开就能用（记录存本机）→ 想同步就在"桌面 → 设置"输入同步码。
     - 删掉手动填令牌的备用方式。创建令牌的说明移到「发新安装包和换令牌」，给发布者自己看。
     - 新增一节「分发给别人用」：把 Release 链接发给对方即可；他的记录只在他自己电脑上；每次打开自动更新题库；AI 助教要他自己装好并登录 Claude Code 或 Codex。
   - `docs/README.md`：只改桌面一节（启动流程、协议命令和消息、设置），用小补丁改。任务 60 正在改同一个文件的助教一节。

## 不做

- 不改 `sealed-tokens.json` 的格式，不改 `seal_tokens.py`，不需要重新加密。
- 不改 `bootstrap.VERSION` 和 `desktop/package.json` 的版本号，主控发版时改。
- 不改判题、题库和网页的做题功能。

## 并行约束（任务 60「助教看草稿、改草稿」正在跑）

- 60 改的是：
  - `server/app/ai/tutor.py`、`server/app/db.py`；
  - `server/app/main.py` 的聊天部分；
  - `web/src/api.ts`、`ChatPanel.tsx`、`CodeEditor.tsx`、`ProblemWorkspace.tsx`；
  - `server/tests/test_tutor.py`、`test_inspect.py`、`test_ai_agents.py`；
  - `docs/README.md` 的助教一节。
- **这些都不要碰。**跑全量测试时，如果失败只出在这些文件上，说明 60 还没写完，不是你的问题，在报告里注明。
- 测试实例端口用 **后端 8032、前端 5202**。

## 安全

- 不读、不打印、不写进日志或报告任何真实的令牌和密码。测试一律用假值，加密文件用测试里现成的生成方式（`desktop/tests/seal.py` 等）。
- 不要动 `.env`，也不要复制它。

## 验收标准

- `cd server && .venv/bin/python -m pytest -q ../bootstrap/tests` 和 `cd server && .venv/bin/python -m pytest -q` 全过。7 个会建临时 git 仓库的同步测试，可以按标准做法排除。
- 新增测试覆盖：
  - 没有凭据时：`begin()` 直接启动，不发解锁类消息，服务配置里令牌为空，`ready.sync` 为 false；
  - `connect_sync`：
    - 码对：存凭据、重启服务、`ready.sync` 为 true；
    - 码错：发 `sync_code_failed` 并计次，第 5 次后要等待；
    - 没有加密文件时：报错；
  - `disconnect_sync`：凭据清空，`ready.sync` 为 false；
  - 没有令牌时：查更新和下载的请求都不带 `Authorization`；
  - 本机模式下记的事件，开启同步后第一次交换会推上去（用 `github_sync` 的假客户端）。
- `node --check desktop/*.cjs desktop/*.js` 通过，`cd web && npm run build` 通过。
- 本机实际走一遍，用假的更新服务和测试密码生成的加密文件，按项目现有测试的搭法。流程：启动 → `ready`（sync false）→ 错码 → 对码 → `ready`（sync true）→ `disconnect_sync` → `ready`（sync false）。写清楚怎么测的。
- 设置页截图：用 Playwright 打开 `desktop/startup.html`，注入假的 `dojoStartup`，截三张：
  - 没开同步；
  - 输错同步码；
  - 已开同步。
- 报告写清楚：
  - 启动流程改成了什么样；
  - 协议增删了哪些命令和消息；
  - 发版前主控要做的步骤（应该只剩改版本号、跑三系统 CI、打标签）。
