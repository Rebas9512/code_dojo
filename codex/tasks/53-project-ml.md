# 53-project-ml：项目 · 机器学习 · NumPy 预测流失（churn.py）

## 背景

用户 2026-11-23 要给高阶线和 SQL 线加"项目"：每个部分一道题，最后拼成一个能完整跑通的脚本或 notebook。用户原话见 `docs/curriculum.md` 的「项目阶段：高阶线和 SQL 线的收尾」一节，那一节的"共同规则"和表格里本项目那一行就是设计。

平台已经由任务 41 做好，格式见 `docs/problem-format.md` 的「项目阶段」（v1.12）。两个可以照着写的夹具：
- `server/tests/fixtures/projects/fit/`（Python）
- `server/tests/fixtures/projects/sales/`（SQL）

参考答案的格式和写法规范见 `docs/problem-format.md`（v1.11 的 `standard.*`）和 `docs/teaching-design.md` 的「参考答案的写法」。

**动手前通读**：项目阶段格式、两个夹具、本线 `track.yaml` / `skills.yaml`，以及本线已有的课和题（看本线已经教了哪些技能、用什么样的数据和题面口吻）。

## 本项目

- **先决条件**：任务 52（数据处理项目）已经完成。数据用它的完整参考脚本产出的 `features.csv`，复制进本项目数据目录，并在数据 `README.md` 里写明来源和生成命令。列的约定见任务 52 的任务文件。
- 只用 NumPy（加上读 CSV 的标准库或 pandas，只用来读）。
- 部分（9–11 个）：
  1. 读入并按用户分层切分训练 / 验证 / 测试，固定种子；
  2. 只用训练集拟合标准化；
  3. 城市独热编码加偏置列；
  4. 逻辑回归的前向和带 L2 的交叉熵；
  5. 梯度；
  6. 梯度下降训练；
  7. 预测和阈值；
  8. 混淆矩阵和 precision、recall、F1；
  9. AUC；
  10. k 折选学习率和 L2；
  11. `main()`：最终训练、打印报告，最后一行 JSON 指标。
- `success`：测试集的 F1 和 AUC 达到阈值，阈值按参考结果略留余量。
- 完整运行在 60 秒以内。

## 要做的事

1. 在 `problems/ml/track.yaml` 末尾加一个 `kind: project` 的阶段，一个单元就是本项目。
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

- 只改 `problems/ml/` 下本项目相关的文件，加上 `track.yaml` 里新增的那一段。不改平台代码、脚本和其他线。
  - 发现平台 bug：在报告里写清复现步骤，绕不过去就停下来报告，不要自己修。别的任务正在并行跑。
- 不写防御性代码（标准做法第 7 条）。
- 不加新依赖。DS 环境里只有 NumPy、pandas 和 CPU 版 PyTorch。
- 测试实例端口用 **后端 8022、前端 5192**，别的端口有别的任务在用。

## 验收标准

- `cd server && .venv/bin/python ../scripts/curriculum/check_curve.py --track ml` 0 错 0 警。
- `cd server && .venv/bin/python ../scripts/verify_bank.py --judge local --only ml-6-` 全部通过，包括项目的完整参考运行达到 `success`。具体参数看脚本帮助，任务 41 加了项目相关的开关。
- `cd server && .venv/bin/python ../scripts/curriculum/verify_standard.py --only ml-6-` 全部通过。
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
