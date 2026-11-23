# 41-project-platform：项目阶段的平台支持

## 背景

用户 2026-11-23 要给高阶线和 SQL 线加"项目"：每个部分一道题，最后拼成一个能完整跑通的脚本或 notebook。设计已经写在 `docs/curriculum.md` 的「项目阶段：高阶线和 SQL 线的收尾」一节，先通读那一节，特别是"共同规则"。用户定的三点：
- 每部分**独立判**，其他部分用参考实现顶上；
- 项目放在本线**最后一个阶段**；
- Python 项目（数据处理、机器学习、训练、手搓 LLM）和 SQL 项目（SQL、产品分析、建模）**都要支持**。

这个任务只做平台，并配一个很小的示例项目来测试。正式内容由后面的任务 42–48 写。

相关代码：
- 题库加载：`server/app/problems.py`（`ProblemMeta`、`ProblemBank`、单元分组 `units.py`）。
- Python / DS 判题：`server/app/judge.py`、`local_judge.py`、`judge/python/`（harness）、`judge/ds/`。
- SQL：前端 `web/src/sql/`（worker、`runScript`、`client.ts`），后端 `server/app/sql_judge.py`，以及 `mode: script` 的检查和探针（`docs/problem-format.md` 的"SQL 脚本题"）。
- 前端：`web/src/pages/MapPage.tsx`、`TrackPage.tsx`、`ProblemWorkspace.tsx`、`App.tsx` 路由。
- 内容检查：`scripts/curriculum/check_curve.py`、`verify_python.py`、`verify_sql.py`、`scripts/verify_bank.py`。

## 要做的事

### 1. 格式（`docs/problem-format.md` 升到 v1.11）

- `track.yaml` 的阶段可以标 `kind: project`。这个阶段里每个单元就是一个项目，单元目录下放 `project.yaml`。目录怎么摆自己定，跟现有单元的组织方式一致即可。
- `project.yaml` 至少包括：
  - `id`、`title`、`summary`；
  - `language`：python / sql；
  - `scaffold`：骨架脚本，每部分一个占位，比如 `# @part load_data` 或 `-- @part sessions`；
  - `reference`：完整参考脚本，由骨架加各部分参考解拼成，或者单独一份，自己选并保证一致；
  - `data`：项目数据目录，或者 SQL 项目用哪个共享库；
  - `parts`：部分题 id 的顺序表；
  - `run`：Python 项目写入口（`main`）、命令行参数、时限（默认 300 秒）；SQL 项目写最终检查；
  - `success`：Python 项目判脚本最后一行 JSON 指标的阈值，比如 `{val_acc: {">=": 0.95}}`；SQL 项目判检查全过。
- 部分题的 `problem.yaml` 加 `project: <项目 id>` 和 `part: <序号>`；`format: combine`，不引入新技能。
  - Python 部分题用现有的 `function` / `class` 模式和 checker。
  - SQL 部分题用现有的 `mode: script`（检查加探针）。

### 2. 判题时注入参考实现

- **Python**：判某一部分时，harness 先在同一个命名空间里执行项目的参考脚本（不调用 `main`），再执行学习者的代码，覆盖同名定义，然后照常跑测试或 checker。
  - 学习者的函数可以直接调用其他部分的函数名，拿到的是参考实现。
  - 项目数据目录通过一个常量交给代码，比如 `DATA_DIR`，并把工作目录设到可写的临时目录。
  - checker 也能拿到这个命名空间，以便端到端地检查这一块。
- **SQL**：判某一部分时，setup 依次是项目数据库 → 前面各部分的参考 SQL → 学习者这一段 → 本部分的检查和探针。前端 PGlite 判题和后端 `sql_judge`（验题用）用同一套顺序。
- 附加题、课、草稿不受影响。

### 3. 拼装、完整运行、导出（后端接口 + 前端）

- **拼装**：用学习者每部分**最近一次通过**的提交代码填进骨架；没通过的部分放 TODO 桩，Python 用 `raise NotImplementedError("第 N 部分还没完成")`，SQL 用注释。返回拼好的文本和各部分的状态。
- **完整运行**：
  - Python 在 DS 环境里跑拼好的脚本，用项目时限，输出逐行显示（流式或轮询，选简单可靠的）。脚本最后一行是 JSON 指标，按 `success` 判定。
  - SQL 在浏览器 Worker 里跑整段 SQL 再做检查。PGlite 现在的 2 秒单句超时，对项目整段要放宽，按项目配置。
  - 达标就记一次"项目完成"，要能随做题记录同步到别的机器，沿用现有的事件和同步机制，不另起一套。
- **导出**：
  - Python 导出 `.py` 和 `.ipynb`。notebook 是 nbformat 4 的 JSON，自己生成，不加依赖；每部分一个 markdown 格（标题和一两句说明）加一个代码格，最后一格调用 `main()`。
  - SQL 导出 `.sql`。
  - 桌面版里，下载交给 Electron 默认的保存对话框；先确认现有 `desktop/` 配置下浏览器下载可用。如果必须改 `desktop/` 才能下载，就退而在页面上提供"复制全文"，并在报告里说明。
- **项目页**（新路由，如 `/project/<id>`）：
  - 目标说明；
  - 部分列表：状态和打开链接；
  - "拼起来"的只读预览（Monaco）；
  - "完整跑一遍"按钮和日志区，最后显示指标和是否达标；
  - 导出按钮。

  风格遵守 `.impeccable.md`。
- **地图和做题页**：
  - 项目单元在地图上用不同的图标，单元详情里有"打开项目"。
  - 部分题的做题页标题旁显示"项目 · 第 3/10 部分"，并链回项目页；题面末尾自动列出"其他部分（判题时用参考实现）"的名字。

### 4. 内容检查

- `check_curve.py` 认识项目阶段：部分题不引入新技能，`requires` 必须都是本线已经引入过的技能。
- `verify_bank.py` / `verify_python.py` / `verify_sql.py`：
  - 每个部分的参考解按注入规则通过自己的测试；
  - 参考脚本完整跑一遍达到 `success`，比较慢，可以用一个开关单独跑，但默认的全库验证里要包含一次；
  - 拼装器用全部参考解拼出的脚本和 `reference` 一致（或者等价，跑出同样的指标）。

### 5. 示例项目（只用来测平台，写进测试夹具，不进正式题库）

- 一个 Python 小项目：3 个部分，比如读数据 → 拟合直线 → `main` 打印 JSON 指标，几秒跑完。
- 一个 SQL 小项目：3 个部分，比如视图 → 汇总表 → 最终查询。
- 两个都放在 `server/tests/fixtures/` 下，不出现在正式地图上。

## 不做

- 不写正式项目内容（后面的任务做）。
- 不改 `desktop/`、`bootstrap/`，下载如确实需要改，见上面的退路。
- 不加新依赖。

## 验收标准

- `docs/problem-format.md` v1.11 写清项目格式、注入规则、拼装和运行；`docs/README.md` 相关节小补丁更新。
- `cd server && .venv/bin/python -m pytest -q` 全过（7 个会建临时 git 仓库的同步测试可以按标准做法排除）。新增测试覆盖：
  - Python 注入（学习者代码覆盖参考定义；其他部分可以调用）；
  - SQL 注入顺序；
  - 拼装（通过的部分用学习者代码，没通过的放桩）；
  - 运行判定（指标达标、不达标、超时）；
  - 导出的 `.ipynb` 是合法的 nbformat 4 JSON；
  - 项目完成事件能进同步。
- `cd web && npm run build`、`node --experimental-strip-types --test web/tests/sql.test.mjs` 通过。
- 全库 `verify_bank` 和 `check_curve` 不回归（现有 1554 题）。
- 用 Playwright 在测试实例（8001 / 5174，独立数据目录，题库指向含示例项目的夹具）上走一遍并截图：
  - 打开示例项目页 → 做第 1 部分（交参考解）→ 拼起来，看到第 1 部分是自己的代码、2–3 部分是桩；
  - 把 3 部分都做完 → 完整跑一遍达标 → 导出 `.py` / `.ipynb`；
  - SQL 示例项目同样走一遍。
