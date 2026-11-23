# 13 · M5：单用户登录 + 一个端口上线 + 部署文档

## 背景

用户 2026-11-22 说："后续我会打算布置到联网我随便用什么机器都能做几题这样"。

设计在 `docs/README.md` 第 7 节「部署」，先读：
- 先走"家里这台台式机 + Cloudflare Tunnel + Cloudflare Access"。
- 以后可能上 VPS，Claude 登录用 `claude setup-token`。

**硬要求**：AI 走的是用户的 Claude 订阅，只能用户自己用。所以 AI 接口，以及其他所有接口，都必须在登录之后（vault findings 2026-11-22）。

Cloudflare 那一侧（建 Tunnel、配 Access）要用户自己在账号里操作。你写好文档、配置模板和脚本，不要尝试联系 Cloudflare。

**并行**：先读 `codex/PLAN.md`。这次只有你一个平台任务。

## 要做的事

### 1. 登录

- **单用户，账号密码**：密码只存哈希，用标准库的 `hashlib.scrypt` 或 `pbkdf2`，不加依赖。
  - 设置方式：命令行脚本 `server/scripts/set_password.py`，交互式输入两遍，写到 `CODE_DOJO_DATA/auth.json`。
  - 也支持环境变量 `CODE_DOJO_PASSWORD_HASH`。
- **会话**：签名 cookie，HttpOnly、SameSite=Lax，HTTPS 下加 Secure。有效期 30 天，可配置。登出要能让 cookie 失效。
- **哪些接口要登录**：除了 `/api/health`（只返回 ok，不暴露题量等信息）和 `/api/auth/*`，所有 `/api/*` 都要。
- **登录限流**：同一 IP 连续失败 5 次，锁 10 分钟。
- **本机开发模式**：`CODE_DOJO_AUTH=off` 时不要求登录，默认 off，这样用户现在的 8000 实例不受影响。部署模式 `CODE_DOJO_AUTH=on` 时没设密码就拒绝启动。
- **前端**：
  - 登录页 `/login`，字少：一个密码框，回车登录。
  - 任何接口返回 401 时跳到登录页，登录后回到原页面。
  - 导航里有"退出"。
- **CSRF**：SameSite=Lax 加上所有写接口要求 `Content-Type: application/json`，基本够用。报告里写一句你的判断。

### 2. 一个端口上线

- 生产模式下 FastAPI 直接托管 `web/dist`（`npm run build` 的产物），前后端同一个端口，SPA 路由回退到 `index.html`。
- 加一个启动脚本 `deploy/run.sh`：构建前端（可选）→ 起 uvicorn（生产参数，不带 reload），读 `deploy/.env`。
- `deploy/.env.example` 列出所有 `CODE_DOJO_*` 变量和说明。

### 3. 部署文档和模板（`deploy/`）

- `deploy/README.md`，写给用户自己照着做，中文、一步一步：
  1. 本机先跑通生产模式：设密码，`run.sh`，浏览器登录。
  2. systemd 用户服务：模板 `deploy/code-dojo.service`，开机自启、崩了自动重启。
     - 写清楚 `claude` 要能在服务的环境里找到。PATH 和 HOME 怎么设，参考 `server/app/ai/provider.py` 的做法。
     - Docker 判题需要用户在 docker 组。
  3. Cloudflare Tunnel：装 cloudflared、登录、建 tunnel、`config.yml` 模板（`deploy/cloudflared-config.example.yml`）、作为服务运行。
  4. Cloudflare Access：给这个域名建一个应用，只允许用户自己的邮箱。这一层和应用自己的登录叠加，两道门。
  5. 以后上 VPS 要改什么：`claude setup-token`、判题镜像要在 VPS 上 build、数据目录备份。
- 不要在任何文件里写用户的邮箱、域名、token。用占位符，比如 `<你的域名>`。

### 4. 文档

`docs/README.md`：
- 第 7 节改成现在的做法，链接到 `deploy/README.md`。
- 第 8 节 M5 标"代码部分已完成，Cloudflare 待用户配置"。
- 「怎么跑」加生产模式。

## 验收标准

1. `server/.venv/bin/python -m pytest -q` 全过。新增测试覆盖：
   - 未登录 401
   - 登录成功、失败
   - 限流
   - 登出
   - AUTH=off 不拦
   - health 不泄露信息
   - 静态托管和 SPA 回退

   现有测试在 AUTH=off 下照旧通过。
2. `npm run build` 通过。
3. 实测生产模式：在 8001 用 `deploy/run.sh` 的方式（AUTH=on，测试密码，数据目录用 `{RUN_DIR}/data`）起服务，浏览器里完整走一遍：
   - 未登录被挡
   - 登录
   - 做一道题
   - 和助教说一句：AI 设为 off，看到"AI 关闭"的提示即可
   - 退出

   截图放 `{RUN_DIR}/`。
4. 用户的 8000 和 5173 实例没被动过，`server/data/` 没被改过。
