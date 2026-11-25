# 61-agent-env：桌面版找得到助教命令，调用时带上登录所需的环境变量（issue #3、#5）

## 背景
用户 2026-11-24 在 Mac 上实测 1.3.0 后开了 6 个 issue，今天说："现在我想 把这6条解决一下，分别先做一下能修的部分，然后其他conflict的问题的话看看出一个推荐方案这样 …… 可以并行做"。

本任务负责其中两条，先用 `gh issue view 3` 和 `gh issue view 5` 读全文（只读，不要评论、不要改 issue）：
- **#3**：从程序坞 / 访达打开时，PATH 只有 `/usr/bin:/bin:/usr/sbin:/sbin`，`shutil.which("claude")` 找不到 `~/.local/bin/claude`，启动器把 `CODE_DOJO_AI_PROVIDER` 设成 off。Linux 上从应用菜单打开 AppImage 也可能遇到。
- **#5**：`CliProvider._run()` 只放行 `HOME`、`PATH`、`LANG`，没有 `USER`。macOS 上 Claude Code 的登录凭据存在钥匙串里，没有 `USER` 就读不到，于是报 "Not logged in"。从终端启动也一样。

同时在跑的其他任务：62 改 `desktop/` 和 `.github/workflows/release-app.yml`，63 改 `web/`，64 只写 `docs/tutor-memory.md`。这些文件你都不要碰。

## 两种代码的发布方式（决定改法的硬约束）
- `bootstrap/` 打在**安装包**里，要等下一版安装包 1.3.1 才会到用户手里。
- `server/app/` 打在**更新包**里，推送 main 后已安装的 1.3.0 会自动更新到。
- 所以 `server/app/` 的改动必须在旧启动器（1.3.0 的 bootstrap）下也能正常工作；bootstrap 也不要依赖更新包里新增的函数。
- 桌面版里，启动器（`bootstrap/service.py`）和后端在**同一个进程**：`serve()` 先调 `has_agent()`，再 `import app.main`，后端的 `Settings` 读的是同一个 `os.environ`。`bootstrap/protocol.py` 是另一个进程，也调用了 `has_agent()`，给设置页显示"AI 助教已启用 / 已关闭"。`dojo.py`（源码运行的启动器）也用 `has_agent()`。

## 要做的事
1. **#5（走更新包，优先）**：`server/app/ai/provider.py` 的 `_run()` 放行 `USER`、`LOGNAME`。在放行列表旁边用一两行注释写清每个变量为什么要放行，免得以后被当成多余的删掉。补一个测试：用假 CLI（比如一个打印环境变量的小脚本）或者 monkeypatch `subprocess.run`，断言传给子进程的 env 里有 `USER`。
2. **#5 的错误提示**：Claude Code 返回 "Not logged in" 一类错误时，助教栏显示的错误改成一句能照着做的话，比如让用户在终端运行 `claude auth status` 确认登录状态。Codex 登录失败的提示同理，只改措辞，不加重试。
3. **#3（走安装包）**：在 `bootstrap/agents.py` 里改。`which` 先找；**只有找不到时**，在 macOS 和 Linux 上用登录 shell 读一次 PATH（`$SHELL`，没有就用 `/bin/zsh`（macOS）或 `/bin/sh`；参数 `-ilc`；用前后标记把 PATH 截出来，因为交互式 shell 启动时可能打印别的内容；限时约 3 秒）。读到的目录并进 `os.environ["PATH"]` 后再找一次。同一进程只读一次。Windows 不变。
   - 这样从终端启动、Windows、已经能找到命令的情况，启动时间完全不受影响。
   - 并进 `os.environ` 以后，同一进程里的后端（`shutil.which`、`subprocess.run` 的 PATH）自然也能找到。
4. **启动器和后端的判断要一致**：#3 指出 `find_codex` 在 `bootstrap/agents.py` 和 `server/app/ai/provider.py` 各写了一份，容易出现一边说找到、另一边运行时找不到。受上面"两种发布方式"的约束，两份代码没法简单合成一份。推荐做法：启动器找到后，把绝对路径写进 `CODE_DOJO_CLAUDE_BIN` / `CODE_DOJO_CODEX_BIN`（只在用户没有自己设置时写），后端拿到绝对路径就不用再找。后端自己的查找只留给不经过启动器、直接跑 uvicorn 的开发模式。如果你读完代码有更简单、也满足版本约束的办法，可以换，在报告里标"推断"并写理由。
5. **常见安装目录兜底（issue #3 的方案 B）这次不做**：终端里能找到命令，登录 shell 就能找到。终端里也找不到，说明 PATH 本身没配好，安装说明里已经有对应的排查步骤。
6. **文档**：
   - `docs/README.md` 里"订阅和命令"那段（约 295 行）写清现在的查找顺序，以及哪些环境变量会传给 CLI。
   - `deploy/README.md` 只改"设置里显示'AI 助教已关闭'"这一节和接 Claude Code / Codex 的说明。macOS 从程序坞打开现在也能找到（新版安装包起）。保留 `CODE_DOJO_CLAUDE_BIN` 这条最后手段，用 `launchctl setenv` 设置，并写明重启电脑后要重新设一次。不要动安装、首次打开那几节，那几节归 62。
   - 不要改版本号（`bootstrap/__init__.py` 的 VERSION、`desktop/package.json`），发版由主控统一改。

## 这次不做
- 不改 `desktop/`、`web/`、`.github/`。
- 设置页显示"检测到的命令路径"（issue 里的可选项）不做。
- 不做常见目录兜底，也不加重试。

## 验收标准
- `cd server && .venv/bin/python -m pytest -q` 全过（报告里写数字）。
- `cd server && .venv/bin/python -m pytest -q ../bootstrap/tests` 全过。为登录 shell 读 PATH 加测试：用一个假的 `SHELL` 脚本，先打印杂讯、再打印带标记的 PATH，断言 `has_agent()` 能找到放在那个 PATH 里的假 `claude`；再测一次 `which` 直接能找到时不会去启动 shell。
- 模拟 GUI 启动：`env -i HOME=$HOME USER=$USER SHELL=$SHELL PATH=/usr/bin:/bin` 下跑 `has_agent()`（本机的 claude 在 `~/.local/bin` 或类似位置，`command -v claude` 先确认），能找到；同样条件下看后端 `available_agents()` 也列出 claude。只看探测结果，不要真的调用 claude 或 codex。
- 测试端口如需起后端用 8011。不要跑真实 AI。
