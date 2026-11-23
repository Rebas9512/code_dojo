# 24 · 平台：本地判题模式（不靠 Docker，Linux / macOS / Windows 三个系统都能跑）

## 背景

用户 2026-11-22 说：
- "能不能把这个项目做成调用机器本地python之类的 然后github存题库每次同步题库就行 本地跑编译检查什么的可以这样做吗"
- "做成3系统支持吧，那这样还能做成一个网页的形式吗"

主控定的方案：
- 每台机器本地跑 code-dojo，形式还是网页，`localhost` 加浏览器。
- 题库和代码放在 GitHub 私有仓库，`git pull` 同步。
- 判题用本机的 Python，**不要求 Docker**。
- 三个系统都支持。

这次只做**判题**这一块。启动器和进度同步是 25 号任务，两个任务同时跑。

现状：
- `judge/python/harness.py` 是纯 Python，用 SIGALRM 和 setitimer 做每个用例的超时（Windows 上没有）。它设了 `sys.setrecursionlimit(200000)`，配合 Docker 的 `--ulimit stack=256MB`。
- `server/app/judge.py` 用 `docker run` 跑 harness，按 runtime 选镜像，python 或 ds（数据科学）。
- 课的 playground 和附加题验证也走 `Judge`。

**并行**：先读 `codex/PLAN.md`。
- 25 号任务会改 `server/app/config.py`、`db.py`、新建启动器。你只在 `config.py` 里加判题相关的配置项，用小补丁改。
- 16（算法阶段 5）、19（张量线）两个内容任务也在跑。

你名下的东西：
- `judge/`
- `server/app/judge.py`
- 新建的本地判题模块
- `.github/workflows/`
- `docs/README.md` 的判题一节

## 要做的事

### 1. harness 跨平台

- **每用例超时**：不再用信号，改成三个系统都能用的做法。
  - 用户代码在一个**大栈的工作线程**里跑：`threading.stack_size(256 * 1024 * 1024)`，Windows 上如果上限更小就取能用的最大值。
  - 主线程等它，等到超时就判 TLE，跳过剩下的用例，然后 `os._exit` 结束进程，和现在"超时后跳过其余用例"的行为一致。
  - 外层再由调用方按总时间预算杀进程，兜底。
- **深递归**：递归上限照旧 200000。`@cache` 递归 5 万层，在三个系统上都要能过：现在 Docker 里实测能过，本地也要。
- **Docker 也用同一份 harness**：Docker 判题照旧，两个镜像都要重新 build 并测过。
- **行为不能变**：除了超时机制，判题结果、输出格式、报错行号这些都不能变。现有测试必须全过。

### 2. 本地判题后端（`Judge` 加 local 模式）

- 配置 `CODE_DOJO_JUDGE=auto|docker|local`：
  - auto：本机有 Docker 而且镜像已经建好就用 docker，否则用 local。
  - `/api/status` 里显示当前用的是哪种。
- **local 模式**：
  - 在临时目录里写好 job，用**专用的 Python 解释器**以 `-I` 模式运行 harness，工作目录是临时目录。
  - 总时间预算和 Docker 一致，超时就杀掉进程树。Windows 上用 `subprocess` 的进程组或 Job 对象；能简单做到的话，就把整棵进程树一起杀掉。
- **内存上限，尽力而为**：
  - Linux 用 `resource.setrlimit(RLIMIT_AS)`。
  - macOS 和 Windows 做不到也可以，报告里写清楚。
  - 超内存时尽量报"内存超限"，和 Docker 的 137 一样处理。
- **断网做不到**：报告里写一句。用户跑的是自己的代码，主控接受这一点。
- **判题用的 Python 环境**，由 uv 管理，放在数据目录下，比如 `<数据目录>/judge-envs/`：
  - python runtime：`uv python install 3.14`，再建一个干净的 venv，不装第三方包，和判题镜像一致。
  - ds runtime：单独一个 venv，装 numpy、pandas、CPU 版 torch，版本和 `judge/ds/Dockerfile` 锁定的一致。
    - torch 在 macOS 和 Windows 上用各自平台的 CPU 包。
    - 第一次用到 ds 题时才安装，界面上提示"正在准备数据科学环境（约 X 分钟，只需一次）"。
    - 装不上就给出清晰的中文报错。
  - 找不到 uv 时给出中文报错和安装指引，三个系统各一行命令。
- **playground、附加题验证、`verify_bank.py`**：都能走 local 模式。`verify_bank.py` 加 `--judge local|docker` 参数。

### 3. 跨平台的细节，逐项检查

- 路径用 `pathlib`，临时目录用 `tempfile`，不写死 `/tmp`。
- **AI 助教**（`server/app/ai/provider.py`）：现在只给子进程留 HOME、PATH、LANG。
  - Windows 上 `claude` 可能是 `claude.cmd`，要用 `shutil.which` 解析出来。
  - Windows 上还需要 `USERPROFILE`、`APPDATA`、`LOCALAPPDATA`、`SystemRoot`、`TEMP` 这类变量。按平台补齐最小集合，不要整体继承。
- 文本文件读写一律 `encoding="utf-8"`，Windows 默认不是 UTF-8。
- 换行符：比较输出时 `\r\n` 和 `\n` 要等价，或者统一处理。
- 检查一下后端其他地方有没有依赖 Unix 才有的东西，比如 `signal`、`fcntl`、`os.getuid`、`/proc`，一并改掉。

### 4. 三个系统的持续集成

- 写 `.github/workflows/ci.yml`，矩阵是 ubuntu-latest、macos-latest、windows-latest：
  - 装 uv 和 Node；
  - `uv sync`；
  - 用 `CODE_DOJO_JUDGE=local` 跑后端 pytest；
  - 跑 `verify_bank.py --judge local --only py-0a- --jobs 2` 做冒烟，再挑几道深递归的算法题和 1 道 ds 题（ds 环境装起来比较慢，可以只在 ubuntu 上跑）；
  - 前端 `npm ci && npm run build`。
- 仓库现在还没推到 GitHub，这个 workflow 你在本地写好就行，主控推上去以后再看结果。本地用 `act` 之类的工具跑**不需要**。

### 5. 测试和文档

- **pytest**：
  - local 模式也要跑通整套判题测试：参数化 docker 和 local；没有 Docker 的环境自动只跑 local。
  - 新增：超时（死循环）、深递归、内存超限（只在 Linux 上测）、Windows 风格的换行。
- **`docs/README.md`**：
  - 判题一节改成"Docker 或本地两种"，写清楚两种的隔离程度有什么差别。
  - 「怎么跑」加 local 模式。

## 验收标准

1. 本机（Linux）上：
   - `CODE_DOJO_JUDGE=local` 和 `docker` 两种模式下，`pytest -q` 都全过。
   - `verify_bank.py --judge local` 全题库通过（ds 线也要，第一次装环境的耗时写进报告）。
   - `--judge docker` 照旧全过。
2. 两种模式下同一批题的判题耗时对比，比如 `py-0a` 全部、`algo-3` 全部，写进报告。
3. 判题结果一致：两种模式对同一批题、同样的错误解，verdict 完全一样。用脚本对比，写进报告。
4. `.github/workflows/ci.yml` 写好，YAML 语法检查通过。
5. 用户的 8000 和 5173 实例没被动过，`server/data/` 没被改过。
