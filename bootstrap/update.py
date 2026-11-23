"""校验更新包，在同一文件系统准备不可变版本，原子切换当前版本指针。"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from http.client import HTTPException
from pathlib import Path, PurePosixPath
from urllib.error import HTTPError, URLError
from zipfile import BadZipFile, ZipFile

from . import VERSION
from .github import GitHub


def version(value: str) -> tuple[int, ...]:
    if not re.fullmatch(r"\d+(?:\.\d+){0,2}", value):
        raise ValueError("版本号无效")
    return tuple(int(n) for n in (value.split(".") + ["0", "0"])[:3])


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def atomic_json(path: Path, obj: dict, *, private: bool = False) -> None:
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        tmp = Path(stream.name)
        try:
            if private and os.name == "posix":
                os.fchmod(stream.fileno(), 0o600)
                if os.fstat(stream.fileno()).st_mode & 0o077:
                    raise PermissionError("此数据目录无法设置 600 权限，令牌仅用于本次运行")
            stream.write(json.dumps(obj, ensure_ascii=False).encode())
            stream.flush()
            os.fsync(stream.fileno())
        except BaseException:
            stream.close()
            tmp.unlink()
            raise
    try:
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


@dataclass(frozen=True)
class Installed:
    root: Path
    manifest: dict
    updated: str


@dataclass
class Result:
    active: Installed | None
    message: str = ""
    installer: str = ""


class Updates:
    def __init__(self, directory: Path, bundle: Path, github: GitHub):
        self.root = directory / "desktop"
        self.root.mkdir(parents=True, exist_ok=True)
        self.bundle = bundle
        self.github = github
        self.pointer = self.root / "current.json"

    def current(self) -> Installed | None:
        if not self.pointer.exists():
            return None
        state = json.loads(self.pointer.read_bytes())
        if not re.fullmatch(r"[0-9a-f]{64}", state["digest"]):
            raise ValueError("本地版本指针无效")
        root = self.root / state["digest"]
        return Installed(root, json.loads((root / "manifest.json").read_bytes()), state["updated"])

    def activate(self, item: Installed) -> None:
        prior = self.current()
        if prior == item:
            return
        atomic_json(self.pointer, {"digest": item.root.name, "updated": item.updated})
        for path in self.root.iterdir():
            if (re.fullmatch(r"[a-f0-9]{64}", path.name) and path != item.root
                    and (not prior or path != prior.root) and path.is_dir() and not path.is_symlink()):
                shutil.rmtree(path, ignore_errors=True)

    def libraries(self, manifest: dict) -> Path:
        return self.root / "dependencies" / manifest["lock_sha256"]

    def prepare_dependencies(self, stage: Path, manifest: dict) -> None:
        if digest(stage / "server/uv.lock") != manifest["lock_sha256"]:
            raise ValueError("依赖锁哈希不符")
        target = self.libraries(manifest)
        if target.is_dir():
            return
        target.parent.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=target.parent) as tmp:
            libraries = Path(tmp) / "libraries"
            if manifest["lock_sha256"] == (self.bundle / "lock.sha256").read_text().strip():
                # 解压新版安装包会替换内置依赖；本地旧题库仍须能离线启动。
                shutil.copytree(self.bundle / "libraries", libraries)
            else:
                subprocess.run([sys.executable, "-I", "-B", "-m", "pip", "--isolated", "install",
                                "--no-cache-dir", "--require-hashes", "--only-binary=:all:",
                                "--target", str(libraries), "-r", str(stage / "requirements.txt")],
                               check=True, timeout=600, stdout=subprocess.DEVNULL,
                               env=os.environ | {"TMPDIR": tmp, "TEMP": tmp, "TMP": tmp})
            libraries.rename(target)

    def check(self, progress=lambda message: None) -> Result:
        old = self.current()
        if not self.github.token:
            return Result(old, "请在设置中填写令牌以开启更新和同步")
        try:
            release = self.github.json("/releases/tags/payload-latest")
            assets = {a["name"]: f"/releases/assets/{int(a['id'])}" for a in release["assets"]}
            with self.github.open(assets["manifest.json"], "application/octet-stream") as response:
                manifest = json.load(response)
            checksum = manifest.pop("payload_sha256")
            if not re.fullmatch(r"[0-9a-f]{64}", checksum):
                raise ValueError("更新包哈希无效")
            if not all(isinstance(manifest.get(k), str) and manifest[k] for k in
                       ("version", "commit", "built_at", "min_bootstrap", "problem_format", "lock_sha256")):
                raise ValueError("更新包清单缺少版本信息")
            if version(manifest["min_bootstrap"]) > version(VERSION):
                repo = self.github.base.rsplit("/repos/", 1)[1]
                return Result(old, "请下载新版安装包", f"https://github.com/{repo}/releases/latest")
            if old and old.root.name == checksum:
                return Result(old)
            final = self.root / checksum
            with tempfile.TemporaryDirectory(dir=self.root) as temporary:
                stage = Path(temporary) / "payload"
                archive = Path(temporary) / "payload.zip"
                with self.github.open(assets["payload.zip"], "application/octet-stream") as source, archive.open("wb") as output:
                    size = int(getattr(source, "headers", {}).get("Content-Length", 0))
                    received = 0
                    last = -1
                    progress("正在下载题库…")
                    while chunk := source.read(1024 * 1024):
                        output.write(chunk)
                        received += len(chunk)
                        percent = min(100, received * 100 // size) if size else 0
                        if size and percent != last:
                            last = percent
                            progress(f"下载题库 {percent}%")
                if digest(archive) != checksum:
                    raise ValueError("更新包 SHA-256 校验失败")
                with ZipFile(archive) as package:
                    for name in package.namelist():
                        path = PurePosixPath(name)
                        if path.is_absolute() or ".." in path.parts or "\\" in name or ":" in name:
                            raise ValueError("更新包内的路径无效")
                    package.extractall(stage)
                if manifest != json.loads((stage / "manifest.json").read_bytes()):
                    raise ValueError("更新包清单不一致")
                for name in ("server/app/main.py", "judge/python/harness.py", "web/dist/index.html",
                             "requirements.txt", "problems", "sql-cache"):
                    if not (stage / name).exists():
                        raise ValueError(f"更新包缺少 {name}")
                progress("准备运行环境…")
                self.prepare_dependencies(stage, manifest)
                if not final.exists():
                    stage.rename(final)
            active = Installed(final, manifest, datetime.now(timezone.utc).isoformat(timespec="seconds"))
            return Result(active)
        except HTTPError as exc:
            return Result(old, f"无法读取更新（HTTP {exc.code}），请检查网络和令牌")
        except URLError:
            return Result(old, "更新失败：无法连接 GitHub，请检查网络")
        except (OSError, HTTPException, ValueError, KeyError, TypeError, BadZipFile, subprocess.SubprocessError):
            return Result(old, "更新包校验或安装失败，请检查下载内容和本机磁盘空间")
