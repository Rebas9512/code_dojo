"""用临时命令目录模拟从桌面和终端启动。"""

import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from bootstrap import agents


@pytest.fixture(autouse=True)
def agent_env(tmp_path):
    agents._login_path.cache_clear()
    with patch.dict(os.environ, PATH=str(tmp_path), HOME=str(tmp_path), USERPROFILE=str(tmp_path)):
        os.environ.pop("CODE_DOJO_CLAUDE_BIN", None)
        os.environ.pop("CODE_DOJO_CODEX_BIN", None)
        yield
    agents._login_path.cache_clear()


@pytest.mark.skipif(os.name == "nt", reason="Windows 不运行登录 shell")
def test_login_shell_path(tmp_path):
    directory = tmp_path / "命令 目录"
    directory.mkdir()
    for name in ("claude", "codex"):
        (directory / name).touch(mode=0o755)
    shell = tmp_path / "login-shell"
    shell.write_text(
        '#!/bin/sh\n[ "$1" = "-ilc" ] || exit 1\n'
        'echo called >> "$HOME/calls"\necho "启动提示"\n'
        'export PATH="$HOME/命令 目录:$PATH"\neval "$2"\necho "退出提示"\n',
        encoding="utf-8",
    )
    shell.chmod(0o755)
    os.environ["SHELL"] = str(shell)

    assert agents.has_agent()
    assert os.get_exec_path() == [str(tmp_path), str(directory)]
    assert os.environ["CODE_DOJO_CLAUDE_BIN"] == str(directory / "claude")
    assert os.environ["CODE_DOJO_CODEX_BIN"] == str(directory / "codex")
    for name in ("claude", "codex"):
        (directory / name).unlink()
    assert not agents.has_agent()
    assert (tmp_path / "calls").read_text().splitlines() == ["called"]


@pytest.mark.parametrize("command,key", [("claude", "CODE_DOJO_CLAUDE_BIN"), ("custom-codex", "CODE_DOJO_CODEX_BIN")])
def test_current_path_skips_shell(tmp_path, monkeypatch, command, key):
    binary = tmp_path / (command + ".exe" if os.name == "nt" else command)
    binary.touch(mode=0o755)
    if command == "custom-codex":
        os.environ[key] = command
    run = Mock()
    monkeypatch.setattr(agents.subprocess, "run", run)
    assert agents.has_agent()
    assert Path(os.environ[key]) == (Path(command) if command == "custom-codex" else binary)
    run.assert_not_called()


@pytest.mark.parametrize("platform,shell", [("darwin", "/bin/zsh"), ("linux", "/bin/sh"), ("win32", None)])
def test_missing_agent_after_timeout(tmp_path, monkeypatch, platform, shell):
    os.environ.pop("SHELL", None)
    monkeypatch.setattr(agents, "sys", Mock(platform=platform))
    run = Mock(side_effect=subprocess.TimeoutExpired("shell", 3))
    monkeypatch.setattr(agents.subprocess, "run", run)
    assert not agents.has_agent()
    assert not agents.has_agent()
    assert os.environ["PATH"] == str(tmp_path)
    if shell:
        run.assert_called_once()
        assert run.call_args.args[0][:2] == [shell, "-ilc"]
        assert run.call_args.kwargs["timeout"] == 3
    else:
        run.assert_not_called()


def fake_command(directory, name, output="1.2.3 (Claude Code)", code=0):
    directory.mkdir(exist_ok=True)
    if os.name == "nt":
        path = directory / (name + ".cmd")
        script = f'@echo off\nif not "%~1"=="--version" exit /b 9\necho {output}\nexit /b {code}\n'
    else:
        path = directory / name
        script = f'#!/bin/sh\n[ "$#" = 1 ] && [ "$1" = --version ] || exit 9\necho "{output}"\nexit {code}\n'
    path.write_text(script)
    path.chmod(0o755)
    return str(path)


def test_manual_priorities_save_and_reset(tmp_path):
    (tmp_path / "desktop").mkdir()
    auto = fake_command(tmp_path, "claude")
    folder = tmp_path / "单独的 目录"
    manual = fake_command(folder, "claude")
    codex = fake_command(folder, "codex", "codex-cli 0.12.0")
    override = fake_command(folder, "developer")

    def resolved(**extra):
        env = os.environ.copy() | extra
        states = agents.service_agents(tmp_path, env)
        assert env["CODE_DOJO_CLAUDE_BIN"] == states["claude"]["path"]
        return states

    assert resolved()["claude"] == dict(source="auto", path=auto, manual=None)
    agents.set_manual_path(tmp_path, "codex", codex)
    agents.set_manual_path(tmp_path, "claude", manual)
    assert resolved()["claude"] == dict(source="manual", path=manual, manual=manual)
    assert resolved(CODE_DOJO_CLAUDE_BIN=override)["claude"] == dict(source="env", path=override, manual=manual)
    missing = str(folder / "missing")
    env = os.environ.copy() | {"CODE_DOJO_CLAUDE_BIN": missing}
    assert agents.service_agents(tmp_path, env)["claude"] == dict(source="env", path=None, manual=manual)
    assert env["CODE_DOJO_CLAUDE_BIN"] == missing
    Path(manual).unlink()
    env = os.environ.copy()
    assert agents.service_agents(tmp_path, env)["claude"] == dict(source="manual", path=None, manual=manual)
    assert env["CODE_DOJO_CLAUDE_BIN"] == manual
    agents.set_manual_path(tmp_path, "claude", None)
    assert agents.manual_paths(tmp_path) == {"codex": codex}
    assert resolved() == dict(claude=dict(source="auto", path=auto, manual=None),
                              codex=dict(source="manual", path=codex, manual=codex))


@pytest.mark.parametrize(("case", "reason"), [
    ("relative", "完整路径"), ("missing", "没有可执行文件"), ("directory", "没有可执行文件"),
    ("not_executable", "执行权限"), ("no_version", "没有返回版本号"),
    ("failed", "退出码 2"), ("timeout", "超过 5 秒"),
])
def test_invalid_path_preserves_previous_choice(tmp_path, monkeypatch, case, reason):
    (tmp_path / "desktop").mkdir()
    saved = fake_command(tmp_path, "good")
    agents.set_manual_path(tmp_path, "claude", saved)
    bad = fake_command(tmp_path, "bad", "no version" if case == "no_version" else "2.0", 2 if case == "failed" else 0)
    if case == "not_executable":
        # 部分共享挂载不支持 chmod，用系统权限查询的结果模拟拒绝执行。
        monkeypatch.setattr(os, "access", lambda path, mode: False)
    elif case == "timeout":
        run = Mock(side_effect=subprocess.TimeoutExpired(bad, 5))
        monkeypatch.setattr(subprocess, "run", run)
    path = {"relative": "relative", "missing": str(tmp_path / "missing"), "directory": str(tmp_path)}.get(case, bad)
    with pytest.raises(ValueError, match=reason):
        agents.set_manual_path(tmp_path, "claude", path)
    if case == "timeout":
        assert run.call_args.args == ([bad, "--version"],)
        assert run.call_args.kwargs["timeout"] == 5
    assert agents.manual_paths(tmp_path) == {"claude": saved}
