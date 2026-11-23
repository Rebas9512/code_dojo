"""离线检查安装、更新事务和 Contents API 的事件合并。"""

import base64
import hashlib
import io
import json
import os
import subprocess
import sys
from pathlib import Path
from threading import Thread
from unittest.mock import Mock
from urllib.error import HTTPError
from zipfile import ZipFile

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from bootstrap import VERSION, credentials
from bootstrap.update import Updates, version
from app.db import Store
from app.sync import ProgressSync


class Release:
    base = "https://api.github.com/repos/owner/code"
    token = "测试"

    def publish(self, number, minimum="1.0", lock=b"lock"):
        self.manifest = dict(version=number, commit="a" * 40, built_at="2026-11-22T00:00:00Z",
                             min_bootstrap=minimum, problem_format="1.7", lock_sha256=hashlib.sha256(lock).hexdigest())
        data = io.BytesIO()
        with ZipFile(data, "w") as z:
            for name in ("web/dist/index.html", "server/app/main.py", "judge/python/harness.py",
                         "problems/test", "sql-cache/hash.json", "requirements.txt"):
                z.writestr(name, number)
            z.writestr("manifest.json", json.dumps(self.manifest))
            z.writestr("server/uv.lock", lock)
        self.archive = data.getvalue()
        self.manifest["payload_sha256"] = hashlib.sha256(self.archive).hexdigest()

    def json(self, path):
        assert path == "/releases/tags/payload-latest"
        return {"assets": [{"name": "manifest.json", "id": 1}, {"name": "payload.zip", "id": 2}]}

    def open(self, path, accept):
        assert accept == "application/octet-stream"
        return io.BytesIO(json.dumps(self.manifest).encode() if path.endswith("/1") else self.archive)


@pytest.fixture
def updates(tmp_path):
    source = Release()
    source.publish("1")
    bundle = tmp_path / "bundle"
    (bundle / "libraries").mkdir(parents=True)
    (bundle / "lock.sha256").write_text(source.manifest["lock_sha256"])
    return Updates(tmp_path / "data", bundle, source)


def test_numeric_versions():
    assert version("1.10") > version("1.2.99")
    assert version("1") == version("1.0.0")
    with pytest.raises(ValueError):
        version("1.a")


def test_switch_after_ready_and_rollback(updates, monkeypatch):
    one = updates.check().active
    assert updates.current() is None
    updates.activate(one)
    updates.github.publish("2")
    two = updates.check().active
    assert updates.current() == one and (two.root / "web/dist/index.html").read_text() == "2"
    replace = os.replace
    def interrupted(src, dst):
        assert updates.current() == one
        raise OSError("模拟断电")
    monkeypatch.setattr(os, "replace", interrupted)
    with pytest.raises(OSError):
        updates.activate(two)
    assert updates.current() == one
    monkeypatch.setattr(os, "replace", replace)
    updates.activate(two)
    assert updates.current() == two and one.root.is_dir()
    assert updates.check().active == two


def test_staged_version_waits_for_next_launch(updates):
    one = updates.check().active
    updates.activate(one)
    updates.github.publish("2")
    two = updates.check().active
    updates.stage(two)
    assert updates.staged() == two and updates.current() == one
    downloads = []
    original = updates.github.open
    updates.github.open = lambda path, accept: (downloads.append(path), original(path, accept))[1]
    assert updates.check().active.root == two.root and not any(p.endswith("/2") for p in downloads)
    updates.activate(two)
    assert updates.staged() is None and updates.current() == two


def test_clean_removes_interrupted_downloads_only(updates):
    leftovers = [updates.root / "tmpab_cd123", updates.root / "dependencies/tmp0z9y8x7w"]
    kept = [updates.root / "tmp", updates.root / ("a" * 64)]  # 后端的临时目录和已装好的版本
    for path in leftovers + kept:
        path.mkdir(parents=True)
    updates.clean()
    assert not any(p.exists() for p in leftovers) and all(p.is_dir() for p in kept)


@pytest.mark.parametrize("failure", ["download", "corrupt", "launcher", "pip"])
def test_update_preserves_previous(updates, monkeypatch, failure):
    one = updates.check().active
    updates.activate(one)
    updates.github.publish("2", minimum=str(version(VERSION)[0] + 1) if failure == "launcher" else "1",
                           lock=b"new" if failure == "pip" else b"lock")
    if failure == "corrupt":
        updates.github.archive = updates.github.archive[:100]  # 下载不完整：不再算哈希，由 zip 本身读不出来拒绝
    if failure == "download":
        original = updates.github.open
        def fail(path, accept):
            if path.endswith("/2"):
                raise OSError("断网")
            return original(path, accept)
        monkeypatch.setattr(updates.github, "open", fail)
    if failure == "pip":
        monkeypatch.setattr(subprocess, "run", Mock(side_effect=subprocess.CalledProcessError(1, "pip")))
    result = updates.check()
    assert result.active == updates.current() == one and result.message
    if failure == "launcher":
        assert result.message == "请下载新版安装包"
        assert result.installer == "https://github.com/owner/code/releases/latest"


def test_lock_installs_once(updates, monkeypatch):
    calls = []
    def install(args, **_kwargs):
        assert "--require-hashes" in args and args[0] == sys.executable
        Path(args[args.index("--target") + 1]).mkdir()
        calls.append(args)
    monkeypatch.setattr(subprocess, "run", install)
    updates.github.publish("2", lock=b"new")
    updates.activate(updates.check().active)
    updates.github.publish("3", lock=b"new")
    assert updates.check().active.manifest["version"] == "3" and len(calls) == 1


def test_tokens_keyring_and_fallback(tmp_path, monkeypatch):
    ring = Mock()
    values = {"code": "假1", "sync": "假2"}
    monkeypatch.setattr(credentials, "keychain", lambda: ring)
    credentials.tokens(tmp_path, values)
    ring.get_password.return_value = json.dumps(values)
    assert credentials.tokens(tmp_path) == values and not list(tmp_path.iterdir())
    monkeypatch.setattr(credentials, "keychain", lambda: None)
    try:
        credentials.tokens(tmp_path, values)
    except PermissionError:
        assert os.name == "posix" and not list(tmp_path.iterdir())
    else:
        file = tmp_path / "github-tokens.json"
        assert credentials.tokens(tmp_path) == values
        assert os.name != "posix" or file.stat().st_mode & 0o777 == 0o600


class Contents:
    token = "假令牌"

    def __init__(self):
        self.files = {}
        self.conflict = False
        self.puts = []

    def open(self, path, accept):
        assert accept.endswith("raw+json")
        return io.BytesIO(self.files[path.removeprefix("/contents/").split("?")[0]])

    def json(self, path, data=None):
        def blob(raw):
            return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
        if path.startswith("/git/trees"):
            entries = [dict(path=p, type="blob", sha=blob(raw)) for p, raw in self.files.items()]
            return dict(sha=blob(repr(entries).encode()), tree=entries)
        name = path.removeprefix("/contents/")
        assert data["branch"] == "main"
        if self.conflict:
            self.conflict = False
            raise HTTPError("测试", 409, "", None, None)
        assert data.get("sha") == (blob(self.files[name]) if name in self.files else None)
        self.files[name] = base64.b64decode(data["content"])
        self.puts.append(name)


def test_contents_roundtrip_retry_and_shutdown(tmp_path, monkeypatch):
    remote = Contents()
    monkeypatch.setattr("app.sync.shutil.which", lambda _: None)
    a, b = [ProgressSync(Store(tmp_path / name / "dojo.db"), "https://github.com/owner/sync.git") for name in ("a", "b")]
    a.github = b.github = remote
    a.start()
    a.store.set_limit(14)
    remote.conflict = True
    a.close()
    assert not a.error and not a.status()["pending"]
    assert not b.sync()["error"] and b.store.daily_limit() == 14
    b.store.set_limit(6)
    with monkeypatch.context() as offline:
        offline.setattr(remote, "json", Mock(side_effect=OSError("离线")))
        assert b.sync()["pending"] and b.error
    assert not b.sync()["pending"] and not a.sync()["error"]
    assert a.store.daily_limit() == 6
    assert [p.split("/")[0] for p in remote.puts] == [a.store.journal.machine, b.store.journal.machine]


def test_desktop_sql_job_and_error():
    from app import desktop_sql
    import time
    result = []
    def execute():
        try:
            result.append(desktop_sql.execute({"datasets": [["SELECT 1"]]}))
        except ValueError as exc:
            result.append(str(exc))
    for reply in (desktop_sql.Reply(tables=[{"rows": [[1]]}]), desktop_sql.Reply(error="语法错误")):
        task = Thread(target=execute)
        task.start()
        deadline = time.monotonic() + 5
        while (job := desktop_sql.take()) is None and time.monotonic() < deadline:
            time.sleep(.01)
        assert job["job"]["datasets"] == [["SELECT 1"]] and desktop_sql.take() is None
        desktop_sql.finish(job["id"], reply)
        task.join(5)
        assert not task.is_alive()
    assert result == [[{"rows": [[1]]}], "语法错误"]


def test_git_present_scopes_credentials_to_sync_repo(tmp_path, monkeypatch):
    from app.sync import git
    from bootstrap.github import repository

    repo = "https://github.com/owner/sync.git"
    assert repository(repo) == repository("git@github.com:owner/sync.git") == "owner/sync"
    sync = ProgressSync(Store(tmp_path / "dojo.db"), repo)
    sync.github = Contents()
    monkeypatch.setattr("app.sync.shutil.which", lambda _: "/git")
    mock = Mock(return_value=subprocess.CompletedProcess([], 0))
    monkeypatch.setattr(subprocess, "run", mock)
    monkeypatch.setattr(sync, "_exchange", lambda: git(tmp_path, "fetch"))
    monkeypatch.delenv("GIT_CONFIG_COUNT", raising=False)
    assert not sync.sync()["error"]
    args, kwargs = mock.call_args
    assert kwargs["env"]["GIT_CONFIG_KEY_0"] == f"http.{repo}.extraHeader"
    header = kwargs["env"]["GIT_CONFIG_VALUE_0"]
    assert base64.b64decode(header.split()[-1]).decode() == "x-access-token:" + sync.github.token
    assert sync.github.token not in repr(args) and header not in repr(args)


def test_keychain_helper_keeps_value_out_of_arguments(monkeypatch):
    from bootstrap.keychain import SystemKeychain
    vault = SystemKeychain("测试钥匙串")
    value = json.dumps({"code": "test-token"})
    payload = base64.b64encode(value.encode())
    call = Mock(side_effect=[b"", payload])
    monkeypatch.setattr(vault, "_call", call)
    vault.set_password("code-dojo", "account", value)
    arguments, secret = call.call_args_list[0].args
    assert payload in secret and payload.decode() not in repr(arguments) and value not in repr(arguments)


def test_api_token_does_not_follow_redirect():
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    from bootstrap.github import GitHub

    headers = []
    class CDN(BaseHTTPRequestHandler):
        def do_GET(self):
            headers.append(self.headers.get("Authorization"))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"payload")

    with ThreadingHTTPServer(("127.0.0.1", 0), CDN) as cdn:
        class API(BaseHTTPRequestHandler):
            def do_GET(self):
                headers.append(self.headers.get("Authorization"))
                self.send_response(302)
                self.send_header("Location", f"http://127.0.0.1:{cdn.server_port}/download")
                self.end_headers()
        with ThreadingHTTPServer(("127.0.0.1", 0), API) as api:
            threads = [Thread(target=s.handle_request, daemon=True) for s in (cdn, api)]
            for thread in threads:
                thread.start()
            client = GitHub("owner/code", "fake", f"http://127.0.0.1:{api.server_port}")
            with client.open("/releases/assets/1", "application/octet-stream") as reply:
                assert reply.read() == b"payload"
            for thread in threads:
                thread.join(3)
    assert headers == ["Bearer fake", None]


def test_matching_lock_uses_bundled_libraries_without_copy(updates):
    active = updates.check().active
    assert updates.libraries(active.manifest) == updates.bundle / "libraries"
    assert not (updates.root / "dependencies").exists()
