"""本机订阅 CLI 的结构化调用、命令发现和测试替身。"""

from __future__ import annotations

import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path
from typing import Any, Callable, Literal, Protocol

from ..config import Settings
from .codex_schema import restore_result, strict_schema

AgentId = Literal["claude", "codex"]


class AIError(RuntimeError):
    pass


class AIProvider(Protocol):
    def complete(self, *, system: str, prompt: str, schema: dict[str, Any], effort: str = "low") -> dict[str, Any]:
        ...


def find_codex(binary: str) -> str | None:
    path = shutil.which(binary)
    if path or os.path.isabs(binary):
        return path
    system = {"darwin": "macos", "win32": "windows"}.get(sys.platform, sys.platform)
    machine = platform.machine().lower()
    arch = {"amd64": "x86_64", "arm64": "aarch64"}.get(machine, machine)
    exe = "codex.exe" if sys.platform == "win32" else "codex"
    extensions = Path.home() / ".vscode/extensions"
    candidates = []
    for folder in extensions.glob("openai.chatgpt-*"):
        match = re.match(r"openai\.chatgpt-(\d+(?:\.\d+)*)", folder.name)
        path = folder / "bin" / f"{system}-{arch}" / exe
        if match and path.is_file() and os.access(path, os.X_OK):
            candidates.append((tuple(map(int, match[1].split("."))), str(path)))
    return max(candidates)[1] if candidates else None


def available_agents(settings: Settings) -> list[dict[str, str]]:
    if settings.ai_provider == "off":
        return []
    agents = []
    if shutil.which(settings.claude_bin):
        agents.append({"id": "claude", "name": "Claude", "model": settings.ai_model})
    if find_codex(settings.codex_bin):
        agents.append({"id": "codex", "name": "Codex", "model": settings.codex_model})
    return sorted(agents, key=lambda agent: agent["id"] != settings.ai_provider)


class CliProvider:
    command: str
    default_model: str
    name: str
    login_env: str
    login_status: str

    def __init__(
        self,
        binary: str | None = None,
        model: str | None = None,
        workdir: Path | None = None,
        timeout_s: float = 180,
        slots: threading.BoundedSemaphore | None = None,
    ):
        self.binary = binary or self.command
        self.model = model or self.default_model
        self.workdir = workdir or Path(tempfile.gettempdir()) / "code-dojo-ai"
        self.timeout_s = timeout_s
        self._slots = slots or threading.BoundedSemaphore(2)  # 应用里由 main 传入，两个助教共用

    def _run(self, cmd: list[str], prompt: str, cwd: Path) -> subprocess.CompletedProcess[str]:
        # HOME 定位用户配置，PATH 查找命令和解释器，LANG 指定语言，USER / LOGNAME 供 macOS 钥匙串识别登录用户。
        # Claude 可用订阅令牌，Codex 用 CODEX_HOME 定位登录配置；Windows 另需用户和应用目录、系统根目录、临时目录、命令解释器和可执行扩展名。
        keys = ("HOME", "PATH", "LANG", "USER", "LOGNAME", self.login_env)
        if os.name == "nt":
            keys += ("USERPROFILE", "APPDATA", "LOCALAPPDATA", "SystemRoot", "TEMP", "TMP", "ComSpec", "PATHEXT")
        env = {k: os.environ[k] for k in keys if k in os.environ}
        env.setdefault("LANG", "C.UTF-8")
        try:
            with self._slots:
                return subprocess.run(
                    cmd, input=prompt, capture_output=True, encoding="utf-8",
                    cwd=cwd, env=env, timeout=self.timeout_s,
                )
        except FileNotFoundError as exc:
            raise AIError(f"找不到 {self.name} 命令 {self.binary}") from exc
        except subprocess.TimeoutExpired as exc:
            raise AIError(f"AI 超过 {self.timeout_s:.0f} 秒没有回复") from exc

    def _cli_error(self, detail: str, fallback: str = "") -> AIError:
        if re.search(r"not (?:logged in|signed in|authenticated)|please (?:log in|run /login)|"
                     r"(?:authentication|login) required|unauthorized", detail, re.IGNORECASE):
            return AIError(f"请在终端运行 {self.login_status} 确认 {self.name} 的登录状态。")
        return AIError(fallback or detail)


class ClaudeCodeProvider(CliProvider):
    command = "claude"
    default_model = "claude-opus-5-5"
    name = "Claude Code"
    login_env = "CLAUDE_CODE_OAUTH_TOKEN"
    login_status = "claude auth status"

    def complete(self, *, system: str, prompt: str, schema: dict[str, Any], effort: str = "low") -> dict[str, Any]:
        self.workdir.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", suffix=".md", dir=self.workdir, delete=False, encoding="utf-8") as f:
            f.write(system)
            system_path = f.name
        binary = shutil.which(self.binary)
        cmd = [
            os.path.abspath(binary) if binary else self.binary, "-p",
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
        try:
            proc = self._run(cmd, prompt, self.workdir)
        finally:
            Path(system_path).unlink(missing_ok=True)
        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            tail = (proc.stderr or proc.stdout)[-500:]
            message = f"AI 返回的不是 JSON（退出码 {proc.returncode}）：{tail}"
            raise self._cli_error(f"{proc.stderr}\n{proc.stdout}", message) from exc
        if data.get("is_error"):
            raise self._cli_error(str(data.get("result") or "AI 调用失败"))
        out = data.get("structured_output")
        if not isinstance(out, dict):
            raise AIError("AI 没有按格式返回结构化结果")
        return out


class CodexProvider(CliProvider):
    command = "codex"
    default_model = "gpt-6.2-astra"
    name = "Codex"
    login_env = "CODEX_HOME"
    login_status = "codex login status"

    def complete(self, *, system: str, prompt: str, schema: dict[str, Any], effort: str = "low") -> dict[str, Any]:
        binary = find_codex(self.binary)
        if binary is None:
            raise AIError(f"找不到 Codex 命令 {self.binary}")
        self.workdir.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=self.workdir) as tmp:
            directory = Path(tmp).resolve()
            cwd = directory / "work"
            cwd.mkdir()
            schema_path = directory / "schema.json"
            output = directory / "reply.json"
            schema_path.write_text(json.dumps(strict_schema(schema), ensure_ascii=False), encoding="utf-8")
            cmd = [
                os.path.abspath(binary), "exec", "--ephemeral", "--skip-git-repo-check",
                "--sandbox", "read-only", "--ignore-user-config", "--ignore-rules", "-C", str(cwd),
                "-m", self.model, "-c", 'forced_login_method="chatgpt"',
                "-c", "developer_instructions=" + json.dumps(system, ensure_ascii=False),
                "-c", "model_reasoning_effort=" + json.dumps("xhigh" if effort == "max" else effort),
                "--output-schema", str(schema_path), "-o", str(output), "-",
            ]
            proc = self._run(cmd, prompt, cwd)
            if proc.returncode:
                raise self._cli_error(f"{proc.stderr}\n{proc.stdout}",
                                      f"Codex 调用失败（退出码 {proc.returncode}），请检查 ChatGPT 登录和模型设置")
            try:
                data = json.loads(output.read_bytes())
            except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError) as exc:
                raise AIError("Codex 没有返回有效的 JSON 回复") from exc
            if not isinstance(data, dict):
                raise AIError("Codex 没有按格式返回结构化结果")
            return restore_result(data, schema)


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
