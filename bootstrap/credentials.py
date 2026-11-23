"""按数据目录区分凭据，优先使用可用的系统钥匙串。"""

import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

from .github import verify_tokens
from .keychain import available
from .update import atomic_json


def keychain():
    try:
        import keyring
        if keyring.get_keyring().priority > 0:
            return keyring
    except Exception:
        pass
    return available()


def tokens(directory: Path, values: dict | None = None) -> dict:
    file = directory / "github-tokens.json"
    account = hashlib.sha256(str(directory.resolve()).encode()).hexdigest()
    ring = keychain()
    if values is None and file.exists():
        return json.loads(file.read_bytes())
    if ring:
        try:
            if values is None:
                return json.loads(ring.get_password("code-dojo", account) or "{}")
            ring.set_password("code-dojo", account, json.dumps(values))
            file.unlink(missing_ok=True)
            return values
        except Exception:
            pass
    if values is not None:
        # NamedTemporaryFile 在 POSIX 创建时就是 0600；替换旧文件也保留该权限。
        atomic_json(file, values, private=True)
    return values or {}


def credential_source(saved: dict, bundle: Path, repo: str, sync_repo: str, api: str) -> tuple[str, dict]:
    if saved.get("code"):
        return "local", saved
    # 只把 github.com 的登录凭据交给对应的官方 API。其他服务使用自己的令牌。
    if api == "https://api.github.com" and (gh := shutil.which("gh")):
        try:
            result = subprocess.run([gh, "auth", "token", "--hostname", "github.com"], check=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                                    timeout=5, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
            if token := result.stdout.decode("ascii").strip():
                values = {"code": token, "sync": token}
                verify_tokens(values, repo, sync_repo)
                return "gh", values
        except (OSError, ValueError, subprocess.SubprocessError):
            pass
    return ("sealed" if (bundle / "sealed-tokens.json").is_file() else "manual"), {}
