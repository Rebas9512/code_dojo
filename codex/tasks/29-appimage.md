# 29 · Linux 打包成 AppImage（配合 AppImageLauncher 放进 ~/Applications）

## 背景

用户 2026-11-22 说："话说linux的能不能做成一个那种appimage之类的然后像其他应用一样放在/home/yixin/Applications目录里面那种"

用户机器上用的是 **AppImageLauncher Lite**：
- `~/Applications` 里放着 Obsidian、LM Studio、Pencil 等 AppImage；
- 它会自动生成 `~/.local/share/applications/appimagekit_<hash>-<名字>.desktop` 菜单项，图标和名字取自 AppImage 内嵌的 `.desktop` 文件和图标。

现状：
- 26、28 号任务做的 Linux 产物是 `code-dojo-<版本>-x86_64-unknown-linux-gnu.tar.gz`，由 `scripts/desktop/build.py` 生成，由 `.github/workflows/release-app.yml` 在 `app-v*` 标签时构建。
- 28 加入了 `sealed-tokens.json`（加密的令牌）。

**动手前先读**：
- `codex/runs/26-desktop-app-*/report.md`
- `codex/runs/28b-continue-*/report.md`
- `scripts/desktop/`
- `bootstrap/`
- `release-app.yml`

**并行**：这次只有你一个任务。

启动器版本保持 `1.0.1`（`bootstrap/__init__.py`）。这个版本还没发布，主控会在你交付后打 `app-v1.0.1` 标签，AppImage 跟着这个版本一起发。令牌的加密结果已经由主控存成 Actions 密钥 `CODE_DOJO_SEALED_TOKENS`，CI 构建 AppImage 时照样放进去。

## 要做的事

1. **AppImage 产物**：`code-dojo-<版本>-x86_64.AppImage`。tar.gz 保留，作为备用。
   - **AppDir 结构**：
     - 内置的 python-build-standalone 运行时，带 Tk；
     - `bootstrap/`；
     - 运行时依赖；
     - `sealed-tokens.json`（构建时有就放）；
     - `AppRun`：启动内置 Python 跑 bootstrap；
     - `code-dojo.desktop`：`Name=code-dojo`，`Comment` 用中文一句话，`Categories=Education;Development;`，`Icon=code-dojo`，`Terminal=false`，`StartupWMClass` 和 Tk 窗口的 class 一致，这样任务栏图标能对上；
     - 图标：PNG 256×256，加一份 SVG。
   - **打包工具**：用 appimagetool（官方 AppImage/appimagetool 的 continuous 或固定版本，校验 SHA-256）。在 CI 和沙箱里没有 FUSE 时，用 `--appimage-extract-and-run` 方式运行 appimagetool。
   - **glibc 兼容**：构建用的系统尽量老一点，比如 ubuntu-22.04 runner。在报告里写清最低支持的 glibc 版本。
2. **只读文件系统**：AppImage 运行时挂载在只读的 squashfs 上。逐项确认启动器不往应用目录里写任何东西：
   - 依赖缓存、payload、判题环境、日志、令牌、锁文件，都要在用户数据目录（`~/.local/share/code-dojo`，或 `CODE_DOJO_DATA`）；
   - 发现有写到安装目录的地方就改掉。
   - 判题子进程用的是内置 Python 解释器的路径，指向 AppImage 的挂载点，只要应用在跑它就一直有效。确认 local 判题和 DS 环境安装（pip 装到数据目录）在 AppImage 里都能正常工作。
3. **图标**：按 `.impeccable.md` 的风格设计一个简洁的图标，字少，可以用"道"或者一个代码符号的抽象图形，深色和浅色桌面上都要清楚。网页的 favicon 也换成同一个图形，保持一致。
4. **CI**：`release-app.yml` 的 Linux job 同时产出 AppImage 和 tar.gz，都发到 Release。Release 说明里写一句"Linux 推荐下载 AppImage"。
5. **文档**：`deploy/README.md`「在一台新电脑上用」的 Linux 部分改成：
   - 下载 AppImage；
   - `chmod +x`；
   - 放进 `~/Applications`，有 AppImageLauncher 或 Gear Lever 会自动加进菜单；
   - 双击打开。

## 验收标准

1. 本机构建出 AppImage，大小写进报告。用 `--appimage-extract-and-run` 方式实测，假令牌、假 payload 服务、全新数据目录：
   - 第一次打开 → 下载 payload → 浏览器能做题，Python 题和 DS 题各交一道；
   - 第二次打开走缓存。
2. 解开 AppImage 检查 `.desktop` 文件：`desktop-file-validate` 能跑就跑；图标路径正确。
3. 确认运行前后，AppImage 解出来的目录没有新增或修改的文件：拿文件清单和哈希做对比。
4. `pytest -q` 全过；workflow 文件语法检查通过。
5. **不要**把 AppImage 放进用户的 `~/Applications`，那一步由主控用 CI 构建出的正式版本来做。不要动用户的 8000 和 5173 实例。
