# /// script
# requires-python = ">=3.12"
# dependencies = ["cryptography==50.0.2"]
# ///
"""在发布者本机校验、加密令牌，把密文通过标准输入交给已登录的 gh。"""

import argparse
import getpass
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from bootstrap import DEFAULT_REPO, DEFAULT_SYNC
from bootstrap.github import repository, verify_tokens
from bootstrap.sealed import seal


def read_env(path: Path, keys: list[str], password_key: str | None) -> tuple[dict[str, str], str | None]:
    if len(keys) != 2 or len(set(keys)) != 2 or not all(re.fullmatch(r"[A-Za-z_]\w*", k) for k in keys):
        raise ValueError("--keys 需要两个不同的变量名，用逗号分开")
    if password_key is not None and (not re.fullmatch(r"[A-Za-z_]\w*", password_key) or password_key in keys):
        raise ValueError("--password-key 需要单独的密码变量名")
    found = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        key, sep, raw = line.strip().removeprefix("export ").partition("=")
        key = key.strip()
        if not sep or (key not in keys and key != password_key):
            continue
        if key != password_key or raw.lstrip().startswith(('"', "'")):
            try:
                parts = shlex.split(raw, comments=True)
            except ValueError:
                parts = []
            if len(parts) != 1:
                raise ValueError(f"{key} 的值或引号无效")
            value = parts[0]
        else:
            # 值中间的井号属于密码；空白后的井号引出行尾注释。
            value = re.split(r"\s+#", raw, maxsplit=1)[0].strip()
        if key in keys and (not value or any(c.isspace() for c in value)):
            raise ValueError(f"{key} 的令牌格式无效")
        found[key] = value
    if any(k not in found for k in keys):
        raise ValueError(".env 缺少所需的令牌变量")
    password = None
    if password_key is not None:
        if password_key not in found:
            raise ValueError(".env 缺少指定的密码变量")
        password = found[password_key]
        if len(password) < 10:
            raise ValueError("密码太短，至少需要 10 个字符")
    return {"code": found[keys[0]], "sync": found[keys[1]]}, password


def ask_password() -> str:
    while True:
        password = getpass.getpass("设置解锁密码（至少 10 个字符）：")
        if len(password) < 10:
            print("密码太短，请重新输入。")
        elif getpass.getpass("再次输入解锁密码：") != password:
            print("两次密码不同，请重新输入。")
        else:
            return password


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env", type=Path, default=ROOT / "../../.env")
    parser.add_argument("--keys", default="code_dojo,code_dojo_sync")
    parser.add_argument("--password-key", help="从同一份 .env 读取解锁密码的变量名")
    parser.add_argument("--repo", default=DEFAULT_REPO, help="保存 Actions 密钥的仓库")
    parser.add_argument("--out", type=Path, help="另存密文；只生成时默认 sealed-tokens.json")
    parser.add_argument("--no-upload", action="store_true")
    args = parser.parse_args(argv)
    try:
        destination = repository(args.repo)
        output = args.out or (Path("sealed-tokens.json") if args.no_upload else None)
        if output and output.resolve() == args.env.resolve():
            raise ValueError("输出文件不能覆盖 .env")
        values, password = read_env(args.env, [k.strip() for k in args.keys.split(",")], args.password_key)
        print("已读取 2 个令牌", flush=True)
        verify_tokens(values, DEFAULT_REPO, DEFAULT_SYNC)
        if password is None:
            password = ask_password()
        sealed = json.dumps(seal(values, password, DEFAULT_REPO, DEFAULT_SYNC), separators=(",", ":"))
        if output:
            output.write_text(sealed + "\n", encoding="utf-8")
            print("已保存加密文件。")
        if not args.no_upload:
            try:
                subprocess.run(["gh", "secret", "set", "CODE_DOJO_SEALED_TOKENS", "--repo", destination],
                               input=sealed.encode(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                               check=True)
            except (OSError, subprocess.SubprocessError):
                raise ValueError("上传失败，请确认已安装并登录 gh，而且有权设置仓库的 Actions 密钥。") from None
            print("已上传 Actions 密钥。")
    except (ValueError, OSError, EOFError, KeyboardInterrupt) as exc:
        print(str(exc) if isinstance(exc, ValueError) else "操作未完成，请检查输入文件、输出目录和终端。", file=sys.stderr)
        return 1
    print("可以删除或妥善保管 .env。")
    if args.no_upload:
        print("发布前需上传密文，然后打新的 app-v* 标签重新构建安装包。")
    else:
        print("下一步：打新的 app-v* 标签，重新构建安装包。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
