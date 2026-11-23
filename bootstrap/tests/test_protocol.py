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
    monkeypatch.setattr(protocol, "tokens", lambda *args: {})
    machine = protocol.Controller(tmp_path, tmp_path)
    active = Installed(tmp_path, {"version": "test.30"}, "now")
    updates = Mock()
    updates.current.return_value = None
    updates.check.return_value = Result(active)
    monkeypatch.setattr(protocol, "Updates", lambda *args: updates)
    def start(_, item):
        machine.item, machine.port = item, 43210
        return True
    monkeypatch.setattr(machine, "start", start)
    return machine


def exchange(controller, commands, capsys):
    wire = "".join(json.dumps(cmd) + "\n" for cmd in commands)
    controller.loop(io.BytesIO(wire.encode()))
    out, err = capsys.readouterr()
    return [json.loads(line) for line in out.splitlines()], out + err


def test_unlock_order_and_private_output(controller, capsys):
    values = {"code": "synthetic-private-code", "sync": "synthetic-private-sync"}
    password = "synthetic-long-password"
    (controller.bundle / "sealed-tokens.json").write_text(json.dumps(seal(values, password, DEFAULT_REPO, DEFAULT_SYNC)))
    commands = [{"command": "unlock", "password": key} for key in ("private-wrong", password)]
    events, output = exchange(controller, commands + [{"command": "quit"}], capsys)
    assert [e["type"] for e in events] == ["status", "need_unlock", "unlock_failed", "status", "status", "ready"]
    assert events[2] == dict(type="unlock_failed", remaining=4, wait=0)
    assert events[-1].items() >= dict(port=43210, version=VERSION, payload_version="test.30").items()
    assert controller.values == values
    assert all(value not in output for value in (*values.values(), password, "private-wrong"))


def test_manual_tokens_and_eof(controller, capsys):
    events, output = exchange(controller, [{"command": "set_tokens", "code": "private-fallback"}], capsys)
    assert [e["type"] for e in events] == ["status", "need_tokens", "status", "status", "ready"]
    assert controller.values["sync"] == "private-fallback"
    assert "private-fallback" not in output


def test_cooldown_blocks_correct_password(controller, capsys):
    for _ in range(5):
        controller.attempts.failed()
    controller.unlock("never-echo-this")
    output = capsys.readouterr().out
    event = json.loads(output)
    assert event["type"] == "unlock_failed" and event["remaining"] == 0 and 0 < event["wait"] <= 30
    assert "never-echo-this" not in output


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
            assert [json.loads(line)["type"] for line in output.splitlines()] == ["status", "need_tokens", "error"]
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
    events, _ = exchange(controller, [{"command": "set_tokens", "code": "test-token"}], capsys)
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
