# codex 任务总排期（主控维护）

用户 2026-11-22 说："等报告回来你就主导让codex做落地就行，可以多派几个并行做反正一路就先把之前讨论的内容落地了就可以"。

这份文件给每个 codex 任务看。几个任务会同时跑，每个任务只改自己名下的文件和编号段。别的任务名下的文件，碰到问题只写进报告，不要动手改。

## 三条线并行，平台任务一个接一个

| 波次 | 平台（改 server/app、web/src，同一时间只跑一个） | Python 基础内容 | 算法内容 | SQL 内容 |
| --- | --- | --- | --- | --- |
| 0 | 01-tracks：track 文件化（✓ 2026-11-22 验收） | | | |
| 1 | ✓ 02-inspect-platform：看数据作答题型、根线"认识数据"、数据处理线改名 wrangle；✓ 02m-map-tree：首页改成 Python / SQL 两个标签页 + 树状图（和 02 并行，文件分开，见 02m 任务） | ✓ 03-py-0a-g6-10：0A 第 6–10 组（89 题） | ✓ 04-algo-s1：算法阶段 1（73 题） | ✓ 05-sql-s1-2：SQL 阶段 1–2（36 题） |
| 2 | ✓ 07-sql-judge（M2）：浏览器 SQL 判题、SQL 附加题 | ✓ 06-intro-content：认识数据根线 + Python 第 0 组 + SQL 开头（等 02） | ✓ 08-algo-s2（79 题） | ✓ 09-sql-s3-5（52 题） |
| 3 | ✓ 11-review（M4）：掌握度、间隔复习、今日计划 | ✓ 10-py-0b：0B 算法入门（31 题） | ✓ 12-algo-s3（92 题） | |
| 4 | ✓ 13-login（M5）：单用户登录 + 部署文档 | | ✓ 14-algo-s4（80 题） | |
| 5 | ✓ 15-ds-judge（M6，和 13 并行，文件分开）；✓ 23-sql-dml（SQL 修改类判题）：数据科学判题镜像和判题方式 | | ✓ 16-algo-s5：面试混合（79 题） | |
| 6 | | 进阶内容：✓ 17-math（80 题；不用等 15，runtime 是 python，Python 内容线空出来就先派）→ ✓ 18-wrangle（100 题）→ ✓ 19-tensor（90 题）→ ✓ 20-ml（87 题）→ ✓ 21-train（80 题）→ 22-llm（等 15；按前置一个接一个跑） | | |

## 本地模式（用户 2026-11-22 改的方向）

每台机器本地跑，网页还是 localhost 加浏览器；代码和题库放 GitHub 私有仓库；Linux、macOS、Windows 三个系统都要支持。拆成两个平台任务同时跑：
- ✓ 24-local-judge：本地判题（Linux 上 1073/1073 两种模式结果一致）（不靠 Docker），跨平台的 harness，三系统 CI；
- ✓ 25-launcher-sync：`dojo` 一条命令启动，做题记录用事件日志 + 单独私有仓库同步。

两者都要改 `config.py`，各自只加自己的配置项。

之后（用户 2026-11-22 定）：26-desktop-app，把应用打包给三个系统用。安装包只带 Python 运行时和一个小启动器，界面、后端、题库都打进更新包，每次打开自动从 GitHub 更新；等 24、25 做完再派。

代码仓库：GitHub 私有仓库 `Rebas9512/code_dojo`（用户 2026-11-22 定的名字），本地 remote 是 origin。2026-11-22 主控做了第一次提交并推送（0716585，1073 题；problems/ml 当时只提交了 track.yaml，因为 20 号任务还在写）。以后每批验收后由主控提交推送，codex 任务照旧不做 git 操作。同步仓库已建好：`Rebas9512/code_dojo_sync`（私有，main 分支，初始只有 README）。

## 文件归属（并行时的规矩）

**单元**：首页树上的节点是单元，也就是技能的 `group`。单元名写在 `track.yaml` 的 `stages[].units` 里，由 02m 写。内容任务给自己阶段的技能加 `group`，算法线的分组按 curriculum.md 6.3 的小节来。

**平台任务**独占这些文件：
- `server/app/`、`server/tests/`、`web/`、`judge/`
- `docs/problem-format.md`、`docs/README.md`
- `scripts/verify_bank.py`
- `check_curve.py` 里的格式校验部分

**内容任务**只改这些：
- 自己那条线 `problems/<track>/` 里，自己负责的阶段或组的题目目录和课文件。
- 共享文件里自己那一段：
  - `problems/<track>/skills.yaml` 里自己负责的技能条目。
  - `docs/curriculum.md`、`docs/teaching-design.md` 里对应自己阶段或组的小节。
  - `scripts/curriculum/check_curve.py` 里的识别表（`PY_*` / `SQL_*` 这些表），只加行，不改别人的行。

**改共享文件的方式**：只用小范围补丁改自己那几段。不整文件重写，不重新排版，不用脚本把整个 yaml 或 md 读出来再写回去，因为别的任务正在同时改同一个文件的其他段。

## 编号段

**Python 基础 0A**（题号 `py-0a-NNN-slug`）：

| 范围 | 题号 NNN | order |
| --- | --- | --- |
| 第 1–5 组（已有） | 001–152 | 10–1080 |
| 第 6–10 组（03） | 200–399 | 2000–5990（第 6 组 2000 起，第 7 组 3000 起，……，第 10 组 5000 起） |
| 第 0 组新题（06） | 400–449 | 06 可以重排第 0–5 组的 order，但不超过 1990 |

**Python 基础 0B**（10）：题号 `py-0b-NNN-slug`，NNN 从 001 起。

**算法**（题号 `algo-<阶段>-NNN-slug`）：每个阶段各自从 001 编起，order 从 10 起、步长 10。

**SQL**：
- 题号 `sql-<阶段>-NNN-slug`；阶段 0 已有题保持不变，06 的新题用 100–149。
- `_db/bookstore` 的表结构，06 和 SQL 内容任务都可能要加数据。规矩是只追加行或新表，不改已有的行。

## 每个任务结束时

- 自己范围内：`verify_bank.py --only <自己的题号前缀>`（Python）或 `scripts/curriculum/verify_sql.py`（SQL）全过。
- `check_curve.py`：自己范围内 0 错。别的任务还没做完造成的报错，写进报告，不要去修。

## 待补（验收时发现的，排进后面的任务）

- ✓ 06b：SQL 阶段 0 补了字符串、日期、ROUND、正则 4 个技能的引入题（8 题），检查脚本加了"有技能没引入题"的警告。
- ✓ 05b：SQL 阶段 1–2 里绕开舍入和日期的 7 道题改回原题考法。
- 主控已修：算法阶段 1 的 9 道栈题加 `unit: 2`；020、021 补上 `py.list-concat-repeat` 前置。
- ✓ 05c：SQL 50 实际覆盖 50/50；check_curve 加了"计划骨架题必须真的有题"（算法阶段 1–3 也满足）。
- ✓ 23：SQL 的 DML 判题模式（sql-3-020 改成真正的 DELETE 题）。09 把"删除重复邮箱"做成了生成 DELETE 清单的只读题，以后可以加一种"执行后比对表状态"的模式。
- ✓ 主控已改：verify_python.py 启动时把栈调到 256MB、递归上限 20 万，和判题镜像一致（12 的报告：本机跑深链树题会 RecursionError）。
- ✓ 主控已改：首页地图节点双击进入题目列表的对应单元（用户要求）。
- `docs/README.md` 里的题量数字：内容任务不能改 README，由主控在每批结束后统一更新。

- ✓ 主控已改：`.gitignore` 加 `deploy/.env`（13 的部署配置会放密码哈希）。
- ✓ 主控已改：verify_python.py 只查 runtime: python 的线（ds 线的题和课示例由 verify_bank 在 DS 镜像里跑）。
- 待定（平台小项）：16 给阶段 5 的题加了 `week: N`（十周混排），格式里还没有这个字段。打算收进格式，题目列表按周分组显示，等下一个平台任务顺手做。
- ⏳ 27：题目语言约定。用户 2026-11-22 要求题干用中文，作答用英文；改约 94 道题和相关的课，规则写进格式文档和附加题提示词。22-llm 已加这条要求。
- ✓ 28：令牌用密码加密后打包进安装包（用户 2026-11-22 定）+ 收尾（week 字段、控制窗口中文字体、地图算法行、README 总量）。
- ✓ 28b：28 被会话关闭打断后接着做；加密脚本加 `--password-key`，可以从 .env 读密码。
- ✓ 29：Linux 打成 AppImage，配合用户的 AppImageLauncher Lite 放进 ~/Applications；加图标。等 28b 做完再派，两者都改 release-app.yml 和 build.py。
- ✓ 主控已跑 seal_tokens.py（用户 .env 里的令牌和密码），Actions 密钥 CODE_DOJO_SEALED_TOKENS 已上传（2026-11-23）。
- ✓ 主控已发 app-v1.0.1（含 AppImage 和加密令牌），并放进用户的 ~/Applications，AppImageLauncher 已经自动集成进菜单。
- ✓ 30（Electron 外壳，界面嵌进应用窗口）和 31 同时跑。31 原本是"Helvetica 风格字体 + 界面打磨"，用户又说要往 VS Code 靠，主控停掉它，改派 31-vscode-workbench。用户随后又收窄了范围，所以再停一次，最终派 31-workspace-vscode：只有做题页按 VS Code 布局（本单元题目列表、题面和代码拆分编辑区、底部面板、右侧助教、状态栏、命令面板 / Ctrl+P）；首页树状地图和外部页面保留结构，只统一配色（VS Code Modern）和字体（Heros + Noto Sans SC + JetBrains Mono，打包进应用）。前端文件归 31；30 只新建 DesktopBridge.tsx 并在 App.tsx 挂载，31 重构布局时保留它的挂载，放进状态栏。用户 2026-11-23 定。
- ✓ 31-workspace-vscode 已验收提交（ae66fdd）。主控补了一处：桌面启动页换成 VS Code 配色和打包的 Heros 字体，CSP 加 font-src 'self'。

## SQL 扩充（用户 2026-11-23："话说sql的题库是不是挺少的 … 看看sql题库有没有什么可以扩充的track之类的"，选了"123"）

- ✓ 32-sql-analytics：新线「产品分析 SQL」（`problems/analytics/`，约 90 题，自带 App 行为库）。
- ✓ 33-sql-deepen：SQL 主线阶段 1–5 加厚（约 +70 题：补阶梯、SQL 50 以外的免费题、改错题）。新题号每阶段从 101 起，已有 id 不改。
- ✓ 34-sql-modeling：平台加 `mode: script`（多语句脚本 + 多条检查 / 探针），再写新线「建模与写数据」（`problems/modeling/`，约 70 题）。要改 server/app、web，等 Opus 清理子代理结束再派。
- 32、33 并行：留存、漏斗、会话切分的深入练习归 32，33 在阶段 5 只补到各一道补全 / 独立写 / 改错。两者都会给 check_curve 的 SQL 识别表加行，只加不改。
- 第 4 条「PostgreSQL 进阶与性能」用户暂不做。
- 2026-11-23 主控验收：SQL 主线 216 题、analytics 90 题、modeling 70 题；verify_sql 361/361、课示例 118/118、check_curve 0 错 0 警、pytest 274。
- 待返工（主控验收时发现）：33 的 5 道"MySQL 改 PostgreSQL"改错题，starter 是已经翻译好的 PG 写法（只是参数顺序错），练不到方言迁移。应改成 starter 就是真 MySQL 写法（IFNULL、DATE_ADD、LIMIT x, y、GROUP_CONCAT、反引号），在 PG 上运行报错，学习者改写；verify_sql 需要允许 fix 题的 starter 报错。

## 桌面应用 1.1.1 / 1.1.2（主控 2026-11-23）
- 1.1.1：Linux AppImage 的 AppRun 一律带 --no-sandbox（Ubuntu 23.10+ 点图标打不开）；桌面版不扫题库。
- 1.1.2：.gitattributes 让 server/uv.lock 在 Windows 检出时不转 CRLF（之前 Windows 首次启动去 PyPI 现装依赖）；锁一致时直接用随包 libraries，不复制。
- CI：推送 main 只跑 Linux；三系统测试 `gh workflow run ci.yml` 手动触发（私有仓库 Actions 额度，macOS 10 倍计费）。发版前先在本机跑 server pytest + bootstrap tests。
- 用户："如果这次构筑没什么问题就先这样吧 如果后续要发新版再说好了"——暂停发版。
