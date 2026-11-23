"""AI 接入层：统一成"系统提示 + 内容 + JSON schema → 结构化结果"。

默认实现走 Claude Code 的无交互模式（`claude -p`），用本机登录的 Claude 订阅，不需要 API key。
固定参数：关掉所有工具、不读用户 / 项目设置、不加载 MCP、不保存会话，在专用空目录里运行，
环境变量只留平台所需的用户目录、命令路径、语言设置和可选的订阅登录令牌。
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import threading
from pathlib import Path
from typing import Any, Callable, Protocol


class AIError(RuntimeError):
    pass


class AIProvider(Protocol):
    def complete(self, *, system: str, prompt: str, schema: dict[str, Any], effort: str = "low") -> dict[str, Any]:
        ...


class ClaudeCodeProvider:
    def __init__(
        self,
        binary: str = "claude",
        model: str = "claude-opus-5-5",
        workdir: Path | None = None,
        timeout_s: float = 180,
        concurrency: int = 2,
    ):
        self.binary = binary
        self.model = model
        self.workdir = workdir or Path(tempfile.gettempdir()) / "code-dojo-ai"
        self.timeout_s = timeout_s
        self._slots = threading.BoundedSemaphore(concurrency)

    def complete(self, *, system: str, prompt: str, schema: dict[str, Any], effort: str = "low") -> dict[str, Any]:
        self.workdir.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", suffix=".md", dir=self.workdir, delete=False, encoding="utf-8") as f:
            f.write(system)
            system_path = f.name
        cmd = [
            shutil.which(self.binary) or self.binary, "-p",
            "--output-format", "json",
            "--json-schema", json.dumps(schema, ensure_ascii=False),
            "--tools", "",
            "--system-prompt-file", system_path,
            "--setting-sources", "",
            "--strict-mcp-config",
            "--no-session-persistence",
            "--model", self.model,
            "--effort", effort,
        ]
        keys = ("HOME", "PATH", "LANG", "CLAUDE_CODE_OAUTH_TOKEN")
        if os.name == "nt":
            keys += ("USERPROFILE", "APPDATA", "LOCALAPPDATA", "SystemRoot", "TEMP", "TMP", "ComSpec", "PATHEXT")
        env = {k: os.environ[k] for k in keys if k in os.environ}
        env.setdefault("LANG", "C.UTF-8")
        try:
            with self._slots:
                proc = subprocess.run(
                    cmd, input=prompt, capture_output=True, encoding="utf-8",
                    cwd=self.workdir, env=env, timeout=self.timeout_s,
                )
        except FileNotFoundError as exc:
            raise AIError(f"找不到 Claude Code 命令 {self.binary}") from exc
        except subprocess.TimeoutExpired as exc:
            raise AIError(f"AI 超过 {self.timeout_s:.0f} 秒没有回复") from exc
        finally:
            Path(system_path).unlink(missing_ok=True)
        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            tail = (proc.stderr or proc.stdout)[-500:]
            raise AIError(f"AI 返回的不是 JSON（退出码 {proc.returncode}）：{tail}") from exc
        if data.get("is_error"):
            raise AIError(str(data.get("result") or "AI 调用失败"))
        out = data.get("structured_output")
        if not isinstance(out, dict):
            raise AIError("AI 没有按格式返回结构化结果")
        return out


class FakeProvider:
    """测试用：按顺序返回预先给定的结果（或由函数根据 prompt 生成）。"""

    def __init__(self, responses: list[dict[str, Any]] | Callable[[str, str], dict[str, Any]]):
        self.responses = responses
        self.calls: list[dict[str, str]] = []

    def complete(self, *, system: str, prompt: str, schema: dict[str, Any], effort: str = "low") -> dict[str, Any]:
        self.calls.append({"system": system, "prompt": prompt, "effort": effort})
        if callable(self.responses):
            return self.responses(system, prompt)
        if not self.responses:
            raise AIError("FakeProvider 没有更多预设回复")
        return self.responses.pop(0)
