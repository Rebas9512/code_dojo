"""以隔离模式加载安装目录中的启动器。"""

import sys
from pathlib import Path

bundle = Path(__file__).resolve().parent
sys.path.insert(0, str(bundle))
if sys.argv[1:2] == ["--serve"]:
    from bootstrap.service import serve
    serve()
else:
    sys.path.insert(1, str(bundle / "libraries"))
    from bootstrap.window import main
    main(bundle)
