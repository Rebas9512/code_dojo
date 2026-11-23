"""单用户密码、可撤销的签名会话，以及 API 统一入口检查。"""

import hashlib
import hmac
import json
import os
import re
import secrets
import sqlite3
import time
from collections.abc import Awaitable, Callable
from contextlib import closing
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from pydantic import BaseModel, SecretStr
from starlette.routing import get_route_path

from .config import Settings

COOKIE = "dojo_session"
ROUNDS = 600_000
PASSWORD_FORMAT = re.compile(rf"pbkdf2_sha256\${ROUNDS}\$([0-9a-f]{{32}})\$([0-9a-f]{{64}})")
SESSION_FORMAT = re.compile(r"([0-9a-f]{32})\.([0-9a-f]{64})")


def digest(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ROUNDS)


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    return f"pbkdf2_sha256${ROUNDS}${salt.hex()}${digest(password, salt).hex()}"


class Sessions:
    def __init__(self, data_dir: Path, days: int):
        encoded = os.environ.get("CODE_DOJO_PASSWORD_HASH")
        if encoded is None:
            try:
                encoded = json.loads((data_dir / "auth.json").read_text(encoding="utf-8"))["password_hash"]
            except (OSError, ValueError, KeyError, TypeError) as exc:
                raise RuntimeError("请先运行 server/scripts/set_password.py 或设置 CODE_DOJO_PASSWORD_HASH") from exc
        match = PASSWORD_FORMAT.fullmatch(encoded) if isinstance(encoded, str) else None
        if not match:
            raise ValueError("密码哈希格式无效，请重新设置密码")
        self.salt, self.password_digest = (bytes.fromhex(part) for part in match.groups())
        self.ttl = days * 86400
        data_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.db = data_dir / "sessions.db"
        with closing(sqlite3.connect(self.db)) as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, key BLOB NOT NULL, expires INTEGER NOT NULL);
                CREATE TABLE IF NOT EXISTS failures (ip TEXT PRIMARY KEY, count INTEGER NOT NULL, until INTEGER NOT NULL);
            """)

    def signature(self, sid: str, key: bytes) -> str:
        # 每台设备有独立的随机密钥。改密后重新启动，旧密码签发的会话也会失效。
        return hmac.digest(key, sid.encode() + self.password_digest, "sha256").hex()

    def login(self, ip: str, password: str) -> str:
        with closing(sqlite3.connect(self.db, timeout=15)) as db, db:
            # 并发尝试按顺序记数，第五次失败与加锁在同一个事务中完成。
            db.execute("BEGIN IMMEDIATE")
            now = int(time.time())
            count, until = db.execute("SELECT count, until FROM failures WHERE ip=?", (ip,)).fetchone() or (0, 0)
            if until > now:
                raise HTTPException(429, "尝试次数过多，请稍后再试", headers={"Retry-After": str(until - now)})
            if hmac.compare_digest(digest(password, self.salt), self.password_digest):
                sid, key = secrets.token_hex(16), secrets.token_bytes(32)
                db.execute("DELETE FROM failures WHERE ip=?", (ip,))
                db.execute("DELETE FROM sessions WHERE expires<=?", (now,))
                db.execute("INSERT INTO sessions VALUES (?, ?, ?)", (sid, key, now + self.ttl))
                return f"{sid}.{self.signature(sid, key)}"
            count = 1 if until else count + 1
            until = now + 600 if count >= 5 else 0
            db.execute("INSERT OR REPLACE INTO failures VALUES (?, ?, ?)", (ip, count, until))
        if until:
            raise HTTPException(429, "尝试次数过多，请在 10 分钟后再试", headers={"Retry-After": "600"})
        raise HTTPException(401, "密码不正确")

    def check(self, cookie: str, *, revoke: bool = False) -> bool:
        match = SESSION_FORMAT.fullmatch(cookie)
        if not match:
            return False
        sid, mac = match.groups()
        with closing(sqlite3.connect(self.db)) as db, db:
            row = db.execute("SELECT key FROM sessions WHERE id=? AND expires>?", (sid, int(time.time()))).fetchone()
            if not row or not hmac.compare_digest(mac, self.signature(sid, row[0])):
                return False
            if revoke:
                db.execute("DELETE FROM sessions WHERE id=?", (sid,))
            return True


class Login(BaseModel):
    password: SecretStr


def install_auth(app: FastAPI, settings: Settings) -> None:
    app.state.sessions = Sessions(settings.data_dir, settings.session_days) if settings.auth_enabled else None

    @app.middleware("http")
    async def protect(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        path = get_route_path(request.scope)
        if not (path == "/api" or path.startswith("/api/")):
            return await call_next(request)
        sessions: Sessions | None = request.app.state.sessions
        public = path == "/api/health" or path.startswith("/api/auth/")
        if sessions and not public and not await run_in_threadpool(sessions.check, request.cookies.get(COOKIE, "")):
            response = JSONResponse({"detail": "请先登录"}, status_code=401)
        elif request.method not in ("GET", "HEAD", "OPTIONS") and (
            len(request.headers.getlist("content-type")) != 1
            or request.headers["content-type"].partition(";")[0].strip().lower() != "application/json"
        ):
            response = JSONResponse({"detail": "写入请求需要 application/json"}, status_code=415)
        else:
            response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.get("/api/auth/session")
    def session(request: Request) -> dict[str, bool]:
        sessions: Sessions | None = request.app.state.sessions
        authenticated = sessions is None or sessions.check(request.cookies.get(COOKIE, ""))
        return {"enabled": sessions is not None, "authenticated": authenticated}

    @app.post("/api/auth/login")
    def login(body: Login, request: Request, response: Response) -> dict[str, bool]:
        sessions: Sessions | None = request.app.state.sessions
        if sessions:
            token = sessions.login(request.client.host if request.client else "unknown", body.password.get_secret_value())
            response.set_cookie(COOKIE, token, max_age=sessions.ttl, httponly=True, samesite="lax",
                                secure=request.url.scheme == "https")
        return {"ok": True}

    @app.post("/api/auth/logout")
    def logout(request: Request, response: Response) -> dict[str, bool]:
        sessions: Sessions | None = request.app.state.sessions
        if sessions:
            sessions.check(request.cookies.get(COOKIE, ""), revoke=True)
        response.delete_cookie(COOKIE, httponly=True, samesite="lax", secure=request.url.scheme == "https")
        return {"ok": True}
