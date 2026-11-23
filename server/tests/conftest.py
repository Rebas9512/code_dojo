"""测试用独立的题库（tests/fixtures/problems）和临时数据目录，不碰真实题库和数据。"""

import os
import tempfile
from dataclasses import replace
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures" / "problems"
os.environ["CODE_DOJO_PROBLEMS"] = str(FIXTURES)
os.environ["CODE_DOJO_DATA"] = tempfile.mkdtemp(prefix="code-dojo-test-data-")
os.environ["CODE_DOJO_AI_PROVIDER"] = "off"  # 测试里不调真 AI，用 FakeProvider 替换
os.environ["CODE_DOJO_AUTH"] = "off"
os.environ.setdefault("CODE_DOJO_BANK_WATCH", "sync")  # 测试里改了文件马上要看到，保持每次请求都检查
os.environ.pop("CODE_DOJO_WEB_DIST", None)
os.environ.pop("CODE_DOJO_SYNC_REPO", None)


def available_backends():
    from app.config import load_settings
    from app.judge import Judge

    settings = load_settings()
    if settings.judge_mode != "auto":
        return [settings.judge_mode]
    probe = Judge.from_settings(replace(settings, judge_mode="docker"))
    return ["local", "docker"] if probe.image_present() else ["local"]


@pytest.fixture(scope="session", params=available_backends())
def judging(request):
    from app import main
    from app.db import Store
    from app.judge import Judge

    judge = Judge.from_settings(replace(main.settings, judge_mode=request.param))
    if request.param == "docker" and not judge.image_present():
        pytest.skip("未构建 Python 判题镜像")
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(main, "judge", judge)
        patch.setattr(main, "store", Store(main.settings.data_dir / f"{request.param}.db"))
        yield judge


@pytest.fixture(scope="session")
def client(judging):
    from fastapi.testclient import TestClient
    from app.main import app
    return TestClient(app, headers={"Content-Type": "application/json"})
