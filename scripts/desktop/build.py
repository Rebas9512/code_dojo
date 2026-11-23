"""从受控文件清单生成运行时安装包和可独立发布的更新包。"""

import argparse
import hashlib
import importlib.util
import json
import os
import platform
import py_compile
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from bootstrap import MIN_BOOTSTRAP, VERSION

PBS = "20261026"
PYTHON = "3.14.10"
TARGETS = {
    ("Linux", "x86_64"): ("x86_64-unknown-linux-gnu", "1b38024924eb7f4cf0cab45d7b871d1f1991354190fccd2625ac7529a43786e2"),
    ("Darwin", "arm64"): ("aarch64-apple-darwin", "30a18bcb9ab75e485b4bf4e5d783dde165571e7e42c56dff47a2d2c5345183a4"),
    ("Windows", "amd64"): ("x86_64-pc-windows-msvc", "98bbe6a0d798bcbad142e96e5930a330e4dc407638e898b515c51eb73a27580d"),
}

APPIMAGETOOL_SHA256 = "ed4ce84f0d9caff66f50bcca6ff6f35aae54ce8135408b3fa33abfc3cb384eb0"
TYPE2_RUNTIME_SHA256 = "2fca8b443c92510f1483a883f60061ad09b46b978b2631c807cd873a47ec260d"


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def download(url: str, path: Path) -> None:
    subprocess.run(["curl", "--fail", "--location", "--retry", "3", "--output", str(path), url], check=True)


def requirements(output: Path) -> None:
    subprocess.run(["uv", "export", "--locked", "--no-dev", "--no-emit-project", "--no-header",
                    "--output-file", str(output)], cwd=ROOT / "server", stdout=subprocess.DEVNULL, check=True)


def payload(args, work: Path) -> None:
    sys.path.insert(0, str(ROOT / "server"))
    from app.problems import ProblemBank
    from app.sql_judge import sql_cases

    bank = ProblemBank(ROOT / "problems")
    bank.refresh(force=True)
    if bank.errors:
        raise ValueError(f"题库加载失败：{bank.errors}")
    problems = [p for p in bank.ordered() if not p.inspect and p.track.language == "sql"]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for _ in pool.map(lambda p: sql_cases(p, work, all_cases=True), problems):
            pass
    print(f"SQL 期望结果：{len(problems)} 题，{len(list((work / 'sql-cache').glob('*.json')))} 份", flush=True)
    requirements(work / "requirements.txt")
    lock = ROOT / "server/uv.lock"
    header = (ROOT / "docs/problem-format.md").read_text(encoding="utf-8").splitlines()[0]
    fmt = re.fullmatch(r"# 题目格式规范 v([\d.]+)", header)
    if not fmt:
        raise ValueError("题目格式文档缺少版本")
    manifest = dict(version=args.version, commit=args.sha, built_at=datetime.now(timezone.utc).isoformat(),
                    min_bootstrap=MIN_BOOTSTRAP, problem_format=fmt[1], lock_sha256=digest(lock))
    archive = args.output / "payload.zip"
    with ZipFile(archive, "w", ZIP_DEFLATED) as zipfile:
        for rel in ("server/app", "judge/python", "judge/ds", "problems", "web/dist"):
            for path in sorted((ROOT / rel).rglob("*")):
                if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
                    continue
                if rel.startswith("judge/") and path.suffix != ".py":
                    continue
                if path == ROOT / "web/dist/index.html":
                    html = path.read_text(encoding="utf-8").replace("<head>", '<head><meta name="code-dojo-desktop">')
                    zipfile.writestr("web/dist/index.html", html)
                else:
                    zipfile.write(path, path.relative_to(ROOT))
        if "web/dist/index.html" not in zipfile.namelist():
            raise ValueError("缺少 web/dist，请先构建网页")
        # 后端以 -B 运行、不写字节码；附上不查源码的 .pyc，启动时不用再编译（更新包目录内容不会变）。
        for path in sorted((ROOT / "server/app").rglob("*.py")):
            rel = path.relative_to(ROOT)
            cfile = work / "pyc" / rel
            py_compile.compile(str(path), cfile=str(cfile), dfile=str(rel), doraise=True,
                               invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH)
            zipfile.write(cfile, importlib.util.cache_from_source(str(rel)))
        for rel in ("scripts/curriculum/check_curve.py", "scripts/curriculum/track_files.py", "server/uv.lock"):
            zipfile.write(ROOT / rel, rel)
        for path in sorted((work / "sql-cache").glob("*.json")):
            zipfile.write(path, path.relative_to(work))
        zipfile.write(work / "requirements.txt", "requirements.txt")
        zipfile.writestr("manifest.json", json.dumps(manifest))
    manifest["payload_sha256"] = digest(archive)
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def appimage(bundle: Path, output: Path) -> None:
    work = bundle.parent
    # 很多发行版禁止普通程序建用户命名空间（Ubuntu 23.10+ 的 AppArmor、Debian 的 unprivileged_userns_clone 等），
    # AppImage 里的 chrome-sandbox 又不可能归 root，Chromium 沙箱起不来会直接退出。逐个判断容易漏，
    # 和 Obsidian、LM Studio 一样一律带 --no-sandbox（用户 2026-11-23 定）。
    # 只用 shell 内建：APPDIR 由 AppImage 运行时设置（含 --appimage-extract-and-run），PATH 可能是空的。
    apprun = bundle / "AppRun"
    apprun.write_text('#!/bin/sh\nexec "${APPDIR:-${0%/*}}/code-dojo" --no-sandbox "$@"\n', encoding="utf-8")
    apprun.chmod(0o755)
    shutil.copy(Path(__file__).with_name("code-dojo.png"), bundle)
    shutil.copy(Path(__file__).with_name("code-dojo.desktop"), bundle)
    shutil.copy(ROOT / "web/public/code-dojo.svg", bundle)
    (bundle / ".DirIcon").symlink_to("code-dojo.png")
    for size, ext in (("256x256", "png"), ("scalable", "svg")):
        icons = bundle / "usr/share/icons/hicolor" / size / "apps"
        icons.mkdir(parents=True)
        icon = bundle / f"code-dojo.{ext}"
        installed = icons / icon.name
        icon.rename(installed)
        icon.symlink_to(installed.relative_to(bundle))

    tool = work / "appimagetool-x86_64.AppImage"
    runtime = work / "runtime-x86_64"
    # 打包工具默认会另取最新的挂载运行时；两份上游二进制都固定且分别校验。
    for repo, tag, path, checksum in (
        ("appimagetool", "1.9.1", tool, APPIMAGETOOL_SHA256),
        ("type2-runtime", "20251108", runtime, TYPE2_RUNTIME_SHA256),
    ):
        download(f"https://github.com/AppImage/{repo}/releases/download/{tag}/{path.name}", path)
        if digest(path) != checksum:
            raise ValueError(f"{path.name} 的 SHA-256 不符")
    tool.chmod(0o755)
    # Lite 2.2 的菜单库只读 gzip/xz。官方工具随附的 mksquashfs 只支持 zstd，
    # 用无需 FUSE 的方式解开工具，再让原版 CLI 从 PATH 找到系统的压缩器。
    if not shutil.which("mksquashfs"):
        raise RuntimeError("构建 Linux AppImage 需要 squashfs-tools 提供的 mksquashfs")
    env = os.environ | {"ARCH": "x86_64", "VERSION": VERSION, "TMPDIR": str(work)}
    subprocess.run([str(tool), "--appimage-extract-and-run", "--version"], cwd=work, check=True,
                   env=env | {"NO_CLEANUP": "1"})
    cli, = work.glob("appimage_extracted_*/usr/bin/appimagetool")
    env["PATH"] += os.pathsep + str(cli.parent)
    image = work / f"code-dojo-{VERSION}-x86_64.AppImage"
    subprocess.run([str(cli), "--runtime-file", str(runtime), "--comp", "gzip",
                    str(bundle), str(image)], cwd=work, check=True, env=env)
    image.replace(output / image.name)


def installer(args, work: Path) -> None:
    sealed = os.environ.pop("CODE_DOJO_SEALED_TOKENS", "")
    system = platform.system()
    target, expected = TARGETS[system, platform.machine().lower()]
    bundle = work / "runtime"
    bundle.mkdir(parents=True)
    source = args.runtime_archive
    if not source:
        source = work / "runtime.tar.gz"
        name = f"cpython-{PYTHON}%2B{PBS}-{target}-install_only.tar.gz"
        download(f"https://github.com/astral-sh/python-build-standalone/releases/download/{PBS}/{name}", source)
    if digest(source) != expected:
        raise ValueError("独立 Python 解释器哈希不符")
    with tarfile.open(source) as tar:
        tar.extractall(bundle, filter="data")
    python = bundle / ("python/python.exe" if system == "Windows" else "python/bin/python3")
    (work / "job.json").write_text(json.dumps({"mode": "stdio", "cases": [{"expected": "42"}]}))
    (work / "user.py").write_text("print(6 * 7)")
    run = subprocess.run([str(python), "-I", "-B", "-X", "utf8", str(ROOT / "judge/python/harness.py"),
                          "job.json", "268435456"], cwd=work, capture_output=True, encoding="utf-8", check=True)
    if json.loads(run.stdout.split("@@CODE_DOJO_RESULT@@")[-1])["verdict"] != "accepted":
        raise ValueError("内置 Python 判题子进程自检失败")
    requirements(work / "requirements.txt")
    subprocess.run([str(python), "-I", "-m", "pip", "--isolated", "install", "--no-cache-dir",
                    "--only-binary=:all:", "--require-hashes", "--target", str(bundle / "libraries"),
                    "-r", str(work / "requirements.txt")], check=True)
    (bundle / "lock.sha256").write_text(digest(ROOT / "server/uv.lock"), encoding="ascii")
    shutil.copytree(ROOT / "bootstrap", bundle / "bootstrap", ignore=shutil.ignore_patterns("__pycache__", "tests"))
    shutil.copy(Path(__file__).with_name("start.py"), bundle)
    # electron-builder 复制文件会改修改时间，按时间戳校验的 .pyc 全部失效，启动器和后端每次启动都在重新编译
    # 标准库和依赖。安装包只读、源码不变，统一改成不查源码的哈希式 .pyc（实测导入共省约 0.5 秒）。
    subprocess.run([str(python), "-I", "-m", "compileall", "-q", "-f", "-j0", "--invalidation-mode", "unchecked-hash",
                    str(bundle / "python"), str(bundle / "libraries"), str(bundle / "bootstrap")], check=True)
    if sealed:
        (bundle / "sealed-tokens.json").write_text(sealed, encoding="utf-8")
    # 用独立解释器实测当前平台的加密库，以及可选信封的版本与结构。
    subprocess.run([str(python), "-I", "-B", "-c",
                    "import json, sys; from pathlib import Path; sys.path[:0] = ['.', 'libraries']; "
                    "from bootstrap.sealed import unpack; p = Path('sealed-tokens.json'); "
                    "unpack(json.loads(p.read_bytes())) if p.exists() else None"], cwd=bundle, check=True)
    desktop = ROOT / "desktop"
    builder = desktop / "node_modules/electron-builder/cli.js"
    output = work / "electron"
    env = os.environ | {"CODE_DOJO_RESOURCES": str(bundle), "CSC_IDENTITY_AUTO_DISCOVERY": "false"}
    subprocess.run(["node", str(builder), "--config", "builder.cjs", "--publish", "never",
                    f"--config.directories.output={output}"], cwd=desktop, env=env, check=True)
    if system == "Linux":
        # 继续使用已验证的 Lite 兼容入口和 gzip 运行时，直接启动带沙箱的 Electron。
        appimage(output / "linux-unpacked", args.output)
    for asset in output.glob("code-dojo-*"):
        if asset.is_file() and asset.name.endswith((".zip", ".tar.gz")):
            asset.replace(args.output / asset.name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    sub = parser.add_subparsers(dest="kind", required=True)
    app = sub.add_parser("app")
    app.add_argument("--runtime-archive", type=Path)
    pack = sub.add_parser("payload")
    pack.add_argument("--sha", required=True)
    pack.add_argument("--version", required=True)
    args = parser.parse_args()
    args.output = args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=args.output) as tmp:
        (installer if args.kind == "app" else payload)(args, Path(tmp))
