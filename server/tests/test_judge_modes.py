"""同一套判题边界用例在本地和 Docker 上运行。"""

import json
import os
import sqlite3
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from app.judge import Judge
from app.config import load_settings
from app.local_judge import LocalEnvironments, PreparationError, run_local


def test_deep_cached_recursion(judging):
    result = judging.run(mode="function", entry="depth", cases=[{"args": [50_000], "expected": 50_000}],
                         code="from functools import cache\n@cache\ndef depth(n): return 1 + depth(n-1) if n else 0")
    assert result["verdict"] == "accepted", result


def test_timeout_retains_previous_case_and_output(judging):
    result = judging.run(mode="function", entry="f", time_limit_ms=150,
                         cases=[{"args": [i], "expected": 0} for i in range(3)],
                         code="def f(n):\n    print('开始')\n    while n: pass\n    return 0")
    assert result["verdict"] == "timeout"
    assert [c["status"] for c in result["cases"]] == ["passed", "timeout", "skipped"]
    assert result["cases"][1]["stdout"] == "开始\n"
    prediction = judging.run(mode="predict", time_limit_ms=150, code="while True: pass", cases=[], answer="")
    assert prediction["verdict"] == "timeout"


def test_windows_line_endings(judging):
    result = judging.run(mode="predict", code="print('甲')\r\nprint('乙')", cases=[], answer="甲\r\n乙\r\n")
    assert result["verdict"] == "accepted"
    result = judging.run(mode="stdio", code="print(input() == '书')", cases=[{"stdin": "书\r\n", "expected": "True\r\n"}])
    assert result["verdict"] == "accepted"


@pytest.mark.skipif(sys.platform != "linux", reason="本地地址空间限制只在 Linux 启用")
def test_memory_limit(judging):
    result = judging.run(mode="stdio", cases=[{"expected": ""}], code="block = bytearray(600 * 1024 * 1024)")
    assert result["verdict"] == "runtime_error", result
    assert "内存" in (result.get("error") or result["cases"][0]["error"])


def test_auto_selects_available_image_per_runtime(tmp_path, monkeypatch):
    monkeypatch.setattr(Judge, "image_present", lambda self, runtime: runtime == "python")
    assert Judge("image", tmp_path, mode="auto").backends == {"python": "docker", "ds": "local"}


def test_uv_missing_and_retry(tmp_path, monkeypatch):
    local = LocalEnvironments(tmp_path)
    monkeypatch.setattr("app.local_judge.shutil.which", lambda _: None)
    with pytest.raises(PreparationError, match="Windows（PowerShell）") as exc:
        local.interpreter("ds")
    assert "Linux：" in str(exc.value) and "macOS：" in str(exc.value)
    monkeypatch.setattr("app.local_judge.shutil.which", lambda _: "uv")
    calls = []

    def install(args):
        calls.append(args)
        if "venv" in args:
            python = Path(args[-1]) / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
            python.parent.mkdir(parents=True, exist_ok=True)
            python.touch()
        elif len(calls) == 2:
            raise subprocess.CalledProcessError(1, args, stderr="安装失败")

    monkeypatch.setattr(local, "_run_uv", install)
    with pytest.raises(PreparationError, match="安装失败"):
        local.interpreter("ds")
    assert local.ds_state() == "unprepared"
    with ThreadPoolExecutor(max_workers=2) as pool:
        # 不同实例模拟后端与命令行同时重试，共用安装锁。
        second = LocalEnvironments(tmp_path)
        monkeypatch.setattr(second, "_run_uv", install)
        paths = list(pool.map(lambda env: env.interpreter("ds"), [local, second]))
    assert paths[0] == paths[1] and local.ds_state() == "ready" and len(calls) == 4


@pytest.mark.parametrize("outer_timeout", [False, True])
def test_local_timeout_reaps_children(tmp_path, outer_timeout):
    # 子进程持有写事务。判题结束后必须能重新获得写锁。
    python = LocalEnvironments(load_settings().judge_envs).interpreter("python")
    child = ("import sqlite3, time; from pathlib import Path; "
             "db=sqlite3.connect('child.db'); db.execute('BEGIN IMMEDIATE'); "
             "Path('locked').touch(); time.sleep(30)")
    code = ("import subprocess, sys, time\nfrom pathlib import Path\n"
            f"subprocess.Popen([sys.executable, '-c', {child!r}])\n"
            "while not Path('locked').exists(): time.sleep(.01)\ntime.sleep(30)")
    (tmp_path / "user.py").write_text(code, encoding="utf-8")
    job = {"mode": "stdio", "time_limit_ms": 30_000 if outer_timeout else 1500, "cases": [{"expected": ""}]}
    (tmp_path / "job.json").write_text(json.dumps(job), encoding="utf-8")
    if outer_timeout:
        with pytest.raises(subprocess.TimeoutExpired):
            run_local(python, tmp_path, 2, "256m")
    else:
        result = Judge._result(run_local(python, tmp_path, 8, "256m"), "256m")
        assert result["verdict"] == "timeout", result
    assert (tmp_path / "locked").exists()
    db = sqlite3.connect(tmp_path / "child.db", timeout=2)
    try:
        db.execute("BEGIN IMMEDIATE")
    finally:
        db.close()
