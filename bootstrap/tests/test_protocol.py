"""在临时目录验证外壳读到的 JSONL，不访问 GitHub 或用户钥匙串。"""
import io
import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from bootstrap import DEFAULT_REPO, DEFAULT_SYNC, VERSION, protocol
from bootstrap.sealed import seal
from bootstrap.update import Installed, Result


@pytest.fixture
def controller(tmp_path, monkeypatch):
    monkeypatch.setenv("CODE_DOJO_GITHUB_API", "http://127.0.0.1:1")
    monkeypatch.setenv("CODE_DOJO_SYNC_REPO", DEFAULT_SYNC)
    monkeypatch.setattr(protocol, "tokens", Mock(return_value={}))
    monkeypatch.setattr(protocol, "clear_tokens", Mock())
    machine = protocol.Controller(tmp_path, tmp_path)
    active = Installed(tmp_path, {"version": "test.30"}, "now")
    updates = Mock()
    updates.current.return_value = None
    updates.check.return_value = Result(active)
    monkeypatch.setattr(protocol, "Updates", lambda *args: updates)
    def start(_, item):
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
    from bootstrap import agents

    monkeypatch.setattr(agents.shutil, "which", lambda _: None)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setattr(agents.sys, "platform", "darwin")
    monkeypatch.setattr(agents.platform, "machine", lambda: "arm64")
    monkeypatch.setenv("CODE_DOJO_AI_PROVIDER", preference)
    codex = tmp_path / ".vscode/extensions/openai.chatgpt-26.10.1/bin/macos-aarch64/codex"
    codex.parent.mkdir(parents=True)
    codex.touch(mode=0o755)
    assert agents.has_agent()
    events, _ = exchange(controller, [], capsys)
    assert events[-1]["type"] == "ready" and events[-1]["ai"] is enabled


def test_launch_starts_installed_then_stages_update(controller, capsys, tmp_path):
    installed = Installed(tmp_path / "a", {"version": "test.1"}, "then")
    newer = Installed(tmp_path / "b", {"version": "test.2"}, "now")
    newer.root.mkdir()
    updates = protocol.Updates()
    updates.current.return_value = installed
    updates.staged.return_value = None
    updates.check.return_value = Result(newer)
    controller.launch()
    events = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    assert [e["type"] for e in events] == ["status", "ready"] and events[-1]["payload_version"] == "test.1"
    source, message = controller.inbox.get(timeout=5)
    assert source == "update"
    controller.checked(*message)
    updates.stage.assert_called_once_with(newer)
    assert capsys.readouterr().out == ""


def test_launch_tries_staged_then_falls_back(controller, capsys, monkeypatch, tmp_path):
    installed = Installed(tmp_path / "a", {"version": "test.1"}, "then")
    staged = Installed(tmp_path / "b", {"version": "test.2"}, "now")
    updates = protocol.Updates()
    updates.current.return_value = installed
    updates.staged.return_value = staged
    updates.check.return_value = Result(installed, "更新失败：无法连接 GitHub，请检查网络")
    started = []
    def start(_, item):
        started.append(item)
        if item is staged:
            return False
        controller.item, controller.port = item, 43210
        return True
    monkeypatch.setattr(controller, "start", start)
    controller.launch()
    events = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    assert started == [staged, installed]
    assert events[-1]["type"] == "ready" and events[-1]["payload_version"] == "test.1" and "恢复" in events[-1]["message"]
    controller.checked(*controller.inbox.get(timeout=5)[1])
    updates.stage.assert_not_called()
    event = json.loads(capsys.readouterr().out)
    assert event["type"] == "status" and event["checked"] and "GitHub" in event["message"]
