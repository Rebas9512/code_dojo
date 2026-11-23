# code-dojo 学习曲线设计

> 2026-11-22 起草，同日按用户决定改为**零基础设计 + 题课合一**（docs/problem-format.md v1.4）。落实 `docs/README.md` 第 2 节"学习路线和学习曲线"的机制，给出三条线（Python 基础、算法与数据结构、SQL）从第一题到面试水平的完整路径。
> 每个技能怎么教（心智模型、具名误解、示例、小测）见 `docs/teaching-design.md`；题目文件格式见 `docs/problem-format.md`；骨架题单的依据见 `docs/reports/2026 技术面试 高频题单 调研.md`。
> 本文的题单表格最初由 `lists.json` 生成，之后直接编辑本文即可；`scripts/curriculum/check_curve.py` 会核对 `plan:python` + `plan:algo` / `plan:sql` 区块恰好覆盖 NeetCode 250（+ 热题 100 补充 + 阶段 5 题池）和 SQL 50 各一次。

## 0. 一页总览

| | Python 基础 → 算法与数据结构 | SQL |
|---|---|---|
| 路线 | 认识数据 → 0A 语法（11 组）→ 0B 算法入门 → 1 基础数据结构 → 2 核心套路 → 3 树和图 → 4 进阶 → 5 面试混合 | 认识数据 → 0 单表 → 1 聚合 → 2 连接 → 3 子查询和 CTE → 4 窗口函数 → 5 综合 |
| 技能图 | `problems/python/skills.yaml`：70 个技能，`problems/algo/skills.yaml`：48 个技能 | `problems/sql/skills.yaml`：59 个技能 |
| 骨架 | NeetCode 250 + 热题 100 补充 17 题 + 阶段 5 题池 69 题；7 道会员题换成原创同构题 | SQL 50（按"用到的最高概念"重排） |
| 阶梯题（计划） | 0A 约 200、0B 约 31、阶段 1–5 约 60 道桥题 | 阶段 0–5 约 43 道桥题（书店库） |
| 已写好 | 0A 第 0–10 组 207 题 + 11 个课文件（61 个技能）；0B 九个单元 31 题 + 9 个课文件（9 个技能） | 阶段 0 书店题 44 题 + 4 个课文件（19 个技能）+ 书店数据库 |

一道题从"第一次见到某个语法"到"面试题"中间的每一步都只多一个新点：0A 以 61 个技能覆盖语法和容器选择，0B 把常用的小套路（线性查找、双下标、前缀和、栈、矩阵、计时）单独练熟，阶段 1–5 在每个新套路前放 1–3 道"桥题"，桥题本身也只引入一个技能。每个技能都有一段按零基础写的教学内容（课），挂在用到它的题旁边。

## 1. 设计原则

1. **按零基础设计。** 每个技能都默认读者从没学过：先讲"是什么、为什么"，再给带步骤名的示例，然后才让人写。会的人不需要内容侧做任何"跳过"设计——做题页默认打开题目，能做就直接做，不会做再切到"课"（第 4 节）。
2. **每题最多引入 1 个新技能**，并且这个技能的前置都已经引入过。新技能 = 新语法（AST / SQL 能识别）或新套路（只能人工标注）。
3. **参考解和示例都不能偷用没学过的东西。** 参考解会展示给学习者（题解、预测题），示例代码就在课里；它们用到的语法必须都在已学范围内——由检查脚本自动核对（第 5 节）。
4. **每个技能一条完整的阶梯：预测 → 补全 →（改错）→ 独立写**，之后是变式和组合。核心是"独立写"。
5. **难度细分。** `difficulty` 1–100，同一阶段内大致递增（预测 / 补全是脚手架，不参与递增检查）。标定：0A 1–25，0B 20–35，LeetCode 简单约 30–45，中等约 45–75，困难约 75–100。

## 2. 题型阶梯

### 2.1 题型与作答方式

| 题型 `format` | 学习者做什么 | 判题模式 `mode` | 典型用时 | 用在哪 |
|---|---|---|---|---|
| `inspect` 看数据作答 | 阅读数据，写短答案或选一项 | `inspect` | 1–3 分钟 | 认识数据、SQL 读结果与表结构 |
| `predict` 预测 | 读程序，写出它打印的全部内容 | `predict` | 1–2 分钟 | 新语法的第一题：先读懂再写；程序专门针对一条具名误解 |
| `complete` 补全 | 代码给了大半，把 `____` 换成正确代码 | `function` / `stdio` | 1–3 分钟 | 新语法第一次动手，只写新的那一小块 |
| `fix` 改错 | 代码有一个 bug，题面描述错误现象 | 同上 | 2–5 分钟 | 常见坑：差一错误、条件顺序、初始值、字符串拼接、AND/OR 优先级、NULL |
| `write` 独立写 | 只给签名（SQL 只给表），从空白写起 | 同上 | 2–10 分钟 | **核心**；计入掌握 |
| `variant` 变式 | 和刚写过的题同一个技能，换一个外壳或条件 | 同上 | 2–8 分钟 | 防止"背答案"；计入掌握 |
| `combine` 组合 | 把新技能和 1–2 个旧技能组合起来 | 同上 | 5–15 分钟 | 组末尾；计入掌握 |

约定：
- `complete` 的空用 `____`（四个下划线，是合法的 Python 名字），起始代码能被解析，空没填时运行会失败。SQL 的补全题同理。
- `fix` 的 bug 必须在 **examples** 上就能看到（点"运行"就失败），不只是在隐藏用例里——由 `verify_python.py` / `verify_sql.py` 检查。
- `predict` 程序必须是确定的（两次运行输出一致），不依赖随机数、时间、集合遍历顺序。
- SQL 没有预测题型（见第 9 节），预测放在课的小测里（"这条查询返回几行""这一本得到哪个标签"）。
- SQL 代码题默认比较查询结果。修改类题用 `mode: dml`，运行单条修改语句后比较 `check_query` 读出的最终状态。

### 2.2 每个技能的阶梯怎么搭

- **语法技能**（0A、0B）：`predict` 引入（程序针对这个技能最常见的误解）→ `complete`（只挖新语法那一块）→ `fix`（常见坑，可选）→ `write` → 后面的 `variant` / `combine` 再用到。0A 第 0–10 组按技能安排不同长度的阶梯（第 6.1 节）。
- **套路技能**（阶段 1–5）：桥题引入（自写，规模小、只练这个套路）→ 骨架题里最简单的一道 → 同类骨架题 → 后面的组合题。
- **骨架题前的阶梯**：新套路前放 1–3 道桥题，每道只多一个点。例：Two Sum 的阶梯是 0A 的"列表里有没有这个数"（`in`）→ 0A 第 7 组"统计每个数出现几次" → 阶段 1 桥题"记录每个值第一次出现的下标" → 0A 的"两数之和（暴力版）"（py-0a-056）→ Two Sum（哈希一次遍历）。
- **焦点技能**：一道题练的是哪个技能——有 `introduces` 就是它；否则是 `requires` 里在学习顺序中**最晚引入**的那个。平台据此统计掌握（建议加显式字段，见第 9 节）。

## 3. 掌握规则与节奏

### 3.1 技能状态

```
未学 ──引入题通过──▶ 学习中 ──两道不同计入题独立写对──▶ 掌握
                                                      │  ▲
                                到期、复习失败或闲置 21 天  │  │ 复习通过且满足掌握条件
                                                      ▼  │
                                                      需复习
```

- **计入题**：认识数据根线的 `inspect` 题计入；代码练习中，`format` 是 `write` / `variant` / `combine`，并且技能在这道题的 `requires ∪ {introduces}` 里。`predict` / `complete` / `fix` 不计入（有脚手架）。
- **掌握** = 至少 2 道**不同的**计入题"独立写对"：首次提交通过、没看任何提示（作者提示和 AI 提示都算）、没看题解（2026-11-22 用户确认）。看过题解的题自动进重写队列，本次不计。
- 引入题通过即进入学习中。直接做计入题取得独立通过也能开始累计。每题可给多个用到的技能记分，同一道题反复写对只计一道。采纳过助教修改也会失去本轮独立资格。运行样例不占首次提交。
- **需复习**：已掌握技能有复习到期，或满 21 天没有正式提交用到它，就显示需复习。复习失败会立即标记原题的技能。独立复习通过后，按当前累计题数、其余到期题和最近使用时间重新判定。
- **间隔**：独立通过后从次日起，按 1、3、7、21、60 天复习，之后维持 60 天。从复习入口打开只给 starter 或空答案。第二轮起优先选同线、同焦点、尚未提交的另一道计入题，优先匹配 `introduces`。没有固定题时，可以在原题下生成同套路附加题。复习失败后次日再练。
- **重写**：打开完整题解即排到明天。AI 修改后通过，或计入题在提示、重试后通过，也从次日重写开始。重写独立通过后，计入题重新从 1 天起排期。复习和重写单独记为 `review`。

### 3.2 选下一题

默认按学习顺序（stage → order）往下走。一题可选当且仅当：
1. `requires` 里的技能都已不是"未学"（学习中也可以——学习中的技能正需要练）；
2. 如果有 `introduces`：本线直接前置按掌握规则检查，跨线前置达到“已学”即可；
3. 全站已有 3 个技能处于学习中时，先挑练这些技能的计入题；引入第 4 个技能的题暂缓推荐。题目列表仍可自由打开。

到期的复习题优先，逾期最久的在前。今日计划的每日上限默认为 5，可设为 0，已经做过的复习扣除当天名额。地图和题目页的“继续”取所在单元或学习线的推荐，今日计划另外列出各条开放学习线的下一道新题。

### 3.3 卡住时

- 统计最近 10 次"首次提交"（不含 `predict`）的通过率，目标 70–85%。
- 满 10 道且低于 70%，或当前焦点技能最近两道计入题的首次提交都失败，题面就给出回退建议。实际实现直接读技能图，优先挑尚未掌握的直接前置，再挑练它的低难度题。根技能使用同技能小题。学习者也可以点按钮让助教出题；有前置小题时附加题挂在它下面。出题时指定目标技能，并用第 5 节同一套 Python AST / SQL 规则核对参考解，允许目标技能和已掌握的技能。人工标注的套路由出题要求约束。推荐过程无需调用 AI。
- 内容侧不设计"跳过"逻辑：会的人直接做题，平台上"跳过教学、直接做题"就是默认行为（第 4 节）。

## 4. 课：按技能写的教学内容（题课合一）

用户 2026-11-22 的决定："每一题我们可以对应一节课（不用做成两个部分），上来我们可以看到题，如果能做就直接做了，做不了我们切到上课部分"。所以：

- **题目列表里只有题**。做题页左栏有两个标签：**题目**（默认）和**课**。
- **课的内容按技能写**，放在 `problems/<track>/lessons/<id>/lesson.yaml`：一个文件讲一组相关技能（0A 每组一个文件，SQL 阶段 0 四个文件，认识数据两个文件），每一步标明讲哪个技能。每个技能只在一个文件里讲。
- 一道题的"课"标签 = 它 `introduces` 的技能的教学内容（展开、放最前）+ 它 `requires` 的技能（折叠）。AI 助教的上下文里也带上这些内容。
- 每个技能的教学内容 = **讲解**（read，150–500 字：是什么、为什么 → 怎么写 → 点名常见误解）+ **示例**（example，可运行、可修改；用 `# ①` 注释给步骤起名字，附一句"改成……再运行"）+ **小测**（quiz，0–2 道单选，每道针对一条具名误解）。
- 题目阶梯（预测 → 补全 → 改错 → 独立写 → 变式 → 组合）不变，就是每个技能的练习。

已写好的课文件：

| 文件 | 讲的技能 | 对应的题 |
|---|---|---|
| `data-0-l01-values` | 读表、值的种类、数量与标签、缺失值 | 认识数据第 1–4 单元 |
| `data-0-l02-shapes` | 列类型和主键、形状、CSV 和 JSON | 认识数据第 5–7 单元 |
| `py-0a-l00-values` | 显示值、五种类型、变量、运算、转换、输入和比较 | 0A 第 0 组 |
| `py-0a-l01-basics` | 定义和调用函数、整除和取余、f-string | 0A 第 1 组 |
| `py-0a-l02-conditions` | if / else、提前 return、elif、and / or / not、abs / min / max / round | 0A 第 2 组 |
| `py-0a-l03-loops` | for 和 range、累加器、while、打擂台、break / continue、嵌套循环 | 0A 第 3 组 |
| `py-0a-l04-strings` | 下标和 len、for 直接遍历、in、切片、字符串方法、ord / chr | 0A 第 4 组 |
| `py-0a-l05-lists` | 列表基础、append、sum / max / min、enumerate、同时赋值、split / join、pop、`[0] * n`、二维列表 | 0A 第 5 组 |
| `py-0a-l06-functions` | 辅助函数、默认与关键字参数、隐式返回、列表别名 | 0A 第 6 组 |
| `py-0a-l07-dicts-sets` | 按键查找、缺键默认值、计数、遍历、分组、集合 | 0A 第 7 组 |
| `py-0a-l08-sequences` | 元组、排序键、三种推导式、生成器表达式、zip、条件表达式、四种容器的选择 | 0A 第 8 组 |
| `py-0a-l09-classes` | 实例属性、方法、节点引用 | 0A 第 9 组 |
| `py-0a-l10-recursion` | 基线与回程、序列的后缀与边界、多分支调用树 | 0A 第 10 组 |
| `py-0b-l01-scan` | 扫描已排除的位置、已读记录的次数 | 0B 线性查找与最值、计数 |
| `py-0b-l02-reverse`、`py-0b-l03-two-index` | 原地交换两端、有序序列各走一个下标 | 0B 反转与交换、双下标 |
| `py-0b-l04-prefix`、`py-0b-l06-simulate` | 边界上的累计值、逐步更新游戏状态 | 0B 前缀和、模拟 |
| `py-0b-l07-matrix` | 行列坐标、方向与边界 | 0B 矩阵遍历 |
| `py-0b-l08-stack`、`py-0b-l08-queue` | 字符撤销、请求的时间窗口 | 0B 栈和队列 |
| `py-0b-l09-growth` | 比较增长速度、给两种重复查找写法计时 | 0B 复杂度直觉 |
| `sql-0-l00-tables` | 查看整张表、读列的类型、可空性和主键 | SQL 阶段 0 开头 |
| `sql-0-l01-select-where` | SELECT、计算列和别名、WHERE、AND / OR、IN、BETWEEN、LIKE | SQL 阶段 0 前半 |
| `sql-0-l02-null-order` | IS NULL、COALESCE、ORDER BY、LIMIT、DISTINCT、CASE | SQL 阶段 0 后半 |
| `sql-0-l03-functions` | 字符串函数、日期函数、ROUND 和类型转换、正则 | SQL 阶段 0 的 150–157，每个技能各有一道补全和一道独立写 |

每个模块的教学设计（核心心智模型、具名误解及对应的预测 / 改错题、示例的步骤名、补全怎么逐步挖空、之后练哪些题）见 `docs/teaching-design.md`。

## 5. 平滑性检查：脚本强制的规则

`scripts/curriculum/check_curve.py`（内容侧，改题库就跑；只依赖标准库 + PyYAML）：

| 检查 | 规则 | 级别 |
|---|---|---|
| 技能图 | id 唯一、本线 `skill_prefix` 前缀 + kebab-case；前置都存在；**无环**；前置的阶段不晚于自己；必修技能不能以选修技能为前置；每个技能有名字和 ≤ 20 行的知识卡 | 错误（卡片超长为警告） |
| 题目文件 | id = 文件夹名、前缀 `<skill_prefix>-<stage>-<三位序号>-`；stage 与所在文件夹一致；同阶段 `order` 不重复；`format` 合法；`predict` ⇔ `mode: predict`；`complete` / `fix` 有 starter；function 模式有 entry 和 signature；difficulty 是 1–100；`optional` 是布尔值；`replaces_premium` 只能是那 7 道会员题之一且 `source: original`；`wrong_examples` 每项有 `why` 和 `sql` / `code`；v1.1 的 `in_lesson` 已取消 | 错误 |
| 学习顺序 | 按 stage → order 走一遍：`requires` 必须都已被前面的题引入；`introduces` 至多 1 个、不能重复引入、它的前置必须都已引入、不能同时出现在 `requires` 里 | 错误 |
| 参考解用到的语法 | Python 用 AST、SQL 用规范化后的正则扫描参考解，把识别到的构造映射成技能；识别出的技能必须在 `requires ∪ {introduces}` **及它们的全部前置**之内（`--strict` 时只允许声明的技能本身） | 错误 |
| 选修 | 必修题（`optional` 不为 true）不能用到只在选修题里引入的技能 | 错误 |
| 课文件 | 只有 id / title / track / skills / steps；步骤只有 read / example / quiz，每一步的 `skill` 属于本文件的 skills；quiz 的 answer 在选项范围内；SQL 示例写存在的 db；每个技能最多在一个文件里讲；文件里列出的技能都有内容 | 错误 |
| 课覆盖 | 每个被某道题 `introduces` 的技能都有至少一段 read 和一个 example | 错误 |
| 示例只用学过的 | 示例代码用到的技能只能是：这个技能、它的前置、学习顺序里更早引入的技能 | 错误 |
| 课的写法 | 讲解 100–900 字；Python 示例有 `# ①` 步骤名；每个技能小测不超过 2 道；第一步是 read | 警告 |
| 引入了却没用 | `introduces` 的技能是可识别的语法，但参考解里没出现 | 警告 |
| 缺少引入题 | 活跃学习线上，技能所在阶段已有题，且整条线没有一道题用 `introduces` 引入该技能。规划中的线与尚无题的阶段跳过 | 警告 |
| 难度 | 同阶段内（不算预测 / 补全）比前面最高难度低 6 以上 | 警告 |
| 计划覆盖 | 本文 `plan:python` 和 `plan:algo` 区块合计恰好覆盖 NC250 + 热题 100 补充 + 阶段 5 题池各一次；`plan:sql` 区块恰好覆盖 SQL 50 各一次 | 错误 |
| 实际覆盖 | 活跃学习线的阶段只要已有一道题，计划表列在该阶段的每个骨架题 slug 都必须出现在本线、本阶段某个 `problem.yaml` 的 `leetcode` 字段中。标“桥”的行是阶梯题。规划中的线和还没有题的阶段跳过。`--track` 限定实际覆盖的学习线 | 错误 |

**为什么允许"前置闭包"**：掌握一个技能意味着已经掌握它的前置（比如 `py.early-return` 的前置里有 `py.if-else`），否则每道题的 `requires` 会越写越长，"课"标签里折叠的相关技能也会变成噪音。`requires` 只需要写"这题直接要用、而且不是其他声明技能的前置"的那些。

**识别表**（都在脚本开头，扩展时只改表）：
- Python：`PY_NODE_SKILLS`（结构：赋值、运算符、if/elif、for-range 与 for-each、while、break、嵌套循环、下标 / 切片 / 二维下标、列表 / 字典 / 集合 / 元组字面量、交换赋值、推导式、lambda、key=、函数定义的种类、提前 return、递归与多分支递归、类与方法、try、yield、nonlocal）、`PY_CALLS`（内置函数，`min/max` 按参数个数分两个技能）、`PY_METHODS_DEFAULT` + `PY_METHODS_BY_TYPE`（方法名；能从类型标注或赋值推断出接收者类型时按类型映射）、`PY_IMPORTS`、`PY_ATTRS`。function 模式题目给定的函数、predict / stdio 程序和课示例里的**第一个**函数都算 `py.func-return`，第二个及以后的顶层函数才算 `py.helper-func`。没登记的调用 / 方法 / import 会报警告或错误，提醒补表。
- SQL：`SQL_RULES`（正则）+ `SQL_FUNC_RULES`（别名、算术、AND/OR/NOT、各种连接、子查询）。
- **识别不了的**：纯套路技能（累加器、打擂台、双指针、滑动窗口、Top-N 每组、留存……）只能靠人工标注；检查脚本保证它们出现在正确的位置和顺序上，但不核对参考解"是否真的用了这个套路"。

**配套的本地校验**（同目录）：
- `verify_python.py`：用本机 CPython 3.14（`uv run --python 3.14`）跑每道 Python 题的参考解和全部用例；预测题打印程序输出供人工核对；`fix` 的 starter 必须在 examples 上就失败，`complete` 的 starter 必须失败；运行课里每个示例（带它的 stdin），必须正常结束并有输出。比较规则与 `judge/python/harness.py` 一致。
- `verify_sql.py` + `pglite_runner.mjs`：在 Node 22 的 PGlite（PostgreSQL 18.7）上跑每道 SQL 题的参考解；打印每个数据集上的结果；每条 `wrong_examples` 必须能运行，并且至少在一个**隐藏**数据集上和参考解结果不同；课里每个 SQL 示例在书店库上必须能运行。

```bash
python3 scripts/curriculum/check_curve.py          # 平滑性 + 课 + 计划覆盖
python3 scripts/curriculum/verify_python.py -q     # 自动切到 CPython 3.14
cd scripts/curriculum && npm install && cd -       # 第一次
python3 scripts/curriculum/verify_sql.py -q
```

## 认识数据根线

Python 和 SQL 的地图共用七个起步单元。默认先做完这 20 道看数据作答题，再进入任一门语言。19 道要求输入短答案，题面按需要给表格、原文或一串值；正式作答计入进度。样例来自同一个书店，前三个单元的数据都完整。学习者到第四单元才会在记录里遇到缺失字段。

| 单元 | 技能 | 在书店数据上做什么 | 题量 |
|---|---|---|---|
| 一张表 | `data.table-intro` | 数行列，查售罄记录，判断表里有无销量 | 3 |
| 值的种类 | `data.value-kinds` | 辨认文字、数与真假值 | 3 |
| 数量还是标签 | `data.quantity-vs-label` | 判断哪些列能求平均，保存号码 | 2 |
| 缺失值 | `data.missing` | 找空城市，区分零库存，选择平均数的分母 | 3 |
| 类型和主键 | `data.column-type-key` | 用编号区别同名版本，找出混入文字的价格 | 3 |
| 数据的形状 | `data.shapes` | 区分五种形状，按行或列定位数据 | 3 |
| CSV 和 JSON | `data.text-formats` | 读空字段、嵌套订单和未经转换的价格 | 3 |

`py.print` 引用值的种类，Python 容器引用形状；`sql.select-star` 引用读表，`sql.schema-types` 引用类型、主键和缺失。检查学习顺序时，前置线的技能视为已学。

## 6. Python 基础与算法路线

### 6.1 0A 语法基础（11 组，207 题）

每组一个课文件。组内每个技能按"预测 → 补全 →（改错）→ 独立写"排题，新技能多从预测或补全开始，程序专门暴露一条具名误解（见 `docs/teaching-design.md`）。第 6 组原计划的"提前 return"提前到第 2 组：function 模式从第一题起就要 `return`，在 if 里直接 return 是最自然的写法。

| 组 | 技能（按引入顺序） | 每组题数 |
|---|---|---|
| 0 值和类型 | print → value-types → var-arith → type-ops → type-convert → stdio-input → compare-bool | 20（已写） |
| 1 函数、整除和格式化 | func-return → floordiv-mod → fstring | 12（已写） |
| 2 条件和布尔 | if-else → early-return → elif → bool-ops → minmax-abs | 17（已写） |
| 3 循环 | for-range → accumulator → while → running-max → break-continue → nested-loop | 21（已写） |
| 4 字符串 | index-len → for-each → in-membership → slice → str-methods → ord-chr | 19（已写） |
| 5 列表 | list-basics → list-append → list-builtins → enumerate → multi-assign → split-join → list-pop → list-concat-repeat → nested-list | 29（已写） |
| 6 函数 | helper-func → default-args → none → aliasing | 15（已写） |
| 7 字典和集合 | dict-basics → dict-get → dict-counting → dict-iter → dict-grouping → set-basics | 21（已写） |
| 8 元组、排序、推导式 | tuple → sorted → sort-key → list-comp → dict-set-comp → genexp → zip → ternary → choose-container | 29（已写） |
| 9 类 | class-basic → class-methods → node-class | 12（已写） |
| 10 简单递归 | recursion → recursion-seq → recursion-multi | 12（已写） |

第 6–10 组共有 89 道必修题，每组最后一道是组合题。下表按做题顺序列出。

<!-- plan:python -->

**第 0 组：值和类型**（已写 20 题；课：`py-0a-l00-values`）

| 题目 | 标题 | 题型 | 新技能 | 难度 |
|---|---|---|---|---|
| `py-0a-001-hello-print` | 第一行输出 | 预测 | `py.print`（print 显示一个值） | 1 |
| `py-0a-101-write-greeting` | 写出三行问候 | 独立写 |  | 1 |
| `py-0a-400-predict-value-types` | 五种值各叫什么 | 预测 | `py.value-types`（五种值和 type()） | 2 |
| `py-0a-401-predict-digit-text` | 看起来像数的文字 | 预测 |  | 2 |
| `py-0a-002-predict-variables` | 变量和算术 | 预测 | `py.var-arith`（变量、赋值和算术） | 2 |
| `py-0a-102-predict-names` | 名字跟着谁走 | 预测 |  | 2 |
| `py-0a-103-complete-order-total` | 补全：订单总价 | 补全 |  | 2 |
| `py-0a-104-write-flower-bed` | 花坛的面积和周长 | 独立写 |  | 2 |
| `py-0a-402-predict-operations` | 加号遇见哪种值 | 预测 | `py.type-ops`（类型决定运算的意思） | 4 |
| `py-0a-403-complete-divider` | 补全收据分隔线 | 补全 |  | 4 |
| `py-0a-404-predict-label-copies` | 重复价签上的字符 | 预测 |  | 4 |
| `py-0a-110-predict-types` | 字符串还是数字 | 预测 | `py.type-convert`（类型转换 int / str / float） | 4 |
| `py-0a-405-fix-tag-total` | 改错：两张价签的总额 | 改错 |  | 4 |
| `py-0a-406-predict-converted-label` | 转换后前导零去了哪里 | 预测 |  | 4 |
| `py-0a-111-complete-read-multiply` | 补全：读两个数相乘 | 补全 | `py.stdio-input`（input() 读进来的是文字） | 5 |
| `py-0a-008-read-two-numbers` | 读入两个数 | 独立写 |  | 5 |
| `py-0a-407-fix-input-sum` | 改错：收银机显示了 12 | 改错 |  | 4 |
| `py-0a-009-predict-compare` | 比较的结果 | 预测 | `py.compare-bool`（比较得到真假值） | 4 |
| `py-0a-408-complete-age-check` | 补全：是否年满十八岁 | 补全 |  | 4 |
| `py-0a-409-write-cheaper-price` | 第一家更便宜吗 | 独立写 |  | 4 |

**第 1 组：函数、整除和格式化**（已写 12 题；课：`py-0a-l01-basics`）

| 题目 | 标题 | 题型 | 新技能 | 难度 |
|---|---|---|---|---|
| `py-0a-105-predict-function` | 函数调用了几次 | 预测 | `py.func-return`（定义和调用函数，return 结果） | 3 |
| `py-0a-106-complete-total-price` | 补全：总价函数 | 补全 |  | 3 |
| `py-0a-003-rectangle-perimeter` | 长方形周长 | 独立写 |  | 3 |
| `py-0a-007-add-number-strings` | 数字字符串相加 | 改错 |  | 5 |
| `py-0a-112-complete-can-vote` | 补全：到年龄了吗 | 补全 |  | 5 |
| `py-0a-004-predict-floordiv` | 整除和取余 | 预测 | `py.floordiv-mod`（整除 // 和取余 %） | 3 |
| `py-0a-107-complete-minutes-left` | 补全：不满一小时的分钟 | 补全 |  | 4 |
| `py-0a-005-digit-sum-3` | 三位数的各位之和 | 独立写 |  | 4 |
| `py-0a-010-is-even` | 是不是偶数 | 独立写 |  | 5 |
| `py-0a-108-predict-fstring` | 花括号里的值 | 预测 | `py.fstring`（f-string 格式化） | 4 |
| `py-0a-006-format-duration` | 分钟换算成小时 | 补全 |  | 5 |
| `py-0a-109-write-price-tag` | 价签 | 独立写 |  | 6 |

**第 2 组：条件和布尔逻辑**（已写 17 题；课：`py-0a-l02-conditions`）

| 题目 | 标题 | 题型 | 新技能 | 难度 |
|---|---|---|---|---|
| `py-0a-113-predict-if-else` | 走哪条路 | 预测 | `py.if-else`（if / else） | 5 |
| `py-0a-011-ticket-price` | 门票价格 | 补全 |  | 5 |
| `py-0a-114-write-absolute` | 手写绝对值 | 独立写 |  | 6 |
| `py-0a-115-predict-return-exits` | return 之后还会运行吗 | 预测 | `py.early-return`（在分支和循环里 return（提前返回）） | 6 |
| `py-0a-012-safe-divide` | 安全的除法 | 补全 |  | 6 |
| `py-0a-013-sign` | 正负号 | 独立写 |  | 6 |
| `py-0a-116-predict-if-vs-elif` | if if 和 if elif | 预测 | `py.elif`（if / elif / else 多分支） | 6 |
| `py-0a-117-complete-clothing` | 补全：穿什么 | 补全 |  | 7 |
| `py-0a-015-shipping-fee` | 快递运费 | 改错 |  | 7 |
| `py-0a-014-letter-grade` | 分数转等级 | 独立写 |  | 7 |
| `py-0a-118-predict-and-or` | and、or、not | 预测 | `py.bool-ops`（and / or / not） | 7 |
| `py-0a-119-complete-in-range` | 补全：在区间里吗 | 补全 |  | 7 |
| `py-0a-016-leap-year` | 闰年 | 独立写 |  | 8 |
| `py-0a-120-predict-builtins` | 内置函数的结果 | 预测 | `py.minmax-abs`（abs / min / max / round） | 6 |
| `py-0a-121-complete-distance` | 补全：两点的距离 | 补全 |  | 6 |
| `py-0a-017-clamp` | 限制在区间内 | 独立写 |  | 7 |
| `py-0a-018-triangle-type` | 三角形的类型 | 组合 |  | 9 |

**第 3 组：循环**（已写 21 题；课：`py-0a-l03-loops`）

| 题目 | 标题 | 题型 | 新技能 | 难度 |
|---|---|---|---|---|
| `py-0a-019-predict-range` | range 数到几 | 预测 | `py.for-range`（for 循环与 range） | 8 |
| `py-0a-122-predict-loop-variable` | 改了 i 会怎样 | 预测 |  | 8 |
| `py-0a-123-complete-count-up` | 补全：从 1 数到 n | 补全 |  | 8 |
| `py-0a-020-print-squares` | 打印平方数 | 独立写 |  | 8 |
| `py-0a-124-predict-accumulator` | 累加器每一轮的值 | 预测 | `py.accumulator`（累加器（求和、计数、累乘）） | 8 |
| `py-0a-021-sum-to-n` | 从 1 加到 n | 补全 |  | 8 |
| `py-0a-022-factorial` | 阶乘 | 变式 |  | 9 |
| `py-0a-023-count-multiples` | 3 或 5 的倍数有几个 | 改错 |  | 9 |
| `py-0a-024-predict-while` | while 循环几次 | 预测 | `py.while`（while 循环） | 9 |
| `py-0a-125-complete-halvings` | 补全：除到 0 要几次 | 补全 |  | 9 |
| `py-0a-025-count-digits` | 数字有几位 | 独立写 |  | 10 |
| `py-0a-028-is-prime` | 质数判断 | 独立写 |  | 11 |
| `py-0a-126-predict-running-max` | 擂主怎么换 | 预测 | `py.running-max`（求最值（打擂台）） | 9 |
| `py-0a-127-complete-smallest-digit` | 补全：最小的那一位 | 补全 |  | 9 |
| `py-0a-026-largest-digit` | 最大的那一位 | 独立写 |  | 10 |
| `py-0a-027-predict-break-continue` | break 和 continue | 预测 | `py.break-continue`（break / continue） | 10 |
| `py-0a-128-complete-first-multiple` | 补全：找到就停 | 补全 |  | 10 |
| `py-0a-129-write-first-over` | 加到超过为止 | 独立写 |  | 10 |
| `py-0a-029-predict-nested-loop` | 循环套循环 | 预测 | `py.nested-loop`（嵌套循环） | 11 |
| `py-0a-130-complete-even-products` | 补全：乘积是偶数的数对 | 补全 |  | 11 |
| `py-0a-030-count-pair-sums` | 和为目标的数对 | 独立写 |  | 12 |

**第 4 组：字符串**（已写 19 题；课：`py-0a-l04-strings`）

| 题目 | 标题 | 题型 | 新技能 | 难度 |
|---|---|---|---|---|
| `py-0a-031-predict-index` | 字符串下标 | 预测 | `py.index-len`（下标与 len） | 11 |
| `py-0a-131-complete-middle-char` | 补全：正中间的字符 | 补全 |  | 11 |
| `py-0a-032-count-char` | 数一数某个字符 | 改错 |  | 11 |
| `py-0a-132-write-first-and-last` | 首尾两个字符 | 独立写 |  | 11 |
| `py-0a-133-predict-for-each` | 一个一个字符 | 预测 | `py.for-each`（for 直接遍历序列） | 11 |
| `py-0a-033-count-digit-chars` | 有几个数字字符 | 补全 |  | 11 |
| `py-0a-134-predict-in` | in 判断的是什么 | 预测 | `py.in-membership`（in / not in 成员判断） | 12 |
| `py-0a-034-count-vowels` | 数元音 | 独立写 |  | 12 |
| `py-0a-035-predict-slice` | 切片 | 预测 | `py.slice`（切片） | 12 |
| `py-0a-135-complete-strip-ends` | 补全：去掉首尾 | 补全 |  | 12 |
| `py-0a-036-is-palindrome` | 回文串 | 独立写 |  | 12 |
| `py-0a-136-predict-str-methods` | 方法改了原字符串吗 | 预测 | `py.str-methods`（常用字符串方法） | 12 |
| `py-0a-137-complete-clean-word` | 补全：整理一个词 | 补全 |  | 12 |
| `py-0a-037-same-word` | 是同一个词吗 | 独立写 |  | 12 |
| `py-0a-038-leading-number` | 开头的数字 | 独立写 |  | 13 |
| `py-0a-039-predict-ord-chr` | 字符和编码 | 预测 | `py.ord-chr`（ord / chr 字符编码） | 13 |
| `py-0a-138-complete-next-letter` | 补全：下一个字母 | 补全 |  | 13 |
| `py-0a-040-caesar-shift` | 凯撒加密 | 组合 |  | 14 |
| `py-0a-041-compress-runs` | 压缩连续字符 | 组合 |  | 15 |

**第 5 组：列表**（已写 29 题；课：`py-0a-l05-lists`）

| 题目 | 标题 | 题型 | 新技能 | 难度 |
|---|---|---|---|---|
| `py-0a-042-predict-list` | 列表初见 | 预测 | `py.list-basics`（列表基础：创建、下标读写、遍历） | 13 |
| `py-0a-139-predict-loop-copy` | 循环里改 x，列表变了吗 | 预测 |  | 13 |
| `py-0a-140-complete-double-all` | 补全：每个数翻倍 | 补全 |  | 13 |
| `py-0a-043-clip-negatives` | 负数归零 | 独立写 |  | 13 |
| `py-0a-141-predict-append` | append 返回什么 | 预测 | `py.list-append`（append 构建新列表） | 13 |
| `py-0a-044-filter-evens` | 挑出偶数 | 补全 |  | 13 |
| `py-0a-045-running-sum` | 累计和 | 独立写 |  | 14 |
| `py-0a-046-find-max` | 手写求最大值 | 改错 |  | 14 |
| `py-0a-142-predict-list-builtins` | sum、max、min | 预测 | `py.list-builtins`（sum / min / max / len 作用于列表） | 14 |
| `py-0a-047-score-summary` | 成绩概览 | 独立写 |  | 14 |
| `py-0a-143-predict-enumerate` | enumerate 给出了什么 | 预测 | `py.enumerate`（enumerate 同时拿下标和值） | 14 |
| `py-0a-144-complete-positions` | 补全：所有出现的位置 | 补全 |  | 14 |
| `py-0a-048-find-index` | 第一次出现的位置 | 独立写 |  | 15 |
| `py-0a-145-predict-swap` | 两种交换写法 | 预测 | `py.multi-assign`（同时赋值与交换） | 14 |
| `py-0a-049-reverse-in-place` | 原地反转列表 | 补全 |  | 15 |
| `py-0a-146-write-swap-ends` | 首尾互换 | 独立写 |  | 15 |
| `py-0a-147-predict-split-join` | 切开和连起来 | 预测 | `py.split-join`（split / join：字符串和列表互转） | 15 |
| `py-0a-148-complete-dash-case` | 补全：用短横线连接 | 补全 |  | 15 |
| `py-0a-050-reverse-words` | 单词倒序（`reverse-words-in-a-string`） | 独立写 |  | 15 |
| `py-0a-051-predict-pop` | pop 和 insert | 预测 | `py.list-pop`（pop / insert / remove） | 15 |
| `py-0a-149-complete-drop-last` | 补全：删掉最后 k 个 | 补全 |  | 15 |
| `py-0a-052-apply-backspaces` | 退格键 | 独立写 |  | 16 |
| `py-0a-150-predict-repeat` | 列表乘以一个数 | 预测 | `py.list-concat-repeat`（列表的 * 重复和 + 拼接） | 15 |
| `py-0a-053-digit-counts` | 数字计数表 | 独立写 |  | 16 |
| `py-0a-054-predict-grid` | 二维列表 | 预测 | `py.nested-list`（二维列表） | 16 |
| `py-0a-151-predict-grid-alias` | 两行其实是同一行 | 预测 |  | 16 |
| `py-0a-152-complete-row-sums` | 补全：每行之和 | 补全 |  | 16 |
| `py-0a-055-column-sums` | 每列之和 | 独立写 |  | 17 |
| `py-0a-056-pair-sum-indices` | 两数之和（暴力版） | 组合 |  | 18 |

**第 6 组：函数**（已写 15 题；课：`py-0a-l06-functions`）

| 题目 | 标题 | 题型 | 新技能 | 难度 |
|---|---|---|---|---|
| `py-0a-200-predict-local-price` | 调价后，外面的价签是多少 | 预测 | `py.helper-func` | 16 |
| `py-0a-201-complete-two-boxes` | 补全两箱书的运费 | 补全 |  | 17 |
| `py-0a-202-count-vowel-notes` | 用小函数数元音 | 独立写 |  | 19 |
| `py-0a-203-shift-label` | 把字母轮转拆成两步 | 变式 |  | 20 |
| `py-0a-204-predict-shared-default` | 没有带袋子的两次调用 | 预测 | `py.default-args` | 16 |
| `py-0a-205-complete-repeat` | 补全名字贴纸 | 补全 |  | 17 |
| `py-0a-206-entry-ticket` | 有默认票价的售票窗 | 独立写 |  | 19 |
| `py-0a-207-predict-missing-return` | 显示在屏幕上，交回给谁 | 预测 | `py.none` | 16 |
| `py-0a-208-complete-absent` | 补全缺失读数的判断 | 补全 |  | 17 |
| `py-0a-209-first-cold` | 第一条负温记录 | 独立写 |  | 19 |
| `py-0a-210-predict-copy-or-alias` | 三张标签指向几张清单 | 预测 | `py.aliasing` | 16 |
| `py-0a-211-complete-backup` | 补全值班表备份 | 补全 |  | 17 |
| `py-0a-212-fix-trial-score` | 修好试算时被改动的成绩 | 改错 |  | 18 |
| `py-0a-213-two-proposals` | 两份候选歌单 | 独立写 |  | 19 |
| `py-0a-214-score-desk` | 用三个小函数生成成绩简报 | 组合 |  | 21 |

**第 7 组：字典和集合**（已写 21 题；课：`py-0a-l07-dicts-sets`）

| 题目 | 标题 | 题型 | 新技能 | 难度 |
|---|---|---|---|---|
| `py-0a-240-predict-price-keys` | 价目表里能找到什么 | 预测 | `py.dict-basics` | 17 |
| `py-0a-241-complete-room` | 补全书架位置 | 补全 |  | 18 |
| `py-0a-242-basket-total` | 按价目表结账 | 独立写 |  | 20 |
| `py-0a-243-predict-read-missing` | 查一张还没发的票 | 预测 | `py.dict-get` | 17 |
| `py-0a-244-complete-price` | 补全未标价商品的价格 | 补全 |  | 18 |
| `py-0a-245-spare-labels` | 给缺席者留个称呼 | 独立写 |  | 20 |
| `py-0a-246-predict-count-visits` | 没有记录的第一票 | 预测 | `py.dict-counting` | 17 |
| `py-0a-247-complete-clicks` | 补全按钮点击次数 | 补全 |  | 18 |
| `py-0a-248-fix-first-vote` | 修好第一张选票 | 改错 |  | 19 |
| `py-0a-249-letter-stock` | 清点字母印章 | 独立写 |  | 20 |
| `py-0a-250-same-letters` | 两袋字母能否互换 | 变式 |  | 21 |
| `py-0a-251-predict-entry-order` | 改了分数，名单怎么念 | 预测 | `py.dict-iter` | 17 |
| `py-0a-252-complete-subtotal` | 补全账本小计 | 补全 |  | 18 |
| `py-0a-253-first-favorite` | 最常被点的歌 | 独立写 |  | 20 |
| `py-0a-254-predict-same-box` | 第二枚红签放到哪里 | 预测 | `py.dict-grouping` | 17 |
| `py-0a-255-complete-buckets` | 补全按长度收词 | 补全 |  | 18 |
| `py-0a-256-initial-trays` | 按首字母装词卡 | 独立写 |  | 20 |
| `py-0a-257-predict-badge-sets` | 两份签到名单有几个人 | 预测 | `py.set-basics` | 17 |
| `py-0a-258-complete-stops` | 补全走过的站数 | 补全 |  | 18 |
| `py-0a-259-first-echo` | 首先再次响起的字符 | 独立写 |  | 20 |
| `py-0a-260-common-in-order` | 两份清单共同的编号 | 组合 |  | 22 |

**第 8 组：元组、排序、推导式与容器选择**（已写 29 题；课：`py-0a-l08-sequences`）

| 题目 | 标题 | 题型 | 新技能 | 难度 |
|---|---|---|---|---|
| `py-0a-280-predict-packed-point` | 坐标是怎样交回来的 | 预测 | `py.tuple` | 18 |
| `py-0a-281-complete-offset` | 补全坐标移动 | 补全 |  | 19 |
| `py-0a-282-temperature-span` | 一趟取出最低温和最高温 | 独立写 |  | 21 |
| `py-0a-283-predict-sort-result` | 排好序的数去了哪里 | 预测 | `py.sorted` | 18 |
| `py-0a-284-complete-high-three` | 补全最高的三个读数 | 补全 |  | 19 |
| `py-0a-285-runner-up` | 第二高的不同读数 | 独立写 |  | 21 |
| `py-0a-286-predict-tied-length` | 同长度的词谁在前 | 预测 | `py.sort-key` | 18 |
| `py-0a-287-complete-word-order` | 补全按长度排词 | 补全 |  | 19 |
| `py-0a-288-award-order` | 同分时按名字排 | 独立写 |  | 21 |
| `py-0a-289-predict-filter-before-square` | 哪些数走进平方表 | 预测 | `py.list-comp` | 18 |
| `py-0a-290-complete-odd-squares` | 补全奇数的平方 | 补全 |  | 19 |
| `py-0a-291-even-labels` | 一行挑出偶数 | 独立写 |  | 21 |
| `py-0a-292-predict-duplicate-initial` | 两张卡写在同一键上 | 预测 | `py.dict-set-comp` | 18 |
| `py-0a-293-complete-unique-lengths` | 补全词长的种数 | 补全 |  | 19 |
| `py-0a-294-last-index` | 每个符号最后一次的位置 | 独立写 |  | 21 |
| `py-0a-295-predict-empty-checks` | 空托盘能通过哪次检查 | 预测 | `py.genexp` | 18 |
| `py-0a-296-complete-alarm` | 补全低温警报 | 补全 |  | 19 |
| `py-0a-297-sign-checks` | 两格体检单 | 独立写 |  | 21 |
| `py-0a-298-predict-short-zip` | 落单的名字会出现吗 | 预测 | `py.zip` | 18 |
| `py-0a-299-complete-pair-sums` | 补全两排数的对应之和 | 补全 |  | 19 |
| `py-0a-300-score-pairs` | 把姓名与成绩配成对 | 独立写 |  | 21 |
| `py-0a-301-predict-lazy-choice` | 没选中的算式算了吗 | 预测 | `py.ternary` | 18 |
| `py-0a-302-complete-direction` | 补全升降标记 | 补全 |  | 19 |
| `py-0a-303-parity-tags` | 给每个数贴奇偶标签 | 独立写 |  | 21 |
| `py-0a-304-predict-log-or-members` | 签到簿与到场名单 | 预测 | `py.choose-container` | 18 |
| `py-0a-305-complete-station-index` | 选一张按站名查车次的表 | 补全 |  | 19 |
| `py-0a-306-marked-squares` | 棋盘上标过几格 | 独立写 |  | 21 |
| `py-0a-307-replay-orders` | 按客人重放点单记录 | 独立写 |  | 21 |
| `py-0a-308-honor-roll` | 从两列成绩生成名次表 | 组合 |  | 23 |

**第 9 组：类**（已写 12 题；课：`py-0a-l09-classes`）

| 题目 | 标题 | 题型 | 新技能 | 难度 |
|---|---|---|---|---|
| `py-0a-340-predict-two-tickets` | 两张票上的座位号 | 预测 | `py.class-basic` | 19 |
| `py-0a-341-complete-name-tag` | 补全行李牌上的名字 | 补全 |  | 20 |
| `py-0a-342-fix-parcel` | 修好包裹上消失的重量 | 改错 |  | 21 |
| `py-0a-343-two-cups` | 两只量杯的读数 | 独立写 |  | 22 |
| `py-0a-344-predict-shared-ledger` | 两本账为何出现同一笔 | 预测 | `py.class-methods` | 19 |
| `py-0a-345-complete-counter` | 补全计数器的累加 | 补全 |  | 20 |
| `py-0a-346-fix-odometer` | 修好不走字的里程表 | 改错 |  | 21 |
| `py-0a-347-bank-account` | 能连续存取的账户 | 独立写 |  | 22 |
| `py-0a-348-predict-last-node` | 最后一节车厢也有编号 | 预测 | `py.node-class` | 19 |
| `py-0a-349-complete-chain-size` | 补全沿链前进一步 | 补全 |  | 20 |
| `py-0a-350-chain-total` | 沿链累计货物重量变化 | 独立写 |  | 22 |
| `py-0a-351-desk-stack` | 桌上的一摞稿纸 | 组合 |  | 24 |

**第 10 组：简单递归**（已写 12 题；课：`py-0a-l10-recursion`）

| 题目 | 标题 | 题型 | 新技能 | 难度 |
|---|---|---|---|---|
| `py-0a-380-predict-return-trip` | 下楼和回来的脚步声 | 预测 | `py.recursion` | 20 |
| `py-0a-381-complete-block-tower` | 补全积木塔的总块数 | 补全 |  | 21 |
| `py-0a-382-fix-countdown` | 修好回程丢失的倒数 | 改错 |  | 22 |
| `py-0a-383-recursive-power` | 用小一次的幂拼出结果 | 独立写 |  | 23 |
| `py-0a-384-predict-suffix-start` | 最后一张数卡有没有读到 | 预测 | `py.recursion-seq` | 20 |
| `py-0a-385-complete-suffix-count` | 补全后缀里的符号数 | 补全 |  | 21 |
| `py-0a-386-recursive-list-sum` | 一层接一层的清单和 | 独立写 |  | 23 |
| `py-0a-387-mirror-edges` | 从两端向内检查回文 | 变式 |  | 24 |
| `py-0a-388-predict-fib-calls` | 同一个小问题来了几次 | 预测 | `py.recursion-multi` | 20 |
| `py-0a-389-complete-calls` | 补全调用树上的节点数 | 补全 |  | 21 |
| `py-0a-390-stair-routes` | 楼梯上有几种走法 | 独立写 |  | 23 |
| `py-0a-391-hanoi-steps` | 记录汉诺塔的每一步 | 组合 |  | 25 |

### 6.2 0B 算法入门（已写，31 题）

九个地图单元按下表排列。31 道必修题包括 18 道原创题、12 道 LeetCode 75 热身题，以及“最长的一段连续亮灯”。题型为 20 道独立写、5 道变式、4 道组合和 2 道预测。计数单元复用 0A 的字典和集合；栈和队列在同一单元分别引入。九个新技能各有知识卡和课。

复杂度单元用同一批输入分别跑单遍求和与两两比较，记录 1000、2000、4000 项的秒数和操作次数。重复编号题用最多 60000 个连续编号检测反复扫描列表的写法，单个用例时限 2000 毫秒。

| 题号 | 主题 | 标题 | 题型 | 新技能 | LeetCode |
|---|---|---|---|---|---|
| 001 | 线性查找与最值 | 从右找最后一次出现的位置 | 独立写 | `py.linear-search`（线性查找） |  |
| 002 | 线性查找与最值 | 收集所有出现的位置 | 变式 |  |  |
| 003 | 线性查找与最值 | 加上糖果后能并列第一吗 | 独立写 |  | `kids-with-the-greatest-number-of-candies` |
| 004 | 线性查找与最值 | 一遍找出第二高的不同读数 | 独立写 |  |  |
| 005 | 线性查找与最值 | 最长的一段连续亮灯 | 独立写 |  | `max-consecutive-ones` |
| 006 | 线性查找与最值 | 走过的最高海拔 | 独立写 |  | `find-the-highest-altitude` |
| 007 | 反转与交换 | 原地反转闭区间 | 独立写 | `py.swap-reverse`（原地交换与反转） |  |
| 008 | 反转与交换 | 只交换元音的位置 | 独立写 |  | `reverse-vowels-of-a-string` |
| 009 | 反转与交换 | 用三次反转把列表向右轮转 | 组合 |  |  |
| 010 | 双下标 | 合并两列有序号码 | 独立写 | `py.two-index`（双下标：两个下标各走一个序列） |  |
| 011 | 双下标 | 保留顺序能否拼出目标词 | 独立写 |  | `is-subsequence` |
| 012 | 双下标 | 两列号码能配成哪些对 | 变式 |  |  |
| 013 | 前缀和 | 建一次前缀和，查多段总和 | 独立写 | `py.prefix-sum`（前缀和） |  |
| 014 | 前缀和 | 寻找左右平衡的位置 | 独立写 |  | `find-pivot-index` |
| 015 | 前缀和 | 有多少个非空区间的和等于 k | 变式 |  |  |
| 016 | 计数 | 找出两份名单各自独有的编号 | 独立写 |  | `find-the-difference-of-two-arrays` |
| 017 | 计数 | 每种编号的出现次数都不同吗 | 独立写 |  | `unique-number-of-occurrences` |
| 018 | 模拟 | 跳几步能离开棋盘 | 独立写 | `py.simulation`（模拟） |  |
| 019 | 模拟 | 花坛还能种下几株花 | 独立写 |  | `can-place-flowers` |
| 020 | 模拟 | 把相邻的相同字符原地压缩 | 组合 |  | `string-compression` |
| 021 | 矩阵遍历 | 把座位表按列抄成新行 | 独立写 | `py.matrix-traverse`（矩阵遍历与方向数组） |  |
| 022 | 矩阵遍历 | 两条对角线共经过哪些格 | 变式 |  |  |
| 023 | 矩阵遍历 | 每个位置旁边有几个 1 | 独立写 |  |  |
| 024 | 矩阵遍历 | 有多少对行和列完全相同 | 组合 |  | `equal-row-and-column-pairs` |
| 025 | 栈和队列 | 预测纸条从栈顶出来的顺序 | 预测 | `py.stack-list`（列表当栈） |  |
| 026 | 栈和队列 | 星号擦掉最近留下的字母 | 独立写 |  | `removing-stars-from-a-string` |
| 027 | 栈和队列 | 预测谁先从队首离开 | 预测 | `py.deque`（collections.deque 当队列） |  |
| 028 | 栈和队列 | 统计最近三千毫秒的请求 | 独立写 |  | `number-of-recent-calls` |
| 029 | 栈和队列 | 环形报数最后留下谁 | 组合 |  |  |
| 030 | 复杂度直觉 | 亲手计时：一次求和与两两比较 | 独立写 | `py.big-o`（复杂度直觉） |  |
| 031 | 复杂度直觉 | 把重复编号的查找加快 | 变式 |  |  |

<!-- /plan:python -->

<!-- plan:algo -->

### 6.3 算法与数据结构阶段 1–4：NeetCode 250 骨架 + 阶梯题

读表方法："桥"是要自己写的阶梯题（标题 + 它引入的技能；不引入新技能的桥题是练习），数字行是骨架题，按表中顺序做。里程碑：B75 = Blind 75，NC150 = NeetCode 150（不含 B75 的部分），T100 = 力扣热题 100；这些标记写进题目的 `milestones` 字段（`blind75` / `nc150` / `top100`）。

**全部必修（2026-11-22 用户决定）**：不分选修和必修。用户原话："那就不分选修必修吧 全部都必修就行了 反正放上去的题我应该都会做的，题量没问题，我准备就是做成有时间做一点的那种长期练习 多点题没关系 后续我可能还会再加别的模块"。数学与几何（13 题）、位运算（10 题）和其他类别一样是必修；之前的 `optional` 标记已去掉（格式和检查脚本仍支持 `optional`，以后需要时可以再用）。

**7 道 LeetCode 会员题换成原创同构题（2026-11-22 用户决定）**：算法思路相同，题面和测试自写；题目里写 `replaces_premium: <原题 slug>`、`source: original`，题表里仍占原题的位置。

| 会员题（不能做） | 原创替代题 | 同一个算法思路 |
|---|---|---|
| encode-and-decode-strings | 《打包与拆包：把字符串列表编成一个字符串》 | 长度前缀编码：每个字符串写成 长度 + '#' + 内容；拆包时先读长度再按长度截取，所以内容里有 '#'、数字也不会出错。 |
| graph-valid-tree | 《修的路能连成一棵树吗》 | n 个村子、若干条双向道路：是树 ⇔ 恰好 n − 1 条边且全部连通（或：并查集合并时从不成环）。 |
| number-of-connected-components-in-an-undirected-graph | 《读书会分成了几个小组》 | n 个人、若干对"互相认识"：数连通块。邻接表 + DFS / BFS，或者并查集数根的个数。 |
| walls-and-gates | 《每个空位到最近出口的步数》 | 网格里 -1 是墙、0 是出口、INF 是空地：把所有出口同时放进队列做多源 BFS，原地填上步数。 |
| meeting-rooms | 《一个人能参加全部会议吗》 | 按开始时间排序，检查相邻两场是否重叠（后一场开始早于前一场结束就冲突）。 |
| meeting-rooms-ii | 《最少需要几间会议室》 | 按开始时间排序，用最小堆存各会议室的结束时间；或者把起止时间分别排序后双指针扫描，同时进行的最大场数就是答案。 |
| alien-dictionary | 《外星字母表的顺序》 | 相邻两个单词第一个不同的字母给出一条先后关系，建图后拓扑排序；有环、或长单词排在它自己的前缀前面时返回空串。 |

和 NeetCode 原顺序的差别（都是为了让曲线更平）：
- 前缀和类的两道题（2D 区域和、和为 K 的子数组）从"数组与哈希"移到阶段 2 的前缀和小节——它们依赖"前缀和 + 哈希"这个阶段 2 的技能。
- "分割等和子集"从一维 DP 移到二维 DP 里"0/1 背包"桥题之后。
- 阶段 4 的顺序：字典树 → 区间 → 贪心 → 一维 DP → 二维 DP → 高级图论（区间、贪心比 DP 和高级图论容易，先做；用户已确认保留）。
- 热题 100 里不在 NC250 的 17 道补进对应小节（表中标"热题 100 补充"）。

#### 阶段 1：基础数据结构（已写，73 道必修题）

按下表的行序练习，题号 001–073。骨架共 53 道（含 1 道原创会员替代题和 5 道热题 100 补充），另有 20 道阶梯题。13 个新技能由 5 个课文件讲解。

**数组与哈希（NC：Arrays & Hashing）**（001–032，20 道骨架 + 12 道阶梯）

| # | 题目 / 阶梯题 | 难度 | 里程碑 | 新技能 / 说明 |
|---|---|---|---|---|
| 1 | `concatenation-of-array` | 简单 |  | 热身：从 0B 过渡 |
| 桥 | 见过就停：用集合找第一个重复的数 | 自写 | | `algo.hash-seen`（集合记录"见过"） |
| 2 | `contains-duplicate` | 简单 | B75 |  |
| 桥 | 用 Counter 比较两个单词的字母 | 自写 | | `algo.counter`（collections.Counter）；前置 0A 第 7 组字典计数 |
| 3 | `valid-anagram` | 简单 | B75 |  |
| 桥 | 记录每个值第一次出现的下标 | 自写 | | `algo.hash-index-map`（字典记录 值 → 下标）；Two Sum 阶梯：0A `in` → 0A 字典计数 → 本题 → 0A 暴力两数之和（py-0a-056） |
| 4 | `two-sum` | 简单 | B75 · T100 | 改写 py-0a-056：一次遍历 + 哈希 |
| 5 | `longest-common-prefix` | 简单 |  |  |
| 6 | `remove-element` | 简单 |  |  |
| 7 | `majority-element` | 简单 | T100 |  |
| 桥 | TinySet：用列表实现 add / contains 的小集合类 | 自写 | | `algo.class-design`（设计题：用内置结构实现接口）；第一道 class 模式设计题 |
| 8 | `design-hashset` | 简单 |  |  |
| 9 | `design-hashmap` | 简单 |  |  |
| 桥 | 按字母签名分组（排序后的单词当键） | 自写 | | `algo.defaultdict`（collections.defaultdict） |
| 10 | `group-anagrams` | 中等 | B75 · T100 |  |
| 桥 | 按出现次数把元素放进桶 | 自写 | | `algo.bucket`（按频率分桶） |
| 11 | `top-k-frequent-elements` | 中等 | B75 · T100 |  |
| 桥 | 长度前缀编码：['ab','c'] → '2#ab1#c' | 自写 | | （不引入新技能）；练习 |
| 12 | `encode-and-decode-strings` | 中等 | B75 | 会员题 → 原创替代《打包与拆包：把字符串列表编成一个字符串》（`replaces_premium`） |
| 桥 | 前缀积数组和后缀积数组 | 自写 | | （不引入新技能）；练习 0B 前缀和 |
| 13 | `product-of-array-except-self` | 中等 | B75 · T100 |  |
| 桥 | 一行 / 一列 / 一宫里有没有重复（宫号 r // 3 * 3 + c // 3） | 自写 | | （不引入新技能）；练习 |
| 14 | `valid-sudoku` | 中等 | NC150 |  |
| 桥 | 找连续序列的起点：x - 1 不在集合里 | 自写 | | （不引入新技能）；练习 |
| 15 | `longest-consecutive-sequence` | 中等 | B75 · T100 |  |
| 16 | `best-time-to-buy-and-sell-stock-ii` | 中等 |  |  |
| 17 | `majority-element-ii` | 中等 |  |  |
| 18 | `sort-colors` | 中等 | T100 |  |
| 桥 | 合并两个有序列表 → 归并排序 | 自写 | | （不引入新技能）；练习 0B 双下标 + 0A 递归 |
| 19 | `sort-an-array` | 中等 |  |  |
| 桥 | 原地把每个数换到它该在的位置（循环交换） | 自写 | | （不引入新技能）；练习 |
| 20 | `first-missing-positive` | 困难 | T100 |  |

**栈（NC：Stack）**（033–050，14 道骨架 + 4 道阶梯）

| # | 题目 / 阶梯题 | 难度 | 里程碑 | 新技能 / 说明 |
|---|---|---|---|---|
| 1 | `baseball-game` | 简单 |  | 前置 0B 列表当栈 |
| 桥 | 只有一种括号：计数器判断是否匹配 | 自写 | | （不引入新技能） |
| 桥 | 多种括号：栈 + 配对字典 | 自写 | | `algo.stack-matching`（栈做匹配） |
| 2 | `valid-parentheses` | 简单 | B75 · T100 |  |
| 3 | `implement-stack-using-queues` | 简单 |  |  |
| 4 | `implement-queue-using-stacks` | 简单 |  |  |
| 5 | `min-stack` | 中等 | NC150 · T100 |  |
| 6 | `evaluate-reverse-polish-notation` | 中等 | NC150 |  |
| 7 | `asteroid-collision` | 中等 |  |  |
| 桥 | 暴力：每个元素向右找第一个更大的数（双重循环） | 自写 | | （不引入新技能） |
| 桥 | 单调栈：下一个更大元素 | 自写 | | `algo.monotonic-stack`（单调栈） |
| 8 | `daily-temperatures` | 中等 | NC150 · T100 |  |
| 9 | `online-stock-span` | 中等 |  |  |
| 10 | `car-fleet` | 中等 | NC150 |  |
| 11 | `simplify-path` | 中等 |  |  |
| 12 | `decode-string` | 中等 | T100 |  |
| 13 | `maximum-frequency-stack` | 困难 |  |  |
| 14 | `largest-rectangle-in-histogram` | 困难 | NC150 · T100 |  |

**链表（NC：Linked List）**（051–073，19 道骨架 + 4 道阶梯）

| # | 题目 / 阶梯题 | 难度 | 里程碑 | 新技能 / 说明 |
|---|---|---|---|---|
| 桥 | 链表遍历：求长度、转成列表 | 自写 | | `algo.ll-traverse`（链表遍历）；前置 0A 第 9 组节点类 |
| 桥 | 删除所有值为 x 的节点（哨兵节点） | 自写 | | `algo.ll-dummy`（哨兵（dummy）节点） |
| 1 | `reverse-linked-list` | 简单 | B75 · T100 | 引入 `algo.ll-reverse`（反转链表） |
| 2 | `merge-two-sorted-lists` | 简单 | B75 · T100 |  |
| 桥 | 找链表中间节点（快慢指针） | 自写 | | `algo.fast-slow`（快慢指针） |
| 3 | `linked-list-cycle` | 简单 | B75 · T100 |  |
| 4 | `palindrome-linked-list` | 简单 | T100 | 热题 100 补充 |
| 5 | `intersection-of-two-linked-lists` | 简单 | T100 | 热题 100 补充 |
| 6 | `reorder-list` | 中等 | B75 | 组合：中点 + 反转 + 合并 |
| 7 | `remove-nth-node-from-end-of-list` | 中等 | B75 · T100 |  |
| 8 | `swap-nodes-in-pairs` | 中等 | T100 | 热题 100 补充 |
| 9 | `linked-list-cycle-ii` | 中等 | T100 | 热题 100 补充 |
| 10 | `copy-list-with-random-pointer` | 中等 | NC150 · T100 |  |
| 11 | `add-two-numbers` | 中等 | NC150 · T100 |  |
| 12 | `find-the-duplicate-number` | 中等 | NC150 · T100 | 快慢指针用在数组上 |
| 13 | `reverse-linked-list-ii` | 中等 |  |  |
| 14 | `sort-list` | 中等 | T100 | 热题 100 补充：链表归并排序 |
| 15 | `design-circular-queue` | 中等 |  |  |
| 桥 | 双向链表：头部插入、删除任意节点 | 自写 | | `algo.doubly-linked`（双向链表 + 哈希（LRU）） |
| 16 | `lru-cache` | 中等 | NC150 · T100 |  |
| 17 | `lfu-cache` | 困难 |  |  |
| 18 | `merge-k-sorted-lists` | 困难 | B75 · T100 | 也可放到阶段 3 堆之后再做一遍 |
| 19 | `reverse-nodes-in-k-group` | 困难 | NC150 · T100 |  |

#### 阶段 2：核心套路（已写 79 题，骨架 66 题 + 阶梯题 13 道）

本阶段全部必修，骨架含 NeetCode 250 的 61 道和热题 100 的 5 道补充。9 个阶段技能分在 6 个单元，每个技能配有讲解、可运行示例和两道小测。二分统一用左闭右开区间。位运算桥先预测结果，再提交补全的取位函数。


**双指针（NC：Two Pointers）**（19 题，001–019，骨架 15 + 阶梯 4）

| # | 题目 / 阶梯题 | 难度 | 里程碑 | 新技能 / 说明 |
|---|---|---|---|---|
| 1 | `reverse-string` | 简单 |  | 前置 0B 原地反转 |
| 2 | `valid-palindrome` | 简单 | B75 |  |
| 3 | `valid-palindrome-ii` | 简单 |  |  |
| 4 | `merge-strings-alternately` | 简单 |  |  |
| 5 | `merge-sorted-array` | 简单 |  | 倒着合并 |
| 桥 | 原地删除指定值：读写指针 | 自写 | | `algo.read-write-pointer`（同向读写指针） |
| 6 | `remove-duplicates-from-sorted-array` | 简单 |  |  |
| 7 | `move-zeroes` | 简单 | T100 | 热题 100 补充 |
| 桥 | 有序数组里找和为 target 的两个数（对向指针） | 自写 | | `algo.two-pointers`（对向双指针） |
| 8 | `two-sum-ii-input-array-is-sorted` | 中等 | NC150 |  |
| 桥 | 排序后遍历时跳过重复值 | 自写 | | （不引入新技能）；练习 |
| 9 | `3sum` | 中等 | B75 · T100 |  |
| 10 | `4sum` | 中等 |  |  |
| 11 | `rotate-array` | 中等 | T100 | 三次反转 |
| 12 | `container-with-most-water` | 中等 | B75 · T100 |  |
| 13 | `boats-to-save-people` | 中等 |  |  |
| 14 | `next-permutation` | 中等 | T100 | 热题 100 补充 |
| 桥 | 前缀最大值数组和后缀最大值数组 | 自写 | | （不引入新技能）；练习 |
| 15 | `trapping-rain-water` | 困难 | NC150 · T100 |  |

**滑动窗口（NC：Sliding Window）**（12 题，020–031，骨架 10 + 阶梯 2）

| # | 题目 / 阶梯题 | 难度 | 里程碑 | 新技能 / 说明 |
|---|---|---|---|---|
| 桥 | 长度为 k 的子数组的最大平均值（LeetCode 75 `maximum-average-subarray-i`） | 自写 | | `algo.window-fixed`（定长滑动窗口） |
| 1 | `contains-duplicate-ii` | 简单 |  |  |
| 2 | `best-time-to-buy-and-sell-stock` | 简单 | B75 · T100 |  |
| 桥 | 最多翻转 k 个 0 后最长的连续 1（LeetCode 75 `max-consecutive-ones-iii`） | 自写 | | `algo.window-variable`（可变滑动窗口） |
| 3 | `longest-substring-without-repeating-characters` | 中等 | B75 · T100 |  |
| 4 | `longest-repeating-character-replacement` | 中等 | B75 |  |
| 5 | `permutation-in-string` | 中等 | NC150 |  |
| 6 | `find-all-anagrams-in-a-string` | 中等 | T100 | 热题 100 补充 |
| 7 | `minimum-size-subarray-sum` | 中等 |  |  |
| 8 | `find-k-closest-elements` | 中等 |  |  |
| 9 | `minimum-window-substring` | 困难 | B75 · T100 |  |
| 10 | `sliding-window-maximum` | 困难 | NC150 · T100 | 单调队列（deque） |

**前缀和（NC 没有独立类别，从数组与哈希移来）**（4 题，032–035，骨架 2 + 阶梯 2）

| # | 题目 / 阶梯题 | 难度 | 里程碑 | 新技能 / 说明 |
|---|---|---|---|---|
| 桥 | 一维区间和查询 | 自写 | | （不引入新技能）；练习 0B 前缀和 |
| 1 | `range-sum-query-2d-immutable` | 中等 |  | NC 数组与哈希 |
| 桥 | 和为 0 的子数组有几个（前缀和 + 计数字典） | 自写 | | `algo.prefix-hash`（前缀和 + 哈希） |
| 2 | `subarray-sum-equals-k` | 中等 | T100 | NC 数组与哈希 |

**二分查找（NC：Binary Search）**（19 题，036–054，骨架 16 + 阶梯 3）

| # | 题目 / 阶梯题 | 难度 | 里程碑 | 新技能 / 说明 |
|---|---|---|---|---|
| 1 | `binary-search` | 简单 | NC150 | 引入 `algo.binary-search`（二分查找） |
| 桥 | 找第一个 >= x 的位置（lower bound） | 自写 | | （不引入新技能）；练习 |
| 2 | `search-insert-position` | 简单 | T100 |  |
| 3 | `guess-number-higher-or-lower` | 简单 |  |  |
| 4 | `sqrtx` | 简单 |  |  |
| 5 | `find-first-and-last-position-of-element-in-sorted-array` | 中等 | T100 | 热题 100 补充 |
| 6 | `search-a-2d-matrix` | 中等 | NC150 · T100 |  |
| 7 | `search-a-2d-matrix-ii` | 中等 | T100 | 热题 100 补充：右上角出发 |
| 桥 | 给定速度能否在 h 小时内吃完（写 feasible 函数） | 自写 | | `algo.binary-search-answer`（二分答案） |
| 8 | `koko-eating-bananas` | 中等 | NC150 |  |
| 9 | `capacity-to-ship-packages-within-d-days` | 中等 |  |  |
| 桥 | 旋转数组：判断哪一半是有序的 | 自写 | | （不引入新技能）；练习 |
| 10 | `find-minimum-in-rotated-sorted-array` | 中等 | B75 · T100 |  |
| 11 | `search-in-rotated-sorted-array` | 中等 | B75 · T100 |  |
| 12 | `search-in-rotated-sorted-array-ii` | 中等 |  |  |
| 13 | `time-based-key-value-store` | 中等 | NC150 | 可用 bisect |
| 14 | `split-array-largest-sum` | 困难 |  |  |
| 15 | `find-in-mountain-array` | 困难 |  |  |
| 16 | `median-of-two-sorted-arrays` | 困难 | NC150 · T100 |  |

**数学与几何（NC：Math & Geometry）**（14 题，055–068，骨架 13 + 阶梯 1）

| # | 题目 / 阶梯题 | 难度 | 里程碑 | 新技能 / 说明 |
|---|---|---|---|---|
| 桥 | 最大公约数：辗转相除；math.gcd | 自写 | | `algo.math-module`（math 模块与数学技巧） |
| 1 | `greatest-common-divisor-of-strings` | 简单 |  |  |
| 2 | `excel-sheet-column-title` | 简单 |  |  |
| 3 | `plus-one` | 简单 | NC150 |  |
| 4 | `roman-to-integer` | 简单 |  |  |
| 5 | `happy-number` | 简单 | NC150 |  |
| 6 | `transpose-matrix` | 简单 |  |  |
| 7 | `rotate-image` | 中等 | B75 · T100 |  |
| 8 | `spiral-matrix` | 中等 | B75 · T100 |  |
| 9 | `set-matrix-zeroes` | 中等 | B75 · T100 |  |
| 10 | `insert-greatest-common-divisors-in-linked-list` | 中等 |  |  |
| 11 | `powx-n` | 中等 | NC150 |  |
| 12 | `multiply-strings` | 中等 | NC150 |  |
| 13 | `detect-squares` | 中等 | NC150 |  |

**位运算（NC：Bit Manipulation）**（11 题，069–079，骨架 10 + 阶梯 1）

| # | 题目 / 阶梯题 | 难度 | 里程碑 | 新技能 / 说明 |
|---|---|---|---|---|
| 桥 | 预测：按位与、或、异或、左移、右移的结果；取第 i 位 | 自写 | | `algo.bit-ops`（位运算） |
| 1 | `single-number` | 简单 | NC150 · T100 |  |
| 2 | `number-of-1-bits` | 简单 | B75 |  |
| 3 | `counting-bits` | 简单 | B75 |  |
| 4 | `add-binary` | 简单 |  |  |
| 5 | `reverse-bits` | 简单 | B75 |  |
| 6 | `missing-number` | 简单 | B75 |  |
| 7 | `reverse-integer` | 中等 | NC150 |  |
| 8 | `sum-of-two-integers` | 中等 | B75 |  |
| 9 | `bitwise-and-of-numbers-range` | 中等 |  |  |
| 10 | `minimum-array-end` | 中等 |  |  |

#### 阶段 3：树和图（已写 92 道必修题，骨架 78 题 + 阶梯题 14 道）

按下表顺序学习。骨架含 NeetCode 250 的 73 个位置（其中 3 个使用原创会员替代）和热题 100 补充的 5 题。

**树（NC：Trees）**（001–033，骨架 28 题 + 阶梯 5 题）

| # | 题目 / 阶梯题 | 难度 | 里程碑 | 新技能 / 说明 |
|---|---|---|---|---|
| 桥 | 手建一棵三节点的树，递归数节点个数 | 自写 | | `algo.tree-basics`（二叉树与递归遍历）；前置 0A 第 9、10 组 |
| 1 | `binary-tree-preorder-traversal` | 简单 |  |  |
| 2 | `binary-tree-inorder-traversal` | 简单 | T100 |  |
| 3 | `binary-tree-postorder-traversal` | 简单 |  |  |
| 4 | `maximum-depth-of-binary-tree` | 简单 | B75 · T100 |  |
| 5 | `invert-binary-tree` | 简单 | B75 · T100 |  |
| 6 | `same-tree` | 简单 | B75 |  |
| 7 | `symmetric-tree` | 简单 | T100 | 热题 100 补充 |
| 8 | `subtree-of-another-tree` | 简单 | B75 |  |
| 桥 | 递归同时返回（高度，是否平衡） | 自写 | | `algo.tree-postorder`（自底向上返回信息） |
| 9 | `balanced-binary-tree` | 简单 | NC150 |  |
| 10 | `diameter-of-binary-tree` | 简单 | NC150 · T100 |  |
| 桥 | 按层打印一棵树（deque） | 自写 | | `algo.tree-bfs`（层序遍历（BFS）） |
| 11 | `binary-tree-level-order-traversal` | 中等 | B75 · T100 |  |
| 12 | `binary-tree-right-side-view` | 中等 | NC150 · T100 |  |
| 桥 | 在 BST 里查找一个值（LeetCode 75 `search-in-a-binary-search-tree`） | 自写 | | `algo.bst`（二叉搜索树） |
| 13 | `lowest-common-ancestor-of-a-binary-search-tree` | 中等 | B75 |  |
| 14 | `insert-into-a-binary-search-tree` | 中等 |  |  |
| 15 | `validate-binary-search-tree` | 中等 | B75 · T100 |  |
| 16 | `kth-smallest-element-in-a-bst` | 中等 | B75 · T100 |  |
| 17 | `convert-sorted-array-to-binary-search-tree` | 简单 | T100 | 热题 100 补充 |
| 18 | `delete-node-in-a-bst` | 中等 |  |  |
| 桥 | DFS 里用 nonlocal 记录全局最大值 | 自写 | | `algo.nested-func`（嵌套函数与 nonlocal） |
| 19 | `count-good-nodes-in-binary-tree` | 中等 | NC150 |  |
| 20 | `lowest-common-ancestor-of-a-binary-tree` | 中等 | T100 | 热题 100 补充 |
| 21 | `path-sum-iii` | 中等 | T100 | 热题 100 补充：前缀和 + 回溯 |
| 22 | `flatten-binary-tree-to-linked-list` | 中等 | T100 | 热题 100 补充 |
| 23 | `construct-binary-tree-from-preorder-and-inorder-traversal` | 中等 | B75 · T100 |  |
| 24 | `construct-quad-tree` | 中等 |  |  |
| 25 | `house-robber-iii` | 中等 |  |  |
| 26 | `delete-leaves-with-a-given-value` | 中等 |  |  |
| 27 | `binary-tree-maximum-path-sum` | 困难 | B75 · T100 |  |
| 28 | `serialize-and-deserialize-binary-tree` | 困难 | B75 |  |

**堆（NC：Heap / Priority Queue）**（034–047，骨架 12 题 + 阶梯 2 题）

| # | 题目 / 阶梯题 | 难度 | 里程碑 | 新技能 / 说明 |
|---|---|---|---|---|
| 桥 | 预测：heappush / heappop 的顺序；用负数做最大堆 | 自写 | | `algo.heapq`（heapq 最小堆） |
| 1 | `last-stone-weight` | 简单 | NC150 |  |
| 桥 | 只保留最大的 k 个数 | 自写 | | `algo.heap-topk`（大小为 k 的堆） |
| 2 | `kth-largest-element-in-a-stream` | 简单 | NC150 |  |
| 3 | `kth-largest-element-in-an-array` | 中等 | NC150 · T100 |  |
| 4 | `k-closest-points-to-origin` | 中等 | NC150 |  |
| 5 | `task-scheduler` | 中等 | NC150 |  |
| 6 | `reorganize-string` | 中等 |  |  |
| 7 | `longest-happy-string` | 中等 |  |  |
| 8 | `car-pooling` | 中等 |  |  |
| 9 | `single-threaded-cpu` | 中等 |  |  |
| 10 | `design-twitter` | 中等 | NC150 |  |
| 11 | `find-median-from-data-stream` | 困难 | B75 · T100 | 两个堆 |
| 12 | `ipo` | 困难 |  |  |

**回溯（NC：Backtracking）**（048–066，骨架 17 题 + 阶梯 2 题）

| # | 题目 / 阶梯题 | 难度 | 里程碑 | 新技能 / 说明 |
|---|---|---|---|---|
| 桥 | 列出所有长度为 n 的 01 串（选 / 不选） | 自写 | | `algo.backtracking`（回溯）；前置 0A 多分支递归、别名 |
| 1 | `sum-of-all-subset-xor-totals` | 简单 |  |  |
| 2 | `subsets` | 中等 | NC150 · T100 |  |
| 3 | `combinations` | 中等 |  |  |
| 4 | `permutations` | 中等 | NC150 · T100 |  |
| 5 | `combination-sum` | 中等 | B75 · T100 |  |
| 6 | `letter-combinations-of-a-phone-number` | 中等 | NC150 · T100 |  |
| 7 | `generate-parentheses` | 中等 | NC150 · T100 |  |
| 桥 | 有重复元素时：排序后同一层跳过相同值 | 自写 | | （不引入新技能）；练习 |
| 8 | `subsets-ii` | 中等 | NC150 |  |
| 9 | `combination-sum-ii` | 中等 | NC150 |  |
| 10 | `permutations-ii` | 中等 |  |  |
| 11 | `word-search` | 中等 | B75 · T100 |  |
| 12 | `palindrome-partitioning` | 中等 | NC150 · T100 |  |
| 13 | `matchsticks-to-square` | 中等 |  |  |
| 14 | `partition-to-k-equal-sum-subsets` | 中等 |  |  |
| 15 | `n-queens` | 困难 | NC150 · T100 |  |
| 16 | `n-queens-ii` | 困难 |  |  |
| 17 | `word-break-ii` | 困难 |  |  |

**图（NC：Graphs，含并查集）**（067–092，骨架 21 题 + 阶梯 5 题）

| # | 题目 / 阶梯题 | 难度 | 里程碑 | 新技能 / 说明 |
|---|---|---|---|---|
| 1 | `island-perimeter` | 简单 |  | 前置 0B 矩阵方向数组 |
| 2 | `find-the-town-judge` | 简单 |  |  |
| 3 | `verifying-an-alien-dictionary` | 简单 |  |  |
| 桥 | 数一数某个格子连着多少个 1（递归涂色） | 自写 | | `algo.grid-dfs`（网格 DFS / BFS） |
| 4 | `number-of-islands` | 中等 | B75 · T100 |  |
| 5 | `max-area-of-island` | 中等 | NC150 |  |
| 6 | `surrounded-regions` | 中等 | NC150 |  |
| 7 | `pacific-atlantic-water-flow` | 中等 | B75 |  |
| 桥 | 边列表建邻接表，数连通块 | 自写 | | `algo.graph-adj-list`（邻接表建图） |
| 8 | `clone-graph` | 中等 | B75 |  |
| 9 | `number-of-connected-components-in-an-undirected-graph` | 中等 | B75 | 会员题 → 原创替代《读书会分成了几个小组》（`replaces_premium`） |
| 10 | `graph-valid-tree` | 中等 | B75 | 会员题 → 原创替代《修的路能连成一棵树吗》（`replaces_premium`） |
| 桥 | 迷宫里从起点到终点的最少步数（BFS） | 自写 | | `algo.graph-bfs`（BFS 求最短步数） |
| 11 | `rotting-oranges` | 中等 | NC150 · T100 | 多源 BFS |
| 12 | `walls-and-gates` | 中等 | NC150 | 会员题 → 原创替代《每个空位到最近出口的步数》（`replaces_premium`） |
| 13 | `open-the-lock` | 中等 |  |  |
| 桥 | 入度表 + 队列给课程排顺序（Kahn） | 自写 | | `algo.topo-sort`（拓扑排序） |
| 14 | `course-schedule` | 中等 | B75 · T100 |  |
| 15 | `course-schedule-ii` | 中等 | NC150 |  |
| 16 | `course-schedule-iv` | 中等 |  |  |
| 17 | `minimum-height-trees` | 中等 |  |  |
| 桥 | 并查集模板：合并 + 判断是否连通 | 自写 | | `algo.union-find`（并查集） |
| 18 | `redundant-connection` | 中等 | NC150 |  |
| 19 | `accounts-merge` | 中等 |  |  |
| 20 | `evaluate-division` | 中等 |  |  |
| 21 | `word-ladder` | 困难 | NC150 |  |

#### 阶段 4：进阶（已写，80 道必修题）

按下表行序练习，题号 001–080。70 道骨架题占 NeetCode 250 的 68 个位置（其中 3 道使用原创会员替代）和热题 100 的 2 个补充位置。10 道桥题各引入一个技能，配 7 份课。一维与二维 DP 的课都用同一组输入对照记忆化递归和自底向上填表。

**字典树（NC：Tries）**（001–005，4 道骨架题 + 1 道桥题）

| # | 题目 / 阶梯题 | 难度 | 里程碑 | 新技能 / 说明 |
|---|---|---|---|---|
| 桥 | 用嵌套字典存单词、判断前缀是否存在 | 自写 | | `algo.trie`（字典树） |
| 1 | `implement-trie-prefix-tree` | 中等 | B75 · T100 |  |
| 2 | `design-add-and-search-words-data-structure` | 中等 | B75 |  |
| 3 | `extra-characters-in-a-string` | 中等 |  |  |
| 4 | `word-search-ii` | 困难 | B75 |  |

**区间（NC：Intervals）**（006–013，7 道骨架题 + 1 道桥题）

| # | 题目 / 阶梯题 | 难度 | 里程碑 | 新技能 / 说明 |
|---|---|---|---|---|
| 桥 | 按起点排序后合并重叠区间（手算三个区间） | 自写 | | `algo.intervals`（区间问题） |
| 1 | `meeting-rooms` | 简单 | B75 | 会员题 → 原创替代《一个人能参加全部会议吗》（`replaces_premium`） |
| 2 | `merge-intervals` | 中等 | B75 · T100 |  |
| 3 | `insert-interval` | 中等 | B75 |  |
| 4 | `non-overlapping-intervals` | 中等 | B75 |  |
| 5 | `meeting-rooms-ii` | 中等 | B75 | 会员题 → 原创替代《最少需要几间会议室》（`replaces_premium`） |
| 6 | `meeting-rooms-iii` | 困难 |  |  |
| 7 | `minimum-interval-to-include-each-query` | 困难 | NC150 |  |

**贪心（NC：Greedy）**（014–028，14 道骨架题 + 1 道桥题）

| # | 题目 / 阶梯题 | 难度 | 里程碑 | 新技能 / 说明 |
|---|---|---|---|---|
| 1 | `lemonade-change` | 简单 |  |  |
| 桥 | 最大子数组和：每一步决定"接上"还是"重新开始" | 自写 | | `algo.greedy`（贪心） |
| 2 | `maximum-subarray` | 中等 | B75 · T100 |  |
| 3 | `maximum-sum-circular-subarray` | 中等 |  |  |
| 4 | `longest-turbulent-subarray` | 中等 |  |  |
| 5 | `jump-game` | 中等 | B75 · T100 |  |
| 6 | `jump-game-ii` | 中等 | NC150 · T100 |  |
| 7 | `jump-game-vii` | 中等 |  |  |
| 8 | `gas-station` | 中等 | NC150 |  |
| 9 | `hand-of-straights` | 中等 | NC150 |  |
| 10 | `dota2-senate` | 中等 |  |  |
| 11 | `merge-triplets-to-form-target-triplet` | 中等 | NC150 |  |
| 12 | `partition-labels` | 中等 | NC150 · T100 |  |
| 13 | `valid-parenthesis-string` | 中等 | NC150 |  |
| 14 | `candy` | 困难 |  |  |

**一维 DP（NC：1-D DP）**（029–048，18 道骨架题 + 2 道桥题）

| # | 题目 / 阶梯题 | 难度 | 里程碑 | 新技能 / 说明 |
|---|---|---|---|---|
| 1 | `pascals-triangle` | 简单 | T100 | 热题 100 补充：用上一行算下一行，DP 热身 |
| 桥 | 斐波那契：递归 → @cache 记忆化（对比调用次数） | 自写 | | `algo.memo-cache`（记忆化搜索（@cache）） |
| 桥 | 斐波那契：自底向上的 dp 数组 → 两个变量 | 自写 | | `algo.dp-1d`（一维 DP） |
| 2 | `climbing-stairs` | 简单 | B75 · T100 |  |
| 3 | `min-cost-climbing-stairs` | 简单 | NC150 |  |
| 4 | `n-th-tribonacci-number` | 简单 |  |  |
| 5 | `house-robber` | 中等 | B75 · T100 |  |
| 6 | `house-robber-ii` | 中等 | B75 |  |
| 7 | `decode-ways` | 中等 | B75 |  |
| 8 | `coin-change` | 中等 | B75 · T100 |  |
| 9 | `perfect-squares` | 中等 | T100 |  |
| 10 | `integer-break` | 中等 |  |  |
| 11 | `combination-sum-iv` | 中等 |  |  |
| 12 | `word-break` | 中等 | B75 · T100 |  |
| 13 | `maximum-product-subarray` | 中等 | B75 · T100 |  |
| 14 | `longest-increasing-subsequence` | 中等 | B75 · T100 |  |
| 15 | `longest-palindromic-substring` | 中等 | B75 · T100 | 中心扩展 |
| 16 | `palindromic-substrings` | 中等 | B75 |  |
| 17 | `longest-valid-parentheses` | 困难 | T100 | 热题 100 补充 |
| 18 | `stone-game-iii` | 困难 |  |  |

**二维 DP（NC：2-D DP）**（049–068，17 道骨架题 + 3 道桥题）

| # | 题目 / 阶梯题 | 难度 | 里程碑 | 新技能 / 说明 |
|---|---|---|---|---|
| 桥 | 网格路径数：dp[i][j] = 上 + 左 | 自写 | | `algo.dp-2d`（二维 DP） |
| 1 | `unique-paths` | 中等 | B75 · T100 |  |
| 2 | `unique-paths-ii` | 中等 |  |  |
| 3 | `minimum-path-sum` | 中等 | T100 |  |
| 桥 | 能否从若干数里挑一些凑出和 s（0/1 背包） | 自写 | | `algo.dp-knapsack`（背包 DP） |
| 4 | `partition-equal-subset-sum` | 中等 | NC150 · T100 | NC 一维 DP，放在背包阶梯之后 |
| 5 | `last-stone-weight-ii` | 中等 |  |  |
| 6 | `target-sum` | 中等 | NC150 |  |
| 7 | `coin-change-ii` | 中等 | NC150 |  |
| 桥 | 两个字符串的 dp 表：最长公共后缀长度 | 自写 | | `algo.dp-string`（字符串 DP） |
| 8 | `longest-common-subsequence` | 中等 | B75 · T100 |  |
| 9 | `edit-distance` | 中等 | NC150 · T100 |  |
| 10 | `interleaving-string` | 中等 | NC150 |  |
| 11 | `best-time-to-buy-and-sell-stock-with-cooldown` | 中等 | NC150 | 状态机 DP |
| 12 | `stone-game` | 中等 |  |  |
| 13 | `stone-game-ii` | 中等 |  |  |
| 14 | `longest-increasing-path-in-a-matrix` | 困难 | NC150 |  |
| 15 | `distinct-subsequences` | 困难 | NC150 |  |
| 16 | `burst-balloons` | 困难 | NC150 |  |
| 17 | `regular-expression-matching` | 困难 | NC150 |  |

**高级图论（NC：Advanced Graphs）**（069–080，10 道骨架题 + 2 道桥题）

| # | 题目 / 阶梯题 | 难度 | 里程碑 | 新技能 / 说明 |
|---|---|---|---|---|
| 桥 | 带权图 + heapq：Dijkstra 模板 | 自写 | | `algo.dijkstra`（Dijkstra 最短路） |
| 1 | `network-delay-time` | 中等 | NC150 |  |
| 2 | `path-with-minimum-effort` | 中等 |  |  |
| 3 | `cheapest-flights-within-k-stops` | 中等 | NC150 | Bellman-Ford / 分层 BFS |
| 桥 | Prim：每次接上离已连部分最近的点 | 自写 | | `algo.mst`（最小生成树） |
| 4 | `min-cost-to-connect-all-points` | 中等 | NC150 |  |
| 5 | `swim-in-rising-water` | 困难 | NC150 |  |
| 6 | `reconstruct-itinerary` | 困难 | NC150 |  |
| 7 | `alien-dictionary` | 困难 | B75 | 会员题 → 原创替代《外星字母表的顺序》（`replaces_premium`） |
| 8 | `find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree` | 困难 |  |  |
| 9 | `build-a-matrix-with-conditions` | 困难 |  |  |
| 10 | `greatest-common-divisor-traversal` | 困难 |  |  |

### 6.4 算法与数据结构阶段 5：面试混合（已写，79 道必修题）

题池 = Grind 169 ∪ Top Interview 150 里不在 NC250、也不是热题 100 补充的题（共 71 道；其中"反转字符串中的单词"已作为 0A 的 py-0a-050，"判断子序列"放在 0B，剩 69 道）。

混排规则（参照 Grind 75 的周计划）：
- 每周 6–8 题，来自至少 4 个不同套路；同一套路两题之间至少隔 2 题；
- 计时按面试设定：中等题 20–25 分钟、困难题 35–40 分钟，"AI 关闭"模式（无提示、无补全）；
- 每周加 1 道"多级递进"设计题（内存数据库、限流器、文件系统……，见调研报告"新题型"一节）和 1 道读码改码题；
- 通过后 AI 扮演面试官追问（复杂度、为什么用这个结构、加一个变化）。

**阶段 5 的新技能（各配 1 道阶梯题）**

| 阶梯题 | 新技能 |
|---|---|
| 解析一行 "key=value" 配置，格式不对返回默认值 | `algo.try-except`（异常处理） |
| 把嵌套列表逐个吐出来（yield 实现迭代器） | `algo.generator`（生成器（yield）） |
| 内存键值库第 1 级：set / get / delete（之后逐级加前缀过滤、TTL、快照） | `algo.oop-design`（多级递进设计） |

**混排题池**（69 题，按套路分组只是为了查找；实际按周混排，见上文）

| 套路 | 题目 |
|---|---|
| 数组 / 字符串 / 模拟 | `summary-ranges`、`h-index`、`length-of-last-word`、`find-the-index-of-the-first-occurrence-in-a-string`、`zigzag-conversion`、`string-to-integer-atoi`、`game-of-life`、`text-justification`、`largest-number` |
| 哈希 | `ransom-note`、`isomorphic-strings`、`word-pattern`、`longest-palindrome`、`contiguous-array`、`top-k-frequent-words`、`max-points-on-a-line` |
| 双指针 / 滑动窗口 | `squares-of-a-sorted-array`、`remove-duplicates-from-sorted-array-ii`、`3sum-closest`、`backspace-string-compare`、`substring-with-concatenation-of-all-words` |
| 栈 / 表达式 | `basic-calculator-ii`、`basic-calculator` |
| 链表 | `middle-of-the-linked-list`、`odd-even-linked-list`、`partition-list`、`rotate-list`、`remove-duplicates-from-sorted-list-ii` |
| 二分 | `first-bad-version`、`find-peak-element`、`random-pick-with-weight` |
| 树 | `path-sum`、`path-sum-ii`、`sum-root-to-leaf-numbers`、`average-of-levels-in-binary-tree`、`binary-tree-zigzag-level-order-traversal`、`maximum-width-of-binary-tree`、`populating-next-right-pointers-in-each-node-ii`、`minimum-absolute-difference-in-bst`、`inorder-successor-in-bst`、`binary-search-tree-iterator`、`count-complete-tree-nodes`、`construct-binary-tree-from-inorder-and-postorder-traversal`、`all-nodes-distance-k-in-binary-tree` |
| 图 / BFS | `flood-fill`、`01-matrix`、`shortest-path-to-get-food`、`minimum-knight-moves`、`minimum-genetic-mutation`、`snakes-and-ladders`、`bus-routes` |
| 堆 | `find-k-pairs-with-smallest-sums`、`smallest-range-covering-elements-from-k-lists` |
| 回溯 | `sudoku-solver`、`palindrome-pairs` |
| DP | `triangle`、`maximal-square`、`best-time-to-buy-and-sell-stock-iii`、`best-time-to-buy-and-sell-stock-iv`、`maximum-profit-in-job-scheduling` |
| 贪心 / 区间 | `minimum-number-of-arrows-to-burst-balloons`、`employee-free-time`、`integer-to-roman` |
| 设计（多级递进的种子） | `insert-delete-getrandom-o1`、`design-hit-counter`、`design-in-memory-file-system` |
| 数学 / 位运算 | `palindrome-number`、`factorial-trailing-zeroes`、`single-number-ii` |

001–003 依次引入异常处理、生成器和多级递进设计。之后的十周共 76 题，含表中 69 个骨架位置，以及 7 道承接旧接口的原创设计练习。每周首题是读码改码，第四题是设计题。把这些位置编进周题数，可以在每周 7–8 题内同时练检索、调试和扩展。各套路内部沿用表中顺序，同一套路跨周也至少隔两题。

| 周 | 题号（按实际学习顺序） | 读码改码 | 设计练习 |
|---:|---|---|---|
| 1 | 004–011 | 004 根到叶的目标和 | 007 键值库：列出前缀 |
| 2 | 012–019 | 012 保存符合目标的路径 | 015 号码池：登记与定位 |
| 3 | 020–027 | 020 每格距零的步数 | 023 号码池：删除与等概率抽取 |
| 4 | 028–035 | 028 奇偶位置重接链表 | 031 脉冲计数：累计次数 |
| 5 | 036–043 | 036 可重排回文长度 | 039 键值库：过期时刻 |
| 6 | 044–051 | 044 最多两轮交易 | 047 脉冲计数：五分钟窗口 |
| 7 | 052–058 | 052 索引卡的后继 | 055 档案目录：建目录与列举 |
| 8 | 059–065 | 059 括号外的符号 | 062 档案目录：读写文件 |
| 9 | 066–072 | 066 等宽排版的余数 | 069 键值库：恢复快照 |
| 10 | 073–079 | 073 删除整组重号 | 076 脉冲计数：分频道查询 |
<!-- /plan:algo -->

## 7. SQL 路线

### 7.1 书店练习数据库

`problems/sql/_db/bookstore/` 有 8 张表。六张基础表收录作者 12、图书 30、用户 20、订单 33、订单明细 47、评分 39 行。登录和行为流水分别有 18、14 行，供后段课程追踪同一读者的活动。桥题沿用熟悉的书店数据，SQL 50 改编题使用题内小表。

| 表 | 内容 | 故意放进去的边界 |
|---|---|---|
| authors | 作者 | 国家、出生年为空；两位作者一本书都没有 |
| books | 图书 | 作者 / 出版社 / 出版日期为空；多本同价（35、39、42、45、55）；两本同名不同版；库存为 0；以 "The" 开头但不是 "The " 的书名；闰日出版 |
| users | 用户 | 手机号 / 城市 / 推荐人为空；两个同名用户；4 位从没下过单；1 位没买却评了分 |
| orders | 订单 | 2024-12 到 2025-06，跨年、月初月末、2 月 28 日；已取消订单；优惠码为空 |
| order_items | 订单明细 | 成交价和现价不同（折扣、涨价）；4 本书从没被买过 |
| ratings | 评分 | 文字评价为空；7 本书从没被评过分；平均分并列 |
| reader_logins | 读者登录日期 | 同日重复、月末连续、断档和只登录一天 |
| reader_events | 浏览、加购、付款的时刻 | 重复浏览、先付款后浏览、不同动作同一时刻 |

表按阶段逐个引入：阶段 0 用 books → users → orders（单表）；阶段 1 加 order_items、ratings；阶段 2 起才把表连起来（authors 在连接阶段第一次出现）。

**隐藏数据集**：每道题的 `datasets` 第一项是 `db:bookstore`（题面展示的样例），其余是 `db:bookstore + datasets/<补丁>.sql`——在样例数据上追加 / 修改几行，专门制造 NULL、并列、重复、边界值（30.00 正好在区间端点、月末最后一天、插入顺序和排序顺序相反）、空分组等情况。每道题在 `problem.yaml` 的 `wrong_examples` 里写下 2–4 条典型错误写法，`verify_sql.py` 保证每一条都至少被一个隐藏数据集抓住；其中不少错误在样例数据上结果完全正确（如 `price <= 30`、`< '2025-06-30'`、`ILIKE`），只有隐藏数据能抓住。

SQL 阶段 0 每个技能的阶梯是：课里的讲解、示例和小测（小测代替预测题）→ `complete` 补全题 → `write` 独立写 →（改错 / 变式 / 组合）。

### 7.2 各阶段顺序

和调研报告映射表的差别（按"用到的最高概念"；用户已确认保留）：
- 620 无聊的电影、610 判断三角形不用聚合，从阶段 1 移到阶段 0；
- 1789 员工的直属部门用 IN 子查询写最自然，从阶段 2 移到阶段 3；
- 196 的清理规则在阶段 3 练习。021 用 SELECT 找到应保留的邮箱，020 用 DELETE 删除其余记录，再按最终通讯录判题。

<!-- plan:sql -->

#### 阶段 0：单表查询（已写 54 题，44 道书店阶梯题 + 10 道 SQL 50 单表题）

先用 `sql.select-star` 取出 users 和 orders 全表，从结果里找行、列和用户编号。接着用 `sql.schema-types` 读 books 的表结构，辨认类型、主键、必填列和可空列，再进入 `sql.select-basic` 练选列。NULL 的比较和筛选接在 WHERE 后面。

**已写好的书店阶梯题**

| 题目 | 标题 | 题型 | 新技能 | 难度 |
|---|---|---|---|---|
| `sql-0-114-complete-all-users` | 补全：打开用户表 | 补全 | `sql.select-star` | 1 |
| `sql-0-115-inspect-users` | 读查询结果的行、列和编号 | 看数据作答 |  | 1 |
| `sql-0-116-write-all-orders` | 查看全部订单 | 独立写 |  | 1 |
| `sql-0-117-inspect-books-schema` | 读懂图书表的列约定 | 看数据作答 | `sql.schema-types` | 2 |
| `sql-0-118-choose-column-types` | 给书号和平均分选类型 | 看数据作答 |  | 2 |
| `sql-0-101-complete-user-emails` | 补全：用户的姓名和邮箱 | 补全 | `sql.select-basic`（SELECT 列 FROM 表） | 1 |
| `sql-0-001-book-titles` | 所有图书的书名和价格 | 独立写 |  | 1 |
| `sql-0-102-complete-sale-price` | 补全：打八折的价格 | 补全 | `sql.select-expr`（计算列与 AS 别名） | 2 |
| `sql-0-002-stock-value` | 每本书的库存总值 | 独立写 |  | 3 |
| `sql-0-103-complete-shanghai-users` | 补全：上海的用户 | 补全 | `sql.where`（WHERE 过滤与比较） | 3 |
| `sql-0-003-scifi-books` | 科幻书有哪些 | 独立写 |  | 4 |
| `sql-0-004-cheap-books` | 30 元以下的书 | 独立写 |  | 5 |
| `sql-0-104-complete-cheap-kids` | 补全：便宜的童书 | 补全 | `sql.and-or`（AND / OR / NOT 与括号） | 5 |
| `sql-0-005-cheap-scifi` | 便宜的科幻书 | 独立写 |  | 6 |
| `sql-0-006-fix-and-or` | 修一修：AND 和 OR 的优先级 | 改错 |  | 8 |
| `sql-0-105-complete-cooking-or-kids` | 补全：两个分类 | 补全 | `sql.in-list`（IN (...) 列表） | 6 |
| `sql-0-007-categories-in` | 三个分类的书 | 独立写 |  | 7 |
| `sql-0-111-complete-price-range` | 补全：40 到 60 元的书 | 补全 | `sql.between`（BETWEEN 范围（含两端）） | 7 |
| `sql-0-008-price-between` | 价格区间 | 独立写 |  | 7 |
| `sql-0-009-march-orders` | 三月份的订单 | 变式 |  | 8 |
| `sql-0-106-complete-li-users` | 补全：姓 Li 的用户 | 补全 | `sql.like`（LIKE 模糊匹配） | 7 |
| `sql-0-010-titles-starting-the` | 以 The 开头的书名 | 独立写 |  | 8 |
| `sql-0-107-complete-unknown-city` | 补全：城市没填的用户 | 补全 | `sql.is-null`（NULL 与 IS NULL） | 8 |
| `sql-0-011-users-without-phone` | 没留手机号的用户 | 独立写 |  | 8 |
| `sql-0-012-not-harbor-press` | 不是 Harbor Press 出版的书 | 变式 |  | 10 |
| `sql-0-112-complete-phone-or-none` | 补全：没有手机号就显示 none | 补全 | `sql.coalesce`（COALESCE 默认值） | 9 |
| `sql-0-013-city-or-unknown` | 城市未填写时显示 unknown | 独立写 |  | 9 |
| `sql-0-108-complete-newest-users` | 补全：最新注册的在前 | 补全 | `sql.order-by`（ORDER BY 排序） | 9 |
| `sql-0-014-sort-by-price` | 按价格排序 | 独立写 |  | 10 |
| `sql-0-113-complete-cheapest-three` | 补全：最便宜的三本 | 补全 | `sql.limit`（LIMIT / OFFSET） | 10 |
| `sql-0-015-top3-expensive` | 最贵的三本书 | 独立写 |  | 11 |
| `sql-0-109-complete-distinct-cities` | 补全：有哪些城市 | 补全 | `sql.distinct`（DISTINCT 去重） | 9 |
| `sql-0-016-distinct-categories` | 有哪些分类 | 独立写 |  | 9 |
| `sql-0-110-complete-stock-label` | 补全：库存标签 | 补全 | `sql.case`（CASE WHEN 条件表达式） | 11 |
| `sql-0-017-price-band` | 价位标签 | 独立写 |  | 12 |
| `sql-0-018-active-buyers` | 上半年下过单的用户 | 组合 |  | 14 |
| `sql-0-150-complete-title-length` | 补全：书名占几个字符 | 补全 | `sql.string-funcs` | 12 |
| `sql-0-151-spine-label` | 书脊上的三个字符 | 独立写 |  | 13 |
| `sql-0-152-complete-order-weekday` | 补全：下单那天是星期几 | 补全 | `sql.date-funcs` | 12 |
| `sql-0-153-order-month-label` | 给订单贴上年月标签 | 独立写 |  | 13 |
| `sql-0-154-complete-member-price` | 补全：会员价精确到分 | 补全 | `sql.round-cast` | 13 |
| `sql-0-155-reading-pace` | 七天读完一本书 | 独立写 |  | 14 |
| `sql-0-156-complete-new-coupons` | 补全：以 NEW 开头的优惠码 | 补全 | `sql.regex` | 13 |
| `sql-0-157-plain-mailboxes` | 筛出纯字母用户名的书店邮箱 | 独立写 |  | 15 |

**SQL 50 单表练习**

做完 157 的正则练习后，依次完成 200–209。每题自带一张小表、一个样例和两个隐藏数据集，复用前面学过的技能。

| 题号 | 题目 | 题型 | 练习重点 |
|---|---|---|---|
| 200 | `invalid-tweets` | 独立写 | 1683 · 筛出超过 15 个字符的消息 |
| 201 | `fix-names-in-a-table` | 独立写 | 1667 · 分别处理首字母和剩余字母，按编号排列 |
| 202 | `recyclable-and-low-fat-products` | 独立写 | 1757 · 两项标记同时满足 |
| 203 | `big-countries` | 独立写 | 595 · 面积和人口两个门槛，任一达标即可 |
| 204 | `find-customer-referee` | 独立写 | 584 · 排除指定推荐人，保留没有推荐人的顾客 |
| 205 | `article-views-i` | 组合 | 1148 · 同行比较作者和读者，作者编号去重后排序 |
| 206 | `not-boring-movies` | 组合 | 620 · 判断编号奇偶，筛短评，按评分降序 |
| 207 | `triangle-judgement` | 独立写 | 610 · 用 CASE 给每组三边标上判断结果 |
| 208 | `patients-with-a-condition` | 独立写 | 1527 · 用 LIKE 找到一串编号中某个编号的开头 |
| 209 | `find-users-with-valid-e-mails` | 独立写 | 1517 · 用正则检查邮箱首字符、允许字符和完整域名 |

#### 阶段 1：聚合（已写 15 题，SQL 50 7 题 + 书店阶梯题 8 道）

编号为 sql-1-NNN，依表中顺序练习，全部必修。城市订单、每日售书清单由题目数据预先配好，本阶段只查单表。配套课为[从一行统计到每组一行](../problems/sql/lessons/sql-1-l01-rows-and-groups/lesson.yaml)和[在一组记录里计算不同指标](../problems/sql/lessons/sql-1-l02-group-metrics/lesson.yaml)。

| NNN | 题目 | 题型 | 新技能或练习重点 |
|---|---|---|---|
| 001 | 有多少读者留下了电话 | 补全 | `sql.count`，登记人数与非空电话数 |
| 002 | 书目价格简报 | 独立写 | `sql.sum-avg`，合计、平均与极值 |
| 003 | 分类书目数 | 补全 | `sql.group-by`，一类一行 |
| 004 | 书目够五种的分类 | 改错 | `sql.having`，分组后的门槛 |
| 005 | `classes-with-at-least-5-students` | 独立写 | 596，恰好五人也开班 |
| 006 | `find-followers-count` | 独立写 | 1729，按作者统计关注人数 |
| 007 | 每座城市有多少位下单读者 | 补全 | `sql.count-distinct`，同一人多单只算一次 |
| 008 | `number-of-unique-subjects-taught-by-each-teacher` | 变式 | 2356，跨分馆的同一课程 |
| 009 | `user-activity-for-the-past-30-days-i` | 组合 | 1141，日期区间内按天数不同读者 |
| 010 | 两列看懂读者的订单 | 补全 | `sql.conditional-agg`，送达数与取消数 |
| 011 | `queries-quality-and-percentage` | 组合 | 1211，逐条计算质量，平均质量与低分百分比分别四舍五入到两位小数 |
| 012 | `monthly-transactions-i` | 组合 | 1193，从收款日期取年月（`YYYY-MM`），按年月和地区汇总 |
| 013 | 把每天卖出的书名连起来 | 补全 | `sql.string-agg`，组内去重、排序、拼接 |
| 014 | `group-sold-products-by-the-date` | 独立写 | 1484，每日品种数与清单 |
| 015 | 每种书的退货率 | 独立写 | `sql.nullif`，分母为零时保留该组 |

#### 阶段 2：连接（已写 21 题，SQL 50 13 题 + 书店阶梯题 8 道）

编号为 sql-2-NNN，全部必修。003 先给出按用户汇总好的订单数，单独练 LEFT JOIN。007–008 引入多表连接与连接后聚合，013 引入多条件连接，再用于机器批次、签到和成交均价。配套课为[两张表怎样配成一行](../problems/sql/lessons/sql-2-l01-matching-rows/lesson.yaml)、[沿订单明细连接，再做汇总](../problems/sql/lessons/sql-2-l02-details-and-totals/lesson.yaml)和[同表的两个角色、价期和完整组合](../problems/sql/lessons/sql-2-l03-roles-periods-and-pairs/lesson.yaml)。

| NNN | 题目 | 题型 | 新技能或练习重点 |
|---|---|---|---|
| 001 | 订单是谁下的 | 补全 | `sql.inner-join`，按用户编号配对 |
| 002 | `product-sales-analysis-i` | 独立写 | 1068，保留每笔交易 |
| 003 | 零订单的读者也上榜 | 补全 | `sql.left-join`，无订单也有一行 |
| 004 | `replace-employee-id-with-the-unique-identifier` | 独立写 | 1378，未领卡的员工 |
| 005 | `employee-bonus` | 组合 | 577，低额或没有补贴记录 |
| 006 | 哪几种书还没有评分 | 改错 | `sql.anti-join`，找不到评分行 |
| 007 | 列出订单里的每一种书 | 补全 | `sql.multi-join`，订单 → 明细 → 书目 |
| 008 | 每位作者卖出了多少钱 | 独立写 | `sql.join-aggregate`，按明细计价 |
| 009 | `customer-who-visited-but-did-not-make-any-transactions` | 独立写 | 1581，统计完全没结账的到访 |
| 010 | 谁推荐了这位读者 | 补全 | `sql.self-join`，一张表的两个角色 |
| 011 | `the-number-of-employees-which-report-to-each-employee` | 组合 | 1731，统计直属人数，将成员平均年龄四舍五入到整岁 |
| 012 | `rising-temperature` | 独立写 | 197，日历上的前一天 |
| 013 | 成交日用哪张价签 | 补全 | `sql.join-conditions`，书号和价期同时匹配 |
| 014 | `average-time-of-process-per-machine` | 组合 | 1661，按机器和批号配对，平均用时保留三位小数 |
| 015 | `managers-with-at-least-5-direct-reports` | 独立写 | 570，区分同名主管 |
| 016 | `project-employees-i` | 独立写 | 1075，项目成员的平均从业年数保留两位小数 |
| 017 | `list-the-products-ordered-in-a-period` | 组合 | 1327，先筛月份再筛组 |
| 018 | `confirmation-rate` | 组合 | 1934，通过率保留两位小数，无请求的账号填 0 |
| 019 | 每位读者在各分类下过几单 | 补全 | `sql.cross-join`，先铺出全部用户 × 分类 |
| 020 | `students-and-examinations` | 组合 | 1280，补齐所有学员 × 科目 |
| 021 | `average-selling-price` | 组合 | 1251，按价期和件数求加权均价，结果保留两位小数 |

#### 阶段 3：子查询和 CTE（已写 21 道必修题：SQL 50 13 题、阶梯题 8 道）

编号 sql-3-001 至 021，顺序如下。三份课依次讲子查询的形状、内外层关联与 CTE、合并与去重清理。最后两题先用 021 查询通讯录中应留下的行，再用 020 实际删除重复邮箱。

[括号里的查询交出什么](../problems/sql/lessons/sql-3-l01-query-shapes/lesson.yaml) · [拿当前行去查，再给中间表命名](../problems/sql/lessons/sql-3-l02-outer-row-and-cte/lesson.yaml) · [合并名单与核对清理结果](../problems/sql/lessons/sql-3-l03-combine-and-clean/lesson.yaml)

| # | 题目 / 阶梯题 | 难度 | 新技能 / 说明 |
|---|---|---|---|
| 桥 | 比平均价贵的书（书店库） | 自写 | `sql.subquery-scalar`（标量子查询） |
| 1 | `percentage-of-users-attended-a-contest` | 简单 | 1633 |
| 2 | `second-highest-salary` | 中等 | 176 · 没有第二名时返回 NULL |
| 桥 | 买过 programming 类图书的用户（IN 子查询）（书店库） | 自写 | `sql.subquery-in`（IN (子查询)） |
| 3 | `employees-whose-manager-left-the-company` | 简单 | 1978 · NOT IN |
| 4 | `primary-department-for-each-employee` | 简单 | 1789（报告原放阶段 2，这里用 IN 子查询写） |
| 桥 | 订单数最多的那一位用户有几单（FROM 子查询）（书店库） | 自写 | `sql.derived-table`（FROM 子查询（派生表）） |
| 5 | `biggest-single-number` | 简单 | 619 |
| 6 | `customers-who-bought-all-products` | 中等 | 1045 |
| 桥 | 比自己所在分类平均价贵的书（书店库） | 自写 | `sql.correlated-subquery`（相关子查询） |
| 桥 | 从没下过单的用户（NOT EXISTS，对比阶段 2 反连接）（书店库） | 自写 | `sql.exists`（EXISTS / NOT EXISTS） |
| 桥 | 把"每位用户首单日期"写成 WITH，再统计（书店库） | 自写 | `sql.cte`（WITH（CTE）） |
| 7 | `immediate-food-delivery-ii` | 中等 | 1174 |
| 8 | `investments-in-2016` | 中等 | 585 |
| 9 | `exchange-seats` | 中等 | 626 |
| 桥 | 评分最多的用户 和 评分最高的书 拼成两行（UNION ALL）（书店库） | 自写 | `sql.set-ops`（UNION / INTERSECT / EXCEPT） |
| 10 | `movie-rating` | 中等 | 1341 |
| 11 | `friend-requests-ii-who-has-the-most-friends` | 中等 | 602 |
| 12 | `count-salary-categories` | 中等 | 1907 |
| 桥 | 清理邮箱后会留下谁（021） | 自写 | 用 NOT EXISTS 查询每个邮箱的最小编号 |
| 13 | `delete-duplicate-emails`（020） | 简单 | 196 · 引入 `sql.dml`，用 DELETE 删除副本，核对保留的编号和邮箱 |

#### 阶段 4：窗口函数（已写 20 道必修题：SQL 50 7 题、阶梯题 9 道、其他免费题 4 道）

编号 sql-4-001 至 020。三份课先用同一批四张价签对比分组和窗口的行数，再读榜单与前后行，最后移动窗口帧并找连续段。日均额桥题提供逐日补齐的日历；补日期本身在阶段 5 练习。

[四张价签怎样分区、编号和排名](../problems/sql/lessons/sql-4-l01-rows-and-ranks/lesson.yaml) · [筛选榜单，读取前后记录](../problems/sql/lessons/sql-4-l02-ranks-and-neighbors/lesson.yaml) · [看清窗口的帧和连续段](../problems/sql/lessons/sql-4-l03-moving-frames/lesson.yaml)

| # | 题目 / 阶梯题 | 难度 | 新技能 / 说明 |
|---|---|---|---|
| 桥 | 每本书价格占所有图书总价的比例（SUM OVER ()）（书店库） | 自写 | `sql.window-agg`（窗口函数入门：聚合 OVER ()） |
| 桥 | 按价格给图书编号（ROW_NUMBER）（书店库） | 自写 | `sql.row-number`（ROW_NUMBER） |
| 桥 | 每个分类内按价格编号（书店库） | 自写 | `sql.partition-by`（PARTITION BY） |
| 桥 | 并列同名次：RANK 和 DENSE_RANK 对比（书店库） | 自写 | `sql.rank`（RANK / DENSE_RANK） |
| 桥 | 每个分类最贵的 2 本书（并列都要）（书店库） | 自写 | `sql.top-n-per-group`（分组 Top N） |
| 1 | `department-top-three-salaries` | 困难 | 185 |
| 2 | `product-sales-analysis-iii` | 中等 | 1070 |
| 3 | `game-play-analysis-iv` | 中等 | 550 |
| 桥 | 每位用户本次和上次下单相隔几天（LAG）（书店库） | 自写 | `sql.lag-lead`（LAG / LEAD） |
| 4 | `consecutive-numbers` | 中等 | 180 |
| 5 | `product-price-at-a-given-date` | 中等 | 1164 |
| 桥 | 按日期累计销售额（书店库） | 自写 | `sql.running-total`（累计求和） |
| 6 | `last-person-to-fit-in-the-bus` | 中等 | 1204 |
| 桥 | 7 日移动平均销售额（ROWS BETWEEN）（书店库） | 自写 | `sql.window-frame`（窗口框架（滑动窗口）） |
| 7 | `restaurant-growth` | 中等 | 1321 |
| 桥 | 每位用户连续下单的天数段（日期减行号）（书店库） | 自写 | `sql.gaps-islands`（连续区间（gaps and islands）） |
| 补 017 | `nth-highest-salary` | 中等 | 177 · 从单行参数表读取 N，缺档也给一行 NULL |
| 补 018 | `rank-scores` | 中等 | 178 · 同分同档，未知排最后 |
| 补 019 | `department-highest-salary` | 中等 | 184 · 各部门同薪榜首全部入选 |
| 补 020 | `human-traffic-of-stadium` | 困难 | 601 · 高客流且编号连续，保留整段明细 |

#### 阶段 5：综合（已写 11 道必修题：阶梯题 6 道、原创综合题 5 道，SQL 50 0 题）

编号 sql-5-001 至 011。三份课分别讲留存与转化、中位数与行列转换、日历与递归层级。后五题复用已引入的技能；试读付费、沉寂读者和按资格分列的报表分别借鉴免费题 3497、3716、262 的业务主题。

[先定一批人，再追踪他们](../problems/sql/lessons/sql-5-l01-return-and-convert/lesson.yaml) · [取中间位置，把分类摊成列](../problems/sql/lessons/sql-5-l02-middle-and-columns/lesson.yaml) · [把缺失的日期和层级补出来](../problems/sql/lessons/sql-5-l03-calendars-and-trees/lesson.yaml)

| # | 题目 / 阶梯题 | 难度 | 新技能 / 说明 |
|---|---|---|---|
| 桥 | 按注册月份的次月留存（书店库） | 自写 | `sql.retention`（留存） |
| 桥 | 浏览 → 加购 → 下单 漏斗（书店库） | 自写 | `sql.funnel`（漏斗） |
| 桥 | 每个分类的价格中位数（PERCENTILE_CONT 和手写两种）（书店库） | 自写 | `sql.median`（中位数与分位数） |
| 桥 | 每位用户各分类购买量：行转列（书店库） | 自写 | `sql.pivot`（行列转换） |
| 桥 | 补全没有订单的日期（generate_series）（书店库） | 自写 | `sql.generate-series`（generate_series 补全日期） |
| 桥 | 推荐链：每位用户往上数几层推荐人（WITH RECURSIVE）（书店库） | 自写 | `sql.recursive-cte`（递归 CTE） |
| 007 | 首登七天后谁还在读 | 组合 | 按首登日分批，目标日重复登录只计一次 |
| 008 | 从试读到续订的七日转化 | 组合 | 含第七天，严格按试读、付费、续订的日期顺序 |
| 009 | 找回沉寂读者最长的登录段 | 组合 | 截止日、按日去重、跨月连续与并列择早 |
| 010 | 用行号核对各线路配送中位数 | 组合 | 奇偶中点、有效数与全空线路 |
| 011 | 把每天的配送结果排成三列 | 组合 | 核对双方账号，按结果分列并计算取消率 |
<!-- /plan:sql -->

## 数学（用代码学）

Python 基础之后可以进入数学线。以列表表示一笔记录或一批记录，用普通 Python、`math` 和固定种子的 `random` 做实验。三阶段共 24 个技能、10 个单元、80 题。表中每行也是一节课，技能从左到右引入。

| 阶段 | 单元 | 技能顺序 | 题数 | 在后续学习线中的用途 |
|---|---|---|---:|---|
| 1 向量和矩阵 | 向量与分量 | 有序分量 → 加减与数乘 | 6 | 张量按轴存放特征；模型参数与更新量逐项相加 |
| 1 | 点积与距离 | 点积与加权求和 → 长度与两点距离 | 6 | 线性模型给特征加权；kNN 比较样本距离 |
| 1 | 行、列与转置 | 矩阵形状 → 转置 | 6 | 分清批次轴与特征轴，为张量的轴交换做准备 |
| 1 | 矩阵的乘法 | 矩阵乘向量 → 矩阵乘矩阵 → 单位矩阵 | 12 | 一次给整批样本打分；用直通权重检验线性层；原表乘转置得到两两匹配分 |
| 2 函数和导数 | 函数表与斜率 | 输入输出的数值表 → 区间平均变化率 | 6 | 用一列参数值观察模型输出或损失随参数变化的方向 |
| 2 | 用差商看导数 | 前向差商 → 验证常见导数 → 链式法则 | 10 | 用小扰动核对自动求导结果，沿复合函数追踪反向传播 |
| 2 | 梯度与下降 | 偏导数与梯度 → 一维下降和步长 → 二维同步更新 | 10 | 组织多个模型参数的梯度；观察学习率过大时损失如何变化 |
| 3 指数对数和概率 | 指数与对数 | 指数增长与自然指数 → 自然对数与对数相加 | 6 | 理解指数权重与对数概率，避免长串概率直接相乘 |
| 3 | 波动与随机结果 | 总体均值、方差和标准差 → 模拟频率 → 期望值 | 10 | 描述特征分布；重放随机实验；按概率汇总损失 |
| 3 | 从打分到损失 | 稳定 softmax → 交叉熵 | 8 | 张量沿类别轴归一化；分类模型从候选分数计算训练损失 |

每个技能先预测一个小程序的输出，再补全一次计算，最后从函数签名独立写。另有 3 道改错题和 5 道组合题。差商题保留有限步长带来的偏差，模拟题明确抽样方法，总体方差题明确分母。每项技能都出现在至少两道独立写或组合题中，供掌握度与复习使用。

## 数据处理（wrangle）

从 Python 基础进入这条线，读表、区分值的种类和认识缺失沿用根线的技能。五个阶段共 28 个技能、14 个单元、100 题。每个技能从预测开始，接一道补全，再独立写。每项技能至少有两道可以计入掌握度的独立练习。

| 阶段 | 单元与练习顺序 | 题数 |
|---|---|---:|
| 1 NumPy 数组 | 数组与形状（4）→ 位置、区间与筛选（9）→ 重排形状与沿轴汇总（7） | 20 |
| 2 广播和向量化 | 广播与整批运算（7）→ 条件选择、累计与名次（10） | 17 |
| 3 pandas 基础 | 从列到表与 CSV（7）→ 选行、排序与更新列（10）→ 缺失值与列类型（6） | 23 |
| 4 分组合并和透视 | 分组统计与连接（7）→ 宽表与长表（6）→ 日期、频数与逐项函数（9） | 22 |
| 5 pandas 版 SQL 题 | 书店的书目与读者清单（7）→ 书店的统计与关联清单（6）→ 每行的组内名次与累计（5） | 18 |

数组题先让学习者区分“一格、一列、一张表”，再要求对齐轴和去掉循环。向量化课中用同一份输入亲手测两段耗时，代码题只检查结果和指定的写法。表格题直接传 DataFrame；CSV 练习传入带表头的文本，可试引号内的逗号、空表和缺失字段。

书店单元有 18 道 SQL 对照题，原题由 `sql_twin` 指向，题面可跳转。3 道预测读出分类、分组计数和窗口序号；15 道函数题从选列、筛选、金额列走到左连接、反连接、档次和累计。函数题的样例是小表，隐藏用例覆盖共享库及对应 SQL 原题的数据补丁。两种写法都遵循同一项查询的行数、重复记录、空值及排序口径。pandas 练习另核对约定的列名。

运行 `node scripts/curriculum/export_bookstore.mjs` 可由 SQL 线的 `_db/bookstore/schema.sql` 和 `seed.sql` 重新生成 `problems/wrangle/_data/bookstore/` 下的 CSV。八张表保留 SQL 的表头、字段顺序和空值。表操作的梯度参考 [Introduction to Pandas](https://leetcode.com/studyplan/introduction-to-pandas/) 和 [30 Days of Pandas](https://leetcode.com/studyplan/30-days-of-pandas/)。

## 张量与 PyTorch（tensor）

从数据处理和数学两条线进入，在 CPU 上用小整数表和浮点张量练习。24 个技能各从一题预测开始，经补全、必要的改错，到独立写。每项技能至少有两道可计入掌握度的独立练习。以下每个单元对应地图上的一个节点和一份课。

| 阶段 | 单元与练习顺序（题数） | 题数 |
|---|---|---:|
| 1 张量和形状 | 张量的格子（3）→ 改形状与交换轴（7）→ 单例轴与广播（6）→ 沿轴汇总（4） | 20 |
| 2 索引和掩码 | 切片、筛选与填值（6）→ 每行的取数与写数地址（6）→ 按条件和名次选择（6）→ 用坐标拼出张量运算（13） | 31 |
| 3 einsum | 用字母写矩阵乘法（6）→ 转置与对角线（3）→ 外积与注意力打分（4） | 13 |
| 4 自动求导和 nn.Module | 从损失读出梯度（8）→ 计算图的边界（4）→ 可学习的参数与线性层（6）→ 自定义层与保存状态（8） | 26 |

先在纸上为每根轴起名字，再逐行预测程序的形状和输出。广播沿用 NumPy 的右对齐规则。独热编码回访根线的 `data.quantity-vs-label`，用目录里的类别数决定列数。11 道坐标题给出整数张量，用 `arange`、广播、索引与逐元素运算构造结果；其中累计和与总和限定最多八格，三轮相距 1、2、4 格的加法即可覆盖全部输入。

einsum 的每一题都与显式算法对拍，包括逐批矩阵乘法、轴交换、对角线提取、外积和未缩放的注意力分数。最后一阶段用标量损失与数值差分读梯度，通过两个批次观察累加和清零，再检查自定义层的前向、参数登记以及更新后仍能独立读取的快照。

## 机器学习手写（ml）

前置线是张量与 PyTorch、数学。全线 24 个技能、16 个单元、87 道题。每个技能先用一组小数或一次形状预测引入，再补全关键一步，最后独立实现。跨单元的复习也计入掌握度，每个技能都有至少两道可计入的独立题。

| 阶段 | 依次练习的单元（题数） | 题数 |
|---|---|---:|
| 1 回归和梯度下降 | 从特征到误差（6）→ 解方程与逐步拟合（6）→ 特征尺度与训练轨迹（7） | 19 |
| 2 分类 | 从分数到类别（8）→ 让近邻投票（3） | 11 |
| 3 聚类和决策树 | 轮流分组与移动中心（5）→ 衡量并选择一次分裂（6）→ 把决策桩接成树（4） | 15 |
| 4 模型评估 | 留出测试集与防止泄漏（7）→ 从混淆矩阵读指标（7）→ 阈值、ROC 与并列分数（4）→ 轮流留出验证折（5） | 23 |
| 5 自动求导和 MLP | 给标量留下运算图（3）→ 沿图反传与梯度检查（5）→ 手写两层网络（7）→ 用 PyTorch 对拍（4） | 19 |

前四阶段在 NumPy 上手写模型。先把数学线的点积写成一批样本的预测，从均方误差导出正规方程和梯度更新。相同的起点配两种学习率，逐步记录更新前的损失，观察收敛和发散。分类把同样的线性分数接到 sigmoid 或逐行 softmax，接着比较直接让邻居投票的方法。k-means 保留每轮分配的标签和移动后的中心。一维树先试阈值，再把同样的切分用到左右子组。

评估从行号入手。先划分，再用训练行拟合标准化；做交叉验证时，每一折都单独拟合。ROC 按不同分数整体移动阈值，AUC 先手算正负配对，再用升序分组累计平手的半分。最后一阶段先用纯 Python 给标量保存输入边与局部斜率，通过拓扑逆序累加共享节点的梯度，再用 NumPy 手写两层 tanh 网络。固定的微型输入使同一个输出、五份梯度都能与 PyTorch 对拍，课堂示例与题目共用 DS 运行环境。

## 8. 决定记录与待定问题

**2026-11-22 用户已决定**
- 所有内容按零基础设计，每块先教再练；会的直接做题。内容侧不设计诊断和跳过逻辑。
- 题课合一（problem-format v1.2）：课按技能写，挂在题目旁边，不单独占学习顺序。
- 全部必修（不分选修，2026-11-22 用户决定）；7 道会员题各写一道原创同构题。
- 0A 保持细粒度；阶段 4 的重排和 SQL 的重新分阶段保留；掌握 = 2 道不同的题不看提示独立写对。

**还需要你决定**
1. ~~选修模块里的 Blind 75 题是否改必修~~：已决定全部必修（2026-11-22）。
2. 0A 第 0 组有 5 道"固定输出"的 stdio 题（没有输入，只能靠自觉用变量写）。是保留，还是把这几步的"独立写"改成课里的示例练习？
3. SQL 的"预测"目前用课里的单选小测代替；要不要请平台加 SQL 预测题型（预测行数 / 结果表，见第 9 节）。

## 9. 对题目格式（docs/problem-format.md）的建议

v1.2 已经采纳了 `wrong_examples`、`optional`、`replaces_premium` 和按技能写的课。剩下的缺口：

1. **`practices`（焦点技能）**：`skills.practices: py.for-range`——这道题练的是哪个技能，平台据此统计"掌握"。没写时按第 2.2 节的规则推断（introduces，否则 requires 里最晚引入的）。
2. **固定输出的 stdio 题**：没有输入的程序（0A 第 0 组的"写出三行问候"）也被要求 2 个 examples + 3 个 hidden，只能写 5 个相同的用例。建议允许 stdio 题只写 1 个用例（`stdin` 为空时）。
3. **SQL 预测题**：建议 `format: predict` 用于 SQL 时，题面展示 `solution.sql`，学习者填"返回几行"或填结果表，判题时运行参考解比对；目前只能用课里的单选小测代替。
4. **stdio / predict 模式的字段说明**：明确这两种模式没有 `entry` / `signature` / `compare`；stdio 的 tests.json 顶层同样是 `{"examples": [...], "hidden": [...]}`（平台和内容都按这个写，但文档里没写明）。
5. **SQL 题的 `starter.sql` 对 `complete` / `fix` 必填**：Python 已写明，SQL 也应该一样（检查脚本已按此检查）。
6. **`ordered: true` 时的并列**：建议写明"ordered 题的排序键必须能唯一决定顺序"。
7. **课示例的输出**：lesson 的 example 没有"期望输出"字段；如果平台想在示例旁显示"运行结果"而不必真的运行，可以加可选的 `output:`（内容侧可以由校验脚本自动填）。
