"""全部使用临时目录、模拟的 gh/GitHub 和合成凭据。"""

import base64
import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock
from urllib.error import HTTPError, URLError

import pytest
from cryptography.exceptions import InvalidTag

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from bootstrap import DEFAULT_REPO, DEFAULT_SYNC, credentials, github
from bootstrap.sealed import seal, unseal
from bootstrap.window import UnlockAttempts
from scripts.desktop import seal_tokens as cli


VALUES = {"code": "sample-first-for-test", "sync": "sample-second-for-test"}
PASSWORD = "用于临时测试的长密码"
REPOS = (DEFAULT_REPO, DEFAULT_SYNC)


@pytest.fixture(scope="module")
def envelope():
    return seal(VALUES, PASSWORD, *REPOS)


def test_roundtrip_and_randomness(envelope):
    assert unseal(envelope, PASSWORD, *REPOS) == VALUES
    other = seal(VALUES, PASSWORD, *REPOS)
    assert all(other[k] != envelope[k] for k in ("salt", "nonce", "ciphertext"))
    assert not any(v in json.dumps(envelope) for v in VALUES.values())


def test_wrong_password_and_tampering(envelope):
    with pytest.raises(InvalidTag):
        unseal(envelope, "错误密码", *REPOS)
    cipher = bytearray(base64.b64decode(envelope["ciphertext"]))
    cipher[0] ^= 1
    with pytest.raises(InvalidTag):
        unseal(envelope | {"ciphertext": base64.b64encode(cipher)}, PASSWORD, *REPOS)
    with pytest.raises(ValueError, match="版本"):
        unseal(envelope | {"version": 2}, PASSWORD, *REPOS)
    with pytest.raises(ValueError, match="仓库"):
        unseal(envelope, PASSWORD, *reversed(REPOS))
    with pytest.raises(InvalidTag):
        unseal(envelope | {"repos": dict(code=DEFAULT_SYNC, sync=DEFAULT_REPO)}, PASSWORD, *reversed(REPOS))
    with pytest.raises(ValueError, match="参数"):
        unseal(envelope | {"kdf": dict(n=2**30)}, PASSWORD, *REPOS)


@pytest.mark.parametrize("saved", [VALUES, {}])
@pytest.mark.parametrize("bundled", [True, False])
def test_start_uses_only_saved_credentials(tmp_path, monkeypatch, saved, bundled):
    from bootstrap.protocol import Controller

    if bundled:
        (tmp_path / "sealed-tokens.json").touch()
    ring = Mock()
    ring.get_password.return_value = json.dumps(saved)
    monkeypatch.setattr(credentials, "keychain", lambda: ring)
    controller = Controller(tmp_path, tmp_path, Mock())
    monkeypatch.setattr(controller, "launch", Mock())
    run = Mock()
    monkeypatch.setattr(subprocess, "run", run)
    controller.begin()
    controller.launch.assert_called_once_with()
    assert controller.values == saved
    run.assert_not_called()


def test_legacy_fallback_and_keyring_both_cleared(tmp_path, monkeypatch):
    ring = Mock()
    ring.get_password.side_effect = [json.dumps(VALUES), None]
    monkeypatch.setattr(credentials, "keychain", lambda: ring)
    fallback = tmp_path / "github-tokens.json"
    fallback.write_text(json.dumps(VALUES))
    assert credentials.tokens(tmp_path) == VALUES
    credentials.clear_tokens(tmp_path)
    assert not fallback.exists() and credentials.tokens(tmp_path) == {}
    ring.delete_password.assert_called_once_with(*ring.get_password.call_args.args)


def test_five_attempts_survive_reopen(tmp_path, monkeypatch):
    from bootstrap import window
    monkeypatch.setattr(window.time, "time", lambda: 100)
    for i in range(5):
        attempts = UnlockAttempts(tmp_path)
        assert attempts.state() == (i, 0)
        attempts.failed()
    assert UnlockAttempts(tmp_path).state() == (5, 30)
    monkeypatch.setattr(window.time, "time", lambda: 130)
    assert attempts.state() == (0, 0)
    attempts.failed()
    attempts.clear()
    assert attempts.state() == (0, 0)


@pytest.mark.parametrize("upload", [True, False])
def test_cli_private_io(tmp_path, monkeypatch, capsys, upload):
    path = tmp_path / ".env"
    path.write_text(f"# 示例\n\nexport A = '{VALUES['code']}'  # 第一项\n B = \"{VALUES['sync']}\"\n", encoding="utf-8")
    out = tmp_path / "sealed.json"
    verify, gh = Mock(), Mock()
    monkeypatch.setattr(cli, "verify_tokens", verify)
    monkeypatch.setattr(cli.getpass, "getpass", Mock(side_effect=["短", PASSWORD, "不同", PASSWORD, PASSWORD]))
    monkeypatch.setattr(cli.subprocess, "run", gh)
    args = ["--env", str(path), "--keys", "A,B", "--out", str(out), "--repo", "owner/release"]
    assert cli.main(args if upload else args + ["--no-upload"]) == 0
    verify.assert_called_once_with(VALUES, *REPOS)
    sealed = json.loads(out.read_bytes())
    assert unseal(sealed, PASSWORD, *REPOS) == VALUES
    if upload:
        assert gh.call_args.args == (["gh", "secret", "set", "CODE_DOJO_SEALED_TOKENS", "--repo", "owner/release"],)
        assert json.loads(gh.call_args.kwargs["input"]) == sealed
    else:
        gh.assert_not_called()
    stdout, stderr = capsys.readouterr()
    assert all(word in stdout for word in ("已读取 2 个令牌", "太短", "两次密码不同"))
    assert not any(v in stdout + stderr for v in (*VALUES.values(), PASSWORD, sealed["ciphertext"]))


@pytest.mark.parametrize(("line", "password", "error"), [
    ('unlock = "十个字符以上 # 带空格和=$" # 注释', "十个字符以上 # 带空格和=$", None),
    ("unlock=pass#word=1234", "pass#word=1234", None),
    ("unlock=short1234", "short1234", "太短"),
    ("unlock= # 留空", "", "太短"),
    ("", "", "缺少指定的密码变量"),
])
def test_cli_password_key(tmp_path, monkeypatch, capsys, line, password, error):
    path, out = tmp_path / ".env", tmp_path / "sealed.json"
    path.write_text(f"code_dojo={VALUES['code']}\ncode_dojo_sync={VALUES['sync']}\n{line}\n", encoding="utf-8")
    verify, prompt, gh = Mock(), Mock(), Mock()
    monkeypatch.setattr(cli, "verify_tokens", verify)
    monkeypatch.setattr(cli.getpass, "getpass", prompt)
    monkeypatch.setattr(cli.subprocess, "run", gh)

    rc = cli.main(["--env", str(path), "--password-key", "unlock", "--no-upload", "--out", str(out)])
    stdout, stderr = capsys.readouterr()
    prompt.assert_not_called()
    gh.assert_not_called()
    for secret in (*VALUES.values(), password):
        if secret:
            assert secret not in stdout + stderr
    if error:
        assert rc == 1 and error in stderr
        verify.assert_not_called()
        assert not out.exists()
    else:
        assert rc == 0 and "已读取 2 个令牌" in stdout
        verify.assert_called_once_with(VALUES, *REPOS)
        assert unseal(json.loads(out.read_bytes()), password, *REPOS) == VALUES


@pytest.mark.parametrize("error", [HTTPError("", 401, "", {}, None), HTTPError("", 404, "", {}, None),
                                    URLError("连接失败")])
def test_probe_fails_privately(tmp_path, monkeypatch, capsys, error):
    from contextlib import nullcontext
    calls = []
    def probe(client, path, accept):
        calls.append((client.base, path, client.token))
        if len(calls) == 2:
            raise error
        return nullcontext()
    monkeypatch.setattr(github.GitHub, "open", probe)
    password, gh = Mock(), Mock()
    monkeypatch.setattr(cli, "ask_password", password)
    monkeypatch.setattr(cli.subprocess, "run", gh)
    path = tmp_path / ".env"
    path.write_text(f"code_dojo={VALUES['code']}\ncode_dojo_sync={VALUES['sync']}\n", encoding="utf-8")
    assert cli.main(["--env", str(path)]) == 1
    password.assert_not_called()
    gh.assert_not_called()
    assert calls == [(f"https://api.github.com/repos/{REPOS[0]}", "/releases?per_page=1", VALUES["code"]),
                     (f"https://api.github.com/repos/{REPOS[1]}", "/readme", VALUES["sync"])]
    stdout, stderr = capsys.readouterr()
    assert "同步仓库" in stderr
    assert not any(v in stdout + stderr for v in VALUES.values())
