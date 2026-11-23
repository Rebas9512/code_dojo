# 14 · 算法与数据结构 阶段 4「进阶」：题 + 课

## 背景

算法线阶段 1 已由 04 号任务写完（`problems/algo/1/`）。这次照同样的做法写阶段 4。**动手前先读 04 号任务的交付**：
- 运行报告 `codex/runs/04-algo-s1-*/report.md`
- 几道阶段 1 的题
- 阶段 1 的课文件

格式、测试密度、`wrong_examples`、课的写法都要和阶段 1 保持一致。

规划在 `docs/curriculum.md` 的「阶段 4：进阶」，共 骨架 70 题 + 阶梯题 10 道。题目顺序、每题引入的新技能、里程碑以那张表为准。

用户的要求：
- 骨架用 NeetCode 250。
- 全部必修。
- 题面用自己的话重写，测试自己写（版权）。
- 会员题换成原创同构题。

**并行**：别的任务在同时写其他线、其他阶段，先读 `codex/PLAN.md`。你只负责算法线阶段 4。

## 要做的事

### 1. 题（`problems/algo/4/`）

- **编号**：题号 `algo-4-NNN-slug`，NNN 从 001 起，按表的顺序编。order 从 10 起、步长 10。
- **骨架题**：
  - 写 `leetcode: <slug>`、`milestones`。
  - 题面自己写，可以换场景，题意和输入输出约定不变。
  - 测试自己构造。
- **3 道会员题换成原创替代**：`meeting-rooms`《一个人能参加全部会议吗》、`meeting-rooms-ii`《最少需要几间会议室》、`alien-dictionary`《外星字母表的顺序》。
  - 每道写 `replaces_premium: <原题 slug>`、`source: original`。
  - 思路照 curriculum.md 的替代题表。
  - 外星字母表有多种合法顺序时，要用 checker。
- **阶梯题（桥）**：按表里的标题和要引入的技能写。
- **测试**：
  - 样例至少 2 个，隐藏用例至少 3 个，要覆盖边界。
  - 要有性能用例：暴力解应该超时，正解能过。
  - 每题写 `wrong_examples`，并确认它们挂掉至少一个用例。
- **DP 题**：课里先讲"状态 → 转移 → 初值 → 顺序"四步，示例同时给自顶向下（`@cache`）和自底向上两种写法。判题镜像支持深递归。
- **字典树**：设计题用 class 模式。
- **技能标注**：
  - `requires` 只能用已引入的技能：Python 基础线全部算已学，再加上算法线阶段 1 到本阶段前面题引入的技能。
  - `introduces` 最多 1 个。
  - 识别表缺规则时，在 `PY_*` 表里加行，只加不改。

### 2. 技能卡和课

- **技能卡**：`problems/algo/skills.yaml` 里阶段 4 的技能卡扩写成完整知识卡，只改阶段 4 的条目。
  - `group` 已经由 02m 号任务按小节加好。小节对应 `track.yaml` 阶段 4 的 `units`。
  - 你新增的阶梯技能也要给 `group`。
  - 题目归哪个单元默认由技能推算。只用到前置线技能的练习题会推错（04 号任务遇到过：9 道栈题被归到了数组与哈希）。这种情况在 `problem.yaml` 里写 `unit: N` 指定，规则见格式文档。交付前用 `/api/tracks` 核对每个单元的题数，写进报告。
- **课文件**：`problems/algo/lessons/algo-4-lNN-…/lesson.yaml`，按小节分（字典树、区间、贪心、一维 DP、二维 DP、高级图论），每个小节一个或两个文件。
  - 每个技能都要有：讲解（read，配复杂度直觉和"什么时候想到这个套路"）、可运行示例（example，带步骤名）、针对常见误解的小测（quiz）。
  - 示例要能在 playground 里跑出注释写的结果。

### 3. 文档

- `docs/curriculum.md` 阶段 4 小节：标"已写"、写实际题数。顺序有调整就同步，并写理由。
- `docs/teaching-design.md` 算法部分：补上阶段 4 的误解，编号接着 AM 往下编。

## 验收标准

1. `cd server && .venv/bin/python ../scripts/verify_bank.py --only algo-4 --jobs 4` 全过。
2. `server/.venv/bin/python scripts/curriculum/check_curve.py --track algo`：阶段 4 范围内 0 错 0 警，计划覆盖照旧满足。
3. 报告里列出：
   - 骨架题数、阶梯题数、题型统计
   - 骨架题的 LeetCode slug 清单
   - 哪些题用了 checker、class 模式或 treenode / listnode 转换
