"""下载更新包，在同一文件系统准备不可变版本，原子切换当前版本指针。"""

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
        self.next = self.root / "next.json"  # 后台下载好、还没启动过的新版本，下次打开先试它

    def _read(self, pointer: Path) -> Installed | None:
        if not pointer.exists():
            return None
        state = json.loads(pointer.read_bytes())
        if not re.fullmatch(r"[0-9a-f]{64}", state["digest"]):
            raise ValueError("本地版本指针无效")
        root = self.root / state["digest"]
        return Installed(root, json.loads((root / "manifest.json").read_bytes()), state["updated"])

    def current(self) -> Installed | None:
        return self._read(self.pointer)

    def staged(self) -> Installed | None:
        return self._read(self.next)

    def stage(self, item: Installed) -> None:
        atomic_json(self.next, {"digest": item.root.name, "updated": item.updated})

    def clean(self) -> None:
        """后台下载或装依赖到一半就退出时（守护线程直接结束）留下的临时目录。只在起服务之前调用。"""
        for parent in (self.root, self.root / "dependencies"):
            for path in parent.glob("tmp*"):
                if re.fullmatch(r"tmp[a-z0-9_]{8}", path.name):
                    shutil.rmtree(path, ignore_errors=True)

    def activate(self, item: Installed) -> None:
        # 换到任何版本都作废待试的版本；下面清理旧目录时它也可能被删掉。
        self.next.unlink(missing_ok=True)
        prior = self.current()
        if prior == item:
            return
        atomic_json(self.pointer, {"digest": item.root.name, "updated": item.updated})
        for path in self.root.iterdir():
            if (re.fullmatch(r"[a-f0-9]{64}", path.name) and path != item.root
                    and (not prior or path != prior.root) and path.is_dir() and not path.is_symlink()):
                shutil.rmtree(path, ignore_errors=True)

    def libraries(self, manifest: dict) -> Path:
        # 和安装包同一份依赖锁时直接用随包依赖，不复制（Windows 上复制两千多个文件要被 Defender 逐个扫描）。
        # 换了依赖不同的新安装包又恰好离线时，旧更新包会缺依赖起不来；联网更新一次即可，不为此常驻一份副本。
        if manifest["lock_sha256"] == (self.bundle / "lock.sha256").read_text().strip():
            return self.bundle / "libraries"
        return self.root / "dependencies" / manifest["lock_sha256"]

    def prepare_dependencies(self, stage: Path, manifest: dict) -> None:
        target = self.libraries(manifest)
        if target.is_dir():
            return
        target.parent.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=target.parent) as tmp:
            libraries = Path(tmp) / "libraries"
            subprocess.run([sys.executable, "-I", "-B", "-m", "pip", "--isolated", "install",
                            "--no-cache-dir", "--require-hashes", "--only-binary=:all:",
                            "--target", str(libraries), "-r", str(stage / "requirements.txt")],
                           check=True, timeout=600, stdout=subprocess.DEVNULL,
                           env=os.environ | {"TMPDIR": tmp, "TEMP": tmp, "TMP": tmp})
            libraries.rename(target)

    def check(self, progress=lambda message: None) -> Result:
        old = self.current()
        try:
            release = self.github.json("/releases/tags/payload-latest")
            assets = {a["name"]: f"/releases/assets/{int(a['id'])}" for a in release["assets"]}
            with self.github.open(assets["manifest.json"], "application/octet-stream") as response:
                manifest = json.load(response)
            # payload_sha256 只当这个更新包的 ID 和目录名用，下载后不再对 zip 算哈希核对。
            checksum = manifest.pop("payload_sha256")
            if not all(isinstance(manifest.get(k), str) and manifest[k] for k in
                       ("version", "commit", "built_at", "min_bootstrap", "problem_format", "lock_sha256")):
                raise ValueError("更新包清单缺少版本信息")
            if version(manifest["min_bootstrap"]) > version(VERSION):
                repo = self.github.base.rsplit("/repos/", 1)[1]
                return Result(old, "请下载新版安装包", f"https://github.com/{repo}/releases/latest")
            if old and old.root.name == checksum:
                return Result(old)
            final = self.root / checksum
            if final.is_dir():
                # 之前已下载解压并准备好依赖（例如后台下载后等待下次启动），不再重复下载。
                return Result(Installed(final, manifest, datetime.now(timezone.utc).isoformat(timespec="seconds")))
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
                with ZipFile(archive) as package:
                    for name in package.namelist():
                        path = PurePosixPath(name)
                        if path.is_absolute() or ".." in path.parts or "\\" in name or ":" in name:
                            raise ValueError("更新包内的路径无效")
                    package.extractall(stage)
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
            return Result(old, f"无法读取更新（HTTP {exc.code}），请稍后重试")
        except URLError:
            return Result(old, "更新失败：无法连接 GitHub，请检查网络")
        except (OSError, HTTPException, ValueError, KeyError, TypeError, BadZipFile, subprocess.SubprocessError):
            return Result(old, "更新包校验或安装失败，请检查下载内容和本机磁盘空间")
