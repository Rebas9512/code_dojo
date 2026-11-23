# 04 · 算法与数据结构 阶段 1「基础数据结构」：题 + 课

## 背景

算法线（`problems/algo/`）是 01 号任务从 Python 线拆出来的。技能在 `problems/algo/skills.yaml`，前缀 `algo.`，前置可以跨线指向 `py.*`。阶段 1 的技能卡目前只写了要点，题和课都还没写。

规划在 `docs/curriculum.md` 6.3 节「阶段 1：基础数据结构」，共 73 题：
- 骨架 53 题：NeetCode 250 的数组与哈希、栈、链表，加上热题 100 的补充。
- 阶梯题 20 道（"桥"）。

题目顺序、每题引入的新技能、里程碑都以那张表为准。

用户的要求：
- 骨架用 NeetCode 250。
- 全部必修。
- 题面不搬运原题，用自己的话重写，测试也自己写（版权）。
- 会员题换成原创同构题。

**并行**：别的任务在同时写 Python 线和 SQL 线，先读 `codex/PLAN.md`。你只负责算法线阶段 1。

## 要做的事

### 1. 题（`problems/algo/1/`）

- **编号**：题号 `algo-1-NNN-slug`，NNN 从 001 起，按表里的顺序编。order 从 10 起、步长 10。
- **骨架题**：
  - 写 `leetcode: <slug>` 和 `milestones`（`blind75` / `nc150` / `top100`，照表），`source` 照格式文档填。
  - 题面用自己的话重写，可以换场景，但要保持同一个题意和同样的输入输出约定。样例和测试全部自己构造。
  - `encode-and-decode-strings` 是会员题，写原创替代题《打包与拆包：把字符串列表编成一个字符串》，`replaces_premium: encode-and-decode-strings`、`source: original`。思路见 curriculum.md 的替代题表。这道题有两个函数，用 class 模式，或者用 checker 比对"编码再解码等于原输入"，你选，写进报告。
- **阶梯题（桥）**：按表里的标题和要引入的技能写，作用是让骨架题前每次只多一个新点。可以用预测、补全、改错、独立写任意题型。
- **判题模式**：
  - 链表题用 `convert: listnode`（看现有夹具 `server/tests/fixtures/problems/algo/1/` 和格式文档）。
  - 设计题（如最小栈）用 class 模式。
  - 多解的题用 `unordered` 或 checker。
- **测试**：
  - 样例至少 2 个，隐藏用例至少 3 个。覆盖空输入、单元素、重复、负数、最大规模（性能用例：O(n²) 应该超时、O(n) 能过，时限照格式文档默认）。
  - 每题写 `wrong_examples`（典型错误或低效解法），并确认它们挂掉至少一个用例。
- **技能标注**：
  - `requires` 只能用已引入的技能：Python 基础线的 `py.*` 全部算已学，再加上阶段 1 前面题引入的 `algo.*`。
  - `introduces` 最多 1 个。
  - `check_curve.py` 用 AST 核对参考解。识别表缺规则（比如 `collections.deque`、`heapq`）时，可以在 `PY_*` 表里加行，只加不改。

### 2. 技能卡和课

- `problems/algo/skills.yaml`：把阶段 1 的技能卡从"要点"扩写成完整知识卡，写法比照 Python 线 0A 的卡。只改阶段 1 的条目。
- 给阶段 1 的每个技能加 `group` 字段，首页地图靠它把技能分进单元：数组与哈希是 1，栈是 2，链表是 3。阶梯题引入的技能，按它所在的小节归组。单元名由 02m 号任务写进 `track.yaml`，你不用改 track.yaml。
- 课文件写在 `problems/algo/lessons/algo-1-lNN-…/lesson.yaml`，按小节分：数组与哈希、栈、链表各一到两个文件。
  - 格式照 `docs/problem-format.md` 的课一节。
  - 每个阶段 1 技能都要有：讲解（read，配复杂度直觉）、可运行示例（example，带步骤名，要能在 playground 跑出注释写的结果）、针对常见误解的小测（quiz）。
  - 链表示例要能在 playground 里跑，自己在示例代码里定义 ListNode。

### 3. 文档

- `docs/curriculum.md` 阶段 1 小节：标"已写"、写实际题数。顺序有调整就同步表格，并写明为什么。
- `docs/teaching-design.md`：在算法部分加阶段 1 的误解目录，比如哈希表存值还是存下标、栈空时 pop、链表断链和丢头。编号用 `AM01` 起。

## 验收标准

1. `cd server && .venv/bin/python ../scripts/verify_bank.py --only algo-1 --jobs 4` 全过，所有题的参考解都 accepted。
2. `server/.venv/bin/python scripts/curriculum/check_curve.py --track algo`：阶段 1 范围内 0 错 0 警。计划覆盖（NeetCode 250）照旧满足。
3. 报告里列出：骨架题数、阶梯题数、题型统计；每道骨架题对应的 LeetCode slug 清单；哪些题用了 checker 或 class 模式。
