"""从受控文件清单生成运行时安装包和可独立发布的更新包。"""

import argparse
import json
import os
import platform
import plistlib
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
from bootstrap.update import digest

PBS = "20261026"
PYTHON = "3.14.10"
TARGETS = {
    ("Linux", "x86_64"): ("x86_64-unknown-linux-gnu", "1b38024924eb7f4cf0cab45d7b871d1f1991354190fccd2625ac7529a43786e2"),
    ("Darwin", "arm64"): ("aarch64-apple-darwin", "30a18bcb9ab75e485b4bf4e5d783dde165571e7e42c56dff47a2d2c5345183a4"),
    ("Windows", "amd64"): ("x86_64-pc-windows-msvc", "98bbe6a0d798bcbad142e96e5930a330e4dc407638e898b515c51eb73a27580d"),
}


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
        for rel in ("scripts/curriculum/check_curve.py", "scripts/curriculum/track_files.py", "server/uv.lock"):
            zipfile.write(ROOT / rel, rel)
        for path in sorted((work / "sql-cache").glob("*.json")):
            zipfile.write(path, path.relative_to(work))
        zipfile.write(work / "requirements.txt", "requirements.txt")
        zipfile.writestr("manifest.json", json.dumps(manifest))
    manifest["payload_sha256"] = digest(archive)
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def shell_launcher(path: Path, app: bool) -> None:
    location = "../Resources" if app else "."
    path.parent.mkdir(exist_ok=True, parents=True)
    path.write_text('#!/bin/sh\nset -eu\nbase=$(CDPATH= cd -- "$(dirname "$0")/' + location
                    + '" && pwd)\nexec "$base/python/bin/python3" -I -B "$base/start.py" "$@"\n', encoding="utf-8")
    path.chmod(0o755)


def installer(args, work: Path) -> None:
    sealed = os.environ.pop("CODE_DOJO_SEALED_TOKENS", "")
    system = platform.system()
    target, expected = TARGETS[system, platform.machine().lower()]
    title = f"code-dojo-{VERSION}-{target}"
    outer = work / ("code-dojo.app" if system == "Darwin" else "code-dojo")
    bundle = outer / "Contents/Resources" if system == "Darwin" else outer
    bundle.mkdir(parents=True)
    source = args.runtime_archive
    if not source:
        source = work / "runtime.tar.gz"
        name = f"cpython-{PYTHON}%2B{PBS}-{target}-install_only.tar.gz"
        subprocess.run(["curl", "--fail", "--location", "--retry", "3", "--output", str(source),
                        f"https://github.com/astral-sh/python-build-standalone/releases/download/{PBS}/{name}"], check=True)
    if digest(source) != expected:
        raise ValueError("独立 Python 解释器哈希不符")
    with tarfile.open(source) as tar:
        tar.extractall(bundle, filter="data")
    python = bundle / ("python/python.exe" if system == "Windows" else "python/bin/python3")
    subprocess.run([str(python), "-I", "-c", "import tkinter, pip; w=tkinter.Tk(); w.withdraw(); "
                    "print('Tk', w.tk.call('package','provide','Tk')); w.destroy()"], check=True)
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
    shutil.copytree(ROOT / "bootstrap", bundle / "bootstrap", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy(Path(__file__).with_name("start.py"), bundle)
    if sealed:
        (bundle / "sealed-tokens.json").write_text(sealed, encoding="utf-8")
    # 用独立解释器实测当前平台的加密库，以及可选信封的版本与结构。
    subprocess.run([str(python), "-I", "-B", "-c",
                    "import json, sys; from pathlib import Path; sys.path[:0] = ['.', 'libraries']; "
                    "from bootstrap.sealed import unpack; p = Path('sealed-tokens.json'); "
                    "unpack(json.loads(p.read_bytes())) if p.exists() else None"], cwd=bundle, check=True)
    if system == "Windows":
        native = work / "native"
        subprocess.run(["cmake", "-S", str(Path(__file__).parent), "-B", str(native), "-A", "x64"], check=True)
        subprocess.run(["cmake", "--build", str(native), "--config", "Release"], check=True)
        shutil.copy(native / "Release/code-dojo.exe", outer)
        shutil.make_archive(str(args.output / title), "zip", work, outer.name)
    elif system == "Darwin":
        shell_launcher(outer / "Contents/MacOS/code-dojo", True)
        with (outer / "Contents/Info.plist").open("wb") as file:
            plistlib.dump(dict(CFBundleExecutable="code-dojo", CFBundleIdentifier="local.code-dojo.desktop",
                               CFBundleName="code-dojo", CFBundlePackageType="APPL",
                               CFBundleShortVersionString=VERSION, CFBundleVersion=VERSION), file)
        subprocess.run(["ditto", "-c", "-k", "--sequesterRsrc", "--keepParent", str(outer),
                        str(args.output / (title + ".zip"))], check=True)
    else:
        shell_launcher(outer / "code-dojo", False)
        with tarfile.open(args.output / (title + ".tar.gz"), "w:gz", compresslevel=5) as tar:
            def permissions(entry):
                # 构建目录可能位于不保存 Unix 权限的共享盘。
                entry.mode = 0o755 if entry.isdir() or "/bin/" in entry.name or entry.name == "code-dojo/code-dojo" else 0o644
                return entry
            tar.add(outer, arcname=outer.name, filter=permissions)


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
