# 07 · M2：SQL 在浏览器里判题（PGlite），SQL 课的示例能跑，SQL 也能出附加题

## 背景

设计在 `docs/README.md` 第 4 节「判题」和第 5 节「AI」，先读。

用户 2026-11-22 同意的方案是：**Python 在服务器上跑，SQL 留在浏览器里跑**，用 PGlite，也就是浏览器里的 PostgreSQL 18。理由是没有差别、反馈更快。

现状：
- 有 SQL 题：阶段 0 有 31 道，05 号任务在写阶段 1–2。
- 内容侧有校验脚本 `scripts/curriculum/verify_sql.py`，加上 `pglite_runner.mjs`（Node 里的 PGlite，`scripts/curriculum/package.json`）。
- 做题页还不能判 SQL，SQL 课的示例也不能跑。

实测数据（vault findings）：
- PGlite 0.5.17 就是 PostgreSQL 18.7，默认排序规则 C、时区 UTC。
- 加载约 0.86 秒，浏览器首次下载约 5 MB（gzip）。
- 20 万行的窗口查询 150 ms。

**并行**：内容任务 06、08、09 可能同时在跑，先读 `codex/PLAN.md`。这次只有你一个平台任务，`server/app`、`web/` 都归你。不要改 `problems/` 下的题、技能和课。

## 要做的事

### 1. 浏览器里的 SQL 引擎（Web Worker）

- 前端加依赖 `@electric-sql/pglite`。版本和 `scripts/curriculum/package.json` 里的一致，用 `npm install` 加，并写进报告。
- 在 Web Worker 里跑 PGlite，**只在 SQL 题、SQL 课的页面才懒加载**，不影响 Python 页面的包大小和加载时间。加载时界面显示"正在准备数据库…"。
- 一个 worker 保持一个 PGlite 实例。每跑一个数据集就重新建一次库，隔离做法二选一，写进报告：
  - 首选：`BEGIN` → 建表（schema + seed + 数据集）→ 跑用户查询 → `ROLLBACK`。PostgreSQL 的 DDL 是事务性的。
  - 也可以：每个数据集用一个独立的 schema，跑完 DROP。
- **用户的 SQL 只允许单条查询**（SELECT 或 WITH 开头，允许结尾一个分号）。
  - 多条语句，或者 INSERT、UPDATE、DROP、BEGIN、COMMIT 这类，直接报中文错误，不执行。
  - 设 `statement_timeout`（比如 2 秒）防止死循环式的查询。超时报"超时"。
- 报错信息：把 PostgreSQL 的英文报错原样显示，并加一句中文提示。常见的几种要有中文提示：
  - 列不存在
  - 表不存在
  - 语法错误（指出位置）
  - 非聚合列不在 GROUP BY 里
  - 类型不匹配

### 2. 判题

**期望结果在服务器上算好**：参考解不发到浏览器。
- 后端用 Node + PGlite，复用 `scripts/curriculum/pglite_runner.mjs` 的做法，或者在 `server/` 下放一份同样的运行器。
- 对每道 SQL 题的每个数据集跑 `solution.sql`，得到期望结果集：列名、行、类型。
- 结果缓存起来，缓存键 = 参考解 + 数据集内容的哈希，放在 `CODE_DOJO_DATA` 下的缓存目录。
- 题目文件改了就自动重算。
- 判题接口给前端的东西：
  - 每个数据集的建表 SQL（schema + seed + 数据集）
  - 期望结果
  - 比较规则：`ordered`、数字精度
- 隐藏数据集的建表 SQL 也会发到浏览器。这是个人自用的站，可以接受，但在 README 里写一句。

**比较规则**和 `docs/problem-format.md`、`verify_sql.py` 完全一致：
- 列数相同
- 数字容差 1e-6
- NULL 等于 NULL
- 日期按 ISO 字符串比
- `ordered: false` 时忽略行序
- 不比较列名

把比较逻辑写成一个前端模块，写单元测试。用 vitest 时可以加 dev 依赖；也可以用 node 直接跑一个测试脚本，你选。最好和 `verify_sql.py` 用同一组测试样例对一遍。

**运行和提交**：
- "运行"只跑可见样例数据集。
- "提交"跑全部数据集。
- 浏览器判完把 verdict 和每个数据集的结果交给后端记录：沿用现有的 `/run`、`/submit`，加 SQL 的字段。单用户，信任前端的判定。
- 记录和 Python 题一样计入通过状态、AI 协助标记。

**结果面板**（复用 `ResultPanel` 的结构）：
- 每个数据集一个标签；隐藏的照旧标"·"。
- 显示你的结果表和期望结果表，各最多 50 行，多了显示"共 N 行"。
- 不一致的地方要标出来：
  - 行数不同
  - 第一处不同的行或值
  - 列数不同
  - 顺序不同（ordered 题）

**改错题**：`starter.sql` 照常作为初始代码。

### 3. SQL 课的示例

- 课里 SQL 的 `example` 步骤（`db` + `patch`）在浏览器里用同一个 worker 跑，体验和 Python 课的 playground 一样：
  - 能改代码再运行
  - 能"恢复"
  - 结果显示成表格
- SQL 课里的 `quiz` 不变。

### 4. 助教和附加题

- **助教**：SQL 题的提示词里带上：
  - 表结构
  - 样例数据集的前几行
  - 参考解（只供判断）
  - 用户当前的 SQL
  - 最近一次结果（含报错）

  共享编辑照旧作用于 SQL 编辑器。检查提示词里有没有写死"Python"的地方，按语言改。
- **附加题**（现在只支持 Python）：加 SQL 分支。
  - 出题 schema 的 SQL 版：题面、用到哪些表、可以自带小表的数据集（样例 1 个 + 隐藏至少 2 个）、参考解、1–2 个典型错误写法、可选的 starter。
  - 服务器上验证，用 Node PGlite，规则同 `verify_sql.py`：
    - 参考解在每个数据集上能跑、结果非空
    - `ordered` 题要有 ORDER BY
    - 每个错误写法至少在一个隐藏数据集上结果和参考解不同
    - 改错题的 starter 在样例上就和参考解不同
  - 不通过就带着错误重出，最多 3 次，和 Python 的流程一样。
  - 前端附加题标签对 SQL 题放开。

### 5. 校验脚本和文档

- `scripts/verify_bank.py`：SQL 题也真的跑参考解，调用和后端同一个 Node 运行器，替代现在"只加载不跑"。保留 `--only`。
- `docs/README.md`：
  - 第 4 节判题、第 5 节 AI 改成现在的实现。
  - 第 8 节 M2 标"已完成"。
  - 「怎么跑」里加上需要的 `npm install`，包括 `scripts/curriculum` 或 `server` 下的 Node 依赖。
- `docs/problem-format.md`：如果 SQL 题的字段有变化，升版本号并说明。

## 验收标准

1. `server/.venv/bin/python -m pytest -q` 全过。新增测试覆盖：
   - 期望结果计算与缓存
   - SQL 判题接口返回的数据
   - SQL 提交的记录
   - SQL 附加题验证（FakeProvider + 真实 Node PGlite）
2. `verify_bank.py` 全题库通过，含 SQL 实跑。
3. `npm run build` 通过；Python 做题页的包没有因为 PGlite 变大，报告里给出前后的包大小。
4. 结果比较模块的单元测试全过。
5. 起 8001 和 5174 测试实例，用浏览器实际走一遍。截图放 `{RUN_DIR}/`，不要放进项目源码，报告里写路径：
   - 打开一道 SQL 阶段 0 题：运行 → 看到结果表；故意写错列名 → 中文提示；提交正确答案 → 通过，地图上进度 +1
   - 一道 `ordered` 题：顺序错时提示"顺序不同"
   - 一道改错题
   - 一节 SQL 课的示例：运行、修改、恢复
   - 首次加载 PGlite 的耗时（报告里写数字）
6. 用户的 8000 和 5173 实例没被动过，`server/data/` 没被改过。
