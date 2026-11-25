# 69-update-on-launch：打开时先更新到最新（显式进度），并修掉网页被缓存成旧版的问题

## 背景
用户 2026-11-25 在本机（Linux，1.3.1）打开应用，看不到这两天加的"继续"按钮、开始一组、输入框分隔条。主控查到两个原因：
1. **更新包要下次打开才生效**：`bootstrap/protocol.py` 的 `launch()` 先用已装的更新包起服务，`check_later()` 在后台下载新版、存成 next，下载完不提示（`Result` 没有 message）。用户两天没开，第一次打开看到的是 11-23 的 v25。
2. **网页被 Chromium 缓存**：重开后后端已经是 v63，界面还是旧的。原因是 `server/app/frontend.py` 发 `index.html` 时只有 Last-Modified / ETag、没有 `Cache-Control`（桌面版 `CODE_DOJO_AUTH=off`，auth 中间件的 `no-store` 不生效）。Chromium 按启发式缓存（文件年龄的约 10%，旧版 index.html 两天前构建 → 缓存约 5 小时），端口又固定（`desktop/port.json`），同一个地址直接用缓存里的旧 index.html 和旧脚本。主控已手动清掉用户的 `chromium/Cache` 和 `Code Cache` 临时解决。

用户的要求："不然就做成打开的时候如果有更新就显式读条更新 加载完以后刷新那种 确保同步打开的时候都是最新的设计"。

## 要做的事
1. **打开时先更新**（`bootstrap/protocol.py`、`bootstrap/update.py`）：
   - 已装过更新包时，`launch()` 也先同步检查 `payload-latest`：启动页显示"正在检查更新…"；有新版就沿用现有进度显示（"下载题库 N%""准备运行环境…"）下载、装好，然后直接用新版起服务。没有新版就用已装的版本起服务。
   - 检查要有短超时（取清单的请求约 5 秒内没回应就放弃）。离线、超时、GitHub 出错时，直接用已装版本起服务，不弹对话框；不能因为网络卡住打不开应用。下载开始以后不设这个短超时（已有进度显示）。
   - 去掉后台 `check_later()` 和"下次打开生效"（`next.json` / `staged`）这一套，除非你发现别处还必须用；1.3.1 留下的 `next.json` 在新逻辑下不能造成问题。菜单"检查更新"保持现在的行为（当场切换并重载）。
   - `min_bootstrap` 高于本启动器时的"请下载新版安装包"提示保持。
   - 报告里写实测：没有新版时，打开到地图可用多花多少时间（用 `codex/runs/65-manual-agent-path-*/protocol-smoke.py` 的做法，假 GitHub 每请求加 0.25 秒延迟，对比改前改后）。
2. **网页缓存**：
   - `server/app/frontend.py`（更新包，1.3.1 也能拿到）：`index.html` 和前端路由回落的入口页发 `Cache-Control: no-cache`（每次用 ETag 向后端确认）；`/assets/` 下带哈希的文件发 `public, max-age=31536000, immutable`；其他静态文件（字体、图标、licenses）发 `no-cache`。
   - `desktop/main.cjs`（安装包）：收到 `ready` 后，若 `payload_version` 和上次载入网页时的不同（记在数据目录里，比如 `desktop/window.json` 旁边的小文件），先 `win.webContents.session.clearCache()` 再 `loadURL`。只清 HTTP 缓存，不碰 Local Storage（草稿和布局偏好存在那里）。菜单"检查更新"切换版本后同样处理。
3. **测试**：
   - `bootstrap/tests`：有新版时先下载再起服务、无新版直接起、离线和超时回落到已装版本、取清单超时不卡、1.3.1 留下的 next.json 不出问题、`min_bootstrap` 提示。
   - `server/tests`：三类静态文件的 `Cache-Control`。
   - `desktop/tests/smoke.cjs`：现在的流程里有"重开后远端无响应时的退出上限"（假 GitHub 卡住），新逻辑下重开时检查会遇到卡住的远端，要确认超时后照常打开、照常能退出；首次打开的下载进度断言保持。按需调整，不要删掉原有的覆盖。
4. **文档**：`deploy/README.md` 的"更新"一节改成"每次打开会先检查题库更新，有新版会显示下载进度，下载完直接用新版；没网时用本机已有的版本"。`docs/README.md` 桌面应用一节写清现在的启动顺序和缓存头。不要改版本号，发版由主控统一改。

## 这次不做
- 不改 `web/`（网页本身）、`server/app/` 里 frontend.py 以外的文件。
- 不做运行中自动更新（用户没要求；菜单"检查更新"已经能当场切换）。

## 验收标准
- `cd server && .venv/bin/python -m pytest -q ../bootstrap/tests` 和 `.venv/bin/python -m pytest -q` 全过（报告写数字，不要跳过 git 同步测试）。
- `for f in desktop/*.cjs desktop/*.js desktop/tests/smoke.cjs; do node --check "$f" || exit 1; done` 通过。
- **不要在本机启动 Electron 窗口**（会弹在用户桌面上）。协议层用 JSONL 实跑：已装旧版 + 假 GitHub 提供新版 → 进度消息依次出现 → 新版起服务；假 GitHub 卡住 → 约 5 秒后用旧版起服务。Electron 冒烟由主控在 CI 上跑。
- 测试端口如需起后端用 8019。
