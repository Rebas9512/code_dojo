# 52-project-wrangle：项目 · 数据处理 · 书店 App 用户特征表（features.py）

## 背景

用户 2026-11-23 要给高阶线和 SQL 线加"项目"：每个部分一道题，最后拼成一个能完整跑通的脚本或 notebook。用户原话见 `docs/curriculum.md` 的「项目阶段：高阶线和 SQL 线的收尾」一节，那一节的"共同规则"和表格里本项目那一行就是设计。

平台已经由任务 41 做好，格式见 `docs/problem-format.md` 的「项目阶段」（v1.12）。两个可以照着写的夹具：
- `server/tests/fixtures/projects/fit/`（Python）
- `server/tests/fixtures/projects/sales/`（SQL）

参考答案的格式和写法规范见 `docs/problem-format.md`（v1.11 的 `standard.*`）和 `docs/teaching-design.md` 的「参考答案的写法」。

**动手前通读**：项目阶段格式、两个夹具、本线 `track.yaml` / `skills.yaml`，以及本线已有的课和题（看本线已经教了哪些技能、用什么样的数据和题面口吻）。

## 本项目

- 数据：用产品分析线的 `problems/analytics/_db/readerapp`（App 的登录、事件、订单、订阅、实验）导出成 CSV，放在项目数据目录。
  - 用户数太少（不到约 500）就用固定种子生成一份同结构、规模大一些（约 2000 用户）的数据，生成脚本放在数据目录，并说明。
  - CSV 要保留真实数据的脏样子：重复行、大小写和空格不一致的城市名、缺失、时区混杂的时间戳、测试账号等。
- 部分（8–10 个，按顺序）：
  1. 读表并定类型；
  2. 清洗用户；
  3. 清洗事件；
  4. 30 分钟会话切分；
  5. 用户活跃特征；
  6. 购买特征；
  7. 合并成特征表并打流失标签（观察窗口之后的 30 天内没有下单记为流失，防止泄漏）；
  8. 汇总报告 + `main()`，把 `features.csv` 写到工作目录，并打印最后一行 JSON 指标。
- **特征表的列是约定，机器学习项目（任务 53）会直接用它**，按这个写：
  `user_id, city, signup_days, sessions_30d, active_days_30d, events_30d, orders_30d, spend_30d, avg_basket, days_since_last_order, churned`。
  - `churned` 是 0 / 1；
  - `days_since_last_order` 没下过单时取观察窗口天数加 1；
  - 数值列都是数值类型。
- `success`：特征表的行数、列名、流失率、`spend_30d` 总和与参考一致（容差自己定）。
- 完整运行要在 60 秒以内。

## 要做的事

1. 在 `problems/wrangle/track.yaml` 末尾加一个 `kind: project` 的阶段，一个单元就是本项目。
   - 已有的阶段、单元、题号一律不动，做题记录按题号存。
2. 写项目配置 `project.yaml`、骨架和数据。数据要注明来源和许可，写在数据目录的 `README.md` 里。
3. 每个部分一道题（`format: combine`）。每道题包含：
   - `problem.yaml`：`project`、`part`；`skills.requires` 只列本线（或前置线）已经引入的技能，`introduces` 留空；
   - `statement.md`：先用一两句说清这一块在整个脚本里管什么，再写签名、示例和约束，用中文；
   - 测试或 checker：examples ≥ 2、hidden ≥ 3，覆盖边界；checker 可以用合并后的命名空间，端到端检查这一块；
   - `starter.*`：签名加一句文档字符串，或者 SQL 的注释提示；
   - `solution.*`；
   - `standard.*` 和 `standard.md`：按参考答案的写法规范，代码优雅简洁、以教学为核心、禁止防御型写法。
4. 每部分只考一块。判题时其他部分用参考实现顶上，所以题面和测试不能依赖学习者前面写的部分。
5. 完整参考脚本在规定时限内跑完并达到 `success`。

## 约束

- 只改 `problems/wrangle/` 下本项目相关的文件，加上 `track.yaml` 里新增的那一段。不改平台代码、脚本和其他线。
  - 发现平台 bug：在报告里写清复现步骤，绕不过去就停下来报告，不要自己修。别的任务正在并行跑。
- 不写防御性代码（标准做法第 7 条）。
- 不加新依赖。DS 环境里只有 NumPy、pandas 和 CPU 版 PyTorch。
- 测试实例端口用 **后端 8021、前端 5191**，别的端口有别的任务在用。

## 验收标准

- `cd server && .venv/bin/python ../scripts/curriculum/check_curve.py --track wrangle` 0 错 0 警。
- `cd server && .venv/bin/python ../scripts/verify_bank.py --judge local --only wrangle-6-` 全部通过，包括项目的完整参考运行达到 `success`。具体参数看脚本帮助，任务 41 加了项目相关的开关。
- `cd server && .venv/bin/python ../scripts/curriculum/verify_standard.py --only wrangle-6-` 全部通过。
- `cd server && .venv/bin/python -m pytest -q`：不回归（7 个会建临时 git 仓库的同步测试可以按标准做法排除）。
- 用 Playwright 在测试实例上：
  - 打开项目页，确认部分列表正确；
  - 交两部分的参考解后"拼起来"，看到这两部分是交上去的代码，其他部分是桩；
  - 全部交完后"完整跑一遍"，达标；
  - 导出 .py 和 .ipynb。

  截图放 `{RUN_DIR}/`。
- 报告写：
  - 部分清单（题号、函数或对象名、一句话说明）；
  - 完整运行的耗时和最终指标；
  - 数据来源和许可；
  - 自己定的事。
