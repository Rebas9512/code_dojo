"""内容任务通过同一条命令检查题号前缀、代码、技能和说明。"""

import sys
from pathlib import Path
from shutil import copytree

import pytest

from app.problems import load_problem

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts/curriculum"))
import verify_standard

FIXTURES = Path(__file__).parent / "fixtures/problems"
PID = "py-0a-001-add"
CODE = "def add(a, b):\n    return a + b\n"
NOTES = "## 思路\n\n两个数相加。直接返回结果。\n\n## 复杂度\n\n时间 O(1)，空间 O(1)。\n\n## 写法要点\n\n- 直接返回。\n"
ADVANCED = "## 进阶写法\n\n用内置函数求和。\n\n```python\ndef add(a, b):\n    return sum((a, b))\n```\n"


@pytest.fixture
def problem(tmp_path):
    track = copytree(FIXTURES / "python", tmp_path / "python")
    folder = track / "0A" / PID
    meta = folder / "problem.yaml"
    meta.write_text(meta.read_text().replace("py.function-return", "py.func-return"))
    (folder / "standard.py").write_text(CODE)
    (folder / "standard.md").write_text(NOTES + "\n" + ADVANCED)
    return load_problem(folder)


@pytest.mark.parametrize(("filename", "content", "error"), [
    ("standard.py", CODE.replace("a + b", "(a + b) % 2000"), "标准写法没通过：wrong_answer"),
    ("standard.py", CODE.replace("a + b", "sum((a, b))"), "标准写法用到 py.list-builtins"),
    ("standard.md", NOTES.replace("## 写法要点", "## 小结"), "小节应依次为"),
    ("standard.md", NOTES + ADVANCED.replace("sum((a, b))", "(a + b) % 2000"), "进阶写法没通过：wrong_answer"),
])
def test_verifier_rejects_invalid_answer(problem, judging, filename, content, error):
    problem.file(filename).write_text(content)
    issues = verify_standard.check_answers(judging, problem)
    assert any(error in issue for issue in issues), issues


def test_cli_loads_only_selected_problems(problem, tmp_path, monkeypatch, capsys):
    unrelated = tmp_path / "other/0/other-0-001-broken"
    unrelated.mkdir(parents=True)
    (unrelated / "standard.py").touch()
    monkeypatch.setenv("CODE_DOJO_PROBLEMS", str(tmp_path))
    for filters in [["--only", "py-0a-001"], ["--track", "python"]]:
        monkeypatch.setattr(sys, "argv", ["verify_standard.py", *filters])
        assert verify_standard.main() == 0
        output = capsys.readouterr().out
        assert f"✓ {PID}" in output and "有参考答案 1 道，通过 1，失败 0" in output
    problem.file("standard.md").unlink()
    assert verify_standard.main() == 1
    assert "缺少 standard.md" in capsys.readouterr().out
