# 59-guest-mode：第二套密码 = 访客模式（只更新题库，进度只存本机）

## 背景

用户 2026-11-23："我想做这样一个功能 如果下载了以后输入另一套密码 这样就是只做题库同步 做题进度可以本地保存这样（每个下载都是新的进度，然后输入以后别人可以自己存自己的做题进度，然后每次开始的时候可以同步一下题库这样我可以分发给一些其他人用），我把这样的一套密码放在env的password2变量里了"

现状（读 `docs/README.md` 的「桌面应用」和 `deploy/README.md` 的「在一台新电脑上用」）：
- 安装包里的 `sealed-tokens.json` 用一个解锁密码加密（scrypt + AES-256-GCM），里面有题库仓库和进度仓库两个令牌。
  - 实现：`bootstrap/sealed.py`；生成：`scripts/desktop/seal_tokens.py`；CI 里用 Actions 密钥 `CODE_DOJO_SEALED_TOKENS` 写进安装包，见 `release-app.yml`。
- 首次解锁后凭据存进系统钥匙串或本机文件（`bootstrap/credentials.py`）。
- 启动器查更新必须有令牌（`bootstrap/update.py` 的 `check()`：没有令牌直接返回"请在设置中填写令牌"）。
- **仓库 `Rebas9512/code_dojo` 已经公开**，`payload-latest` Release 不需要令牌就能读和下载。进度仓库 `code_dojo_sync` 仍是私有的。

## 要做的事

1. **加密文件改成多个槽（v2）**：
   - 一个文件里有多个独立加密的槽，各自有盐和 nonce，同一套 scrypt 参数。
   - 解锁时依次试每个槽，能解开哪个用哪个。
   - 明文是 JSON，带 `profile` 字段：
     - `owner`：`{"profile": "owner", "code": ..., "sync": ...}`，和现在一样；
     - `guest`：`{"profile": "guest"}`，**不含任何令牌**。
   - 不用兼容 v1 文件：发新安装包之前主控会重新生成并上传密钥。测试里的 v1 夹具相应更新。
2. **`seal_tokens.py`**：新增 `--guest-password-key`（比如 `password2`），从同一份 `.env` 读访客密码，再加一个 guest 槽。
   - 用法：`--password-key password --guest-password-key password2`。
   - 生成 v2 文件，照旧通过 gh 上传成 `CODE_DOJO_SEALED_TOKENS`。
   - 访客密码和主密码不能相同，相同就报错。
3. **访客模式（启动器）**：
   - 用访客密码解锁后，在凭据存储里记下 `profile: guest`（不存任何令牌）。之后打开直接进访客模式，不再问密码，和主人模式首次解锁后的体验一样。
   - 访客模式下**不带令牌**查更新、下载更新包，走公开仓库，未认证请求即可。主人模式要是没有令牌，也照这样查更新。
   - 访客模式下**关闭进度同步**：不设 `CODE_DOJO_SYNC_REPO`，或者用等价方式让后端不同步。做题记录只写本机数据目录。
   - JSONL 协议的 `ready` 消息加 `profile` 字段，前端据此显示。
4. **界面**：
   - 桌面启动页和设置里显示"访客模式：只更新题库，做题记录保存在本机"。不显示令牌设置，也不提示"填写令牌以开启同步"。
   - 做题页状态栏的同步状态在访客模式下显示"本机保存"，不显示"未开启同步"。
   - 设置里给一个"换一个密码解锁"按钮：清掉已存的凭据，回到解锁页。方便一台机器从访客换成主人，或者反过来。
5. **文档**：
   - `deploy/README.md` 加一节"分发给别人用"：发安装包链接和访客密码；访客的记录只在他自己电脑上；每次打开自动更新题库；AI 助教要他自己装 Claude Code 或 Codex。
   - `docs/README.md` 的桌面一节相应更新。

## 不做

- 不给访客任何令牌，不做访客之间的进度同步。
- 不改后端判题、题库和网页的做题功能。
- 不改 `bootstrap.VERSION` 和 `desktop/package.json` 的版本号（主控发版时改）。

## 安全

- 不读、不打印、不写进日志或报告任何真实的令牌和密码。测试一律用假值。
- `.env` 不要动，也不要复制。

## 验收标准

- `cd server && .venv/bin/python -m pytest -q ../bootstrap/tests` 和 `cd server && .venv/bin/python -m pytest -q` 全过（7 个会建临时 git 仓库的同步测试可以按标准做法排除）。新增测试覆盖：
  - v2 两个槽各自能解开，错密码两个都解不开；
  - guest 槽里没有令牌；
  - 访客解锁后凭据存储只有 profile；
  - 访客模式下查更新的请求不带 Authorization；
  - 访客模式下不启动进度同步；
  - `ready` 带 `profile`；
  - "换一个密码解锁"清掉凭据；
  - `seal_tokens.py` 用假 `.env` 生成两个槽、两个密码相同时报错。
- `node --check desktop/*.cjs desktop/*.js`（或项目现有的桌面测试方式）通过；`cd web && npm run build` 通过。
- 用假的密文和假更新服务，在本机起一次启动器走访客流程：解锁 → 拿到 ready（profile guest）→ 后端没有同步。写清怎么测的。
- 报告写清楚：v2 文件格式、凭据存储里记了什么、访客模式下哪些路径关闭了，以及发版前主控要做的步骤（重新加密上传密钥、改版本号、打标签）。
