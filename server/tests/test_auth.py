"""以真实路由检查登录边界，独立数据库隔离浏览器、IP 与会话时钟。"""

import json
import os
import secrets
from dataclasses import replace
from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.datastructures import State

from app import auth, main
from app.ai.provider import ClaudeCodeProvider
from app.frontend import Frontend

PASSWORD = "测试用的口令"


@pytest.fixture(scope="module")
def encoded():
    return auth.hash_password(PASSWORD)


@pytest.fixture
def browser(tmp_path, monkeypatch, encoded):
    monkeypatch.setenv("CODE_DOJO_PASSWORD_HASH", encoded)
    sessions = auth.Sessions(tmp_path, 2)
    monkeypatch.setattr(main.app, "state", State({"sessions": sessions}))
    return TestClient(main.app, base_url="https://testserver")


def login(client, password=PASSWORD):
    return client.post("/api/auth/login", json={"password": password})


def test_public_health_and_private_routes(browser):
    assert browser.get("/api/health").json() == {"ok": True}
    assert browser.get("/api/auth/session").json() == {"enabled": True, "authenticated": False}
    for path in ("/api/status", "/api/tracks", "/api/today", "/api/new-endpoint", "/api/health/private"):
        assert browser.get(path).status_code == 401
    for path in ("/api/problems/a/chat", "/api/playground/run", "/api/problems/a/submit"):
        assert browser.post(path, json={}).status_code == 401
    mounted = TestClient(main.app, root_path="/dojo")
    assert mounted.get("/dojo/api/tracks").status_code == 401
    assert mounted.get("/dojo/api/health").json() == {"ok": True}


def test_login_logout_and_replay(browser):
    assert login(browser, "错").status_code == 401
    response = login(browser)
    assert response.json() == {"ok": True}
    header = response.headers["set-cookie"].lower()
    assert all(field in header for field in ("httponly", "samesite=lax", "secure", "max-age=172800"))
    token = browser.cookies[auth.COOKIE]
    assert browser.get("/api/tracks").status_code == 200
    assert browser.get("/api/auth/session").json()["authenticated"]
    other = TestClient(main.app)
    other_login = login(other)
    assert other_login.status_code == 200
    assert "secure" not in other_login.headers["set-cookie"].lower()
    assert browser.post("/api/auth/logout", json={}).status_code == 200
    assert browser.get("/api/today").status_code == 401
    browser.cookies.set(auth.COOKIE, token)
    assert browser.get("/api/today").status_code == 401
    assert other.get("/api/today").status_code == 200


def test_signature_expiry_and_restart(browser, tmp_path, monkeypatch):
    clock = Mock()
    clock.time.return_value = 1000
    monkeypatch.setattr(auth, "time", clock)
    assert login(browser).is_success
    token = browser.cookies[auth.COOKIE]
    restarted = auth.Sessions(tmp_path, 2)
    assert restarted.check(token)
    assert not restarted.check(token[:-1] + ("0" if token[-1] != "0" else "1"))
    clock.time.return_value += restarted.ttl
    assert not restarted.check(token)
    clock.time.return_value = 1000
    monkeypatch.setenv("CODE_DOJO_PASSWORD_HASH", auth.hash_password("新密码"))
    assert not auth.Sessions(tmp_path, 2).check(token)


def test_lockout_by_ip_and_recovery(browser, monkeypatch, tmp_path):
    clock = Mock()
    clock.time.return_value = 1000
    monkeypatch.setattr(auth, "time", clock)
    for _ in range(4):
        assert login(browser, "错").status_code == 401
    assert login(browser).is_success  # 登录成功清零
    for _ in range(4):
        assert login(browser, "错").status_code == 401
    assert login(browser, "错").status_code == 429
    main.app.state.sessions = auth.Sessions(tmp_path, 2)
    clock.time.return_value += 599
    locked = login(browser)
    assert locked.status_code == 429 and locked.headers["retry-after"] == "1"
    other_ip = TestClient(main.app, client=("192.0.2.2", 1234))
    assert login(other_ip).is_success
    clock.time.return_value += 1
    assert login(browser).is_success


def test_json_required_including_empty_writes(browser):
    assert browser.post("/api/auth/login", data={"password": PASSWORD}).status_code == 415
    assert login(browser).is_success
    assert browser.put("/api/today/settings", content='{"daily_limit":2}', headers={"Content-Type": "text/plain"}).status_code == 415
    assert browser.delete("/api/problems/a/chat").status_code == 415
    assert browser.post("/api/auth/logout").status_code == 415
    assert browser.get("/api/today").is_success
    assert browser.post("/api/auth/logout", headers={"Content-Type": "application/json; charset=utf-8"}).is_success


def test_auth_off():
    client = TestClient(main.app)
    assert client.get("/api/auth/session").json() == {"enabled": False, "authenticated": True}
    assert client.get("/api/today").is_success


def test_password_sources_and_startup(tmp_path, encoded, monkeypatch):
    monkeypatch.delenv("CODE_DOJO_PASSWORD_HASH", raising=False)
    settings = replace(main.settings, data_dir=tmp_path, auth_enabled=True)
    with pytest.raises(RuntimeError, match="set_password"):
        auth.install_auth(FastAPI(), settings)
    (tmp_path / "auth.json").write_text(json.dumps({"password_hash": encoded}), encoding="utf-8")
    app = FastAPI()
    auth.install_auth(app, settings)
    assert login(TestClient(app)).is_success
    monkeypatch.setenv("CODE_DOJO_PASSWORD_HASH", "格式错误")
    with pytest.raises(ValueError, match="哈希"):
        auth.install_auth(FastAPI(), settings)


def test_static_files_and_spa(tmp_path):
    (tmp_path / "index.html").write_text("学习地图", encoding="utf-8")
    (tmp_path / "assets").mkdir()
    (tmp_path / "assets/app.js").write_text("window.dojo = true", encoding="utf-8")
    app = FastAPI()
    app.mount("/", Frontend(tmp_path))
    client = TestClient(app)
    for path in ("/", "/login", "/p/deep-link", "/t/python/skills"):
        assert client.get(path).text == "学习地图"
        assert client.head(path).status_code == 200
    assert client.get("/assets/app.js").text == "window.dojo = true"
    for path in ("/assets/absent", "/absent.js", "/api/unknown", "/api"):
        assert client.get(path).status_code == 404
    assert client.post("/login").status_code == 405


def test_subscription_token_reaches_only_claude(tmp_path, monkeypatch):
    token = secrets.token_urlsafe()
    monkeypatch.setenv("CLAUDE_CODE_OAUTH_TOKEN", token)
    monkeypatch.setenv("CODE_DOJO_PASSWORD_HASH", "只给应用")
    run = Mock(return_value=Mock(stdout='{"structured_output":{}}'))
    monkeypatch.setattr("app.ai.provider.subprocess.run", run)
    binary = str(tmp_path / ("claude.cmd" if os.name == "nt" else "claude"))
    monkeypatch.setattr("app.ai.provider.shutil.which", lambda _: binary)
    ClaudeCodeProvider(workdir=tmp_path).complete(system="系统", prompt="测试", schema={})
    env = run.call_args.kwargs["env"]
    assert run.call_args.args[0][0] == binary
    if os.name == "nt":
        for key in ("USERPROFILE", "APPDATA", "LOCALAPPDATA", "SystemRoot", "TEMP"):
            assert env.get(key) == os.environ.get(key)
    assert env["CLAUDE_CODE_OAUTH_TOKEN"] == token
    assert "CODE_DOJO_PASSWORD_HASH" not in env
