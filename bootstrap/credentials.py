"""按数据目录区分凭据，优先使用可用的系统钥匙串。"""

import hashlib
import json
from pathlib import Path

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
