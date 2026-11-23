"""本机订阅 CLI、严格格式和按请求选择助教。测试只调用替身。"""

import json
import os
import subprocess
import tomllib
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import pytest

from app import main
from app.ai import extra, provider, tutor
from app.ai.codex_schema import restore_result, strict_schema
from app.ai.provider import AIError, CodexProvider, FakeProvider
from app.db import Store


@pytest.mark.parametrize("schema", [tutor.SCHEMA, extra.INSPECT_SCHEMA, extra.SqlExtra.model_json_schema(), extra.SCHEMA],
                         ids=["tutor", "inspect", "sql", "python"])
def test_strict_schemas(schema):
    def check(node):
        assert not ({"default", "format", "pattern", "oneOf", "const"} & node.keys())
        assert "type" in node or "anyOf" in node
        if node.get("type") == "object":
            assert node["additionalProperties"] is False
            assert node["required"] == list(node["properties"])
            for child in node["properties"].values():
                check(child)
        if node.get("type") == "array":
            check(node["items"])
        branches = node.get("anyOf", [])
        first_keys = [next(iter(child["properties"])) for child in branches if child.get("type") == "object"]
        assert len(first_keys) == len(set(first_keys))
        for child in branches:
            check(child)

    before = deepcopy(schema)
    wire = strict_schema(schema)
    check(wire)
    for key in set(schema["properties"]) - set(schema["required"]):
        assert {"type": "null"} in wire["properties"][key]["anyOf"]
    assert schema == before


def test_restore_sql_and_inspect_results():
    sql = {"mode": None, "ordered": False, "checks": [{"label": "列", "query": "select 1", "ordered": None},
                                                     {"label": "约束", "probe": "select 2", "expect": "ok"}]}
    assert restore_result(sql, extra.SqlExtra.model_json_schema()) == {
        "ordered": False, "checks": [{"label": "列", "query": "select 1"}, sql["checks"][1]]}
    for answer in ({"type": "short", "accept": ["A"], "normalize": None},
                   {"type": "choice", "options": ["A", "B"], "correct": 0}):
        data = {"answer": {**answer, "misconceptions": [{"key": "1", "value": "DM02"}]}}
        result = restore_result(data, extra.INSPECT_SCHEMA)["answer"]
        assert result == {k: v for k, v in answer.items() if v is not None} | {"misconceptions": {"1": "DM02"}}
    required = {"type": "object", "properties": {"x": {"type": ["string", "null"]}}, "required": ["x"]}
    assert restore_result({"x": None}, required) == {"x": None}


@pytest.mark.parametrize("effort,expected", [("low", "low"), ("medium", "medium"), ("high", "high"),
                                            ("xhigh", "xhigh"), ("max", "xhigh")])
def test_codex_exec(tmp_path, monkeypatch, effort, expected):
    system = '原样传递引号 "、换行\n和反斜杠 \\'
    result = {"reply": "看一眼输入", "edits": [], "make_extra": "", "delete_extras": []}
    binary = str(tmp_path / "命令/codex")
    monkeypatch.setattr(provider.shutil, "which", lambda _: binary)
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "登录目录"))
    for secret in ("OPENAI_API_KEY", "CODEX_API_KEY", "CLAUDE_CODE_OAUTH_TOKEN", "CODE_DOJO_PASSWORD_HASH"):
        monkeypatch.setenv(secret, "测试专用")

    def run(cmd, *, input, env, cwd, timeout, **kwargs):
        assert cmd[:2] == [binary, "exec"] and cmd[-1] == "-" and input == "学生的问题"
        assert Path(cmd[cmd.index("-C") + 1]) == cwd and not list(cwd.iterdir())
        assert cmd[cmd.index("--sandbox") + 1] == "read-only" and timeout == 180
        assert {"--ephemeral", "--skip-git-repo-check", "--ignore-user-config", "--ignore-rules"} <= set(cmd)
        assert cmd[cmd.index("-m") + 1] == "gpt-6.2-astra"
        config = tomllib.loads("\n".join(cmd[i + 1] for i, arg in enumerate(cmd) if arg == "-c"))
        assert config == dict(developer_instructions=system, model_reasoning_effort=expected, forced_login_method="chatgpt")
        allowed = {"HOME", "PATH", "LANG", "CODEX_HOME"}
        if os.name == "nt":
            allowed.update(("USERPROFILE", "APPDATA", "LOCALAPPDATA", "SystemRoot", "TEMP", "TMP", "ComSpec", "PATHEXT"))
        assert env == {key: os.environ[key] for key in allowed if key in os.environ} | {"LANG": os.getenv("LANG", "C.UTF-8")}
        assert json.loads(Path(cmd[cmd.index("--output-schema") + 1]).read_bytes()) == strict_schema(tutor.SCHEMA)
        Path(cmd[cmd.index("-o") + 1]).write_text(json.dumps(result), encoding="utf-8")
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(provider.subprocess, "run", run)
    assert CodexProvider(workdir=tmp_path).complete(system=system, prompt="学生的问题", schema=tutor.SCHEMA, effort=effort) == result
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize("failure,detail", [("missing", "找不到"), ("timeout", "秒没有回复"), ("empty", "JSON"),
                                            ("invalid", "JSON"), ("exit", "退出码")])
def test_codex_failure_cleans_temp(tmp_path, monkeypatch, failure, detail):
    def run(cmd, **kwargs):
        if failure == "missing":
            raise FileNotFoundError
        if failure == "timeout":
            raise subprocess.TimeoutExpired(cmd, 180)
        if failure == "invalid":
            Path(cmd[cmd.index("-o") + 1]).write_text("非 JSON", encoding="utf-8")
        return subprocess.CompletedProcess(cmd, int(failure == "exit"))

    monkeypatch.setattr(provider, "find_codex", lambda _: "/test/codex")
    monkeypatch.setattr(provider.subprocess, "run", run)
    with pytest.raises(AIError, match=detail):
        CodexProvider(workdir=tmp_path).complete(system="设定", prompt="问题", schema=tutor.SCHEMA)
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize("system,machine,rel", [("linux", "x86_64", "linux-x86_64/codex"),
                                                ("darwin", "arm64", "macos-aarch64/codex"),
                                                ("win32", "AMD64", "windows-x86_64/codex.exe")])
def test_codex_extension_version(tmp_path, monkeypatch, system, machine, rel):
    monkeypatch.setattr(provider.sys, "platform", system)
    monkeypatch.setattr(provider.platform, "machine", lambda: machine)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    for version in ("26.9.303", "26.11.2"):
        binary = tmp_path / f".vscode/extensions/openai.chatgpt-{version}-platform/bin" / rel
        binary.parent.mkdir(parents=True)
        binary.touch(mode=0o755)
    monkeypatch.setattr(provider.shutil, "which", lambda _: None)
    assert provider.find_codex("codex") == str(binary)
    monkeypatch.setattr(provider.shutil, "which", lambda name: "/path/codex" if name == "custom" else None)
    assert provider.find_codex("custom") == "/path/codex"


def test_status_discovers_agents_each_time(client, tmp_path, monkeypatch):
    monkeypatch.setattr(main, "settings", replace(main.settings, ai_provider="codex", claude_bin="cc", codex_bin="cx",
                                                  ai_model="模型甲", codex_model="模型乙"))
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    installed = {}
    monkeypatch.setattr(provider.shutil, "which", installed.get)
    claude = {"id": "claude", "name": "Claude", "model": "模型甲"}
    codex = {"id": "codex", "name": "Codex", "model": "模型乙"}
    for names, expected in [([], []), (["cc"], [claude]), (["cx"], [codex]), (["cc", "cx"], [codex, claude])]:
        installed.clear()
        installed.update({key: "/test/" + key for key in names})
        status = client.get("/api/status").json()
        assert status["ai_agents"] == expected
        assert status["ai"] == (expected[0]["id"] if expected else "off")
        assert status["ai_model"] == (expected[0]["model"] if expected else None)
    monkeypatch.setattr(main, "settings", replace(main.settings, ai_provider="off"))
    status = client.get("/api/status").json()
    assert (status["ai"], status["ai_model"], status["ai_agents"]) == ("off", None, [])


def test_selected_agent_and_shared_history(client, fake_agents, monkeypatch, tmp_path):
    store = Store(tmp_path / "chat.db")
    monkeypatch.setattr(main, "store", store)
    claude = FakeProvider([{"reply": "先看第一行", "edits": []}])
    codex = FakeProvider([{"reply": "再看第二行", "edits": []}])
    fake_agents(claude=claude, codex=codex)
    base = "/api/problems/py-0a-001-add"
    assert client.post(base + "/chat", json={"message": "开始"}).json()["assistant"]["agent"] == "claude"
    assert client.post(base + "/chat", json={"message": "继续", "agent": "codex"}).json()["assistant"]["agent"] == "codex"
    assert "先看第一行" in codex.calls[0]["prompt"] and len(claude.calls) == 1
    fake_agents(claude=claude)
    for endpoint in ("/chat", "/extras"):
        response = client.post(base + endpoint, json={"message": "继续", "agent": "codex"})
        assert response.status_code == 400 and "Codex" in response.json()["detail"]
    assert [m["agent"] for m in client.get(base + "/chat").json()] == [None, "claude", None, "codex"]
    assert client.get(base + "/extras").json() == []


def test_chat_sources_survive_sync_with_old_messages(tmp_path):
    source = Store(tmp_path / "source/chat.db")
    source.add_chat("题", "assistant", "以前的回复", notes=["旧记录"])
    source.add_chat("题", "assistant", "这次的回复", notes=["重试"], agent="codex")
    target = Store(tmp_path / "target/chat.db")
    records = source.pending_events()
    assert all("agent" not in event["payload"]["row"] for event in records)
    target.import_events(records)
    assert [m["agent"] for m in target.chat("题")] == ["claude", "codex"]
