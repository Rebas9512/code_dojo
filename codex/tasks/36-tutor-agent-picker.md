# 36-tutor-agent-picker：助教支持 Codex，下拉选择本机有的 agent

## 背景

用户 2026-11-23 原话："然后助教的话帮我也支持一下codex吧 就是做个下拉选项选择本机有的agent这样 有Claude就可以选claude 有codex可以选codex，如果都有就都可以选这样"

现状：
- `server/app/ai/provider.py`：只有 `ClaudeCodeProvider`，调 `claude -p --json-schema …`，用本机订阅，返回 `structured_output`。
- `server/app/main.py`：全局 `ai`，由 `settings.ai_provider == "claude"` 决定。`/api/status` 返回 `ai` 和 `ai_model`。
- 用到 AI 的地方：助教聊天（`ai/tutor.py`）和出附加题（`ai/extra.py`，后台线程）。都调 `provider.complete(system, prompt, schema, effort)`。
- 前端：`web/src/components/ChatPanel.tsx`，`aiOn` 由 `ProblemWorkspace.tsx` 传进来（`status.ai !== 'off'`）。
- 桌面启动器：`bootstrap/service.py` 找不到 `claude` 就把 `CODE_DOJO_AI_PROVIDER` 设成 `off`；`bootstrap/protocol.py` 按 claude 是否存在报 AI 状态；`desktop/startup.js` 显示"需要时请安装并登录 Claude Code"。

用户的 AI 走订阅：Claude 用 Claude Max 订阅，Codex 用 ChatGPT 登录（本机 `codex login status` → Logged in using ChatGPT）。不走 API 按量计费，不要求 API key。

## 本机 codex 的情况（主控实测）

- codex 不一定在 PATH 里。这台机器上只有 VS Code 插件自带的那份：`~/.vscode/extensions/openai.chatgpt-<版本>/bin/linux-x86_64/codex`，版本 `codex-cli 0.171.0-alpha.13`。
  - macOS 上目录是 `bin/macos-aarch64/codex`，Windows 上是 `bin/windows-x86_64/codex.exe`。
  - 插件可能装了好几个版本，取版本号最大的。
- 无交互调用用 `codex exec`，可用的参数：
  - `--output-schema <FILE>`：最终回复按 JSON Schema 输出。
  - `-o/--output-last-message <FILE>`：最后一条回复写进文件。
  - `--ephemeral`：不落会话文件。
  - `--skip-git-repo-check`、`--sandbox read-only`、`-C <DIR>`、`-m <MODEL>`。
  - `--ignore-user-config`：不读 `~/.codex/config.toml`，登录照样用 `CODEX_HOME`。
  - `--ignore-rules`。
  - `-c key=value`：推理强度是 `-c model_reasoning_effort="low"`。
  - 提示词可以从 stdin 读（参数写 `-`）。
- 没有 `--system-prompt-file` 这种参数。系统提示怎么传自己查：看 `-c developer_instructions=…` / `-c instructions=…` 这类配置在 0.171 有没有效。查不实就把系统提示放在 stdin 提示词的最前面，用清楚的分节。选了哪种写进报告。
- OpenAI 的结构化输出要求严格 schema：
  - 每个 object 都要 `additionalProperties: false`；
  - `required` 必须列出全部属性，原本可选的字段改成"类型 | null"；
  - 部分关键字不支持，比如 `default`，以及某些 `format` / `pattern` 用法，要去掉。
  - 现有 schema（tutor 的 `SCHEMA`、extra 的 `INSPECT_SCHEMA`、`SqlExtra.model_json_schema()`、extra 里 Python 题的 schema）都要能转换。转换后结果里多出来的 `null` 可选字段要去掉，让下游代码拿到的形状和 Claude 一样。

## 要做的事

1. **后端：provider 层**（`server/app/ai/provider.py`）
   - 新增 `CodexProvider`，接口和 `ClaudeCodeProvider.complete()` 一样，走 `codex exec`。在专用空临时目录里运行，只读沙箱。环境变量只留必需的：`HOME`、`PATH`、`LANG`、`CODEX_HOME`，Windows 再加和 Claude 那边同一组。
     - 超时、并发槽和 Claude 一样。
     - 推理强度映射：low→low、medium→medium、high→high，xhigh / max→xhigh。
     - 用到的临时文件（schema、输出）用完删掉。
     - 报错写成中文，比如找不到命令、超时、没返回 JSON。
   - 严格 schema 转换和结果去 null 写成独立函数，方便单测。
   - 找 agent 的函数：返回本机可用的 agent 列表 `[{id: 'claude'|'codex', name: 'Claude' | 'Codex', model}]`。
     - Claude：`shutil.which(settings.claude_bin)`。
     - Codex：先 `shutil.which(settings.codex_bin)`，找不到再按上面的插件目录找。
     - 每次 `/api/status` 现查，查一次很便宜。provider 实例按 id 缓存复用（并发槽要共享）。
2. **后端：配置和接口**
   - `config.py` 加 `CODE_DOJO_CODEX_BIN`（默认 `codex`）和 `CODE_DOJO_CODEX_MODEL`（默认 `gpt-6.2-astra`）。
   - `CODE_DOJO_AI_PROVIDER` 的含义改成：`off` = 全关；`claude` / `codex` = 默认用哪个。默认值仍是 `claude`；默认的那个本机没有，就用另一个。
   - `/api/status`：`ai` 返回默认 agent 的 id，一个都没有返回 `off`。这样前端 `aiOn` 不用改。`ai_model` 是默认 agent 的模型。新增 `ai_agents` 列表。
   - 助教聊天和出附加题的请求体加可选字段 `agent`（`'claude' | 'codex'`），没给就用默认的。给了但本机没有，返回 400，带中文说明。附加题后台线程用发起请求时选的那个。
   - 测试里怎么注入 FakeProvider，跟着现有做法改好（看 `server/tests/` 里现有的写法和 `conftest.py`）。
3. **前端**
   - `api.ts`：`Status` 类型加 `ai_agents`。聊天和 `createExtra` 的请求带上 `agent`，取自偏好 `dojo-ai-agent`（用 `readPref`）。`createExtra` 自己在 `api.ts` 里读偏好，这样 `ProblemWorkspace.tsx` 不用改。
   - `ChatPanel.tsx`：顶部加下拉框，列出本机有的 agent，显示成 `Claude · claude-opus-5-5` / `Codex · gpt-6.2-astra`。
     - 选择存进偏好 `dojo-ai-agent`。存的那个不在列表里就用第一个。
     - 只有一个 agent 时下拉框照样显示，但禁用。一个都没有就保持现在的"AI 助教没有开启"，提示改成"安装并登录 Claude Code 或 Codex 后重新打开应用"。
     - agent 列表 ChatPanel 自己调 `api.status()` 取，或复用已有的 status 数据，看哪个改动小。**不改 `ProblemWorkspace.tsx`。**
     - 每条助教回复下面用小字淡色标出是哪个 agent 回的，中途切换后能分清。
     - 聊天历史切换 agent 后照常带上，新 agent 接着答。
   - 样式加在 `web/src/styles.css`。**不改 `workbench.css`**，那是并行任务 35 的文件。遵守 `.impeccable.md`。
4. **桌面启动器**：这部分随下一版安装包才生效，现在只改代码、跑测试，不发版。
   - `bootstrap/service.py`：claude 和 codex 都找不到才设 `off`。codex 的查找逻辑和后端一致，可以复用或复制一份小函数（bootstrap 不能 import server）。
   - `bootstrap/protocol.py`：AI 状态按"有任一 agent"算。
   - `desktop/startup.js`：提示文字改成"需要时请安装并登录 Claude Code 或 Codex，再重新打开应用。"
   - 不改 `bootstrap.VERSION`，不改 `desktop/package.json` 版本号。
5. **文档**：`docs/README.md` 里写 AI 接入和桌面版助教的地方补上 Codex：怎么找到命令、走订阅、怎么在助教里切换、新增的环境变量。只用小补丁改这几节，任务 35 也在改这个文件的别的节。

## 并行约束（任务 35 正在同时跑）

- 35 拥有：`web/src/components/ProblemWorkspace.tsx`、`web/src/components/WorkbenchPanel.tsx`、`web/src/components/workbench.css`。这三个文件不要碰。
- `docs/README.md` 两边都改，只用小补丁改你自己的节，不要整文件重写。
- 测试实例端口用 **后端 8002、前端 5175**。35 在用 8001 / 5174，用户的 8000 / 5173 也不要碰。

## 不做

- 不加 API key / 按量计费的接入方式。
- 不改助教和出题的提示词内容（只改传递方式）。
- 不加第三种 agent。
- **不跑真实的 claude 或 codex**（标准做法第 4 条）。真实调用由主控验收时跑。报告里给出一条主控可以直接跑的冒烟命令：用 CodexProvider 对 tutor 的 SCHEMA 发一次 low 强度的请求，再对 extra 的一个 schema 发一次。

## 验收标准

- `cd server && .venv/bin/python -m pytest -q` 全过。新增测试至少覆盖：
  - CodexProvider 拼出来的命令和环境变量（monkeypatch `subprocess.run`）；
  - 严格 schema 转换（对上面列的每个现有 schema 都转一遍并断言满足严格规则）和结果去 null；
  - 找 agent（monkeypatch `which` / 插件目录）：只有 claude、只有 codex、两个都有、都没有；
  - `/api/status` 的 `ai` / `ai_agents`；
  - 聊天请求带 `agent` 时用的是对应的 provider（FakeProvider 注入），给了本机没有的 agent 返回 400。
- bootstrap 的测试照旧全过（跑法看 `docs/README.md` 或 `.github/workflows/ci.yml`），再加一条"只有 codex 时 AI 不关"。
- `cd web && npm run build` 通过。
- 起测试实例（8002 / 5175，`CODE_DOJO_AI_PROVIDER=off` 时下拉框应显示没开启）。再用一个假的 `codex` 和 `claude` 脚本放进临时 PATH（脚本只打印固定 JSON，不联网），起一次后端看 `/api/status` 列出两个 agent，用 Playwright 打开做题页，看下拉框有两项、能切换、刷新后记住。截图放 `{RUN_DIR}/`。
