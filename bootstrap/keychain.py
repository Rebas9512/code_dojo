"""独立解释器没有 Python keyring 时使用系统已有的凭据工具。"""

import base64
import os
import shutil
import subprocess
import sys


class SystemKeychain:
    def __init__(self, tool: str):
        self.tool = tool

    def _call(self, args, payload=None):
        result = subprocess.run([self.tool, *args], input=payload or b"", capture_output=True,
                                timeout=20, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        if result.returncode:
            raise OSError("系统钥匙串不可用")
        return result.stdout.strip()

    def _windows(self, service, account, value=None):
        # PasswordVault 使用当前登录用户的 Windows 凭据保管库，秘密只通过标准输入交给系统。
        script = ("$ErrorActionPreference='Stop';"
                  "$v=[Windows.Security.Credentials.PasswordVault,Windows.Security.Credentials,ContentType=WindowsRuntime]::new();")
        if value is None:
            script += f"$c=$v.Retrieve('{service}','{account}');$c.RetrievePassword();[Console]::Write($c.Password)"
        else:
            script += ("$c=[Windows.Security.Credentials.PasswordCredential,Windows.Security.Credentials,ContentType=WindowsRuntime]"
                       f"::new('{service}','{account}',[Console]::In.ReadToEnd());$v.Add($c)")
        return self._call(["-NoProfile", "-NonInteractive", "-Command", script], value)

    def get_password(self, service: str, account: str) -> str:
        if sys.platform == "darwin":
            raw = self._call(["find-generic-password", "-s", service, "-a", account, "-w"])
        elif os.name == "nt":
            raw = self._windows(service, account)
        else:
            raw = self._call(["lookup", "service", service, "account", account])
        return base64.b64decode(raw, validate=True).decode()

    def set_password(self, service: str, account: str, value: str):
        # 固定服务名、目录摘要和 Base64 在系统命令里都只有安全的单词字符。
        encoded = base64.b64encode(value.encode())
        if sys.platform == "darwin":
            command = f"add-generic-password -U -s {service} -a {account} -w ".encode() + encoded + b"\n"
            self._call(["-i"], command)
        elif os.name == "nt":
            self._windows(service, account, encoded)
        else:
            self._call(["store", "--label=code-dojo", "service", service, "account", account], encoded)
        if self.get_password(service, account) != value:
            raise OSError("系统钥匙串未确认保存")


def available():
    name = "security" if sys.platform == "darwin" else "powershell.exe" if os.name == "nt" else "secret-tool"
    tool = shutil.which(name)
    return SystemKeychain(tool) if tool else None
