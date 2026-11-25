# 65-manual-agent-path：设置里手动指定 Claude Code / Codex 的位置

## 背景
issue #3：macOS 从程序坞打开时找不到 `~/.local/bin/claude`。任务 61 已经在 `bootstrap/agents.py` 里加了自动补救：两个命令都找不到时，读一次登录 shell 的 PATH。但这个办法还没在 Mac 上实测过，登录 shell 也可能超时或读不到。用户 2026-11-24 说："如果不行的话可以在设置里做一个手动链接agent的这个设计"。

现在的最后手段写在 `deploy/README.md` 里，是 `launchctl setenv CODE_DOJO_CLAUDE_BIN …`，电脑重启后就失效，普通用户也不会用。本任务做一个应用内的替代：在设置窗口里手动指定命令的位置，存下来，以后每次启动都用它。

先读：`bootstrap/agents.py`（61 刚改过：登录 shell PATH，以及把找到的绝对路径写进 `CODE_DOJO_CLAUDE_BIN` / `CODE_DOJO_CODEX_BIN`）、`bootstrap/protocol.py`（`ready()` 里的 `ai=`、`connect_sync` / `disconnect_sync` 后用 `restart_service()` 重启后端）、`bootstrap/service.py`、`desktop/main.cjs` / `preload.cjs` / `startup.html` / `startup.js` / `startup.css`（62 刚加了"完成"按钮和 Esc 关闭）、`desktop/tests/smoke.cjs`。现在没有其他任务在跑。

## 要做的事
1. **设置页的"AI 助教"一节**：分别显示 Claude Code 和 Codex 的状态：已找到（显示实际用的路径）、手动指定（显示路径）、未找到。每个都有：
   - 一个路径输入框，可以粘贴终端里 `command -v claude` 的输出；
   - "浏览…"按钮，打开系统文件选择框（Electron `dialog.showOpenDialog`，要能看到隐藏目录，比如 `~/.local/bin`）；
   - "保存"，以及手动指定过时出现的"改回自动查找"。
   - 说明文字一句话就够，告诉用户在终端运行 `command -v claude` 可以查到路径。界面遵守 `.impeccable.md`，字少、安静。窗口放不下就适当调大设置窗口。
2. **保存时检查**：文件存在、可执行，并且用 `<路径> --version` 跑一次（限时约 5 秒），能返回版本号才算有效；无效时在设置页显示原因，不保存。不要调用会消耗订阅额度的命令。
3. **存在哪、怎么生效**：
   - 存在用户数据目录里（比如 `desktop/agents.json`），只在本机有效，不进同步仓库。
   - 优先级：环境变量 `CODE_DOJO_CLAUDE_BIN` / `CODE_DOJO_CODEX_BIN`（开发者用）> 设置里手动指定的路径 > 自动查找（PATH → 登录 shell → VS Code 扩展里的 codex）。
   - 保存或改回自动以后，用现有的 `restart_service()` 重启后端，让助教当场可用，不用重开应用；设置页的状态同时更新。
   - 后端（`server/app/`）不用改：启动器把路径写进环境变量，后端照旧读取。和 61 一样，`server/app/` 必须能和 1.3.0 的旧启动器配合。
4. **"AI 助教已关闭"的提示**：改成指向这个设置，不再让用户"重新打开应用"。
5. **冒烟测试**：`smoke.cjs` 加一个用例：放一个假的 `claude` 脚本（支持 `--version`），不在 PATH 上，在设置里填入它的路径并保存，断言状态变成已启用、后端 `/api/status` 列出 claude；再改回自动，断言恢复原状。冒烟里已经有假命令目录（`bin`），可以沿用。
6. **启动器测试**：`bootstrap/tests` 覆盖优先级、保存、无效路径被拒、改回自动。
7. **文档**：
   - `deploy/README.md` 的"设置里显示'AI 助教已关闭'"一节：把 `launchctl setenv` 那段换成"在设置里指定位置"的步骤，macOS、Linux、Windows 都适用。别的节不动。
   - `docs/README.md` 的"桌面应用"和"订阅和命令"两处写清优先级和保存位置。
   - 不要改版本号，发版由主控统一改。

## 这次不做
- 不改 `server/`、`web/`。
- 不做自动探测更多目录。

## 验收标准
- `cd server && .venv/bin/python -m pytest -q ../bootstrap/tests` 全过。
- `for f in desktop/*.cjs desktop/*.js desktop/tests/smoke.cjs; do node --check "$f" || exit 1; done` 通过。
- **不要在本机启动 Electron 窗口**（本机没有 xvfb，会弹在用户的桌面上）。可以照 62 的做法，用 node `vm` 加载 `startup.js` / `main.cjs` 模拟 DOM 和 IPC，检查设置页各状态；真正的 Electron 冒烟由主控在 CI 上跑。
- 协议层可以本机实跑：参考 `codex/runs/59-local-first-sync-code-*/protocol-smoke.py`，用 JSONL 驱动启动器，测保存路径 → 重启后端 → `/api/status` 列出 claude。只用假的 claude 脚本，不跑真实 AI。
- 报告写清楚需要在 Mac 上实测的步骤。
