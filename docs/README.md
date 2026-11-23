# code-dojo · 开发文档入口

> 给自己用的手写代码练习网站：从学习地图进入各条线，按阶段和知识点练固定题库，AI 随时答疑、分级提示、按需当场出新题。
> 最后更新 2026-11-23。摘要层（状态、发现、决策、可复用知识）在 Obsidian vault `coding_practice/projects/code-dojo/`；本文件和代码里的注释是原始文档。

## 这个项目是什么
- **目标**：长时间没手写代码，手很生。做一个类似 LeetCode 的网页，从 beginner 开始一步步把手写能力练回来，同时覆盖求职常用的标准题单。
- **学习线**：12 条线全部开放，共 1554 题。认识数据（20）是 Python 基础（238）与 SQL（216）的共同起点。SQL 之后可学产品分析 SQL（90）和建模与写数据（70）。其余为算法与数据结构（403）、数学（80）、数据处理（100）、张量（90）、机器学习（87）、训练（80）、手搓 LLM（80）。
- **使用方式**：每台机器运行自己的本机网页，代码和题库在公开仓库 `Rebas9512/code_dojo`，个人学习记录用另一个私有仓库同步。助教使用个人订阅。也可以在自己的服务器启用登录后远程访问。
- **当前成果**：地图和知识点页展示技能掌握度，今日计划安排到期复习和新题，手感统计按周展示练习趋势。Python 可用本机解释器或 Docker 判题，SQL 在浏览器中判题，两者都支持可运行的课、AI 助教和附加题。

## 目录
```
code-dojo/
├── dojo.py、dojo、dojo.ps1  本机启动、环境诊断和旧记录导入
├── desktop/              Electron 主进程、受限 preload、本地启动页与打包配置
├── bootstrap/            JSONL 控制协议、令牌、更新包校验与本机服务启动
├── .github/workflows/    测试（推送跑 Linux，手动触发跑三系统）、更新包发布、桌面安装包发布
├── docs/
│   ├── README.md         本文件
│   ├── problem-format.md 题目 / 技能 / 课 / track 的文件格式（合同）
│   ├── curriculum.md     学习曲线设计、各线题单规划
│   ├── teaching-design.md 教学设计和具名误解目录
│   ├── reports/          调研报告
│   └── research_notes/   调研的原始笔记（一个调研一个文件夹）
├── web/                  前端：登录、学习地图、练习工作区、今日计划、手感统计；SQL 查询、单条修改与多语句脚本在 PGlite Worker 中判题
├── codex/                派给 codex 的任务：brief.md（标准做法）、PLAN.md（排期和文件归属）、tasks/、runs/（运行记录，不进 git）
├── deploy/               单端口启动脚本、环境变量、systemd 与 Cloudflare Tunnel 模板
├── judge/python/         本地和两个 Docker 镜像共用的 Python 判题程序、普通 Python 镜像定义
├── judge/ds/             数据科学判题镜像（numpy + pandas + CPU 版 torch，从 Python 镜像复制 harness）
├── server/               后端：FastAPI（uv）；Python 判题（本地或 Docker）、题库、掌握度、复习日程与 AI 服务
├── problems/             固定题库（文件，git 管理）
│   ├── modeling/         建模与写数据：技能、课、分阶段脚本题与稽核题
│   ├── <track>/track.yaml     名称、顺序、语言、运行环境、前置线、阶段和单元名
│   ├── <track>/skills.yaml    本线技能、前置技能、知识卡
│   ├── <track>/lessons/       按技能编排的课
│   ├── python/、algo/         Python 基础（0A/0B）与算法（1–5），题在 <阶段>/<题目 id>/
│   ├── sql/                  SQL 题（含 MySQL 迁移练习）与 _db/ 下的共享练习库
│   ├── data/                 认识数据，看数据作答
│   └── math/、wrangle/、tensor/、ml/、train/、llm/   进阶线题库与配置
└── scripts/              题库校验；desktop/ 加密发布令牌、构建独立安装包（含 Linux AppImage）和含 SQL 期望表的更新包
```

## 桌面应用

桌面版 1.1.2 在同一个 Electron 窗口里完成解锁、进地图和做题。Linux x86-64 提供 AppImage 与备用 tar.gz，Apple Silicon macOS 提供 .app zip，Windows x64 提供便携 zip。安装包内有 Chromium、CPython 3.14、pip、锁定的后端依赖及启动器。Linux 的 AppImage 可以交给 AppImageLauncher Lite 集成到菜单，也可以使用 `--appimage-extract-and-run` 启动。AppImage 的 `AppRun` 是一个只用 shell 内建的包装脚本，一律带 `--no-sandbox` 启动 Electron。Ubuntu 23.10 起默认禁止普通程序建用户命名空间，AppImage 里的 `chrome-sandbox` 又不可能归 root，不带这个参数就会直接退出。网页仍然是 sandbox + contextIsolation 的隔离页面，冒烟测试确认这个参数还在。Windows 和 macOS 照常启用 Chromium 沙箱。[首次安装和令牌设置](../deploy/README.md#在一台新电脑上用)

Electron 主进程建好窗口后，同时载入随包启动页和启动 `python -m bootstrap serve --protocol jsonl`，之后通过标准输入输出驱动它。启动器依次查本机凭据、能读取两个仓库的 GitHub CLI 登录、包内加密令牌，最后提供手动填写。输入的密码与令牌经本地启动页和标准输入传递。连续输错五次需等待 30 秒。首次解锁后优先存入系统钥匙串，备用位置是受保护的本机文件。

协议使用 UTF-8，每行一个 JSON 对象。stdin 的 `command` 支持 `unlock`（`password`）、`set_tokens`（`code`、可选的 `sync`）、`sync`、`check_update` 和 `quit`。stdout 的 `type` 为 `status`、`need_unlock`、`need_tokens`、`unlock_failed`、`ready`、`sync` 或 `error`。`unlock_failed` 返回剩余次数 `remaining` 和等待秒数 `wait`。`ready` 返回 `port`、启动器 `version` 和 `payload_version`。

启动器从 `CODE_DOJO_REPO`（默认 `Rebas9512/code_dojo`）的 `payload-latest` Release 获取清单。更新包包含 FastAPI 代码及其预编译字节码、网页、固定题库、判题程序、技能识别规则和预先计算的 SQL 期望表。清单记录版本、提交 SHA、生成时间、最低启动器版本、题库格式版本和依赖锁 SHA-256。外部清单还记录整个 zip 的 SHA-256，它只用作这个更新包的 ID 和目录名，下载后不再计算哈希核对；依赖锁 SHA-256 同样只用作依赖目录名和与安装包的比较。

下载和解压均在用户数据目录的 `desktop/` 下完成。更新包的依赖锁和安装包的 `lock.sha256` 一致时，后端直接使用安装包里的 `libraries`，不复制。锁不一致时，内置 pip 按带哈希的运行时依赖清单安装到 `desktop/dependencies/<锁哈希>`；这时若又离线，旧更新包会缺依赖，联网更新一次即可。`.gitattributes` 让 `server/uv.lock` 在 Windows 检出时不转成 CRLF，否则两边的锁哈希对不上。已装过更新包时，启动器直接用 `current.json` 指向的版本起服务，同时在后台查更新，网络往返不挡启动。后台下载好的新版本记在 `desktop/next.json`，下次打开时先试它，起来了才原子替换 `current.json` 并保留上一个版本，起不来就回到原版本并提示。菜单里的“检查更新”仍是当场下载并换上新版本。断网、下载不完整或安装失败时仍可用原版本练习，后台查更新失败或启动器过旧时窗口弹出提示，后者附新版安装包链接。第一次使用需要联网下载题库，这次在启动页显示下载进度。

本机服务绑定 `127.0.0.1`，优先复用上次端口。启动器发出 `ready` 后，主窗口载入该端口的学习地图，原题等外链交给系统浏览器。网页运行在隔离的渲染进程中，通过 preload 提供的有限接口使用桌面功能。顶栏“桌面”可立即同步、打开设置或查看版本，原生菜单另有检查更新和退出。设置提供令牌更换和助教状态。再次启动会聚焦原窗口。关闭窗口先推送进度，最多等待 10 秒。记录使用与 `dojo` 相同的数据目录和事件格式。进度仓库由 `CODE_DOJO_SYNC_REPO` 指定，默认 `Rebas9512/code_dojo_sync`。有 Git 时使用 Git，没有 Git 时通过 GitHub Contents API 同步 main 上每台机器自己的月度 JSONL。同步失败的事件保留在本机。

普通 Python 题直接用随包解释器运行独立的 harness 子进程。数据科学题首次使用时在数据目录的 `judge-envs/` 创建专用环境并安装 NumPy、pandas 和 CPU 版 PyTorch。AppImage 启动时会将 `desktop/python-<解释器版本>` 链接到当前挂载的运行时，使同一 Python 版本的判题环境在重开后仍然可用。固定 SQL 题从更新包读取期望表，用户 SQL 和附加题的动态校验都在应用窗口内的 PGlite Worker 中运行。助教使用本机登录的 Claude Code 或 Codex，在做题页助教面板选择。桌面“设置”显示助教状态。只有 Codex 的机器需要含双助教探测的启动器；已发布的 1.1.2 启动器仍按 Claude Code 判断开关。

**发布**。推送到 main 后，`ci.yml` 在 Linux 上测试，通过才触发 `release-payload.yml`。仓库自 2026-11-23 起公开，标准机器的 Actions 不计费；推送时仍只跑 Linux，更新包发得快。三系统测试手动触发（`gh workflow run ci.yml`），改了判题、启动器或发版前跑一次。固定 Release 提供桌面更新，另保留最近五个带版本号的 `payload-v*` Release。需要回退时将目标版本的一对 `payload.zip` 和 `manifest.json` 依次覆盖固定 Release 的同名资产。修改启动器时同步更新 `bootstrap.VERSION` 和 `desktop/package.json` 中的版本与 npm 锁文件，发布对应的 `app-vX.Y.Z` 标签。`release-app.yml` 用 electron-builder 在三系统构建，在 Linux 上用 xvfb 和 Playwright 实际解锁、交卷并检查退出推送，全部成功后发布安装包。可选的 Actions 密钥 `CODE_DOJO_SEALED_TOKENS` 由发布者在本机加密后上传，打包时写入 `sealed-tokens.json`。本版更新包的最低启动器版本是 1.0.0。有不兼容更新时先发布新版安装包，再提高 `bootstrap.MIN_BOOTSTRAP` 并发布更新包。

## 怎么跑

**本地模式（默认）**。安装 Git、uv、Node.js 22.13 或更高版本（含 npm），用 `git clone <代码仓库地址> code-dojo` 下载项目，进入 `code-dojo` 目录。

- Linux、macOS 运行 `./dojo`，Windows PowerShell 运行 `.\dojo.ps1`。三个系统也可以用 `uv run dojo.py`。
- 启动器检查环境，在工作区干净时快进更新代码和题库，准备依赖、构建网页并打开浏览器。FastAPI 仅监听 `127.0.0.1:8765`，端口占用时自动换到空闲端口。可用 `CODE_DOJO_PORT` 指定首选端口。
- `./dojo doctor` 查看环境，`./dojo --no-pull` 跳过代码与题库更新。Claude Code 和 Codex 都是可选的。判题环境由 `CODE_DOJO_JUDGE` 选择，`local` 使用本机 Python。
- Linux 默认记录目录为 `~/.local/share/code-dojo`（支持 `XDG_DATA_HOME`），macOS 为 `~/Library/Application Support/code-dojo`，Windows 为 `%APPDATA%\code-dojo`。三个系统都可用 `CODE_DOJO_DATA` 覆盖。迁移时运行 `./dojo import-legacy <旧数据目录>`，从旧 `code_dojo.db` 的只读快照导入。
- 设置 `CODE_DOJO_SYNC_REPO` 后，启动、每次正式提交通过、每 10 分钟和 Ctrl+C 退出时交换学习记录。启动时的那次在后台进行，不挡服务就绪；网页打开后才完成的那次同步结束时，页面自动刷新一次数据。点网页右上角的同步时间可以立即同步。离线提交保存在本机，下次连接时重试。[本地模式和同步仓库怎么建](../deploy/README.md#本地模式和同步仓库怎么建)

**开发模式**。从项目根目录分别在两个终端运行后端和 Vite。

要固定使用本地判题，在后端终端先运行 `export CODE_DOJO_JUDGE=local`（Linux / macOS）或 `$env:CODE_DOJO_JUDGE = "local"`（Windows PowerShell）。首次运行代码时，uv 会安装或复用 CPython 3.14 并创建专用环境。固定使用镜像可把值设为 `docker`。[uv 安装指引](https://docs.astral.sh/uv/getting-started/installation/)

```bash
# 选用 Docker 判题时准备镜像
docker build -t code-dojo-judge-py:3.14 judge/python
docker build -t code-dojo-judge-ds:3.14 judge/ds

# 从项目根目录安装服务端 SQL 运行器依赖（Node 22.13+）
(cd scripts/curriculum && npm install)

# 2. 后端：http://127.0.0.1:8000
cd server && uv sync && uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# 3. 前端：http://127.0.0.1:5173（/api 转发到后端）
cd web && npm install && npm run dev

# 生产模式（从项目根目录执行；首次准备配置、输入两次密码）
test -e deploy/.env || install -m 600 deploy/.env.example deploy/.env
deploy/run.sh --set-password
deploy/run.sh --build                                   # 浏览器打开 http://127.0.0.1:8001
# 后续启动用 deploy/run.sh 复用已构建的前端

# 测试与校验
cd server && uv run pytest -q                          # API、Python 判题与 Node PGlite
cd server && uv run python ../scripts/verify_bank.py --judge local   # 可改用 --judge docker
cd server && uv run python ../scripts/curriculum/verify_sql.py       # SQL 题、方言迁移原稿报错和课示例
(cd web && node --experimental-strip-types --test tests/sql.test.mjs)
cd web && npm run build                                # 类型检查 + 打包
```
开发后端默认 `CODE_DOJO_AUTH=off`，记录保存在 `server/data/`。生产脚本启用登录，默认在用户的 Linux 数据目录保存个人记录，前端与 API 共用一个端口。后端测试使用独立数据目录和样例题库。[全部环境变量](../deploy/.env.example) · [部署步骤](../deploy/README.md)

## 代码结构
- `bootstrap/update.py` 管理不可变版本目录和活动版本指针。`protocol.py` 管理凭据、更新和后端生命周期。`desktop/main.cjs` 持有窗口、导航与菜单，`preload.cjs` 为启动页和练习页提供各自的接口。`service.py` 从选定更新包加载后端。`credentials.py` 选择凭据来源，`sealed.py` 与发布者的 `scripts/desktop/seal_tokens.py` 共用加解密格式。`scripts/desktop/build.py` 在发布机器上导出锁定依赖和预计算数据。安装包里的解释器、依赖和启动器统一编译成不查源码的哈希式 `.pyc`（electron-builder 复制时会改文件修改时间，按时间戳校验的 `.pyc` 会全部失效、每次启动都重新编译），更新包也附带 `server/app` 的同类 `.pyc`。Linux 发布构建在 Ubuntu 22.04 上运行，校验 appimagetool 和 Type 2 运行时的 SHA-256，用系统的 `squashfs-tools` 生成 AppImageLauncher Lite 2.2 可读的 gzip 镜像。桌面图标和网页 favicon 共用 `web/public/code-dojo.svg` 的图形。
- `server/app/github_sync.py` 通过 Contents API 读写与 Git 后端兼容的 JSONL。`desktop_sql.py` 将动态 SQL 验证交给网页，网页与 Node 共用 `web/src/sql/validate.ts`。
- `server/app/events.py` 给学习记录分配跨机器标识、导出按月分隔的 JSONL。写记录和登记待导出的事件共用一个 SQLite 事务。`sync.py` 管理独立 Git 克隆、重试和定时同步。`GET /api/sync` 返回状态，`POST /api/sync` 立即交换进度，外部页面顶栏和做题页状态栏共用 `web/src/components/SyncStatus.tsx`。
- `server/app/auth.py` 管理密码校验、登录限流和签名会话，`server/scripts/set_password.py` 交互设密。`web/src/pages/LoginPage.tsx` 提供登录页，`web/src/api.ts` 统一处理 401。`server/app/frontend.py` 托管静态文件并支持直接打开前端路由。
- 首页的 `pages/MapPage.tsx` 用 `pages/mapTree.ts` 组装学习线树，样式在 `pages/map.css`。`server/app/units.py` 按本阶段技能分组归题，供地图和题目列表共用。
- `server/app/mastery.py` 根据正式提交和复习日程计算技能状态、下一题、卡住提示和周统计。`main.learning()` 按题库版本、数据库写入次数（`Store.version`）和日期缓存这份进度，没有新提交时各接口直接复用。`db.py` 以 SQLite 事务保存提交与复习日程，并记录提示、题解和每日上限。启动时升级旧表，首次读取学习进度时按历史通过日期补排到期日。
- `pages/PlanPages.tsx` 提供 `/today` 今日计划和 `/stats` 手感统计，对应 `GET /api/today`、`GET /api/stats`。页面通过 `PUT /api/today/settings` 保存每日上限。复习链接携带原题与到期日，运行和提交分别向已有接口传 `review_source`、`review_due`。过期或重复交卷返回 409，可回到今日计划取当前题目。统计展示最近八个周一开始的自然周，日期按服务器本地时间划分。
- `server/app/result_preview.py` 在判题结束后生成摘要。样例的单个输入、期望、实际等字段超过约 2 KB 时保存前缀和总字符数，隐藏用例使用更短的预览。SQLite 保存这份摘要。SQL 的即时结果面板使用 Worker 的表格预览，Python 和数据题显示服务器返回的摘要。
- `judge/python/harness.py` 在工作目录读 `job.json`，逐个执行用例，以 `@@CODE_DOJO_RESULT@@` 前缀输出一行 JSON。checker 需要检查学生源码时，从当前工作目录读取 UTF-8 的 `user.py`。工作线程使用 256 MiB 栈和 20 万层递归上限。主线程负责计时，超时后保留已完成的用例，把剩余用例标为跳过。
- `server/app/judge.py` 选择判题后端，`local_judge.py` 用 uv 准备专用解释器并管理子进程。题库、课和技能索引由 `tracks.py` 和 `problems.py` 加载，文件修改后自动重载。YAML 用 libyaml（`yaml.CSafeLoader`）解析，各题的 `tests.json`（全题库约 46 MB）在第一次判题或打开题目时才读。桌面版 `CODE_DOJO_BANK_WATCH=off`，启动时只加载一次，不扫修改时间。服务就绪前在 `lifespan` 里载入题库并算好学习进度。`db.py` 保存提交和 AI 对话，`main.py` 提供相应 API。
- `server/app/sql_judge.py` 展开 SQL 数据集、缓存期望表并调用 `sql_runner.mjs`。开发后端和 `scripts/verify_bank.py` 使用这个 Node 入口，内容侧 `verify_sql.py` 通过 `pglite_runner.mjs` 批量验题。两个入口共用 `server/app/validate_sql.mjs` 校验 MySQL 原稿、修改题与脚本题。浏览器的入口在 `web/src/sql/client.ts` 和 `worker.ts`，两个环境共用 `engine.ts` 和 `compare.ts`。
- `server/app/inspect_data.py` 是题库加载、内容检查和 AI 附加题共用的数据块与答案校验。前端 `components/InspectData.tsx` 显示五种题面数据和课里的 CSV 编辑视图。
- `server/app/ai/provider.py` 探测本机命令，通过 `claude -p` 和 `codex exec` 使用个人订阅，测试用 `FakeProvider`。`codex_schema.py` 转换严格输出格式并还原可选字段和误解映射。`tutor.py` 组装题面、参考解、带行号的当前代码、最近一次判题和对话历史，并检查修改建议的位置。
- `web/src/pages/` 的学习地图、题目列表、知识点、今日计划、统计和登录页共用深浅两套 VS Code Modern 色板。界面使用本地 TeX Gyre Heros 和按需加载的 Noto Sans SC 分片，代码和数值使用 JetBrains Mono。字体和图标的署名及许可证随前端发布到 `/licenses/`。
- 做题页（带 Monaco）和知识点页（带 Markdown）单独打包，首页的包里没有它们。首页画好后，`App.tsx` 趁浏览器空闲预先载入做题页和 Monaco，第一次点开题目不用再等编辑器初始化。`pages/ProblemPage.tsx` 打开做题工作区。`api.ts` 给题目详情、学习线题目列表和今日计划留 60 秒读缓存，任何写请求完成后全部作废；判题状态一个页面会话只读一次。做题页提前取好上一题、下一题、继续和单元列表里悬停的题，切题时路由不等网络。路由等数据超过 120ms 时顶边出现一条蓝线。`components/WorkbenchLayout.tsx` 管理本单元题目列表、分隔线和布局偏好。`ProblemWorkspace.tsx` 在两个编辑器组中显示题面、课、附加题和作答区；每题独立保存草稿。`LessonView.tsx` 显示讲解、可运行的示例和小测。`ChatPanel.tsx` 提供共享编辑框和快捷提问。宽度小于 900px 时，编辑器组上下排列，题目列表和助教从两侧呼出。
- 每道题都有草稿，按题保存在当前浏览器。点文件标签或按 Alt+S 可在答案与草稿之间切换。在草稿中按 Ctrl+Enter 只看运行输出，不记作答。普通 SQL 题的 `scratch.sql` 使用本题首个样例库，SQL 看数据题使用书店练习库。其余题的 `scratch.py` 运行 Python。Ctrl+Shift+Enter 始终提交答案。
- `WorkbenchPanel.tsx` 的测试结果页使用 `ResultPanel.tsx` 展示用例和结果表，输出页显示用例 stdout 和最近运行的草稿或课示例，问题页的源代码行可跳回答案编辑器。运行和提交会展开面板。22px 状态栏显示行列、用时、判题方式、同步状态和上下题，桌面菜单位于最右。布局尺寸和开关由浏览器保存。
- 导航与接口：`/` 展示地图，`/t/:track` 展示题目，`/t/:track/skills` 展示知识点，`/p/:id` 是做题页，旧地址 `/sql` 跳转到 `/t/sql`。根路由共享 `GET /api/tracks` 的名称、阶段、题量、下一题和前置完成状态，提交后刷新进度。`GET /api/tracks/{track}/skills` 返回技能卡、带所属线的前置、课和引入它的题，`used_by` 统计全题库中只用到它的题数。
- Ctrl+P 在各页按题名、题号或 LeetCode slug 快速打开题目；受保护的题库需要先登录。做题页 Ctrl+Shift+P 打开命令面板。Ctrl+B 开关单元列表，Ctrl+J 开关底部面板，Ctrl+Alt+I 或 Alt+I 开关助教。Ctrl+Enter 运行，Ctrl+Shift+Enter 提交；看数据作答还支持数字 1–9 选项和 Ctrl+Enter 提交。Alt+L 切换课，Alt+B 切换裸写。状态栏箭头按题库顺序切题；Alt+← 返回上一题，Alt+→ 继续推荐练习。
- 列表状态：● 绿 = 有一次通过时未应用 AI 修改、● 黄 = 仅有 AI 协助通过、◐ = 提交过没通过。知识点页另列技能状态、独立写对题数和最近使用时间；技能接口对应字段为 `state`、`counted_solves`、`last_used`。
- 课相关接口：`/api/problems/{id}/lesson`（这道题的课：按技能拼出的教学内容）、`/api/playground/run`（运行 Python 示例，只看输出）。SQL 示例随课取得共享库及补丁，在做题页的 Worker 中执行并显示结果表。助教的上下文里也带着这道题的课。
- 附加题（2026-11-22）：左栏标签"题目 | 课 | 附加题 1 | 附加题 2 … | ＋"。点"＋"或在助教里说"再来一道 / 换个场景 / 难一点"，后台由 `server/app/ai/extra.py` 出题。inspect 附加题验证内联数据和答案，SQL 附加题用 PGlite 验证，桌面端在浏览器运行，开发模式在服务端运行。Python 附加题在判题沙箱验证（参考解全过、典型错误写法和挖空 / 带 bug 的初始代码都被测试抓住，不过就带着问题重出，最多 3 次），出好自动切过去；实测 13–19 秒。助教也能按编号删附加题（`delete_extras`），用户在标签上点两下 × 删除。附加题存在 SQLite（`extra_problems` 表，编号删了不复用），id 形如 `x-12`，判题、课、共享编辑框都和原题一样用；原题和附加题共用一段助教对话，助教知道当前在看哪一道。接口：`GET/POST /api/problems/{id}/extras`、`DELETE /api/problems/{id}/extras/{seq}`。已知不足："只用原题的技能"目前只是提示词约束，以后可以把 check_curve 的 AST 技能检测接进验证。开发时 `CODE_DOJO_API=http://127.0.0.1:8001 npx vite --port 5174` 可以让前端指向另一个后端（比如用样例题库起的测试实例）。

## 设计

### 1. 核心原则：练"手写"，不是刷数量
- AI 默认不替你写代码；只有逐级点到"完整题解"才给，而且看过题解的题自动进重写队列、本次不算掌握。
- 掌握一个技能需要独立写对两道不同的计入题。作者提示、助教提示、应用过 AI 修改、看完整题解都会影响本轮独立资格。普通练习看第一次正式提交，次日从空白重写可以重新取得资格。
- 从今日计划或“继续”进入复习，编辑器使用 starter，答案框留空。间隔为 1、3、7、21、60 天，之后每 60 天再练。第二轮起换同套路的新题，题库不足时可以在原题下生成一道。复习失败隔天再练。看题解或 AI 协助通过也安排次日重写。
- 手感按普通提交统计。首次通过率取每道非预测题的第一次交卷；语法错误按出错提交计次；用时取各题首次通过的 `elapsed_ms` 周平均；提示按各题交卷时新增的条数累计；AI 协助比例为通过提交中应用过 AI 修改的比例。复习记录单列为 `kind=review`。

### 2. 学习路线和学习曲线
从“认识数据”进入 Python 或 SQL。根线的平台和阶段配置已就位，正式题和课待编写，测试题库提供单选、短答案和交互课实例。Python 基础完成后可进入算法与数据结构，后者以 NeetCode 250 为骨架。SQL 以 SQL 50 为骨架（依据见 docs/reports/）。

**Python 基础（0A/0B）**

| 阶段 | 内容 | 题源 |
| --- | --- | --- |
| 0A 语法基础 | ① 变量、整除/取余、f-string ② 条件和布尔逻辑 ③ for/range、while、break/continue、累加/计数/求最值 ④ 字符串：下标、切片、常用方法、ord/chr ⑤ 列表：下标、append/pop、切片、嵌套、enumerate、原地修改 ⑥ 函数：参数、返回值、提前 return、辅助函数 ⑦ 字典和集合：查找、计数、分组 ⑧ 元组、排序（key / lambda）、推导式 ⑨ 类：`__init__`、方法、节点类 ⑩ 简单递归 | 自编，约 100 道短题 |
| 0B 算法入门 | 线性查找、最值、计数、反转与交换、双下标、前缀和、模拟、矩阵遍历、用列表当栈/队列、复杂度直觉（亲手计时 O(n) 和 O(n²)） | 自编约 40 道 + LeetCode 75 的简单题 |

**算法与数据结构（1–5）**

| 阶段 | 内容 | 题源 |
| --- | --- | --- |
| 1 基础数据结构 | 数组与哈希、栈、链表 | NeetCode 250（50）+ 阶梯题 |
| 2 核心套路 | 双指针、滑动窗口、二分、前缀和、排序、数学、位运算 | NeetCode 250（59）+ 阶梯题 |
| 3 树和图 | 树、堆、回溯、图（含并查集） | NeetCode 250（73）+ 阶梯题 |
| 4 进阶 | 字典树、高级图论、一维/二维 DP、贪心、区间 | NeetCode 250（68）+ 阶梯题 |
| 5 面试混合 | 各类混排、设计类、公司签名题、多级递进题 | Grind 169 / Top Interview 150 多出的 84 道 + 自编 |

Blind 75 / NeetCode 150 / 热题 100 作为里程碑标记；热题 100 里不在 NeetCode 250 的 17 道补进对应阶段。

**SQL**
| 阶段 | 内容 | 题源 |
| --- | --- | --- |
| 0 单表查询 | SELECT、别名、WHERE（比较 / AND / OR / IN / BETWEEN / LIKE）、NULL（IS NULL、COALESCE）、ORDER BY、LIMIT、DISTINCT、CASE、基础字符串和日期函数 | 自编阶梯题 + SQL 50 |
| 1 聚合 | COUNT / SUM / AVG、GROUP BY、HAVING、条件聚合 | 自编阶梯题 + SQL 50 |
| 2 连接 | INNER → LEFT → 反连接 → 自连接 → 多表 | 自编阶梯题 + SQL 50 |
| 3 子查询和 CTE | 标量 → IN → 相关子查询 → EXISTS → WITH | 自编阶梯题 + SQL 50 |
| 4 窗口函数 | ROW_NUMBER → PARTITION BY → RANK / DENSE_RANK → 分组 Top 1 → Top N → LAG / LEAD → 累计和 → 连续区间 | 自编为主 + SQL 50 的 7 道 + 免费题 177、178、184、601 |
| 5 综合 | 留存、漏斗、连续登录、中位数、行列转换 | 自编 + AI 出题 |

SQL 题按"用到的最高概念"归阶段，不照搬 SQL 50 的分节。阶段 0–3 的入门题用一个固定的练习数据库（虚构的网上书店：用户、图书、订单、评分），新表按需逐个引入，不用每题重新读一套表结构；到 SQL 50 的题再换成各自的表。

**让曲线平滑的机制（提议）**
1. **技能图**：把内容拆成原子技能（Python 基础 67 个、算法与数据结构 48 个、SQL 56 个），每个技能写明前置技能，例：`dict-counting` 前置 `for-loop`、`dict-basics`。存成 `problems/<track>/skills.yaml`，每个技能配一张知识卡。
2. **每道题标注**：需要的技能、新引入的技能（**最多 1 个**）、题型、细分难度（1–100，比 Easy/Medium/Hard 细）。
3. **平滑性检查**（scripts/，改题库就跑）：按学习顺序走一遍，任何一题用到还没引入的技能、或一次引入超过 1 个新技能，就报错。标注自动核对：Python 参考解用 AST 识别用到的语法和库（字典、推导式、递归、类、切片、heapq 等），SQL 参考解解析出 JOIN、子查询、CTE、窗口函数等，和标注对不上就报错。回退按钮生成的前置小题复用这套识别表校验技能范围。
4. **每个技能内部的阶梯**（参考教学法 PRIMM：预测 → 运行 → 探究 → 修改 → 编写）：读代码预测输出 → 补全代码 → 改错 → 独立写 → 变式 → 和旧技能组合。前几级是一两分钟的热身；会做的题可从列表直接进入。
5. **阶梯题**：骨架题单里每个新套路前放 1–3 道阶梯题。例：Two Sum 之前依次是"判断列表里有没有某个数"→"统计每个数出现几次"→"记录每个值的下标"→"双重循环找两数之和"→ Two Sum（哈希一次遍历），每步只多一个新点。
6. **自适应节奏**：
   - 技能状态：未学 → 学习中 → 掌握 → 需复习。掌握 = 不看提示独立写对 2 道不同的题。
   - 推荐新题要求用到的技能已经学过。引入新技能时，同线直接前置需掌握，跨线前置需已学。全站有三个技能在学习中时，优先做能推进它们的计入题。
   - 最近十道首次提交通过率低于 70%，或同一技能连续两道计入题首次失败时，题面提供前置小题与按需出题的入口。
   - 按零基础设计（用户 2026-11-22 定）：每道题先给题，会做直接做；不会再切到"课"。已经会的部分用户自己跳过。
7. **卡住时回退**：从焦点技能的直接前置中选择针对性小题，由学习者决定是否回退或请助教出题。具体计分和排期规则见 [课程设计第 3 节](curriculum.md#3-掌握规则与节奏)。

### 2b. 按 track 整理知识点，进阶模块
用户原话："数据科学类的 数据操作，模型训练，tensor操作，手搓大语言模型……模型训练的内容可以只做训练脚本的检查或者模拟训练"；"可以把知识点按不同的track去做整理"。

**Track 地图**（箭头 = 前置 track；一个 track 内部仍是 阶段 → 技能 → 题 + 课）
```
认识数据（data）
├─ Python 基础 ┬─ 算法与数据结构
│              ├─ 数学（用代码学）──┐
│              └─ 数据处理（wrangle）┴─ 张量与 PyTorch ─ 机器学习手写 ─ 训练 ─ 手搓 LLM
└─ SQL ┬─ 产品分析 SQL
       └─ 建模与写数据
```

机器学习手写还直接以数学为前置。数据处理线用 `sql_twin` 关联 SQL 题，便于对照练习同一查询的 pandas 和 SQL 写法。

| track | 知识点（按顺序） | 判题环境 | 参考来源（题面全部自己写） |
| --- | --- | --- | --- |
| 认识数据（`data`） | 表、值的种类、缺失、形状、CSV 与 JSON | 服务端核对单选或短答案 | 自编 |
| Python 基础 | 0A / 0B | Python 沙箱 | 自编 |
| 算法与数据结构 | 现在的阶段 1–5（NeetCode 250 + 面试混合） | Python 沙箱 | NeetCode 250 |
| SQL | 现在的阶段 0–5 | 浏览器 PGlite | SQL 50 + 自编 |
| 产品分析 SQL（`analytics`） | 产品指标、留存、实验分析 | 浏览器 PGlite | 自编 |
| 建模与写数据（`modeling`） | 建表、约束、写入、增量载入、维度建模、质量检查、履约和会员面试 | 浏览器 PGlite / 看数据作答 | 自编 |
| 数学（用代码学） | 向量和点积、矩阵乘法、函数和图像、导数（数值求导）、链式法则、梯度、指数和对数、概率和期望、均值和方差、softmax | Python 沙箱 | 自编 |
| 数据处理（`wrangle`） | NumPy：数组、形状、下标和切片、布尔掩码、广播、向量化（不许写循环）、聚合和 axis → pandas：Series / DataFrame、筛选、排序、缺失值、groupby、merge、pivot、时间列、pandas 版 SQL 题 | 数据科学沙箱 | numpy-100（MIT）、LeetCode Introduction to Pandas / 30 Days of Pandas（只参考题目）、自编 |
| 张量与 PyTorch | 张量和 dtype、view / reshape / permute、广播、索引 / gather / 掩码、einsum、autograd 基础、nn.Module | 数据科学沙箱 | Tensor Puzzles（MIT）、TorchLeet（MIT） |
| 机器学习手写 | 线性回归（梯度下降）、逻辑回归、softmax 回归、kNN、k-means、决策树、评估指标（精确率 / 召回 / AUC）、交叉验证、手写自动求导（micrograd 式）、MLP 反向传播 | 数据科学沙箱 | 自编；Deep-ML 只参考题目名（许可只限教育用途） |
| 训练 | Dataset / DataLoader、训练循环、train / eval 和 no_grad、优化器和学习率、正则化、保存和加载、读 loss 曲线、训练脚本改错 | 数据科学沙箱（模拟训练） | 自编 |
| 手搓 LLM | 字符级分词 → BPE、embedding 和位置编码、注意力（单头 → 因果掩码 → 多头）、LayerNorm 和残差、Transformer 块、GPT 前向、采样（temperature / top-k）、KV cache、小模型训几十步 | 数据科学沙箱 | 自编；参考 nanoGPT / minbpe（MIT）、LLMs-from-scratch（Apache-2.0） |

**怎么整理**
- 每条线的 `problems/<track>/track.yaml` 定义名称、顺序、语言、判题环境、阶段和前置线。新增阶段只需修改该配置。数学使用 Python 沙箱，另五条进阶线使用数据科学沙箱。
- 技能按线保存、全局检索。例如 `algo.hash-seen` 使用 `py.set-basics` 的知识卡。曲线检查按前置线的拓扑顺序进行，直接和间接前置线的技能都算已学。
- 首页有 Python 和 SQL 两个标签。URL 的 `tab` 优先于浏览器保存的标签，首次打开选 Python。两页共用无语言的根线，按配置顺序排列兄弟线，第一条前置决定缩进，其余前置列在行首。SQL 页也可跳到数据处理线。
- 顶栏“继续”选择当前标签下最近运行或提交过的开放学习线（附加题算在原题线上），没有练习记录时选第一条根线。线上还没有提交过原题时从首道必修题开始，否则按地图顺序找到最靠后提交过的原题，先从它后面找本单元未做的必修题，再从单元开头补漏，最后依次找后续单元，找不到时隐藏按钮。
- 每条线按阶段横排单元，宽屏空间不足时在阶段之间换行。圆点上的绿色弧长表示通过比例，全部通过后填实；角上的小点表示含 AI 协助通过。当前标签的推荐单元带外圈，优先标记有到期复习的单元。学习线与单元详情均列出掌握数。点击或回车查看详情，左右键沿单元移动，上下键切线。窄屏可以横滑单条线，仍有隐藏单元的一侧显示渐隐提示，详情在树下方。
- `GET /api/tracks` 的每个阶段返回 `units`。每个单元包含题量、进度、技能和下一题。技能的小点取引入该技能的题目里最好的提交状态。题目列表的 `unit` 字段与地图共用归属。阶段内含 `week` 时按周列题，算法阶段 5 的 76 道周练按十周排列，其余 3 道在“未分周”中。没有周次的阶段沿用单元分组。题目列表和知识点页均支持 `#u-<阶段>-<单元>` 定位，包括空单元。展开知识点可读知识卡、打开引入该技能的题。

**数据科学题怎么判（M6）**

- 运行、提交、课里的 Python 示例和附加题验证都按题目的 `runtime` 选择环境。DS 环境包含 NumPy 2.5.5、pandas 3.1.1 和 CPU 版 PyTorch 2.15.0，数值库按单线程运行。默认内存预算 1 GiB，每个用例 10 秒。镜像名、内存和用例时限可分别用 `CODE_DOJO_DS_IMAGE`、`CODE_DOJO_DS_MEMORY`、`CODE_DOJO_DS_TIME_LIMIT_MS` 设置。
- 数组和张量用 `allclose`，依次比形状、整数 / 浮点 / 布尔类别和逐元素容差。表和 Series 用 `frame`，可放宽行序、索引和列名。失败用例显示第一处差异。形状预测沿用 `predict`，在 DS 环境运行展示程序后与学生填写的输出比对。
- 题目可声明 `no_loops`、`forbid_imports`、`forbid_calls`。提交时先做 AST 检查，命中就显示“写法不符”、行号和原因。
- checker 可以拿到学生函数，在同一组输入上与参考实现对拍。手写反向题用 `check_grad` 将学生的梯度逐项与中心差分核对。训练改错题使用 `simulate_train` 在固定种子的小批次上执行训练，记录实际反向传播的 loss，检查清梯度顺序、步数、评估模式、梯度开关和验证集使用。checker 可检查首尾 loss 均值、单批次拟合和逐步轨迹。
- `server/tests/fixtures/problems/dsfix/` 提供七道可实跑的夹具和一节可运行的 NumPy 示例课。题目字段和 checker 接口见[题目格式规范](problem-format.md#数据科学比较和写法约束)。

单核可行性实测（2026-11-22，同版本 CPU 依赖）：
  - 镜像 1.63 GB（压缩后 349 MB）；起容器并 `import torch` 共约 1.3 秒，三个库导入合计 0.9 秒。
  - 3 层 MLP 回归训 300 步 0.5 秒；2 层字符级 GPT（10.6 万参数，上下文 64，批 16）训 100 步 0.9 秒，loss 2.74 → 0.09；整次运行约 3 秒，峰值内存 393 MB，512 MB 限额够用。
  - 同种子两次运行 loss 完全一致，"和参考实现对拍 loss 轨迹"可行。

### 3. 题库
- **固定题库**：题目是仓库里的文件，版本固定、循序渐进。开发时由 Claude Code 编写，每道题都用 `scripts/` 的校验跑过参考解和测试才入库。
- **标准题单**（调研建议，待确认；详见 `docs/reports/2026 技术面试 高频题单 调研.md`）：算法与数据结构用 NeetCode 250 做骨架，Blind 75 / NC150 / 热题 100 做里程碑，另加"面试混合"阶段；SQL 用 SQL 50 按题目用到的最高概念重排，窗口函数和综合阶段靠自写和 AI 出题。只存题号、slug、套路标签、原题链接（leetcode.com），题面和测试用自己的话重写，不搬运原题面（版权）。各题单成员数据在 `docs/research_notes/2026 技术面试 高频题单 调研/lists.json`（2026-11-22 一次性快照）。
- **公司标签**：独立的私有元数据表（公司、时间窗口、名次、快照日期），不写进题目文件；数据来自公开 GitHub 数据集，无许可证、LeetCode 条款禁止爬取，所以只私用、不自己爬。
- **我的题**：AI 当场出的题存这里，标 `ai`；觉得好可以提升进固定题库。

### 4. Python 用 Docker 或本地解释器判题，SQL 在浏览器中判题

- **Python 使用原生 CPython 3.14**。后端启动时读取 `CODE_DOJO_JUDGE`。默认 `auto` 分别检查普通和 DS 镜像，可用的镜像走 Docker，其余 runtime 走本地。`local` 和 `docker` 固定后端。`GET /api/status` 的 `judge_backends` 给出两种 runtime 的实际选择，`judge_mode` 给出普通 Python 的选择。
  - **Docker** 每次提交起一个临时容器，断网、只读、非 root，限制 1 核、64 个进程和内存（普通题 256 MiB，DS 题默认 1 GiB）。部署时需要容器隔离，可固定设置 `CODE_DOJO_JUDGE=docker`。
  - **本地** 适合运行自己的练习代码。每次提交用专用解释器的 `-I` 模式，在临时工作目录中执行。代码拥有当前系统用户的文件和网络访问权限。Linux 用 `RLIMIT_AS` 限制进程虚拟地址空间，为线程栈另外预留 256 MiB。macOS 和 Windows 仅限制时间。两种后端的总时限都是「每例时限 × 用例数（至少 1）+ 8 秒」，准备本地环境的时间另计。
  - 环境保存在 `<数据目录>/judge-envs/`，可用 `CODE_DOJO_JUDGE_ENVS` 更换位置。普通环境只有标准库，第一次运行 DS 题或课示例时才安装 DS 环境。页面在实际安装期间显示提示。安装失败会返回中文原因，下次运行可重试。
  - 函数模式：题目声明入口函数和参数类型；测试是 JSON（`args` / `expected`）；平台调用函数并比对。比对方式：`exact` / `unordered` / `float(1e-6)` / 题目自带 checker（多解题）。
  - 链表、二叉树按 LeetCode 的数组格式自动转换。
  - 阶段 0 也支持"读输入、打印输出"模式。
  - 报错：traceback 行号对回用户代码。
- **SQL（PGlite = 浏览器里的 PostgreSQL，Web Worker）**
  - SQL 做题页按需加载一个 Worker 和内存数据库。每份答案在独立事务里建表、填数据，执行后回滚。查询题允许单条只读 SELECT 或 WITH 查询。修改题允许单条 DELETE、UPDATE 或 INSERT（可带 WITH），执行后用题目指定的只读 `check_query` 读取最终状态。脚本题执行整段 DDL、DML 后依次检查。课示例可执行多条语句，显示末条语句的结果。执行时限为 2 秒。
  - `GET /api/problems/{id}/sql-cases?scope=sample|all` 返回建表脚本、期望列名、类型和行，修改题另返回 `mode: dml` 和 `check_query`。桌面端优先读取随版本发布的期望表，动态数据集由浏览器校验。开发服务器用 Node PGlite 跑参考解，在 `CODE_DOJO_DATA/sql-cache/` 按内容的 SHA-256 缓存。修改题的缓存键含模式、检查查询、排序要求、参考解和数据脚本。脚本题返回 checks 和各项期望，缓存键包含整份检查定义。固定题的参考解留在服务器。个人站点允许提交时将隐藏数据集的建表与数据脚本、期望结果发到浏览器。
  - 脚本题的每一项 query 与参考脚本生成的结果表比对，每个 probe 验证一次试写应成功或失败。逐项使用保存点并撤销，最后回滚整个数据集。脚本内的事务控制命令会得到中文提示。结果面板逐项显示标签和判定，失败项展开两侧结果和数据库错误。固定脚本题与脚本附加题均要求所有参考检查通过，且每份典型错误写法在至少一个数据集上判错。
  - 修改题在结果面板并排显示“修改后的表”和“期望的表”，按数据集显示影响行数。行数不同时，较大表的预览中会标出缺失或多出的行。当前作答可切换查看各数据集的表格，历史记录保存紧凑摘要。
  - 固定修改题与 SQL 附加题共用验证规则。参考解必须在每个数据集上改变检查查询的结果，每段典型错误写法至少要在一个隐藏数据集上产生错误的最终状态。
  - SQL 主线有五道 MySQL 迁移题。学习者先运行编辑器中的原稿，在“测试结果”查看 PostgreSQL 报错，再改写并用样例核对查询结果。`starter_dialect: mysql` 要求原稿在可见样例上报错，普通改错查询的原稿须在样例上显示错误结果。
  - 运行只比样例，提交比较全部数据集。比较列数、行数和单元格值，数字用相对和绝对容差 1e-6，NULL 等于 NULL，日期按 ISO 文本比较。只在 ordered 题比较行序，列名供显示。结果表各显示前 50 行，并指出首处差异。
  - 浏览器通过原有 `/run` 和 `/submit` 上报代码、判定、各数据集的结果摘要和 AI 写入行数。单用户模式信任浏览器判定，正式提交计入地图进度。

**实测：浏览器和本机的差别（2026-11-22，Chrome 152 Web Worker / Node 22 / 本机 CPython 3.14）**
- SQL：PGlite 就是 PostgreSQL 18.7，结果和服务器版一样。默认排序规则是 C（大写排在小写前）、时区 UTC；判题时参考解和用户查询都在 PGlite 上跑，不影响对错。
- Python：结果一致，但有三处差别：
  - 慢 1.3–3 倍（BFS 700×700：268 vs 88 ms）。
  - 经过 C 层的递归很浅，而且是整个 Worker 卡死，不报 RecursionError：`@cache` 约 700 层卡死，生成器里递归（`max(dfs(c) for c in ...)`）约 3000 层卡死；本机都能到 10000。普通递归、方法递归、手写 dict 记忆化没有这个问题。
  - 没有线程。
- 结论（2026-11-22 用户同意）：**Python 改到服务器上原生跑**（Docker：断网、限内存/CPU/进程数、超时），因为 `@cache` 自顶向下 DP 正是面试里最常用的写法，浏览器里会无故卡死；后端本来就要跑 AI，服务器反正要在线。**SQL 留在浏览器里跑**，没有差别，反馈更快。

看数据作答由服务器直接核对。单选提交下标，短答案按题目规则规范化。两种都返回对错与解释，命中具名误解时显示针对性反馈。和代码题一样，正式提交计入进度。助教能看到题目数据、当前回答和只供判断的正确答案。单选只对话，短答案可以共享编辑。

Python 基础和算法题共用 Python 判题格式，SQL 题使用各自目录下的数据集。可对照以下真实文件阅读。

- Python 基础第一道预测题展示一段程序，请学习者写出输出。[第一行输出](../problems/python/0A/py-0a-001-hello-print/problem.yaml)
- 算法线的测试夹具声明链表输入和输出，由判题器转换。[反转链表](../server/tests/fixtures/problems/algo/1/algo-1-001-reverse-list/problem.yaml)
- SQL 起步题使用书店数据集，题目描述中列出样例，隐藏数据用于校验。[补全用户姓名和邮箱](../problems/sql/0/sql-0-101-complete-user-emails/problem.yaml)

### 5. AI
- **订阅和命令**。先登录 Claude Code（Claude Max）或用 ChatGPT 登录 Codex。后端从 PATH 找 `CODE_DOJO_CLAUDE_BIN`（默认 `claude`）和 `CODE_DOJO_CODEX_BIN`（默认 `codex`），也可填可执行文件的绝对路径。找不到 Codex 时，从 `~/.vscode/extensions/openai.chatgpt-*/bin/` 选含本平台可执行文件的最高数字版本。Linux x64、Apple Silicon 和 Windows x64 分别使用 `linux-x86_64/codex`、`macos-aarch64/codex` 和 `windows-x86_64/codex.exe`。
- **默认助教**。`CODE_DOJO_AI_PROVIDER` 可设为 `claude`（默认）或 `codex`，缺少首选命令时使用另一个。`off` 关闭全部助教。Claude 模型由 `CODE_DOJO_AI_MODEL` 指定（默认 `claude-opus-5-5`），Codex 模型由 `CODE_DOJO_CODEX_MODEL` 指定（默认 `gpt-6.2-astra`）。`GET /api/status` 每次探测命令，返回默认助教、模型和默认项排在首位的 `ai_agents`。
- **切换和历史**。助教顶部列出本机可用的助教和模型，浏览器记住选择。聊天、左栏「＋」和复习出题都使用所选助教。后台出题沿用发起时的选择。每条助教回复下方显示来源，同一道题的历史会传给接手的助教。
- **调用**。两种助教共用 `complete(system, prompt, schema, effort)` 和两个并发槽。Claude 通过 `claude -p --json-schema` 返回 `structured_output`。Codex 在空工作目录以只读沙箱运行 `codex exec --ephemeral --output-schema`，通过 `developer_instructions` 接收教学设定，stdin 接收本轮内容，最后一条 JSON 回复从临时文件读取。聊天默认 `low`，由 `CODE_DOJO_AI_EFFORT` 调整，附加题使用 `medium`。

**已实现（2026-11-22）：助教聊天 + 共享编辑框**
- 做题页右侧是助教面板（Ctrl+Alt+I 或 Alt+I 开关）。快捷提问包括「讲讲思路」「我卡住了」「帮我补一下」，判题没过时还可以问「这个错误是什么意思」。
- SQL 助教还会看到样例库各表的列名、类型和前三行，以及学生的查询、最近的差异或 PostgreSQL 报错。
- 助教看得到：题面、样例、本题技能、参考解（只供判断）、带行号的当前代码、最近一次运行结果、本题对话历史、已应用过几次修改。
- 共享编辑框（用户 2026-11-22 决定，替代了最初的"建议 + 点应用"）：助教看得到编辑框里的当前内容，它给的修改（`edits`：若干处 `old` → `new` + 一句理由，按顺序生效）直接写进编辑框，可以 Ctrl+Z 撤销；AI 写入的行有淡底色和左侧细线，聊天里折叠显示改了哪几处。`old` 为空表示接在末尾追加。预测输出题没有代码，编辑框里是用户写的预测输出。
- 教学约束全部是**提示词软约束**（用户 2026-11-22 决定）：默认只讲思路，学生要求或提示过仍卡住才给修改；尽量只补卡住的一小块，不一次写完；不整段透露参考解；以判题结果为准。代码里只检查修改建议能不能在当前代码里唯一定位，定位不了就让 AI 重来一次，再不行只保留文字。
- 掌握度：代码里应用过 AI 修改时，提交带 `ai_lines`，通过记为"AI 协助"，不算独立通过。

**当场出题**。左栏的「＋」和助教对话都能生成附加题。SQL 出题包含中文题面、表名、参考查询、1–2 个典型错误查询、初始代码和各自可建库的脚本。第一个数据集为样例，至少另有两个隐藏数据集。服务端逐库验证参考结果非空、排序题有 ORDER BY、每个错误查询能运行且至少在一个隐藏集上答错。改错题的初始查询在可见样例上就要答错。验证失败会附带原因重出，最多三次。通过后保存到 SQLite，用户可直接切到附加题练习。

**计划中的功能**
- 随时问：侧边栏，自动带上题面、当前代码、最近一次运行结果。默认分级提示：方向 → 思路和数据结构 → 伪代码 → 完整题解，逐级手动点开，用到几级记入记录。报错旁有"解释这个错误"。
- 通过后点评（复杂度、漏掉的边界、更地道的写法）。

### 6. 架构
```
浏览器（任何机器）
  React + Vite + Monaco
  Web Worker：PGlite（SQL 判题）
        │ HTTPS
后端 FastAPI（先本机，之后部署）
  ├─ Python 判题 → 本地专用解释器或 Docker 临时容器（原生 CPython 3.14）
  ├─ AI 出题验证 → Python 用同一个沙箱，SQL 用 Node 里的 PGlite
  ├─ 题库 API（固定题库 = problems/ 下的文件）
  ├─ 进度 / 提交 / 对话 / 我的题（SQLite）
  ├─ AI 服务 → claude -p（Claude Max）或 codex exec（ChatGPT 登录）
  └─ 登录（单用户）
```

### 7. 部署

默认在每台机器上运行本地模式。浏览器和 FastAPI 共用一个回环端口，本机免登录。设置同步仓库后可在不同机器间接着做题。

可选的服务器部署使用 systemd 用户服务运行 `deploy/run.sh`。FastAPI 从 `web/dist` 提供前端，默认监听 `127.0.0.1:8001`。家外访问使用 Cloudflare Tunnel，Access 应用覆盖整个主机名，仅允许本人的邮箱。通过 Access 后，还需输入应用密码。Cloudflare 账号中的配置由用户完成。[部署步骤与迁移到 VPS](../deploy/README.md)

- 生产模式要求有效的密码哈希。优先读 `CODE_DOJO_PASSWORD_HASH`，也可从 `CODE_DOJO_DATA/auth.json` 加载。登录后签发默认 30 天的 HttpOnly、SameSite=Lax cookie，HTTPS 下带 Secure。各设备可分别退出；每个 IP 连续输错 5 次锁定 10 分钟。
- `GET /api/health` 仅返回 `{"ok":true}`。`/api/auth/session` 查询当前会话，`POST /api/auth/login` 与 `POST /api/auth/logout` 处理登录、退出。其他所有 API（含 AI、判题、题库诊断 `/api/status`）均受登录保护。写请求要求 `Content-Type: application/json`，包括无正文的操作。
- 本机开发直接启动后端时默认免登录。部署脚本固定启用登录。VPS 可用 `claude setup-token` 配置个人订阅令牌，判题镜像在新机器上构建。

### 8. 分阶段
1. **M1 Python 能刷题**：前端骨架 + Monaco；服务器 Python 判题（Docker；函数模式 + 类模式）；后端题库 API + 提交记录；题目格式、技能图、平滑性检查；Python 0A 第一批约 40 题。
2. **M2 SQL 能刷题（已完成）**：阶段 0–2 的固定题库、浏览器 PGlite 判题、可运行的 SQL 课和经服务端验证的 SQL 附加题。
3. **M3 AI**：provider 层、侧边栏问答、分级提示、报错解释、通过后点评、当场出题（含验证）。
4. **M4 路线和复习（已完成）**：地图与知识点页展示掌握度，“继续”按复习到期日、前置技能与学习中技能数推荐。今日计划支持限量复习和从空白重写，题目页提供卡住回退，手感统计展示五项周趋势和各单元掌握数。
5. **M5 部署（代码部分已完成，Cloudflare 待用户配置）**：单用户登录、单端口服务、systemd 和 Tunnel / Access 部署指南。
6. **M6 进阶 track**（见 2b）平台已完成，内容待写。数据科学镜像支持数值和表格对拍、梯度检查、写法约束、模拟训练和形状预测。

### 9. 待用户确认
- 题单骨架：等调研报告（docs/reports/）出来再定。
- 已定（2026-11-22）：判题位置 Python 服务器 / SQL 浏览器；SQL 方言 PostgreSQL。

## 还可以做的
- 桌面启动再提速：更新包构建时把全部 YAML 预先解析成一个文件，启动时不再逐个读 1700 多个文件（本机约省 0.1 秒，Windows 上文件多时收益更大）。
- 限时模拟面试模式。
- 更多语言（需要时再加；浏览器里不好跑的语言要回到服务器沙箱）。
