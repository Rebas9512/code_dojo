# 30 · 桌面应用改用 Electron 外壳：界面嵌在应用窗口里，不再开浏览器

## 背景

用户 2026-11-23 说："那既然都做成应用了前端还需要浏览器吗直接做到应用里行吗"

现状：
- 26、28、29 号任务做的桌面应用，由 `bootstrap/`（内置 CPython 3.14）完成这些事：
  - 检查更新包（payload）
  - 用令牌或解锁密码取得 GitHub 访问
  - 起本地后端
  - 打开**系统浏览器**
- 同时还有一个 Tk 小控制窗口，上面有"打开浏览器 / 立即同步 / 退出"。
- 打包：
  - Linux：AppImage（加 tar.gz）
  - macOS：arm64 的 zip
  - Windows：zip

**主控定的方案**：用 **Electron** 做外壳，界面直接显示在应用窗口里。
- 选它的理由：内置 Chromium，和我们一直用来验收的浏览器引擎一致；Monaco 编辑器、PGlite（WASM + Worker）不会出意外。
- Python 后端和 `bootstrap` 的更新、令牌、同步逻辑都保留，改由 Electron 主进程来驱动。

**动手前先读**：
- `codex/runs/26-desktop-app-*/report.md`
- `codex/runs/28b-continue-*/report.md`
- `codex/runs/29-appimage-*/report.md`
- `bootstrap/`
- `scripts/desktop/`
- `.github/workflows/release-app.yml`
- `deploy/README.md`

**并行**：31 号任务在同时改前端的字体和界面样式（`web/src` 的 CSS 和字体、各页面的视觉），先读 `codex/PLAN.md`。

你名下的东西：
- 新建的 `desktop/`（Electron）；
- `bootstrap/`；
- `scripts/desktop/`；
- `.github/workflows/release-app.yml`；
- `deploy/README.md`；
- `docs/README.md` 的桌面应用一节。

前端只加**一个新组件文件**，加上在 `App.tsx` 里挂载它的最少几行，见第 4 节。不要改样式文件和别的页面，那些归 31。

## 要做的事

### 1. bootstrap 加无界面模式

`python -m bootstrap serve --protocol jsonl`：
- **stdout**：一行一个 JSON 事件。事件类型：
  - `status`：比如"检查更新""下载题库 37%""准备运行环境"
  - `need_unlock`：需要解锁密码
  - `need_tokens`：需要手动令牌
  - `unlock_failed`：附剩余尝试次数和等待秒数
  - `ready`：附 port、版本、payload 版本
  - `sync`：同步状态
  - `error`：附中文说明
- **stdin**：接收命令：`unlock`（密码）、`set_tokens`、`sync`、`check_update`、`quit`。
- **取令牌的优先级**和 28 一样：本机已存 → gh → 包里的加密令牌（解锁密码）→ 手动粘贴。
- **安全**：密码和令牌只走 stdin，不进命令行参数、不进日志、不出现在任何事件里。
- **Tk 窗口**：去掉 Tk 控制窗口，代码可以删。如果保留一个 `--tk` 回退模式，就说明理由。

### 2. Electron 外壳（`desktop/`）

- **依赖**：electron 和 electron-builder 锁定版本；用 TypeScript 或纯 JS 都行。
- **主进程**：
  - 单实例锁：第二次打开就聚焦已有窗口。
  - 启动内置 Python 跑 `bootstrap serve`，读事件。
  - 先显示一个本地的**启动页**（打包在 `desktop/` 里的 HTML），上面显示：进度、解锁密码输入框、令牌输入（备用）、错误和重试。
  - 收到 `ready` 后，主窗口加载 `http://127.0.0.1:<port>/`。
- **外部链接**：LeetCode 原题、GitHub 等用系统浏览器打开（`setWindowOpenHandler` 加 `shell.openExternal`）。只允许 127.0.0.1 本地地址在应用里导航。
- **安全设置**：
  - `contextIsolation: true`
  - `nodeIntegration: false`
  - `sandbox: true`
  - 页面只能通过 preload 暴露的少数几个接口和主进程通信：同步、设置、退出、版本信息。
- **原生菜单**（Mac 放应用菜单；Windows 和 Linux 放窗口菜单或者用快捷键）：立即同步、检查更新、设置（令牌、AI 助教状态）、关于（版本）、退出。
- **窗口**：记住大小和位置。默认 1440×900，最小 1024×700。标题 `code-dojo`。图标用 29 做的。
- **关窗口或退出**：先发 `sync` 和 `quit`，等后端推送完再退出，最多等 10 秒；界面上显示"正在同步…"。
- **崩溃处理**：后端进程意外退出时，窗口显示错误和"重启"按钮。

### 3. 打包（electron-builder）

- Python 运行时和 `bootstrap`、依赖、`sealed-tokens.json`（构建时有就放）作为 `extraResources`，沿用 26 和 29 的构建脚本。
- **产物**：
  - Linux：AppImage（推荐），tar.gz 备用。`.desktop` 文件和图标照 29 的做法，让 AppImageLauncher 能识别。
  - macOS：arm64 的 dmg 或 zip，不签名，文档照旧写首次右键"打开"。
  - Windows：nsis 安装程序或者便携 zip，你选，写理由。
- **AppImage 只读**：照 29 的要求，确认 AppImage 里面什么都不写。
- **CI**：`release-app.yml` 改用 electron-builder 构建三个系统，`app-v*` 标签触发。启动器版本升到 `1.1.0`。

### 4. 前端：桌面版的小入口

新建 `web/src/components/DesktopBridge.tsx`：
- 检测到 preload 暴露的 `window.dojoDesktop` 时，在顶栏右侧放一个小菜单：立即同步、设置、关于。
- 浏览器里访问时不显示。
- 只在 `App.tsx` 挂载它，不改别的页面和样式文件；样式先用现有的 CSS 变量。

### 5. 测试和文档

- **bootstrap 的 jsonl 协议**做单元测试：事件顺序、解锁失败、密码不出现在输出里。
- **Electron 冒烟测试**：用 Playwright 的 `_electron` 启动打好的 Linux 应用，CI 上用 xvfb。在假 payload 服务、假令牌的条件下，走一遍：启动页 → 输解锁密码 → 进入地图 → 交一道 Python 题 → 退出。
- **`deploy/README.md`**：「在一台新电脑上用」改成新的流程；Linux 部分保留 AppImageLauncher 的说明。
- **`docs/README.md`**：桌面应用一节改成 Electron 架构。

## 验收标准

1. `pytest -q` 全过，含新的协议测试。`npm run build` 通过。
2. 本机构建出 Linux AppImage，用 `--appimage-extract-and-run` 实测：假令牌、假 payload、全新数据目录。窗口里能看到：
   - 启动页的进度
   - 解锁：先输错，再输对
   - 学习地图
   - 做一道 Python 题、一道 SQL 题
   - 外部链接用系统浏览器打开（mock `shell.openExternal` 来断言）
   - 关窗口时先同步再退出

   截图放 `{RUN_DIR}/`。
3. 报告里写安装包大小，和 1.0.1 对比。
4. workflow 语法检查通过；macOS 和 Windows 的构建由主控打标签后看 CI。
5. 用户的 8000 和 5173 实例没被动过，`server/data/`、`~/Applications`、用户的真实令牌都没碰过。
