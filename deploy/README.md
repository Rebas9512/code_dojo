# 安装和使用 code-dojo

code-dojo 是一个桌面应用。下载后打开就能练，不用注册账号，做题记录只保存在你自己的电脑上。界面和题目都是中文。

AI 助教是可选的，要在你电脑上自己装好并登录 Claude Code 或 Codex（见第 4 节）。不装也能用其他所有功能：课、判题、参考答案、项目和一组练习。

想从源码运行、给自己的仓库发版，或者部署到服务器上从浏览器访问，请看 [self-host.md](self-host.md)。

## 1. 下载

打开最新的 Release 页面，在 Assets 里下载和你的系统对应的文件。[下载安装包](https://github.com/Rebas9512/code_dojo/releases/latest)

| 系统 | 下载哪个文件 | 大小 |
|---|---|---|
| Windows 10 / 11（x64） | `code-dojo-X.Y.Z-x64-windows.zip` | 约 220 MB |
| macOS，Apple 芯片（M1 及以后） | `code-dojo-X.Y.Z-arm64-mac.zip` | 约 160 MB |
| Linux x86-64 | `code-dojo-X.Y.Z-x86_64.AppImage`（打不开时换 `x86_64-linux.tar.gz`） | 约 220 MB |

目前没有 Intel Mac、ARM 版 Windows 和 ARM 版 Linux 的安装包，这些机器可以从源码运行。

请另外留出约 2 GB 磁盘空间，用来放题库和数据科学题的判题环境。

## 2. 第一次打开

Windows 和 macOS 首次打开时可能会要求确认，按对应系统的步骤操作即可。

### Windows

1. 右键 zip，选“全部解压缩”。请不要在压缩包里直接双击运行。
2. 打开解压出来的文件夹，双击 `code-dojo.exe`。
3. 如果弹出“Windows 已保护你的电脑”，先点“更多信息”，再点“仍要运行”。

整个文件夹都要保留，可以把它放到任意位置。想从桌面打开时，右键 `code-dojo.exe`，选“发送到 → 桌面快捷方式”。

### macOS

Apple 芯片版的 `.app` 带有 ad-hoc 签名，可校验安装包的完整性。Apple 尚未公证此版本，首次打开时可能提示“无法验证开发者”。

1. 双击 zip 解压，把 `code-dojo.app` 拖进“应用程序”文件夹。
2. 在“应用程序”里双击 code-dojo。如果系统拦截，关掉提示，随即打开“系统设置 → 隐私与安全性”，在 code-dojo 旁点“仍要打开”，按提示验证身份，再点“打开”。系统会记住这次选择。
3. 如果使用旧版本，或从本项目 Release 重新下载后仍提示“已损坏”，可在“终端”运行下面的命令移除下载隔离标记，再打开应用。

   ```sh
   xattr -dr com.apple.quarantine /Applications/code-dojo.app
   ```

### Linux

在下载目录打开终端，给文件加上执行权限，再放进 `~/Applications`。命令里的 `X.Y.Z` 要换成实际的版本号：

```sh
chmod +x code-dojo-X.Y.Z-x86_64.AppImage
mkdir -p ~/Applications
mv code-dojo-X.Y.Z-x86_64.AppImage ~/Applications/
```

然后在文件管理器里双击就能打开。想让它出现在应用菜单里，可以用 AppImageLauncher 或 Gear Lever。

如果双击没有反应，多半是系统缺 FUSE。可以用下面两种办法之一：

- 安装 FUSE。Ubuntu 22.04 运行 `sudo apt install libfuse2`，Ubuntu 24.04 运行 `sudo apt install libfuse2t64`。
- 不装 FUSE，在终端用 `./code-dojo-X.Y.Z-x86_64.AppImage --appimage-extract-and-run` 启动。

也可以不用 AppImage：下载 tar.gz，完整解压后运行里面的 `./code-dojo`。

### 第一次启动会做什么

- 应用会先联网下载题库（约 25 MB），窗口里有进度条。下载完会自动进入学习地图。
- 以后每次打开，应用都会在后台检查题库更新，下载好的新题库从下一次启动开始生效。题库下载过一次之后，不联网也能练。
- 做 Python 基础、算法和 SQL 题，不需要再下载任何东西。
- 数据处理、张量、机器学习这几类题会用到 numpy、pandas 和 PyTorch。第一次交这类题时，应用会自动下载这三个库，装好后约 1 GB，要等几分钟。以后就不用再下载了。

## 3. 开始练习

- **学习地图**是首页。所有路线都从“认识数据”开始，之后再分成 Python、算法、SQL、机器学习等分支。
- **继续**按钮会带你去当前路线里最新的进度，不会让你回到第一题。前面跳过的题，等后面的都做完了再补。
- **一组练习**一次给你 3、5 或 8 道新题，并打开全屏专注模式；当前题通过后自动进入下一题。想先做到期的复习题，可以在“热身”里选“先做到期复习”。
- 题目通过以后，可以打开**参考答案**，和自己的代码逐行对比。

完整的功能介绍和截图见仓库首页。[功能介绍](../README.md)

## 4. 接上 AI 助教（可选）

应用本身不带 AI，也不需要 API key。它会在你的电脑上调用 `claude` 或 `codex` 命令行工具，这两个工具需要你自己安装并登录，用量计入你自己的订阅。助教能看到题目、你的答案、你的草稿和对话内容，这些会发给 Anthropic（Claude）或 OpenAI（Codex）。

应用调用助教时不给它额外权限：Claude 的所有工具都被关掉；Codex 在只读沙箱里运行，不能修改你电脑上的文件。助教对答案和草稿的修改，由应用写进编辑器。

Claude Code 和 Codex 装一个就行。两个都装了的话，可以在助教栏里切换。

### 用 Claude Code

需要一个能在 Claude Code 里用 `claude-opus-5-5` 模型的 Claude 账号。

1. 安装。macOS 和 Linux 在终端运行：

   ```sh
   curl -fsSL https://claude.ai/install.sh | bash
   ```

   Windows 在 PowerShell 里运行：

   ```powershell
   irm https://claude.ai/install.ps1 | iex
   ```

   其他安装方式（Homebrew、WinGet、npm）见官方文档。[Claude Code 安装说明](https://code.claude.com/docs/en/setup)
2. 新开一个终端窗口，运行 `claude`，按提示在浏览器里登录。登录好以后输入 `/exit` 退出。
3. 在新开的终端里运行 `claude auth status`，确认输出中的 `loggedIn` 为 `true`（已登录）。

### 用 Codex

需要 ChatGPT 的付费计划（Plus、Pro、Business 等），并且要用“Sign in with ChatGPT”登录。用 API key 登录的 Codex 不能给 code-dojo 用。应用调用的模型是 `gpt-6.2-astra`。

1. 安装。装了 Node.js 的话，运行 `npm install -g @openai/codex`；macOS 也可以运行 `brew install --cask codex`。其他方式见官方文档。[Codex CLI 安装说明](https://developers.openai.com/codex/cli)
2. 运行 `codex`，选 “Sign in with ChatGPT”，在浏览器里登录。
3. 在新开的终端里运行 `codex login status`，确认显示已用 ChatGPT 登录。

如果你已经在 VS Code 里装了 OpenAI 的 ChatGPT / Codex 扩展，并且已经登录，可以跳过上面的步骤，应用会自动找到扩展自带的 codex。

### 让应用认出助教

1. 装好、登录好以后，**完全退出** code-dojo 再打开。应用只在启动时查找助教。退出方法：用菜单里的“退出”，或者按 Ctrl+Q（macOS 按 Cmd+Q）。
2. 打开顶栏的“桌面 → 设置”。最下面显示“AI 助教已启用”，就说明已经接上了。
3. 进入任意一道题，右侧的助教栏就可以用了。助教栏顶部的下拉框可以切换 Claude 和 Codex。

### 设置里显示“AI 助教已关闭”

先在**新开的**终端里运行 `claude --version` 或 `codex --version`：

- **终端里也找不到命令**：说明命令所在的目录不在 PATH 里。请按安装程序最后的提示，把这个目录加进 PATH。Claude Code 默认装在 `~/.local/bin`；Windows 上是 `%USERPROFILE%\.local\bin`。加好以后，新开一个终端再试。
- **终端里能找到，应用里找不到**：
  1. 在 macOS 或 Linux 终端运行 `command -v claude` 或 `command -v codex`。在 Windows PowerShell 运行 `where.exe claude` 或 `where.exe codex`，选择输出中的 `.exe` 或 `.cmd` 文件。
  2. 打开“桌面 → 设置”，在“AI 助教”下找到对应命令，粘贴完整路径。也可以点“浏览…”选择文件，包括 `~/.local/bin` 等隐藏目录里的文件。如果看不到路径输入框，请先更新桌面安装包。
  3. 点“保存”。应用会运行一次 `--version` 检查文件，成功后会显示“手动指定”和实际路径，回到练习即可使用。位置只保存在这台电脑上，重启后仍然有效。要撤销时，点“改回自动查找”。

如果设置里显示已启用，但提问时报登录错误，在终端运行 `claude auth status` 或 `codex login status`。如果显示未登录，按上面对应的步骤登录。如果终端显示已登录，1.3.0 用户可以先从应用菜单“检查更新”取得助教登录修复，再试一次。

## 5. 记录保存在哪

所有数据都在下面这个文件夹里，包括做题记录、草稿、助教对话、题库和判题环境：

| 系统 | 位置 |
|---|---|
| Windows | `%APPDATA%\code-dojo` |
| macOS | `~/Library/Application Support/code-dojo` |
| Linux | `~/.local/share/code-dojo`（设置了 `XDG_DATA_HOME` 时是 `$XDG_DATA_HOME/code-dojo`） |

- **备份**：先退出应用，再复制整个文件夹。
- **换安装位置**：退出应用后，可以随意移动或替换安装包，记录不会受影响。
- **同步**：“桌面 → 设置”里的同步码是作者给自己多台电脑同步用的，你不用填。不填的话，记录只保存在本机，顶栏显示“本机保存”。想用自己的私有仓库在多台电脑之间同步，需要从源码运行。[从源码运行和自己的同步仓库](self-host.md#从源码运行和自己的同步仓库)

## 6. 更新

- **题库**会自动更新。不想等的话，可以用菜单里的“检查更新”手动检查。新题库从下一次启动开始生效。
- **应用本身**需要更新时，窗口里会出现“下载新版安装包”的链接。下载后按第 2 节的方法替换旧版：Windows 删掉旧文件夹，解压新的 zip；macOS 用新的 `code-dojo.app` 覆盖“应用程序”里的旧版；Linux 用新的 AppImage 替换旧的。记录保存在数据文件夹里，替换后都还在。

## 7. 卸载

先删掉应用（Windows 是解压出来的文件夹，macOS 是“应用程序”里的 `code-dojo.app`，Linux 是 AppImage 文件），再删掉第 5 节表格里的数据文件夹。

## 8. 其他问题

- **第一次打开时题库下载失败**：应用要从 github.com 下载题库。如果你需要代理，Windows 和 macOS 打开系统代理就可以；Linux 要先在终端里设置 `HTTPS_PROXY`，再从同一个终端启动应用。
- **数据科学判题环境装不上**：这一步要从 PyPI 和 download.pytorch.org 下载，请检查网络和磁盘空间，然后重新交卷。
- **问题反馈**：这是个人项目，作者不接收 issue 和 PR。代码用 MIT 许可公开，欢迎 fork 后自己修改。
