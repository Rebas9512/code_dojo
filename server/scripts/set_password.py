"""在终端输入两次密码，将加盐哈希原子写入数据目录。"""

import json
import os
import sys
from getpass import getpass
from pathlib import Path
from tempfile import NamedTemporaryFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.auth import hash_password
from app.config import load_settings


def main() -> None:
    directory = load_settings().data_dir
    password = getpass("新密码：")
    if not password:
        raise SystemExit("密码不能为空")
    if password != getpass("再次输入："):
        raise SystemExit("两次密码不同")
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    path = directory / "auth.json"
    f = NamedTemporaryFile(mode="w", encoding="utf-8", dir=directory, delete=False)
    tmp = Path(f.name)
    try:
        with f:
            json.dump({"password_hash": hash_password(password)}, f)
            f.write("\n")
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)
    print(f"密码哈希已写入 {path}。已运行的服务需要重启以读取新密码。")
    if "CODE_DOJO_PASSWORD_HASH" in os.environ:
        print("当前设置了 CODE_DOJO_PASSWORD_HASH，服务会优先使用环境变量。")


if __name__ == "__main__":
    main()
