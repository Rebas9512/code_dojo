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
- ✓ 38-sql-mysql-port-rework（用户 2026-11-23："这个也可以一起做了"）：5 道题的 starter 改成真 MySQL 写法，格式 v1.10 加 `starter_dialect: mysql`，验题要求 starter 在 PG 上报错；主控复核 SQL 361/361。原记录：33 的 5 道"MySQL 改 PostgreSQL"改错题，starter 是已经翻译好的 PG 写法（只是参数顺序错），练不到方言迁移。应改成 starter 就是真 MySQL 写法（IFNULL、DATE_ADD、LIMIT x, y、GROUP_CONCAT、反引号），在 PG 上运行报错，学习者改写；verify_sql 需要允许 fix 题的 starter 报错。

## 桌面应用 1.1.1 / 1.1.2（主控 2026-11-23）
- 1.1.1：Linux AppImage 的 AppRun 一律带 --no-sandbox（Ubuntu 23.10+ 点图标打不开）；桌面版不扫题库。
- 1.1.2：.gitattributes 让 server/uv.lock 在 Windows 检出时不转 CRLF（之前 Windows 首次启动去 PyPI 现装依赖）；锁一致时直接用随包 libraries，不复制。
- CI：推送 main 只跑 Linux；三系统测试 `gh workflow run ci.yml` 手动触发（私有仓库 Actions 额度，macOS 10 倍计费）。发版前先在本机跑 server pytest + bootstrap tests。
- 用户："如果这次构筑没什么问题就先这样吧 如果后续要发新版再说好了"——暂停发版。

## 做题页草稿标签（用户 2026-11-23："在answer这个写代码的tab旁边加一个scratch pad 这样我可以中途运行一些和答案无关的测试内容或者中间内容什么的看结果"）
- ✓ 35-scratch-pad：编辑区加 `scratch.py` / `scratch.sql` 标签，草稿走 playground / PGlite runExample，只看输出不判题；预测题、看数据题不加。只改前端（ProblemWorkspace、WorkbenchPanel、workbench.css、docs/README.md）。
- 发布不走 Actions（额度 12-01 重置）：提交带 `[skip ci]`，更新包在本机用 `scripts/desktop/build.py payload` 构建，`gh release` 上传到 `payload-latest`。

## 助教支持 Codex（用户 2026-11-23："助教的话帮我也支持一下codex吧 就是做个下拉选项选择本机有的agent这样 有Claude就可以选claude 有codex可以选codex，如果都有就都可以选这样"）
- ✓ 36-tutor-agent-picker：后端加 CodexProvider（`codex exec --output-schema`，走 ChatGPT 订阅；严格 schema 转换），按本机实际有的 agent 列出；助教顶部下拉框选 agent，请求带 `agent`。和 35 并行：不碰 ProblemWorkspace / WorkbenchPanel / workbench.css，测试端口 8002 / 5175。
- bootstrap / desktop 的改动（只有 codex 时不关 AI）随下一版安装包生效；这次只发更新包。

## 主页"继续最新进度"（用户 2026-11-23："在主页还想加一个直接进入最新进度的一个按钮 就是直接进到track的最远一个未完成node里最新的还没做过的题这样"）
- ✓ 37-map-resume-frontier：后端每条线加 `frontier`（做过的最靠后那题所在单元里下一道没做过的题，规则见任务文件）和 `last_active`；主页顶栏按钮进当前标签页最近练过的那条线的前沿。测试端口 8004 / 5177。

## 主控小改（2026-11-23）
- 做题页标题旁显示本题状态（● 已通过 / ● AI 协助通过 / ◐ 做过没通过）：ProblemWorkspace.tsx、ProblemStatus.tsx 导出 STATUS_NAME、workbench.css。用户："在做题页面 题目本身上如果已完成可以有个标记"。
- 辅助模式的引号配对改 `autoClosingQuotes: 'always'`（CodeEditor.tsx）：Monaco 默认在字母后不补引号，f"、r"、b" 补不上。用户："现在这个只补括号系列不补引号"。
- 36 验收：codex_schema.py 保留数组的 minItems / maxItems（严格模式支持）；之前全丢，真实 Codex 出 SQL 附加题给了 4 条错误写法，超过 SqlExtra 的上限 2。
- 主控验收时发现并修复：编辑器受控写法的竞态（@monaco-editor/react 的 value 回写在 useEffect 里，按键间隔 < 20 ms 时拿旧值覆盖编辑器，丢字；答案编辑器原来就有）。CodeEditor.tsx 改为 defaultValue + 忽略自己发出的旧值，只把外部改动（重置、载入草稿）写回编辑器；5 ms 间隔 0/3 丢字。

## 启动性能（用户 2026-11-23："顺便可以做一下性能优化最好把启动流程之类的能够提速多点之类的"）
- ✓ Opus 子代理：先实测启动各阶段（Electron → 启动器 → 查更新 → 后端 import / 题库 / lifespan → ready → 地图首屏 → 首次开题），优先做更新包能发的优化；bootstrap / desktop 的改动随下一版安装包。和 37 并行：不碰 tracks()、units.py、MapPage、mapTree、map.css、TrackInfo；端口 8005 / 5178。报告在主控 scratchpad 的 perf-report.md。
- 结果：热启动地图可用 4.00 → 0.97 s、冷启动 4.47 → 1.26 s（只发更新包为 2.47 / 2.83 s）。更新包：题库 YAML 走 libyaml、tests.json 用到才读（内存 427 → 72 MB）、启动同步放后台、地图空闲预载做题页和 Monaco、知识点页懒加载。随下一版安装包：先用已装版本起服务后台查更新、安装包 .pyc 预编译、去掉更新包 / 依赖锁 / 清单三处校验（用户："除了那种对齐进度必须要的点 其他没必要的哈希感觉可以优化"）。

## 每道题都有草稿（用户 2026-11-23："不过我想做成每题都有草稿这样 有时候讨论的时候我也想打开草稿写点东西这样"）
- ✓ 39-scratch-everywhere（主控验收：预测、认识数据选择题、SQL 看数据题和普通题都过；删掉了书店库接口的兜底分支）：预测题、看数据题也加草稿。SQL 线用 scratch.sql，其他线用 scratch.py；看数据题右侧可以在答案区和草稿之间切换。起因是用户在 Windows 上以为草稿没加载出来。主控复现确认：Alt+S 只在题目加载完之前按才会无效，不是 bug。

## 做题心流（用户 2026-11-23："感觉目前有点难进入心流状态，能不能帮我调查一下有没有什么好的小机制或者小设计"）
- ✓ 主控调研：docs/reports/做题心流 调研.md。用户选了：一组练习（带热身和连续首次通过计数）、专注模式、安静计时、通过提示音（默认关）。组内自适应、事先定规则、停下留一句暂不做。
- ✓ 40-flow-session（主控验收：开组、自动推进、跳过、刷新续做、小结数字、专注模式、静止状态栏都过）：上面四项一起做（都要改 ProblemWorkspace，不拆分）。排题走后端纯函数 + `/api/session-plan`；组状态存在前端 localStorage；全屏用网页的 Fullscreen API，不改 desktop/。
- ✓ 主控已修：主页"继续"在 SQL 标签下消失。「认识数据」是两个标签共用的根线，它最近练过但已全部做完（frontier 为空），被选成了目标线，按钮就隐藏了。选线要改成：只在 frontier 不为空的线里按 last_active 挑；都没练过就取树里第一条已解锁且有 frontier 的线。40 的 session-plan 选线也要按同一规则。用户真实数据核对过：Python 标签指向 003 是对的。

## 项目阶段（用户 2026-11-23：高阶线"每块拆成一题，最后拼成能完整跑通的 notebook / 标准训练脚本"；"sql什么的你看着也可以设计一些这样的项目"）
- 设计：docs/curriculum.md「项目阶段：高阶线和 SQL 线的收尾」。七个项目：数据处理、机器学习、训练、手搓 LLM、SQL、产品分析、建模。每部分独立判（其他部分用参考实现），放在本线最后一个阶段。
- ⏳ 41-project-platform：格式 v1.11、判题注入、拼装、完整运行、导出（.py / .ipynb / .sql）、项目页、地图节点、内容检查。等 40 完成再派（都改 ProblemWorkspace / MapPage / main.py）。
- 待派：42–45 四个 Python 项目（并行）→ 46–48 三个 SQL 项目（并行），都等 41 验收后再派。

## 参考答案（用户 2026-11-23："每题我做完正确以后 最好有一个比较标准的参考答案可以选择性的查看"；量大，"还是先全给codex去做吧 要确保代码优雅简洁，以教学为核心，禁止防御型写作"；简短说明）
- ✓ 42-standard-answer-platform（主控验收：技能范围改成和参考解同一规则——requires ∪ introduces 及其前置，撤回 codex 为示范改的 4 处 requires；对比视图窄栏改行内；5 道示范风格合格）：standard.* + standard.md、verify_standard.py、通过后的"参考答案"标签和对比视图、写法规范（teaching-design.md）、5 道示范。先于 41 派（两者改同一批文件）。
- 参考答案内容 9 个任务（43–51，按线和阶段切分，只新建 standard.*）。第一批 41 + 43/44/46/47 并行；41 完成后派 45/48/49/50/51。完成后主控抽查各线关键题。
- 项目内容任务编号顺延为 52–58（41 验收后派；部分题同时写参考答案）。
- ✓ 44-standard-algo-3：92 道（72 沿用参考解、20 重写），verify 92/92。主控抽查 026 前缀和、046 双堆中位数、083 Kahn、088 并查集、080 多源 BFS、092 单词接龙：思路和复杂度都对。格式上有 PEP 8 小毛病（逗号后少空格、类和函数之间只空一行）→ 全部答案任务完成后统一用格式化工具过一遍所有 standard.py，再跑 verify_standard。
- ✓ 43-standard-algo-1-2：152 道（128 沿用、22 重写），verify 73/73 + 79/79。抽查最小覆盖子串、每日温度、Koko 二分、接雨水：都是最优解法。
- ✓ 46-standard-python：169 道（152 沿用、15 重写、4 道带进阶写法），verify 169/169。抽查倍数计数、银行账户类：用的都是已学写法。
- ✓ 47-standard-sql：213 道（90 原样、86 只调排版、36 调整表达），verify 213/213。抽查体育馆人流（连续段用 id − ROW_NUMBER）、推荐层级（递归 CTE）：标准写法。
- ✓ 45/48/49/50/51 参考答案：算法 4–5（159）、产品分析和建模（148）、数学和数据处理（128）、张量和机器学习（129）、训练和 LLM（110），verify 全过。抽查零钱兑换 DP、手写 autograd（h+h 要用 +=）、SCD2 关闭旧版本、pandas merge / loc：都合格。参考答案 1300 道全部完成；PEP 8 统一格式化在项目任务完成后做。
