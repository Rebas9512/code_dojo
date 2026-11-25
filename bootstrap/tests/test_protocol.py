"""在临时目录验证外壳读到的 JSONL，不访问 GitHub 或用户钥匙串。"""
import io
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from threading import Event
from urllib.error import HTTPError, URLError
from zipfile import ZipFile
from unittest.mock import Mock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from bootstrap import DEFAULT_REPO, DEFAULT_SYNC, VERSION, agents, protocol
from bootstrap.sealed import seal
from bootstrap.update import Installed, Result, Updates


@pytest.fixture
def controller(tmp_path, monkeypatch):
    monkeypatch.setenv("CODE_DOJO_GITHUB_API", "http://127.0.0.1:1")
    monkeypatch.setenv("CODE_DOJO_SYNC_REPO", DEFAULT_SYNC)
    monkeypatch.setenv("PATH", str(tmp_path))
    monkeypatch.delenv("CODE_DOJO_CLAUDE_BIN", raising=False)
    monkeypatch.delenv("CODE_DOJO_CODEX_BIN", raising=False)
    monkeypatch.setattr(agents, "_login_path", lambda: "")
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setattr(protocol, "tokens", Mock(return_value={}))
    monkeypatch.setattr(protocol, "clear_tokens", Mock())
    machine = protocol.Controller(tmp_path, tmp_path)
    active = Installed(tmp_path, {"version": "test.30"}, "now")
    updates = Mock()
    updates.current.return_value = None
    updates.check.return_value = Result(active)
    monkeypatch.setattr(protocol, "Updates", lambda *args: updates)
    def start(_, item):
        machine.agents = agents.service_agents(machine.data, os.environ.copy())
        machine.item, machine.port, machine.child = item, 43210, Mock()
        return True
    monkeypatch.setattr(machine, "start", start)
    return machine


def exchange(controller, commands, capsys):
    wire = "".join(json.dumps(cmd) + "\n" for cmd in commands)
    controller.loop(io.BytesIO(wire.encode()))
    out, err = capsys.readouterr()
    return [json.loads(line) for line in out.splitlines()], out + err


def test_local_connect_disconnect(controller, capsys, monkeypatch):
    values = {"code": "synthetic-private-code", "sync": "synthetic-private-sync"}
    password = "synthetic-long-password"
    (controller.bundle / "sealed-tokens.json").write_text(json.dumps(seal(values, password, DEFAULT_REPO, DEFAULT_SYNC)))
    commands = [{"command": "connect_sync", "code": key} for key in ("private-wrong", password)]
    start = Mock(wraps=controller.start)
    stop = Mock(wraps=controller.stop)
    monkeypatch.setattr(controller, "start", start)
    monkeypatch.setattr(controller, "stop", stop)
    events, output = exchange(controller, commands + [{"command": "disconnect_sync"}], capsys)
    assert [e["type"] for e in events] == [
        "status", "status", "status", "ready", "sync_code_failed", "status", "ready", "status", "ready"]
    assert events[4] == dict(type="sync_code_failed", remaining=4, wait=0)
    ready = [e for e in events if e["type"] == "ready"]
    assert [e["sync"] for e in ready] == [False, True, False]
    assert all(e.items() >= dict(port=43210, version=VERSION, payload_version="test.30").items() for e in ready)
    protocol.tokens.assert_any_call(controller.data, values)
    protocol.clear_tokens.assert_called_once_with(controller.data)
    assert start.call_count == 3 and all(call.args[1] is controller.item for call in start.call_args_list)
    stop.assert_any_call("disconnect")
    protocol.Updates().check.assert_called_once()
    assert all(value not in output for value in (*values.values(), password, "private-wrong"))


@pytest.mark.parametrize("saved,token", [({}, ""), ({"code": "old-code", "sync": "old-sync"}, "old-sync")])
def test_begin_passes_saved_token_to_service(controller, monkeypatch, capsys, saved, token):
    protocol.tokens.return_value = saved
    service = Mock(stdout=io.StringIO('{"ready":43210}\n'), stdin=io.StringIO())
    monkeypatch.setattr(subprocess, "Popen", Mock(return_value=service))
    monkeypatch.setattr(controller, "start", protocol.Controller.start.__get__(controller))
    controller.begin()
    config = json.loads(service.stdin.getvalue().splitlines()[0])
    assert config["token"] == token and config["data"] == str(controller.data)
    events = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    assert [e["type"] for e in events] == ["status", "status", "status", "ready"]
    assert events[-1]["sync"] is bool(token)


def test_missing_envelope_keeps_local_service(controller, capsys):
    controller.begin()
    child = controller.child
    controller.command({"command": "connect_sync", "code": "test-only"})
    events = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    assert events[-2]["type"] == "ready" and not events[-2]["sync"]
    assert events[-1] == dict(type="error", scope="settings", message="这个安装包不支持同步码")
    assert controller.child is child


def test_cooldown_blocks_correct_code(controller, capsys, monkeypatch):
    from bootstrap import window
    monkeypatch.setattr(window.time, "time", lambda: 100)
    values = {"code": "test-code", "sync": "test-sync"}
    password = "never-echo-this"
    (controller.bundle / "sealed-tokens.json").write_text(json.dumps(seal(values, password, DEFAULT_REPO, DEFAULT_SYNC)))
    commands = [{"command": "connect_sync", "code": code} for code in ["wrong"] * 5 + [password]]
    events, output = exchange(controller, commands, capsys)
    failures = [(e["remaining"], e["wait"]) for e in events if e["type"] == "sync_code_failed"]
    assert failures == [(4, 0), (3, 0), (2, 0), (1, 0), (0, 30), (0, 30)]
    assert [e["sync"] for e in events if e["type"] == "ready"] == [False]
    assert password not in output


def test_module_entry_quits_with_stdin_open(tmp_path):
    env = os.environ | {"CODE_DOJO_DATA": str(tmp_path), "CODE_DOJO_GITHUB_API": "http://127.0.0.1:1",
                        "CODE_DOJO_SYNC_REPO": DEFAULT_SYNC, "CODE_DOJO_AI_PROVIDER": "off", "PATH": ""}
    with subprocess.Popen([sys.executable, "-B", "-m", "bootstrap", "serve", "--protocol", "jsonl"],
                          cwd=Path(__file__).resolve().parents[2], env=env, stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8") as proc:
        try:
            proc.stdin.write('{"unexpected":"private-malformed-value"}\n{"command":"quit"}\n')
            proc.stdin.flush()
            assert proc.wait(timeout=10) == 0
            output = proc.stdout.read()
            assert [json.loads(line)["type"] for line in output.splitlines()] == ["status", "status", "error", "error"]
            assert "private-malformed-value" not in output and proc.stderr.read() == ""
        finally:
            if proc.poll() is None:
                proc.kill()


@pytest.mark.parametrize("preference,enabled", [("claude", True), ("codex", True), ("off", False)])
def test_codex_alone_in_extension(controller, capsys, monkeypatch, tmp_path, preference, enabled):
    monkeypatch.setenv("CODE_DOJO_CODEX_BIN", "codex")
    monkeypatch.setattr(agents.shutil, "which", lambda *args, **kwargs: None)
    monkeypatch.setattr(agents.sys, "platform", "darwin")
    monkeypatch.setattr(agents.platform, "machine", lambda: "arm64")
    monkeypatch.setenv("CODE_DOJO_AI_PROVIDER", preference)
    codex = tmp_path / ".vscode/extensions/openai.chatgpt-26.10.1/bin/macos-aarch64/codex"
    codex.parent.mkdir(parents=True)
    codex.touch(mode=0o755)
    assert agents.has_agent()
    service = Mock(stdout=io.StringIO('{"ready":43210}\n'), stdin=io.StringIO())
    monkeypatch.setattr(subprocess, "Popen", Mock(return_value=service))
    monkeypatch.setattr(controller, "start", protocol.Controller.start.__get__(controller))
    events, _ = exchange(controller, [], capsys)
    assert events[-1]["type"] == "ready" and events[-1]["ai"] is enabled
    assert events[-1]["agents"]["codex"]["path"] == str(codex)
    assert subprocess.Popen.call_args.kwargs["env"]["CODE_DOJO_CODEX_BIN"] == str(codex)


def test_agent_path_commands_restart_only_on_success(controller, capsys, monkeypatch):
    monkeypatch.setenv("CODE_DOJO_AI_PROVIDER", "claude")
    folder = controller.data / "desktop"
    folder.mkdir()
    restart = Mock(wraps=controller.restart_service)
    monkeypatch.setattr(controller, "restart_service", restart)
    command = {"command": "set_agent_path", "agent": "claude"}
    # 解释器本身支持 --version，且位置独立于测试 PATH。
    events, _ = exchange(controller, [command | {"path": str(folder / "missing")},
                                      command | {"path": sys.executable},
                                      {"command": "reset_agent_path", "agent": "claude"}], capsys)
    assert [(e["type"], e.get("agent")) for e in events if e["type"] in ("error", "ready")] == [
        ("ready", None), ("error", "claude"), ("ready", None), ("ready", None)]
    assert restart.call_count == 2
    ready = [e for e in events if e["type"] == "ready"]
    assert [e["ai"] for e in ready] == [False, True, False]
    assert [e["agents"]["claude"]["path"] for e in ready] == [None, sys.executable, None]
    assert agents.manual_paths(controller.data) == {}


@pytest.fixture
def installed(controller, tmp_path, monkeypatch):
    hub = Mock(base="https://api.github.com/repos/test/code")
    hub.json.return_value = {"assets": [{"name": "manifest.json", "id": 1}, {"name": "payload.zip", "id": 2}]}
    updates = Updates(tmp_path, tmp_path, hub)
    (tmp_path / "libraries").mkdir()
    (tmp_path / "lock.sha256").write_text("test")
    manifest = dict(version="1", commit="first", built_at="today", min_bootstrap="1", problem_format="1", lock_sha256="test")
    old = Installed(updates.root / ("a" * 64), manifest, "then")
    old.root.mkdir()
    (old.root / "manifest.json").write_text(json.dumps(manifest))
    updates.activate(old)
    monkeypatch.setattr(controller, "updates", lambda: updates)
    return updates


def offer(updates, *, newer=False, minimum="1"):
    old = updates.current()
    manifest = old.manifest | {"min_bootstrap": minimum}
    if newer:
        manifest.update(version="2", commit="second")
    remote = manifest | {"payload_sha256": "b" * 64 if newer else old.root.name}

    def open_asset(path, accept):
        if path == "/releases/assets/1":
            return io.BytesIO(json.dumps(remote).encode())
        assert path == "/releases/assets/2" and newer
        stream = io.BytesIO()
        with ZipFile(stream, "w") as archive:
            archive.writestr("manifest.json", json.dumps(manifest))
            for name in ("server/app/main.py", "judge/python/harness.py", "web/dist/index.html",
                         "requirements.txt", "problems/", "sql-cache/"):
                archive.writestr(name, "")
        stream.headers = {"Content-Length": str(stream.tell())}
        stream.seek(0)
        return stream
    updates.github.open.side_effect = open_asset


def test_launch_downloads_before_start(controller, installed, capsys, monkeypatch):
    offer(installed, newer=True)
    start = Mock(wraps=controller.start)
    monkeypatch.setattr(controller, "start", start)
    events, _ = exchange(controller, [], capsys)
    assert [e["message"] for e in events] == [
        "正在检查本机凭据…", "正在检查更新…", "正在下载题库…", "下载题库 100%", "准备运行环境…", "正在启动本机服务…", ""]
    assert events[-1]["type"] == "ready" and events[-1]["payload_version"] == "2"
    start.assert_called_once_with(installed, controller.item)
    assert (controller.item.root / "web/dist/index.html").is_file()


def test_menu_switches_version_in_same_session(controller, installed, capsys):
    offer(installed)
    controller.begin()
    offer(installed, newer=True)
    controller.command({"command": "check_update"})
    events = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    assert [event["payload_version"] for event in events if event["type"] == "ready"] == ["1", "2"]
    assert events[-2]["message"] == "正在启动本机服务…"


def test_download_can_outlast_manifest_deadline(controller, installed, capsys, monkeypatch):
    from bootstrap import update
    offer(installed, newer=True)
    fetch = installed.github.open.side_effect
    def slow_archive(path, accept):
        if path.endswith("/2"):
            time.sleep(.2)
        return fetch(path, accept)
    installed.github.open.side_effect = slow_archive
    monkeypatch.setattr(update, "MANIFEST_TIMEOUT", .1)
    events, _ = exchange(controller, [], capsys)
    assert events[-1]["payload_version"] == "2" and events[-1]["message"] == ""


def test_launch_current_ignores_obsolete_pointer(controller, installed, capsys):
    offer(installed)
    legacy = installed.root / "next.json"
    legacy.write_text(json.dumps({"digest": "b" * 64, "updated": "then"}))
    events, _ = exchange(controller, [], capsys)
    assert [e["message"] for e in events] == ["正在检查本机凭据…", "正在检查更新…", "正在启动本机服务…", ""]
    assert events[-1]["payload_version"] == "1"
    installed.github.open.assert_called_once_with("/releases/assets/1", "application/octet-stream")
    assert not legacy.exists()


@pytest.mark.parametrize("error", [URLError("离线"), TimeoutError(), OSError("连接中断"),
                                   HTTPError("", 503, "", None, None)])
def test_launch_network_failure_is_silent(controller, installed, capsys, error):
    installed.github.json.side_effect = error
    events, _ = exchange(controller, [], capsys)
    assert events[-1]["type"] == "ready" and events[-1]["payload_version"] == "1"
    assert events[-1]["message"] == events[-1]["installer"] == ""
    assert all(e["type"] != "error" for e in events)


def test_release_missing_manifest_uses_installed(controller, installed, capsys):
    installed.github.json.return_value = {"assets": []}
    events, _ = exchange(controller, [], capsys)
    assert events[-1]["payload_version"] == "1" and events[-1]["message"] == ""
    installed.github.open.assert_not_called()


def test_manifest_deadline_prevents_late_download(controller, installed, capsys, monkeypatch):
    from bootstrap import update
    entered, release, finished = Event(), Event(), Event()
    offer(installed, newer=True)
    fetch = installed.github.open.side_effect

    def slow_asset(path, accept):
        if path.endswith("/1"):
            entered.set()
            assert release.wait(5)
            finished.set()
        return fetch(path, accept)

    installed.github.open.side_effect = slow_asset
    monkeypatch.setattr(update, "MANIFEST_TIMEOUT", .1)
    try:
        events, _ = exchange(controller, [], capsys)
        assert entered.is_set() and not finished.is_set()
        assert events[-1]["payload_version"] == "1" and events[-1]["message"] == ""
    finally:
        release.set()
    assert finished.wait(2)
    installed.github.open.assert_called_once_with("/releases/assets/1", "application/octet-stream")


def test_launch_and_menu_keep_installer_prompt(controller, installed, capsys):
    offer(installed, newer=True, minimum="99")
    events, _ = exchange(controller, [{"command": "check_update"}], capsys)
    ready, _, checked = events[-3:]
    assert ready["payload_version"] == "1" and checked["checked"]
    assert ready["message"] == checked["message"] == "请下载新版安装包"
    assert ready["installer"] == checked["installer"] == "https://github.com/test/code/releases/latest"


def test_launch_restores_previous_if_new_service_fails(controller, installed, capsys, monkeypatch):
    offer(installed, newer=True)
    previous = installed.current()
    start = controller.start
    attempted = []
    def try_start(updates, item):
        attempted.append(item.manifest["version"])
        return item == previous and start(updates, item)
    monkeypatch.setattr(controller, "start", try_start)
    events, _ = exchange(controller, [], capsys)
    assert attempted == ["2", "1"]
    assert events[-1]["payload_version"] == "1" and "恢复" in events[-1]["message"]
