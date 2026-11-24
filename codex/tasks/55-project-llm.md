# 55-project-llm：项目 · 手搓 LLM · 字符级小 GPT（gpt.py）

## 背景

用户 2026-11-23 要给高阶线和 SQL 线加"项目"：每个部分一道题，最后拼成一个能完整跑通的脚本或 notebook。用户原话见 `docs/curriculum.md` 的「项目阶段：高阶线和 SQL 线的收尾」一节，那一节的"共同规则"和表格里本项目那一行就是设计。

平台已经由任务 41 做好，格式见 `docs/problem-format.md` 的「项目阶段」（v1.12）。两个可以照着写的夹具：
- `server/tests/fixtures/projects/fit/`（Python）
- `server/tests/fixtures/projects/sales/`（SQL）

参考答案的格式和写法规范见 `docs/problem-format.md`（v1.11 的 `standard.*`）和 `docs/teaching-design.md` 的「参考答案的写法」。

**动手前通读**：项目阶段格式、两个夹具、本线 `track.yaml` / `skills.yaml`，以及本线已有的课和题（看本线已经教了哪些技能、用什么样的数据和题面口吻）。

## 本项目

- 数据：一小段公版英文文本，约 150–200 KB，比如 Project Gutenberg 上的公版作品。数据 `README.md` 写清来源和公版声明。
- 字符级分词（本线前面已经练过 BPE，项目用字符级，是为了训练快；在题面说明这一点）。
- 部分（11–12 个）：
  1. 词表与 `encode` / `decode`；
  2. 切分训练 / 验证集和 `get_batch`（随机窗口，目标右移一位）；
  3. 因果自注意力（多头）；
  4. 前馈层；
  5. Transformer 块（pre-norm、残差）；
  6. GPT（词嵌入加位置嵌入、若干块、末层 LayerNorm、输出头、交叉熵损失）；
  7. AdamW 参数分组（weight decay 只作用于矩阵）；
  8. 预热加余弦学习率；
  9. 训练循环（梯度裁剪，定期估计验证损失）；
  10. 采样（温度、top-k）；
  11. KV cache 生成（同种子下与无缓存的逐字一致）；
  12. `main()`：训练、打印一段生成文本，最后一行 JSON 指标。
- 模型规模自己定（建议宽 128、4 层、4 头、上下文 64 上下）。要在 CPU 上 2–3 分钟内训到验证损失明显下降。`project.yaml` 的 `run.timeout` 按实测留余量。
- `success`：验证损失低于阈值；`cache_match` 为 1（有缓存和无缓存的生成完全一致）；生成文本长度符合要求。

## 要做的事

1. 在 `problems/llm/track.yaml` 末尾加一个 `kind: project` 的阶段，一个单元就是本项目。
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

- 只改 `problems/llm/` 下本项目相关的文件，加上 `track.yaml` 里新增的那一段。不改平台代码、脚本和其他线。
  - 发现平台 bug：在报告里写清复现步骤，绕不过去就停下来报告，不要自己修。别的任务正在并行跑。
- 不写防御性代码（标准做法第 7 条）。
- 不加新依赖。DS 环境里只有 NumPy、pandas 和 CPU 版 PyTorch。
- 测试实例端口用 **后端 8024、前端 5194**，别的端口有别的任务在用。

## 验收标准

- `cd server && .venv/bin/python ../scripts/curriculum/check_curve.py --track llm` 0 错 0 警。
- `cd server && .venv/bin/python ../scripts/verify_bank.py --judge local --only llm-6-` 全部通过，包括项目的完整参考运行达到 `success`。具体参数看脚本帮助，任务 41 加了项目相关的开关。
- `cd server && .venv/bin/python ../scripts/curriculum/verify_standard.py --only llm-6-` 全部通过。
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
