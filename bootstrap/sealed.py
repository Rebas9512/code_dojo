"""安装包的令牌信封。只接受本版本固定的算法和资源开销。"""

import base64
import hashlib
import json
import secrets
from datetime import datetime, timezone

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


VERSION = 1
KDF = {"name": "scrypt", "n": 2**17, "r": 8, "p": 1}


def _encode(value: bytes) -> str:
    return base64.b64encode(value).decode("ascii")


def _key(password: str, salt: bytes) -> bytes:
    return hashlib.scrypt(password.encode(), salt=salt, n=KDF["n"], r=KDF["r"], p=KDF["p"],
                          dklen=32, maxmem=256 * 1024**2)


def _aad(version: int, repos: dict, created_at: str) -> bytes:
    return json.dumps([version, repos, created_at], sort_keys=True, separators=(",", ":")).encode()


def seal(values: dict, password: str, repo: str, sync_repo: str) -> dict:
    salt, nonce = secrets.token_bytes(16), secrets.token_bytes(12)
    repos = {"code": repo, "sync": sync_repo}
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    ciphertext = AESGCM(_key(password, salt)).encrypt(nonce, json.dumps(values).encode(), _aad(VERSION, repos, stamp))
    return dict(version=VERSION, kdf=KDF.copy(), repos=repos, created_at=stamp,
                salt=_encode(salt), nonce=_encode(nonce), ciphertext=_encode(ciphertext))


def unpack(envelope: dict) -> tuple[bytes, bytes, bytes]:
    if not isinstance(envelope, dict) or type(envelope.get("version")) is not int or envelope["version"] != VERSION:
        raise ValueError("不支持的令牌包版本")
    if (set(envelope) != {"version", "kdf", "repos", "created_at", "salt", "nonce", "ciphertext"}
            or envelope["kdf"] != KDF):
        raise ValueError("令牌包格式或派生参数无效")
    try:
        repos = envelope["repos"]
        if set(repos) != {"code", "sync"} or not all(isinstance(v, str) and v for v in repos.values()):
            raise ValueError
        datetime.fromisoformat(envelope["created_at"])
        salt, nonce, ciphertext = (base64.b64decode(envelope[k], validate=True) for k in ("salt", "nonce", "ciphertext"))
        if len(salt) != 16 or len(nonce) != 12 or len(ciphertext) < 16:
            raise ValueError
    except (TypeError, ValueError, AttributeError):
        raise ValueError("令牌包内容无效") from None
    return salt, nonce, ciphertext


def unseal(envelope: dict, password: str, repo: str, sync_repo: str) -> dict:
    salt, nonce, ciphertext = unpack(envelope)
    repos = envelope["repos"]
    if repos != {"code": repo, "sync": sync_repo}:
        raise ValueError("令牌包与当前仓库不匹配")
    aad = _aad(envelope["version"], repos, envelope["created_at"])
    # 密码错误与密文被修改都会导致 InvalidTag，界面对两者给出同样的提示。
    plain = AESGCM(_key(password, salt)).decrypt(nonce, ciphertext, aad)
    values = json.loads(plain)
    if not isinstance(values, dict) or set(values) != {"code", "sync"} or not all(
            isinstance(v, str) and v.strip() for v in values.values()):
        raise ValueError("令牌包缺少令牌")
    return values
