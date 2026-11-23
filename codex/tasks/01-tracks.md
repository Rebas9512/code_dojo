# 01 · 知识点按 track 整理：track 改成文件配置，拆出"算法与数据结构"，铺好进阶 track，首页做成 track 地图

## 背景

用户 2026-11-22 的原话：
- "对到后面进阶的内容我也想做一些 比如数据科学类的 数据操作，模型训练，tensor操作，手搓大语言模型之类的"
- "然后可以把知识点按不同的track去做整理"

设计在 `docs/README.md` 的「2b. 按 track 整理知识点，进阶模块」一节，先读它。

现在代码里只有两条线，`python` 和 `sql`，写死在三个地方：
- `server/app/problems.py`：`STAGE_ORDER` 和 `Literal["python", "sql"]`。
- `web/src/labels.ts`：`STAGE_NAMES`、`STAGE_ORDER`。
- `scripts/curriculum/check_curve.py`：`STAGE_ORDER`。

这次要把 track 改成由文件配置，并按设计拆分和新增 track。

**这次不做**：
- 进阶 track 的题、课和技能内容。
- 数据科学判题镜像（M6 再做）。
- 零基础"认识数据"阶段（另一个任务做，等调研报告）。
- 结构要留好口子：给某个 track 加一个阶段，只需要改它的 `track.yaml`。

## 要做的事

### 1. 每条线一个 `track.yaml`

放在 `problems/<track>/track.yaml`，格式（写进 `docs/problem-format.md`，升到 v1.3）：

```yaml
id: python                 # 和目录名一致
name: Python 基础
summary: 从变量、条件、循环到函数、字典和类，再到最基本的算法。   # 一句话，地图上显示
order: 1                   # 地图上的顺序
language: python           # python | sql：决定编辑器语言、判题方式、能不能出附加题
runtime: python            # python（现在的 Docker 判题镜像）| pglite（浏览器里的 SQL）| ds（数据科学镜像，M6 才有）
status: active             # active | planned（planned = 规划中：地图上灰显，没有题也不报错）
requires: []               # 前置 track 的 id
skill_prefix: py           # 本线技能 id 的前缀（py.xxx）
stages:
  - id: 0A
    name: 语法基础
  - id: 0B
    name: 算法入门
```

阶段 id 一律按字符串处理，沿用 `normalize_stage`。

### 2. 九条线

| id | name | language / runtime | status | requires | skill_prefix | stages（id 名称） |
| --- | --- | --- | --- | --- | --- | --- |
| python | Python 基础 | python / python | active | — | py | 0A 语法基础、0B 算法入门 |
| algo | 算法与数据结构 | python / python | active | python | algo | 1 基础数据结构、2 核心套路、3 树和图、4 进阶、5 面试混合 |
| sql | SQL | sql / pglite | active | — | sql | 0 单表查询、1 聚合、2 连接、3 子查询和 CTE、4 窗口函数、5 综合 |
| math | 数学（用代码学） | python / python | planned | python | math | 1 向量和矩阵、2 函数和导数、3 指数对数和概率 |
| data | 数据处理 | python / ds | planned | python | data | 1 NumPy 数组、2 广播和向量化、3 pandas 基础、4 分组合并和透视、5 pandas 版 SQL 题 |
| tensor | 张量与 PyTorch | python / ds | planned | data, math | tensor | 1 张量和形状、2 索引和掩码、3 einsum、4 自动求导和 nn.Module |
| ml | 机器学习手写 | python / ds | planned | tensor, math | ml | 1 回归和梯度下降、2 分类、3 聚类和决策树、4 模型评估、5 自动求导和 MLP |
| train | 训练 | python / ds | planned | ml | train | 1 数据管道、2 训练循环、3 评估和调参、4 训练脚本改错 |
| llm | 手搓 LLM | python / ds | planned | train | llm | 1 分词、2 嵌入和注意力、3 Transformer 块、4 GPT 前向和采样、5 训练和 KV cache |

几点说明：
- **summary**：活跃的三条线按现有内容写一句。规划中的六条按 README 2b 表格里的知识点写一句，不超过 40 个字。
- **规划中的 track**：只建 `track.yaml`，不建 `skills.yaml`、题目和课。代码要允许没有 `skills.yaml`。
- **SQL**：不依赖 Python，`requires` 为空。

### 3. 把 Python 线拆成 `python` 和 `algo`

- `problems/python/skills.yaml` 里 stage 为 1–5 的 48 个技能，挪到新文件 `problems/algo/skills.yaml`。
  - id 前缀从 `py.` 改成 `algo.`，比如 `py.two-pointers` → `algo.two-pointers`。
  - 所有引用一起改：其他技能的 prereqs、`docs/curriculum.md`、`docs/teaching-design.md`、脚本里的识别表（`check_curve.py` 里映射到技能 id 的表）。
  - 主控已经确认过：0A/0B 的技能、题和课都没有引用 stage 1–5 的技能。挪完后，algo 技能的前置可以指向 `py.*`，这就是跨线前置。
- 真实题库里还没有 stage 1–5 的题。
- 测试夹具要一起改：
  - 把 `server/tests/fixtures/problems/python/1/py-1-001-reverse-list` 和 `5/py-5-001-lru-cache` 挪到 `server/tests/fixtures/problems/algo/`，题目 id 改成 `algo-1-001-reverse-list`、`algo-5-001-lru-cache`。
  - 夹具的每条线都补上 `track.yaml`，夹具里也要有一条 planned 线。
  - 测试里引用旧 id 的地方一起改。
- 题目 id 约定：`<前缀>-<阶段小写>-NNN-slug`。现在 python 线用 `py-0a-…`，algo 线用 `algo-1-…`，sql 线用 `sql-0-…`，保持不变。

### 4. 后端

- `ProblemBank.refresh()` 按 `order` 读 `problems/*/track.yaml`，存成 `bank.tracks`，键是 track id。
  - 题目的 `track` 必须是已加载的 track，`stage` 必须在该线的 stages 里；违反算加载错误，进 `load_errors`，不要让整个服务挂掉。
  - `ProblemMeta.track` 不再用 `Literal`。
- 技能：保留按线分的 `bank.skills[track]`，另加一个全局索引 `bank.skill_index`（id → 技能，带所属 track）。
  - 凡是"查技能名、知识卡"的地方都改用全局索引，因为前置可能在别的线。涉及 `skill_cards`、`lesson_sections`、附加题和助教里取技能名的地方。
  - `skill_lesson`（技能 → 课）也改成全局的，同一个技能只能在一个课文件里讲，跨线也一样。
- 凡是用 `track == "python"` / `track == "sql"` 判断语言的地方，都改成看该线的 `language`。比如附加题现在只支持 Python，以后 algo 线的题也要能出附加题。
- 题目详情接口加 `language` 字段，前端靠它选编辑器语言和判题方式。
- `GET /api/tracks` 按 order 返回每条线：
  - 基本字段：`id, name, summary, order, language, runtime, status, requires`。
  - 题量和状态：`stages: [{id, name, total, solved}]`，以及 `total, solved, assisted, attempted`，状态口径和现在的题目列表一致。
  - `skills`：本线技能数。
  - `next`：按顺序第一道没通过的题 `{id, title}`，没有就是 null。
  - `requires_done`：每条前置线的 `solved == total`，而且 `total > 0`。
- `GET /api/tracks/{track}/skills` 返回本线技能，按 stage → group → 原顺序排。每个技能带：
  - `id, name, stage, group, card`。
  - `prereqs: [{id, name, track}]`。
  - `lesson: {id, title} | null`。
  - `problems`：引入这个技能的题，`[{id, title, format, status}]`，按学习顺序排。
  - `used_by`：只用到、不引入这个技能的题数。

  "掌握度"这次不做，M4 再做。前端用 `problems` 里的状态显示进度就行。
- 未知 track 返回 404（中文报错）。planned 线的 problems、skills 返回空列表，不报错。
- 数据库不用迁移：`submissions.track` 存的还是题目所在线的 id，0A 题仍然是 `python`。

### 5. 检查脚本

`scripts/curriculum/check_curve.py`、`scripts/curriculum/verify_python.py`、`scripts/verify_bank.py`、`scripts/curriculum/verify_sql.py`，凡是写死 track 或阶段的地方都改成读 `track.yaml`。

`check_curve.py` 多线规则：
- 按 `requires` 的拓扑序查各线。有环、或引用不存在的线，都报错。
- 一条线开始时，它的所有前置线（传递闭包）里的技能都算"已学"。
- 技能的前置如果在别的线，这条线必须在本线的前置闭包里，否则报错。
- 技能 id 的前缀必须等于本线的 `skill_prefix`。
- 计划覆盖（NeetCode 250、SQL 50）照旧要满足。NeetCode 的阶段现在在 algo 线上，`docs/curriculum.md` 里的计划表要相应地标成 algo。
- planned 线没有技能和题，跳过，但要检查 `track.yaml` 格式。
- `--track` 参数照旧可以只查一条线。

### 6. 前端

去掉 `labels.ts` 里的 `STAGE_NAMES` 和 `STAGE_ORDER`，track 和阶段名都从 `/api/tracks` 取（做一个共享的 hook 或 context，取一次）。`Track` 类型改成 `string`。

路由：
- `/`：**track 地图**（新页面）。
- `/t/:track`：这条线的题目列表，就是现在的 TrackPage。
- `/t/:track/skills`：这条线的**知识点**视图（新页面）。
- `/p/:id`：不变。
- 旧的 `/sql` 重定向到 `/t/sql`。
- 题目页的面包屑、返回链接都指向 `/t/<track>`。

顶部导航：
- 现在是"Python | SQL"。改成：左边站名（链接到地图），后面是当前所在线的名字；在线内的页面上再加"题目 | 知识点"切换。
- 不再把所有线平铺在导航里，九条线太多。

track 地图 `/`：
- 按 order 列出全部线，用列表或分组，不做同尺寸卡片网格。
- 每条线显示：名字、一句话 summary、进度（solved/total，有 assisted 就一起显示）、前置线（"先学：Python 基础"，前置没做完时提示但不锁）、"继续：<下一题名>"链接、阶段名一行。
- 规划中的线灰显，写"规划中"，可以点进去看阶段列表，但没有题。
- 要能看出线和线的前置关系。最简单的做法是缩进或分组：Python 基础下面挂算法、数学、数据处理……这一支；SQL 单独一支。如果能用很轻的 SVG 或字符画连线表达，并且符合 `.impeccable.md` 也可以。选简单的。

知识点视图 `/t/:track/skills`：
- 按阶段 → 组列出技能：技能名；引入它的题的状态（用现有的状态符号）；有课的标"课"；前置技能（跨线的标出线名）。
- 点开一个技能显示知识卡（Markdown，复用现有的渲染），以及引入它的题的链接。
- planned 线显示阶段列表和"规划中"。

题目页：
- 编辑器语言看题目详情里的 `language`，不再看 track。
- 面包屑显示线名和阶段名，都从 API 取。

### 7. 文档

- `docs/problem-format.md` 升 v1.3：
  - 写 `track.yaml` 的格式、跨线前置规则、技能前缀、题目 id 约定。
  - 开头的版本说明一句话写清 v1.3 改了什么。
- `docs/README.md`：
  - 「目录」「代码结构」按新结构改。
  - 「2. 学习路线」里的 Python 表拆成"Python 基础（0A/0B）"和"算法与数据结构（1–5）"两张。
  - 「2b」里"怎么整理"那几条，已经实现的改成现在时；没做的保持"规划"。
  - 「怎么跑」里的命令如果变了就同步。
- `docs/curriculum.md`、`docs/teaching-design.md`：只改 id 和线名的引用，不改教学内容。

## 验收标准

主控会逐条复查。

1. `server/.venv/bin/python -m pytest -q` 全部通过。要新增测试，覆盖这几项：
   - track 加载。
   - 未知 track / stage 进 `load_errors`。
   - 跨线前置的技能卡能取到名字。
   - `/api/tracks` 的字段和顺序。
   - planned 线返回空列表。
   - `/api/tracks/{track}/skills` 的结构。
2. `verify_bank.py`：真实题库 108/108 通过，`load_errors` 为 0。
3. `check_curve.py`：0 错 0 警，计划覆盖照旧满足。
4. `npm run build` 通过。
5. 起 8001 和 5174 测试实例，这些页面都能打开、没有控制台报错：
   - `/`：9 条线，3 条活跃、6 条规划中。
   - `/t/python`：和现在的列表一样，108 题。
   - `/t/python/skills`：0A/0B 的 67 个技能。
   - `/t/algo/skills`：48 个技能，前置里能看到 `py.*` 并标出"Python 基础"。
   - `/t/sql`。
   - `/t/llm`：规划中。
   - 任意一道 0A 题的做题页，面包屑和上一题 / 下一题正常。
6. 用户的 8000 和 5173 实例没被动过；`server/data/` 没被改过。
