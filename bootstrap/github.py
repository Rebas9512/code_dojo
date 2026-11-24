"""公开 Release 和私有进度仓库共用的 HTTPS 请求。"""

import json
import re
import ssl
from urllib.parse import urlsplit
from urllib.request import HTTPSHandler, Request, build_opener


def repository(name: str) -> str:
    for prefix in ("git@github.com:", "https://github.com/"):
        if name.startswith(prefix):
            name = name.removeprefix(prefix).removesuffix(".git")
            break
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", name, flags=re.ASCII) or {".", ".."} & set(name.split("/")):
        raise ValueError("GitHub 仓库请填写为 账户/仓库名")
    return name


class GitHub:
    def __init__(self, repo: str, token: str, api: str = "https://api.github.com"):
        url = urlsplit(api)
        if url.scheme != "https" and not (url.scheme == "http" and url.hostname in {"127.0.0.1", "::1"}):
            raise ValueError("GitHub API 需要使用 HTTPS")
        self.base = f"{api.rstrip('/')}/repos/{repository(repo)}"
        self.token = token
        context = ssl.create_default_context()
        # 独立解释器在部分系统上没有默认 CA 路径，pip 自带公共根证书。
        try:
            from pip._vendor import certifi
            context.load_verify_locations(certifi.where())
        except ImportError:
            pass
        self.opener = build_opener(HTTPSHandler(context=context))

    def open(self, path: str, accept: str, data: dict | None = None):
        body = json.dumps(data).encode() if data is not None else None
        req = Request(self.base + path, data=body, method="PUT" if body else "GET",
                      headers={"Accept": accept, "User-Agent": "code-dojo-desktop",
                               "Content-Type": "application/json"})
        # Release 下载会跳到带临时签名的 CDN；凭据只交给原始 API 请求。
        if self.token:
            req.add_unredirected_header("Authorization", f"Bearer {self.token}")
        return self.opener.open(req, timeout=20)

    def json(self, path: str, data: dict | None = None):
        with self.open(path, "application/vnd.github+json", data) as response:
            return json.load(response)


def verify_tokens(values: dict, repo: str, sync_repo: str) -> None:
    """只检查两个仓库的读取权限；不发送写请求，也不显示响应正文。"""
    from http.client import HTTPException
    from urllib.error import HTTPError

    for label, name, key, path in (("代码", repo, "code", "/releases?per_page=1"),
                                   ("同步", sync_repo, "sync", "/readme")):
        try:
            with GitHub(name, values[key]).open(path, "application/vnd.github+json"):
                pass
        except HTTPError as exc:
            if exc.code == 401:
                reason = "令牌无效或已过期"
            elif exc.code in (403, 404):
                reason = "请检查仓库选择和 Contents 读权限"
                if key == "sync":
                    reason += "，并确认仓库中有 README"
            else:
                reason = "GitHub 暂时无法处理请求"
            raise ValueError(f"{label}仓库校验失败（HTTP {exc.code}），{reason}") from None
        except (OSError, HTTPException, ValueError):
            raise ValueError(f"无法校验{label}仓库，请检查网络与令牌格式") from None
