# 51-standard-train-llm：参考答案 · 训练 + 手搓 LLM

## 背景

任务 42 已经做好"做对之后能看的参考答案"：
- 格式见 `docs/problem-format.md`（v1.11 的 `standard.*` 和 `standard.md`）；
- 写法规范见 `docs/teaching-design.md` 的「参考答案的写法」；
- 校验脚本是 `scripts/curriculum/verify_standard.py`；
- 5 道示范：`py-0a-409-write-cheaper-price`、`py-0a-104-write-flower-bed`、`algo-1-007-two-sum`、`algo-2-020-fixed-window-average`、`sql-0-001-book-titles`。

用户要求（2026-11-23）："要确保代码优雅简洁，以教学为核心，禁止防御型写作"，说明选"简短说明"。

**动笔前先读写法规范和 5 道示范**，照它们的深浅和语气写。

## 范围

训练（`problems/train/`）和手搓 LLM（`problems/llm/`），DS 运行环境。

范围内每道代码题（`format` 不是 `predict` / `inspect`）都写 `standard.py` 和 `standard.md`。已经有参考答案的跳过。

## 怎么写

- **先读题**：`statement.md`、`problem.yaml`（`skills`、`mode`、`entry`）、`tests.json` 或 SQL 的数据集，再看现有的 `solution.py`。
- **从参考解出发**：`solution.py` 已经是简洁、地道的写法，就直接用它当标准写法，只写说明。参考解啰嗦、有防御性写法、变量名含糊，或者复杂度不是最优，就写一份更好的。
- **技能范围**：标准写法只能用本题 `requires ∪ introduces` 及其前置里的技能（和参考解同一规则）。超纲但更地道的写法，放进 `## 进阶写法`。
- **绝对不要改** `problem.yaml`（尤其是 `requires`）、`solution.*`、测试、数据集和任何脚本。规则卡住写不下去，就退一步写在范围内能写出的最好版本。
- **说明**：`## 思路` 2–4 句；`## 复杂度` 按规范写；`## 写法要点` 1–3 条，写和常见写法比好在哪里，不复述代码。`## 进阶写法` 只在真的值得学时才加，别每题都加。
- **禁止防御型写法**：不校验题目保证合法的输入，不包 `try/except`，不给约束不允许的空输入写特判，不 `assert` 参数。
- 每写完一个单元就跑一次校验，不要攒到最后。

## 并行约束

- 同时还有别的参考答案任务（其他线或其他阶段）和平台任务 41 在跑。只在自己范围内的题目目录里**新建** `standard.*` / `standard.md`，不改别的文件。
- 校验脚本偶尔因为 41 正在改公共脚本而出现导入错误，这时等一分钟重试，**不要去修脚本**。

## 验收标准

- `cd server && .venv/bin/python ../scripts/curriculum/verify_standard.py --track train && .venv/bin/python ../scripts/curriculum/verify_standard.py --track llm`：范围内全部通过，汇总里"有参考答案"的数量等于范围内代码题的数量。
- `cd server && .venv/bin/python ../scripts/curriculum/check_curve.py`：0 错。
- `git status` 里只有范围内新增的 `standard.*` 文件，没有任何修改过的已有文件。
- 报告写：
  - 范围内代码题数、写了几份、其中几份直接沿用参考解、几份重写了；
  - 重写的那些逐题一句话写原因，比如"参考解用双重循环，改成哈希一趟"；
  - 挑 **8 道关键题**（核心套路、最容易写啰嗦的），贴出标准写法和 `standard.md` 全文，供主控抽查。
