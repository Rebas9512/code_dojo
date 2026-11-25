"""检查三系统启动决策；测试替换程序调用，不打开浏览器也不拉取代码仓库。"""

import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import dojo


@pytest.fixture
def agent_commands(monkeypatch):
    monkeypatch.setenv("CODE_DOJO_CLAUDE_BIN", "claude")
    monkeypatch.setenv("CODE_DOJO_CODEX_BIN", "codex")
    monkeypatch.setattr("bootstrap.agents._login_path", lambda: "")


@pytest.mark.parametrize(("platform", "suffix"), [
    ("linux", ".local/share/code-dojo"), ("darwin", "Library/Application Support/code-dojo"),
    ("win32", "AppData/Roaming/code-dojo"),
])
def test_data_directory(tmp_path, monkeypatch, platform, suffix):
    for key in ("CODE_DOJO_DATA", "XDG_DATA_HOME", "APPDATA"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setattr(dojo.sys, "platform", platform)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    assert dojo.data_directory() == tmp_path / suffix
    monkeypatch.setenv("CODE_DOJO_DATA", str(tmp_path / "override"))
    assert dojo.data_directory() == tmp_path / "override"


def test_dependencies_and_doctor(tmp_path, monkeypatch, capsys, agent_commands):
    monkeypatch.setenv("CODE_DOJO_DATA", str(tmp_path))
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setattr(dojo.shutil, "which", lambda name, path=None: None)
    assert dojo.main(["doctor"]) == 1
    out = capsys.readouterr().out
    assert all(s in out for s in ("Linux", "macOS", "Windows", "AI 助教会关闭"))
    monkeypatch.setattr(dojo.shutil, "which", lambda name, path=None: name)
    monkeypatch.setattr(dojo.subprocess, "check_output", lambda *a, **kw: "v22.12.0")
    assert not dojo.dependencies()
    monkeypatch.setattr(dojo.subprocess, "check_output", lambda *a, **kw: "v22.13.0")
    assert dojo.main(["doctor"]) == 0


def test_busy_port_remains_reserved():
    with dojo.bind_port(0) as busy, dojo.bind_port(busy.getsockname()[1]) as alternate:
        assert busy.getsockname()[0] == alternate.getsockname()[0] == "127.0.0.1"
        assert busy.getsockname()[1] != alternate.getsockname()[1]


def test_no_pull_clean_dirty(monkeypatch):
    run = Mock()
    status = Mock(return_value=b" M web/file")
    monkeypatch.setattr(dojo.subprocess, "run", run)
    monkeypatch.setattr(dojo.subprocess, "check_output", status)
    dojo.pull_bank(True)
    status.assert_not_called()
    dojo.pull_bank(False)
    run.assert_not_called()
    status.return_value = b""
    dojo.pull_bank(False)
    run.assert_called_once_with(["git", "pull", "--ff-only"], cwd=dojo.ROOT, check=True)


def test_build_cache(tmp_path, monkeypatch):
    modules = tmp_path / "node_modules"
    lock = tmp_path / "package-lock.json"
    lock.write_text('{"packages":{"":{"name":"test"}}}', encoding="utf-8")
    run = Mock(side_effect=lambda *a, **kw: modules.mkdir(exist_ok=True))
    monkeypatch.setattr(dojo.subprocess, "run", run)
    dojo.prepare_node(tmp_path)
    dojo.prepare_node(tmp_path)
    assert run.call_count == 1
    lock.write_text('{"packages":{"":{"name":"new"}}}', encoding="utf-8")
    dojo.prepare_node(tmp_path)
    assert run.call_count == 2
    assert dojo.needs_build(tmp_path)
    index = tmp_path / "dist/index.html"
    index.parent.mkdir()
    index.touch()
    assert not dojo.needs_build(tmp_path)
    (tmp_path / "src").mkdir()
    source = tmp_path / "src/app.ts"
    source.touch()
    import os
    os.utime(source, (index.stat().st_mtime + 2,) * 2)
    assert dojo.needs_build(tmp_path)


@pytest.mark.parametrize("installed,expected", [({}, "off"), ({"codex": "/codex"}, "codex")])
def test_launch_uses_single_local_backend(tmp_path, monkeypatch, installed, expected, agent_commands):
    monkeypatch.setattr(dojo, "dependencies", lambda: True)
    monkeypatch.setattr(dojo.shutil, "which", lambda name, path=None: installed.get(name))
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setenv("CODE_DOJO_DATA", str(tmp_path))
    monkeypatch.setenv("CODE_DOJO_AUTH", "on")
    monkeypatch.setenv("CODE_DOJO_AI_PROVIDER", "codex")
    pull, backend, prepare = Mock(), Mock(return_value=0), Mock()
    monkeypatch.setattr(dojo, "pull_bank", pull)
    monkeypatch.setattr(dojo, "backend", backend)
    monkeypatch.setattr(dojo, "prepare_node", prepare)
    monkeypatch.setattr(dojo, "needs_build", lambda _: False)
    monkeypatch.setattr(dojo.subprocess, "run", Mock())
    assert dojo.main(["--no-pull"]) == 0
    pull.assert_called_once_with(True)
    backend.assert_called_once_with(["--serve"])
    assert prepare.call_count == 2
    assert dojo.os.environ["CODE_DOJO_AUTH"] == "off"
    assert dojo.os.environ["CODE_DOJO_AI_PROVIDER"] == expected


def test_legacy_rejects_same_directory_before_opening(tmp_path, monkeypatch):
    monkeypatch.setenv("CODE_DOJO_DATA", str(tmp_path))
    source = tmp_path / "code_dojo.db"
    source.touch()
    with pytest.raises(ValueError, match="不同目录"):
        dojo.import_legacy(tmp_path)
    assert source.read_bytes() == b""
