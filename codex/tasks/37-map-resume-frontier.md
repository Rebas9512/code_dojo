# 37-map-resume-frontier：主页加"继续最新进度"按钮

## 背景

用户 2026-11-23 原话："在主页还想加一个直接进入最新进度的一个按钮 就是直接进到track的最远一个未完成node里最新的还没做过的题这样"

现状：
- 主页是 `web/src/pages/MapPage.tsx`（树状地图）和 `web/src/pages/mapTree.ts`。顶栏 `.map-bar` 有 Python / SQL 两个标签页。
- 地图上已有的两样东西都不是用户要的：
  - 标成"下一步"的节点来自 `track.next`（`state.next_item`），按复习到期和推荐算，不一定是进度最前面。
  - 单元详情里有"继续：某题"（`unit.next`），要先点开单元才看得到。
- 每条线的数据由后端 `server/app/main.py` 的 `tracks()` 生成（`/api/tracks`），单元分组和进度在 `server/app/units.py`（`group_units`、`stage_progress`）。题目状态来自 `store.status_by_problem(track)`，取值 solved / assisted / attempted / 无。

## 要做的事

1. **后端：每条线的进度前沿**。在 `tracks()` 的每条线上加两个字段：
   - `frontier: PracticeLink | null`：最新进度要进的那道题，格式和现有的 `next` / `unit.next` 一样，前端能直接用 `practicePath()`。算法如下，顺序按 `group_units` 的阶段 → 单元 → 题目顺序：
     1. 找这条线里有任何状态（solved / assisted / attempted）的、顺序最靠后的那道题，记为 last，它所在的单元记为 U。
     2. 一道都没做过：返回整条线第一道非 optional 的题。
     3. U 里 last 后面有没做过（状态为空）的非 optional 题：返回其中第一道。
     4. 否则，U 里 last 前面有没做过的非 optional 题（跳过没做的）：返回其中第一道。
     5. 否则，返回 U 之后各单元里第一道没做过的非 optional 题。
     6. 都没有（整条线都做过了）：`null`。
   - `last_active: str | null`：这条线里题目最近一次提交或运行的时间（`submissions.created_at` 的最大值，附加题记到原题所在的线；具体怎么查看 `server/app/db.py`）。没有就是 `null`。
   - 前沿的计算写成 `units.py`（或新文件）里的纯函数，方便单测。
2. **前端：主页按钮**。
   - `api.ts` 的 `TrackInfo` 加 `frontier`、`last_active`。
   - `MapPage.tsx` 顶栏放一个主按钮（`Link`）：`继续 · <线名> · <题名> →`。
     - 目标线：当前标签页里可见的、`status === 'active'` 的线中 `last_active` 最新的那条。当前标签页一条都没练过时，取这个标签页树的第一条根线（`mapTree` 的 roots 第一条）。
     - 目标线的 `frontier` 为空时不显示按钮。
   - 样式遵守 `.impeccable.md`（安静、字少、不用卡片），放在 `web/src/pages/map.css`。窄屏（390px）不能撑出横向滚动。题名太长就省略，完整内容放进 `title`。
   - 快捷键可选：选一个不和现有冲突的，写进报告；不加也行。
3. **文档**：`docs/README.md` 里讲学习地图的地方补一两句，写清楚前沿怎么算。只用小补丁改这一节。

## 不做

- 不改地图上已有的"下一步"节点和单元详情里的"继续"。
- 不碰这些文件（主控正在改或验收）：`web/src/components/ProblemWorkspace.tsx`、`ProblemStatus.tsx`、`CodeEditor.tsx`、`ChatPanel.tsx`、`WorkbenchPanel.tsx`、`workbench.css`、`styles.css`，以及 `server/app/ai/`。
- 测试实例端口用 **后端 8004、前端 5177**。8003 / 5176 是主控的验收实例，8000 / 5173 是用户的，都不要碰。

## 验收标准

- `cd server && .venv/bin/python -m pytest -q` 全过。新增测试至少覆盖：
  - 前沿的 6 种情况：一道没做、单元里往后走、单元里回去补跳过的题、单元做完进下一单元、整条线做完返回 null、optional 题不会被选中；
  - `last_active` 有提交时有值、没有时为 null；
  - `/api/tracks` 返回这两个字段。
- `cd web && npm run build` 通过。
- 起测试实例（8004 / 5177，`CODE_DOJO_AI_PROVIDER=off`，`CODE_DOJO_JUDGE=local`，独立数据目录）。用 Playwright：
  1. 空数据：Python 标签页显示按钮，指向这个标签页根线的第一题；
  2. 在某条线做几道题（可以直接调提交接口，跳过一道），回到主页，按钮指向按算法应去的那道题，点进去是那道题；
  3. 切到 SQL 标签页，按钮跟着变；
  4. 390px 宽，没有横向滚动。
- 截图放 `{RUN_DIR}/`。
