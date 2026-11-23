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
