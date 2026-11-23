# 把 code-dojo 部署在自己的机器上

每台机器可用本地模式从浏览器练习。下方第 1–5 节是可选的服务器部署，适合想从浏览器远程访问同一台常开电脑的情况。

## 在一台新电脑上用

1. **下载安装包。** 登录有仓库访问权的 GitHub 账号，打开最新的 `app-v*` Release。在 Assets 中选平台。Linux x86-64 解压 tar.gz，运行目录里的 `./code-dojo`。Apple Silicon Mac 解压 zip，将 `code-dojo.app` 移到“应用程序”。安装包未签名，首次请右键点“打开”，再确认“打开”。如果系统仍拦截，可在“系统设置 → 隐私与安全性”确认打开。Windows x64 先完整解压 zip，再双击 `code-dojo.exe`。保留解压后的整个目录。[下载安装包](https://github.com/Rebas9512/code_dojo/releases/latest)
2. **创建令牌。** 在 GitHub 头像菜单中依次打开 Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token。选择仓库所有者和有效期。在 Repository access 选择 Only select repositories，只选 `Rebas9512/code_dojo`，将 Repository permissions → Contents 设为 Read-only。生成并复制令牌。重复一次，只选 `Rebas9512/code_dojo_sync`，将 Contents 设为 Read and write。一个 fine-grained 令牌对其选中的仓库共用权限，分别创建可将代码仓库保持只读。[GitHub 令牌创建页](https://github.com/settings/personal-access-tokens/new) · [GitHub 权限说明](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
3. **第一次打开。** 在控制窗口的两个密码框分别粘贴令牌并点“保存”。首次完成下载后默认浏览器打开学习地图。令牌优先存系统钥匙串，备用位置是用户数据目录的 `github-tokens.json`。Linux 和 macOS 的备用文件权限为 600；磁盘不支持权限保护时，窗口提示令牌仅用于本次运行。以后在“设置 → 令牌与 AI 助教”可更新令牌。第一次通过一道题后，在第二台电脑使用同一进度仓库即可接续。关闭窗口前保持联网，断网时待推送记录留在本机。
4. **可选，启用 AI。** 按官方说明安装 Claude Code，在终端运行 `claude` 并按提示登录个人订阅。确认命令在 PATH 中可用，或将 `CODE_DOJO_CLAUDE_BIN` 设为其绝对路径，再重新打开桌面应用。窗口的“设置”提供安装入口。[Claude Code 安装说明](https://code.claude.com/docs/en/setup)

使用自己的仓库时，在打开应用前设置 `CODE_DOJO_REPO` 和 `CODE_DOJO_SYNC_REPO`，值可写成 `账户/仓库名`。进度仓库需私有，有 main 分支且可读写，初始提交只有 README 即可。`CODE_DOJO_DATA` 可指定本机数据目录。Linux 默认使用 `~/.local/share/code-dojo`，macOS 使用 `~/Library/Application Support/code-dojo`，Windows 使用 `%APPDATA%\code-dojo`。每台电脑各用自己的目录。应用退出后可以移动或替换安装目录，学习记录保存在数据目录。

## 本地模式和同步仓库怎么建

1. 安装 Git、uv 和 Node.js 22.13+（含 npm）。克隆私有代码仓库，进入项目目录，Linux 或 macOS 运行 `./dojo`，Windows PowerShell 运行 `.\dojo.ps1`。浏览器自动打开本机网页。三个系统的通用入口是 `uv run dojo.py`，环境诊断用 `uv run dojo.py doctor`。
2. 在 GitHub 新建**另一个私有仓库**，例如 `dojo-progress`。空仓库或只有 README 的仓库都可以。每台机器都需有读写权限。使用 SSH 时，在 GitHub 账户中添加这台机器的 SSH 公钥，提前用 `ssh -T git@github.com` 确认连接。使用 HTTPS 时，可运行 `gh auth login` 选择 HTTPS，然后运行 `gh auth setup-git`。
3. 将同一个仓库地址写入每台机器的环境变量。下面使用 SSH 地址。使用 HTTPS 凭据时替换为 `https://github.com/<账户>/dojo-progress.git`。

   ```sh
   # Linux / macOS，可将这一行放入自己的 shell 配置
   export CODE_DOJO_SYNC_REPO='git@github.com:<账户>/dojo-progress.git'
   ./dojo
   ```

   ```powershell
   # Windows，当前 PowerShell 窗口立即生效，并保存供以后使用
   $env:CODE_DOJO_SYNC_REPO = 'git@github.com:<账户>/dojo-progress.git'
   [Environment]::SetEnvironmentVariable('CODE_DOJO_SYNC_REPO', $env:CODE_DOJO_SYNC_REPO, 'User')
   .\dojo.ps1
   ```

4. 旧版用户可先运行 `uv run dojo.py import-legacy "<旧数据目录>"`，再正常启动。源目录包含 `code_dojo.db`，新目录由启动器选择，也可指定 `CODE_DOJO_DATA`。请在新机器使用新的数据目录，启动器会生成它自己的机器标识。
5. 第一次在 A 机交卷通过后，顶栏会显示同步时间。在 B 机启动或点击顶栏时间，即可看到提交、复习日程、每日上限、助教对话和完整附加题。顶栏显示有待推送事件或错误时，仍可继续练习，恢复连接后点击重试。未设置同步地址时，顶栏显示“未开启同步”。

本机运行时使用 SQLite。学习记录的 JSONL 在数据目录的 `events/<机器 UUID>/YYYY-MM.jsonl`，同步用的克隆在同级 `sync/`。每台机器只向仓库追加自己的日志，按事件 UUID 去重。提交和复习结果保留每次交卷，同一日程或设置取时间较晚的写入。掌握度从合并后的提交与日程计算。仓库里含代码和对话明文，应保持私有。

## 1. 先在本机登录并做题

以下命令从项目根目录执行。准备好 Docker、uv、Node.js 22.13 或更高版本和 npm。已有依赖和镜像可以复用。在新机器上执行一次：

```bash
(cd server && uv sync --frozen)
(cd web && npm ci)
(cd scripts/curriculum && npm ci)
docker build -t code-dojo-judge-py:3.14 judge/python
```

1. 首次运行时执行 `install -m 600 deploy/.env.example deploy/.env`，打开新文件查看 `CODE_DOJO_DATA`。模板默认把个人数据存在 `~/.local/share/code-dojo`（设置过 `XDG_DATA_HOME` 时使用它），首次打开是空进度。目录应位于仅本人能读写的 Linux 文件系统。要带上现有记录，按第 5 节备份并恢复 `code_dojo.db`。部署和开发实例使用各自的数据目录。
2. 执行 `deploy/run.sh --set-password`，输入两遍密码。脚本读取同一份 `.env` 并调用 `server/scripts/set_password.py`，只把加盐哈希写入数据目录的 `auth.json`。也可以直接运行 `CODE_DOJO_DATA='/你的数据目录' server/.venv/bin/python server/scripts/set_password.py`。若使用环境变量，取 `auth.json` 中的 `password_hash` 整个值填入 `CODE_DOJO_PASSWORD_HASH`，用单引号保留其中的美元符号。环境变量优先。
3. 运行 `deploy/run.sh --build`。看到 Uvicorn 就绪后，打开 `http://127.0.0.1:8001/today`，输入密码按回车，应回到今日计划。进入一道题提交，点导航里的“退出”，再访问今日计划应回到登录页。模板先关闭 AI，助教栏会显示“AI 助教没有开启”。
4. 前台实例用 Ctrl+C 结束。已有前端构建时用 `deploy/run.sh` 直接启动。改前端后再用 `--build` 重建。要轮换密码，重新执行设密步骤并重启该部署实例，各设备需重新登录。

脚本以单进程监听 `127.0.0.1:8001`，不需要 Vite。端口可用 `CODE_DOJO_PORT` 调整。脚本加载 `deploy/.env`，其中赋值覆盖同名环境变量。如果项目所在的磁盘无法限制文件权限，把模板复制到个人 Linux 主目录的私有文件中，通过 `export CODE_DOJO_ENV_FILE="$HOME/.config/code-dojo/production.env"` 指定它，用户服务中也添加对应的 `Environment="CODE_DOJO_ENV_FILE=%h/.config/code-dojo/production.env"`。部署需要 `CODE_DOJO_AUTH=on` 和有效的密码哈希。会话默认 30 天，`CODE_DOJO_SESSION_DAYS` 可填正整数。同一 IP 连续输错 5 次，锁定 10 分钟。

## 2. 交给 systemd 用户服务

1. 用将来运行服务的 Linux 用户执行 `docker info`。常规 Docker 安装需要这个用户加入 docker 组，可执行 `sudo usermod -aG docker "$USER"`。重新登录，使新登录会话和用户服务管理器都取得新组（已启用 linger 的机器可在方便时重启）。docker 组拥有管理本机容器的权限。
2. 用该用户运行 `command -v node docker claude`，记下可执行文件的位置。模板通过 `HOME=%h` 指向该用户的主目录，通过 `PATH` 查找这些命令。用户服务不读取交互式 shell 配置。如果 Node 在版本管理器目录，或 Claude 装在其他目录，把真实的 bin 目录加入服务的 `Environment="PATH=…"`。也可以在 `.env` 用 `CODE_DOJO_CLAUDE_BIN` 指定 Claude 的绝对路径。Claude 子进程在专用目录运行，从服务继承 HOME、PATH、LANG 和可选的订阅令牌。
3. 安装服务文件。打开副本，把两处 `/绝对路径/code-dojo` 换成项目的绝对路径（`pwd` 可查看），检查 PATH。路径含空格时，把 ExecStart 的整个可执行文件路径放在双引号内。

```bash
mkdir -p ~/.config/systemd/user
cp deploy/code-dojo.service ~/.config/systemd/user/
${EDITOR:-nano} ~/.config/systemd/user/code-dojo.service
systemctl --user daemon-reload
systemctl --user enable --now code-dojo.service
sudo loginctl enable-linger "$USER"
systemctl --user status code-dojo.service
journalctl --user -u code-dojo.service -n 40
```

`enable-linger` 让用户服务在开机时启动，退出桌面后仍继续运行。服务故障退出会在 5 秒后重启。访问本机地址验证；`curl -fsS http://127.0.0.1:8001/api/health` 应仅返回 `{"ok":true}`。更改 `.env` 后执行 `systemctl --user restart code-dojo.service`，更改服务文件后先执行 `daemon-reload`。更新前端可在项目里执行 `(cd web && npm run build)` 后重启服务。

## 3. 准备 Cloudflare Tunnel

以下步骤由域名和 Cloudflare 账号的所有者操作。先把域名接入自己的 Cloudflare 账号，选一个专供 code-dojo 的主机名。先准备隧道和配置，第 4 节设好邮箱规则后再接入公网。

1. Debian / Ubuntu 可以从官方发布页选择与系统架构一致的 `.deb`。下面的命令下载并安装对应包。[cloudflared 官方发布](https://github.com/cloudflare/cloudflared/releases)

```bash
curl -fL -o cloudflared.deb "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-$(dpkg --print-architecture).deb"
sudo dpkg -i cloudflared.deb
cloudflared --version
cloudflared tunnel login
cloudflared tunnel create code-dojo
```

2. 在浏览器授权自己的域名。创建命令会显示 UUID，并在 `~/.cloudflared/` 写入对应的隧道凭据。复制下面的模板，将 `<隧道UUID>` 和 `<你的域名>` 替换成实际值。主机名填完整子域名，不含协议。若已修改应用端口，同步调整 `service` 地址。末尾规则使其余主机名返回 404。

```bash
sudo install -d -m 700 /etc/cloudflared
sudo install -m 600 "$HOME/.cloudflared/<隧道UUID>.json" "/etc/cloudflared/<隧道UUID>.json"
sudo install -m 600 deploy/cloudflared-config.example.yml /etc/cloudflared/config.yml
sudoedit /etc/cloudflared/config.yml
sudo cloudflared tunnel --config /etc/cloudflared/config.yml ingress validate
```

应用只接受本机回环地址的代理转发头，按 Uvicorn 解析出的客户端 IP 限流，按访问协议设置 Secure cookie。Tunnel 指向本机 HTTP，公网浏览器使用 HTTPS。路由器无需转发应用端口。[本机管理的 Tunnel](https://github.com/cloudflare/cloudflare-docs/blob/production/src/content/docs/tunnel/features/locally-managed-tunnels/create-local-tunnel.mdx)

## 4. 只允许自己的邮箱，再启动隧道

1. 进入 Cloudflare Zero Trust，启用一个本人能使用的身份验证方式，例如邮箱一次性验证码（One-time PIN）。
2. 在 **Access → Applications** 新建 **Self-hosted** 应用，填入与 ingress 完全相同的主机名，路径留空以覆盖整站（含 `/api`）。
3. 添加 **Allow** 策略。**Include → Emails** 只填 `<你的邮箱>`，选择上一步的登录方式，保存应用。检查这个主机名及其路径的所有匹配规则，移除面向所有人、整个邮箱域或 Bypass 的放行规则。
4. 用刚才创建隧道的普通用户添加 DNS 路由，再安装并启动系统级 cloudflared 服务。下面的安装步骤用于这台机器的第一个 cloudflared 服务；若已有服务，先由管理员将新主机规则合入相应隧道的配置。

```bash
cloudflared tunnel route dns code-dojo '<你的域名>'
sudo cloudflared --config /etc/cloudflared/config.yml service install
sudo systemctl enable --now cloudflared
sudo systemctl status cloudflared
```

5. 在另一台机器用隐私窗口打开 `https://<你的域名>/today`。应先看到 Access 身份验证；验证自己的邮箱后才看到应用密码框。登录后应返回今日计划。浏览器开发者工具中 `dojo_session` 应带 Secure、HttpOnly、SameSite=Lax。点“退出”会撤销这台浏览器的应用会话。要在共用机器上同时退出 Access，可再打开同一域名的 `/cdn-cgi/access/logout` 并关闭隐私窗口。
6. 两道登录都确认后，如需启用助教，把 `deploy/.env` 中的 `CODE_DOJO_AI_PROVIDER` 改为 `claude`，确认服务用户已登录个人 Claude 订阅，然后重启 code-dojo 用户服务。

## 5. 搬到 VPS 与备份

1. 在 VPS 建立专用普通用户。按第 1、2 节安装现有依赖、在 VPS 本机重新构建判题镜像和前端，并给该服务用户配置 Docker 权限。使用数据科学题时也要构建项目的 `judge/ds` 镜像，名称与 `CODE_DOJO_DS_IMAGE` 一致。
2. 在已登录自己 Claude 订阅的终端交互运行 `claude setup-token`。把生成的值通过私密渠道配置为 VPS 用户服务的 `CLAUDE_CODE_OAUTH_TOKEN`，例如在权限为 600 的私有环境文件中通过 systemd 的 `EnvironmentFile=` 加载。服务仍需安装 Claude Code 并设置 PATH / HOME。项目的 provider 显式向 Claude 子进程传递这一变量。令牌到期或撤销后重新生成并重启用户服务。[Claude Code 环境变量](https://code.claude.com/docs/en/env-vars)
3. 备份前选定一个仅本人可访问的目录。SQLite 的在线备份可在原站继续使用时生成一致的快照。以下示例需要系统的 `sqlite3` 命令；源路径使用实际的 `CODE_DOJO_DATA`。若从文件设密，再备份 `auth.json`。使用环境哈希时，在私有配置中单独备份该值。

```bash
umask 077
mkdir -p "$HOME/code-dojo-backup"
sqlite3 '/你的数据目录/code_dojo.db' ".backup '$HOME/code-dojo-backup/code_dojo.db'"
cp '/你的数据目录/auth.json' "$HOME/code-dojo-backup/"
```

4. 在 VPS 停止新站的 code-dojo 服务，将记录快照和密码哈希恢复到新数据目录，权限限服务用户读写。让应用新建 `sessions.db`，所有设备在新站重新登录。确认题目记录、最近提交和今日计划后再切换域名的隧道路由。继续使用同一条本人邮箱的 Access 策略。切换前先暂停旧站写入，做最后一次备份并恢复，带上试迁移期间新增的练习。
