"""从只读安装目录加载后端控制管道，后端的依赖由所选更新包决定。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bootstrap.service import serve

serve()
