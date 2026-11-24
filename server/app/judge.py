"""Python 判题：本机专用解释器和 Docker 容器使用同一份用例和判题程序。"""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import threading
import uuid
from pathlib import Path
from typing import Any

from .config import Settings
from .local_judge import LocalEnvironments, PreparationError, run_local

RESULT_MARK = "@@CODE_DOJO_RESULT@@"
STARTUP_ALLOWANCE_S = 8  # 容器启动等开销


class Judge:
    def __init__(self, image: str, tmp_root: Path, concurrency: int = 2, *,
                 mode: str = "docker", envs: Path | None = None,
                 ds_image: str = "code-dojo-judge-ds:3.14", ds_memory: str = "1g", ds_time_limit_ms: int = 10000):
        self.image = image
        self.ds_image = ds_image
        self.ds_memory = ds_memory
        self.ds_time_limit_ms = ds_time_limit_ms
        self.tmp_root = tmp_root
        self._slots = threading.BoundedSemaphore(concurrency)
        self.local = LocalEnvironments(envs or tmp_root / "judge-envs")
        self.backends = {
            runtime: ("docker" if self.image_present(runtime) else "local") if mode == "auto" else mode
            for runtime in ("python", "ds")
        }

    @classmethod
    def from_settings(cls, settings: Settings, concurrency: int | None = None) -> Judge:
        return cls(settings.judge_image, settings.judge_tmp, concurrency or settings.judge_concurrency,
                   mode=settings.judge_mode, envs=settings.judge_envs,
                   ds_image=settings.ds_image, ds_memory=settings.ds_memory, ds_time_limit_ms=settings.ds_time_limit_ms)

    def image_for(self, runtime: str) -> str:
        return {"python": self.image, "ds": self.ds_image}[runtime]

    def image_present(self, runtime: str = "python") -> bool:
        try:
            out = subprocess.run(
                ["docker", "image", "inspect", self.image_for(runtime)], capture_output=True, timeout=10
            )
            return out.returncode == 0
        except (OSError, subprocess.TimeoutExpired):
            return False

    def run(
        self,
        *,
        mode: str,
        code: str,
        cases: list[dict[str, Any]],
        entry: str | None = None,
        compare: str = "exact",
        convert: dict[str, Any] | None = None,
        runtime: str = "python",
        time_limit_ms: int | None = None,
        constraints: dict | None = None,
        compare_options: dict | None = None,
        checker: str | None = None,
        answer: str | None = None,
        reference: str | None = None,
        data: Path | None = None,
        args: list[str] | None = None,
        log: Path | None = None,
    ) -> dict[str, Any]:
        image = self.image_for(runtime)
        memory = self.ds_memory if runtime == "ds" else "256m"
        if time_limit_ms is None:
            time_limit_ms = self.ds_time_limit_ms if runtime == "ds" else 2000
        job = {
            "runtime": runtime,
            "mode": mode,
            "entry": entry,
            "compare": compare,
            "constraints": constraints,
            "compare_options": compare_options or {},
            "convert": convert,
            "time_limit_ms": time_limit_ms,
            "cases": cases,
            "answer": answer,
            "args": args or [],
        }
        self.tmp_root.mkdir(parents=True, exist_ok=True)
        work = Path(tempfile.mkdtemp(prefix="job-", dir=self.tmp_root))
        local = self.backends[runtime] == "local"
        try:
            if log is not None:
                job["log"] = str(log.resolve()) if local else "/work/project.log"
                if not local:
                    log.chmod(0o666)
                    (work / "project.log").touch()  # 在只读 /work 中预建单文件挂载点
            if data is not None:
                shutil.copytree(data, work / "data")
                (work / "scratch").mkdir(mode=0o777)
                if reference is not None:
                    (work / "reference.py").write_text(reference, encoding="utf-8")
            (work / "job.json").write_text(json.dumps(job, ensure_ascii=False), encoding="utf-8")
            (work / "user.py").write_text(code, encoding="utf-8")
            if checker is not None:
                (work / "checker.py").write_text(checker, encoding="utf-8")
            budget_s = time_limit_ms / 1000 * max(len(cases), 1) + STARTUP_ALLOWANCE_S
            if local:
                python = self.local.interpreter(runtime)
            else:
                work.chmod(0o755)
                for f in work.iterdir():
                    if f.is_file():
                        f.chmod(0o644)
                if data is not None:
                    (work / "scratch").chmod(0o777)
            with self._slots:
                if local:
                    proc = run_local(python, work, budget_s, memory)
                else:
                    proc = self._docker(work, budget_s, image, memory, log)
            return self._result(proc, memory)
        except subprocess.TimeoutExpired:
            return {"verdict": "timeout", "error": f"整体运行超过 {budget_s:.0f} 秒，已终止", "cases": []}
        except (OSError, ValueError, PreparationError) as exc:
            return {"verdict": "system_error", "error": str(exc), "cases": []}
        finally:
            shutil.rmtree(work, ignore_errors=True)

    def _docker(self, work: Path, budget_s: float, image: str, memory: str,
                log: Path | None = None) -> subprocess.CompletedProcess:
        name = f"cdj-{uuid.uuid4().hex[:12]}"
        cmd = [
            "docker", "run", "--rm", "--name", name,
            "--network", "none",
            "--memory", memory, "--memory-swap", memory,
            "--cpus", "1", "--pids-limit", "64",
            "--read-only", "--tmpfs", "/tmp:size=16m",
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--ulimit", "stack=268435456:268435456",
            "-v", f"{work}:/work:ro",
            *(["-v", f"{work}/scratch:/work/scratch:rw"] if (work / "scratch").exists() else []),
            *(["-v", f"{log.resolve()}:/work/project.log:rw"] if log else []),
            image, "/work/job.json",
        ]
        try:
            return subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace", timeout=budget_s)
        except subprocess.TimeoutExpired:
            subprocess.run(["docker", "kill", name], capture_output=True)
            raise

    @staticmethod
    def _result(proc: subprocess.CompletedProcess, memory: str) -> dict[str, Any]:
        for line in reversed(proc.stdout.splitlines()):
            if line.startswith(RESULT_MARK):
                return json.loads(line[len(RESULT_MARK):])
        if proc.returncode in (137, -9):
            return {"verdict": "runtime_error", "error": f"进程被终止：可能超过内存上限 {memory}", "cases": []}
        tail = (proc.stderr or proc.stdout)[-1500:]
        return {"verdict": "system_error", "error": f"判题程序没有返回结果（退出码 {proc.returncode}）\n{tail}", "cases": []}
