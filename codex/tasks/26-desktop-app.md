# 26 · 打包成桌面应用（Linux / macOS / Windows），打开时自动从 GitHub 更新

## 背景

用户 2026-11-22 的原话：
- "行那我们走打包应用的方案好了 每次打开的时候从github同步题库 只要github有更新自动同步进去这样"
- 之前他还说过："做成3系统支持吧"。

24 号任务做了本地判题：不靠 Docker，跨平台的 harness，uv 管 Python。25 号任务做了 `dojo` 启动器和做题记录同步：事件日志加单独的私有仓库，用 git 命令。这次在它们外面包一层，做成**任何电脑下载一个安装包就能用**，不需要装 git、uv、Node。

**动手前先读**：
- `codex/runs/24-local-judge-*/report.md`
- `codex/runs/25-launcher-sync-*/report.md`
- `docs/README.md`

代码仓库是 GitHub 私有仓库 `Rebas9512/code_dojo`，配置项 `CODE_DOJO_REPO` 默认就填这个值，但要可以改。同步仓库已建好：`Rebas9512/code_dojo_sync`（私有，main 分支，初始只有 README），也要可以改。

## 主控定的设计

**安装包很薄**，只放：
- 独立的 Python 3.14 运行时，用 python-build-standalone 的 install_only 版本，要带 tkinter；
- 后端运行时依赖（fastapi、uvicorn、pyyaml、pydantic 等，按 `server/uv.lock` 锁定）；
- 一个小启动器 `bootstrap`。

**其余东西打成"更新包"（payload）**，每次推送后由 GitHub Actions 生成：
- `server/` 的代码
- `web/dist`
- `problems/`
- 预先算好的 SQL 期望结果
- 一份 `manifest.json`：版本、commit sha、生成时间、需要的最低启动器版本、题库格式版本、依赖锁的哈希

**应用每次打开**：
1. 检查 GitHub 上最新的 payload。私有仓库要用令牌，见下文。
2. 和本地版本不同就下载，校验哈希后**原子替换**：下到临时目录，再整体切换；失败就继续用旧版本。
3. 如果 manifest 要求更新的启动器，提示"请下载新版安装包"，给出链接，继续用旧 payload。
4. 如果依赖锁变了，用内置的 Python 和 pip 装新依赖。
5. 起服务，只听 127.0.0.1，端口自动选。
6. 打开默认浏览器。

**小控制窗口**（Tk）：
- 显示"正在运行 · 端口 xxx"、当前版本、上次更新时间、同步状态；
- 三个按钮："打开浏览器""立即同步""退出"；
- 关窗口就退出：先推送做题记录，再停服务。

**令牌**：第一次打开时，在控制窗口里请用户填一个 GitHub fine-grained 令牌，权限是：
- 代码仓库：Contents 只读；
- 同步仓库：Contents 读写。

令牌保存在用户数据目录，Linux 和 macOS 设成 600 权限；能用系统钥匙串（`keyring`）就用钥匙串。界面上给出一步一步建令牌的说明链接，链接用占位符。

**做题记录同步**：25 用的是 git 命令。这次加一个**不需要 git** 的传输方式：
- 用 GitHub Contents API，读写同步仓库里本机自己的 JSONL 文件；
- 机器上有 git 就继续用 git。

事件格式和合并规则沿用 25。

**数据科学依赖**：numpy、pandas、torch 第一次用到时用内置的 pip 装进用户数据目录的单独环境，沿用 24 的做法。

**AI**：检测 PATH 里的 `claude`，没有就在设置里显示安装和登录说明，AI 功能关闭，其他照常。

## 要做的事

1. **`bootstrap`**：启动器、更新、控制窗口、令牌设置，跨平台。
   - 单元测试覆盖：版本比较、下载失败回退、哈希不对拒绝、原子切换、启动器版本过旧时提示。用本地的假 GitHub 服务，或者 mock 来测，不要访问真的 GitHub。
2. **打包**：每个系统生成一个可分发的产物：
   - Linux：AppImage 或 tar.gz；
   - macOS：.app 打成 zip 或 dmg，不签名，文档里写首次打开要右键"打开"；
   - Windows：zip 加一个能双击的 exe 启动器，或者 Inno Setup 安装包。

   选在 GitHub Actions runner 上能稳定构建的工具，报告里写选择理由。**要求**：包里的 Python 必须是真正的解释器，判题要用它起子进程跑用户代码，所以不能用把 Python 冻结掉的方案，或者要能证明冻结方案也能起子进程跑 harness。
3. **GitHub Actions**：
   - `ci.yml`：24 已经写了三系统测试，接着用。
   - `release-payload.yml`：推送到 main 后，测试通过就生成 payload 并发布。发到一个固定的 Release（比如 `payload-latest`），旧资产替换掉，保留最近 5 个带版本号的 payload 方便回退。
   - `release-app.yml`：打 tag（`app-v*`）时为三个系统构建安装包，发布到对应的 Release。
4. **开发模式不受影响**：主控和 codex 在这台台式机上照旧用 `dojo`、Vite 和 Docker 开发。打包应用读的是用户数据目录里的 payload，不读仓库工作区。
5. **文档**：
   - `docs/README.md` 加"桌面应用"一节，写明它是怎么组成的、更新流程、令牌、怎么发新版。
   - `deploy/README.md` 加一节"在一台新电脑上用"：
     1. 下载安装包；
     2. 建令牌；
     3. 第一次打开；
     4. 可选：装 Claude Code 并登录，打开 AI。

## 验收标准

1. 新代码的单元测试全过，`pytest -q` 全过。
2. 在本机（Linux）实际构建 Linux 产物，模拟一台新电脑：用全新的临时用户数据目录，令牌用假的，payload 用本地假服务提供。走一遍：
   - 第一次打开下载 payload → 打开浏览器能做题；
   - 改一下 payload 版本 → 再打开时自动更新；
   - 断网 → 用旧版本照常启动。

   截图放 `{RUN_DIR}/`。
3. 三个 workflow 文件语法检查通过。macOS 和 Windows 的构建步骤写好，等主控推到 GitHub 后由 Actions 验证。报告里列出主控推送后要看哪几个 job。
4. 用户的 8000 和 5173 实例没被动过，`server/data/` 没被改过。
