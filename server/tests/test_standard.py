"""参考答案只读，正式通过时解锁。"""

from pathlib import Path
from shutil import copytree

import pytest

from app.db import Store
from app.problems import ProblemBank

FIXTURES = Path(__file__).parent / "fixtures/problems"
PID = "py-0a-001-add"
NOTES = "## 思路\n\n把两个数相加。\n\n## 复杂度\n\n时间 O(1)，空间 O(1)。\n\n## 写法要点\n\n- 直接返回和。"
ADVANCED = "## 进阶写法\n\n也可以用内置函数求和。\n\n```python\ndef add(a, b):\n    return sum((a, b))\n```"


@pytest.mark.parametrize("ai_lines", [0, 2])
def test_standard_unlocks_on_submit(client, tmp_path, monkeypatch, ai_lines):
    from app import main

    store = Store(tmp_path / "data/test.db")
    monkeypatch.setattr(main, "store", store)
    bank = ProblemBank(tmp_path / "problems")
    track_dir = copytree(FIXTURES / "python", bank.root / "python")
    monkeypatch.setattr(main, "bank", bank)
    path = track_dir / "0A" / PID
    solution = (path / "solution.py").read_text()
    code = "def add(a: int, b: int) -> int:\n    return a + b\n"
    if not ai_lines:
        (path / "standard.py").write_text(code)
        (path / "standard.md").write_text(NOTES + "\n\n" + ADVANCED)
    url = f"/api/problems/{PID}"
    assert client.get(url + "/standard").status_code == 403
    assert client.post(url + "/run", json={"code": code}).json()["verdict"] == "accepted"
    assert client.post(url + "/submit", json={"code": "def add(a,b): return a-b"}).json()["verdict"] == "wrong_answer"
    locked = client.get(url + "/standard")
    assert locked.status_code == 403 and "正式提交通过" in locked.json()["detail"]
    assert client.post(url + "/submit", json={"code": code, "ai_lines": ai_lines}).json()["verdict"] == "accepted"
    version = store.version
    assert client.get(url + "/standard").json() == {
        "code": solution if ai_lines else code, "language": "python", "has_notes": not ai_lines,
        "notes_md": "" if ai_lines else NOTES, "advanced_md": "" if ai_lines else ADVANCED,
    }
    assert store.version == version


def test_standard_excludes_other_exercises(client, tmp_path, monkeypatch):
    from app import main

    monkeypatch.setattr(main, "store", Store(tmp_path / "test.db"))
    extra = main.store.create_extra(PID, "测试参考答案")
    for pid in [extra["id"], "py-0a-003-predict-loop", "data-0-001-book-key"]:
        assert client.get(f"/api/problems/{pid}/standard").status_code == 404
