# 63-chat-input：助教输入框不再被压扁，可以拖动调高度（issue #4）

## 背景
用户 2026-11-24 开了 6 个 issue，今天说："现在我想 把这6条解决一下，分别先做一下能修的部分 …… 可以并行做"。

本任务只负责 #4，先用 `gh issue view 4` 读全文（只读，不要评论、不要改 issue）。要点：
- `.chat` 是纵向 flex，子元素都没设 `flex: none`。`.chat-list` 是 `flex: 1 1 auto`，消息一多，初始高度就是全部内容的高度；放不下时多出来的部分按比例分给所有能缩的子元素去缩，输入框也被压成约一行半。
- `.chat-input` 写死了 `resize: none`，只有 `rows={3}`，旁边没有拖动条。工作台其他几处（题目列表宽度、题面和编辑器比例、助教栏宽度、底部面板高度）都能拖。

同时在跑的其他任务：61 改 `bootstrap/`、`server/app/ai/provider.py`，62 改 `desktop/`、`.github/`，64 只写 `docs/tutor-memory.md`。你只改 `web/`，另外可以改 `docs/README.md` 里讲做题页布局的那一句。

## 要做的事
1. **先修被压扁**：`.chat-head` / `.chat-agent`、`.chat-quick`、输入区都不参与收缩（`flex: none`），`.chat-list` 加 `min-height: 0`，只让对话列表自己滚动。
2. **拖动调高度**：沿用 `WorkbenchLayout.tsx` 里现有的 `Separator` 和 `useSize`，和其他几处拖动条的手感、样式、键盘操作保持一致。
   - `useWorkbenchLayout()` 里加 `chatInput = useSize('dojo-chat-input-height', …)`，记进布局偏好，下次打开还是这个高度。默认值让输入框大约 3 行。
   - 把"快捷按钮 + 输入框"包进一个容器，高度用 CSS 变量控制，在它顶边放 `Separator`（`label="调整输入框高度"`）。`Separator` 用 `e.currentTarget.parentElement` 的高度当拖动的初始值，所以它必须是这个容器的直接子元素。
   - 上限要随助教栏高度变化（比如不超过助教栏高度的一半），不能把对话列表挤没。
3. **不做**输入框随内容自动长高（issue 里的可选项）：和拖动二选一，选拖动，因为和工作台其他几处一致。
4. 窄屏（宽度小于 900px，助教从侧边呼出）下也检查一遍：输入框高度正常、拖动条能用或者合理地隐藏。

## 这次不做
- 不改助教的请求、回复格式和后端。
- 不改别的面板的布局。

## 验收标准
- `cd web && npm run build` 通过；如果 `web/` 有前端测试（`package.json` 里的 test 脚本），一并跑过。
- 起测试实例时后端用 8013、前端用 5183（`CODE_DOJO_AI_PROVIDER=off`）。助教对话可以用 `FakeProvider`，或者在页面里塞假消息，把对话撑到超过一屏，确认输入框高度不变。
- 截图放 `{RUN_DIR}/`：消息很多时的助教栏、拖高后的输入框、刷新后高度还在、窄屏抽屉模式。
- 报告"请主控复查"一节写清楚在浏览器里怎么复现、怎么看。
