"""为隔离的桌面冒烟包生成合成信封。"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from bootstrap import DEFAULT_REPO, DEFAULT_SYNC
from bootstrap.sealed import seal

print(json.dumps(seal({"code": "test-read", "sync": "test-write"}, "dojo-smoke-unlock", DEFAULT_REPO, DEFAULT_SYNC)))
