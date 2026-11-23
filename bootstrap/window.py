"""桌面控制窗口。耗时的发布检查与后端启动在工作线程中完成。"""

import json
import os
import queue
import shutil
import sqlite3
import subprocess
import sys
import threading
import time
import webbrowser
from datetime import datetime
from pathlib import Path
from tkinter import BOTH, DISABLED, LEFT, NORMAL, X, Menu, StringVar, Tk, Toplevel, font, messagebox, ttk

from . import DEFAULT_REPO, DEFAULT_SYNC
from cryptography.exceptions import InvalidTag

from .credentials import credential_source, tokens
from .github import GitHub, repository
from .sealed import unseal
from .update import Result, Updates, atomic_json


class StartupError(RuntimeError):
    pass


def data_directory() -> Path:
    if override := os.environ.get("CODE_DOJO_DATA"):
        return Path(override).expanduser().resolve()
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA") or Path.home() / "AppData/Roaming")
    elif sys.platform == "darwin":
        base = Path.home() / "Library/Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share")
    return base / "code-dojo"


def window_fonts(root: Tk) -> font.Font:
    families = {family.casefold(): family for family in font.families(root)}
    candidates = {"linux": ("Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Micro Hei"),
                  "darwin": ("PingFang SC",), "win32": ("Microsoft YaHei UI",)}
    for family in candidates.get(sys.platform, ()):
        if family.casefold() in families:
            for name in ("TkDefaultFont", "TkTextFont", "TkMenuFont", "TkHeadingFont"):
                font.nametofont(name, root=root).configure(family=families[family.casefold()])
            break
    heading = font.nametofont("TkDefaultFont", root=root).copy()
    heading.configure(size=13, weight="bold")
    return heading


class UnlockAttempts:
    """同一数据目录在关闭窗口或重启应用后仍保留冷却时间。"""

    def __init__(self, data: Path):
        self.path = data / "unlock-attempts.json"

    def state(self) -> tuple[int, float]:
        if self.path.exists():
            record = json.loads(self.path.read_bytes())
            remaining = record["until"] - time.time()
            if remaining > 0 or record["count"] < 5:
                return record["count"], max(0, remaining)
        return 0, 0

    def failed(self) -> None:
        count, _ = self.state()
        atomic_json(self.path, {"count": count + 1, "until": time.time() + 30 if count >= 4 else 0})

    def clear(self) -> None:
        self.path.unlink(missing_ok=True)


class Window:
    def __init__(self, root: Tk, bundle: Path, data: Path):
        self.root, self.bundle, self.data = root, bundle, data
        self.repo = repository(os.environ.get("CODE_DOJO_REPO", DEFAULT_REPO))
        self.sync_repo = repository(os.environ.get("CODE_DOJO_SYNC_REPO", DEFAULT_SYNC))
        if self.repo.casefold() == self.sync_repo.casefold():
            raise ValueError("代码与学习记录需要使用两个独立仓库")
        self.api = os.environ.get("CODE_DOJO_GITHUB_API", "https://api.github.com")
        self.values = {}
        saved = tokens(data)
        for key, env in (("code", "CODE_DOJO_GITHUB_TOKEN"), ("sync", "CODE_DOJO_SYNC_TOKEN")):
            if supplied := os.environ.pop(env, ""):
                saved.setdefault(key, supplied)
        self.events = queue.Queue()
        self.child = None
        self.url = ""
        self.busy = False
        self.closing = False
        self.dialog = None
        self.session_notice = ""
        self.prompt = "pending"
        self.attempts = UnlockAttempts(data)
        self.heading = window_fonts(root)
        self.root.title("code-dojo")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.theme_file = data / "desktop-theme.json"
        self.theme = StringVar(value=json.loads(self.theme_file.read_bytes())["theme"] if self.theme_file.exists() else "dark")
        menu = Menu(root)
        settings = Menu(menu, tearoff=False)
        settings.add_command(label="更新令牌与 AI 助教…", command=self.settings, state=DISABLED)
        self.settings_menu = settings
        settings.add_separator()
        for title, value in (("深色", "dark"), ("浅色", "light")):
            settings.add_radiobutton(label=title, variable=self.theme, value=value, command=self.change_theme)
        menu.add_cascade(label="设置", menu=settings)
        root.config(menu=menu)
        self.style = ttk.Style(root)
        self.style.theme_use("clam")
        self.colors()
        panel = ttk.Frame(root, padding=(22, 18))
        panel.pack(fill=BOTH, expand=True)
        self.state, self.release, self.sync, self.note = (StringVar() for _ in range(4))
        ttk.Label(panel, textvariable=self.state, font=self.heading).pack(anchor="w")
        for text in (self.release, self.sync, self.note):
            ttk.Label(panel, textvariable=text, wraplength=470).pack(anchor="w", pady=(5, 0))
        self.download = ttk.Button(panel, text="下载新版安装包")
        bar = ttk.Frame(panel)
        bar.pack(fill=X, pady=(14, 0))
        self.browser = ttk.Button(bar, text="打开浏览器", command=lambda: webbrowser.open(self.url), state=DISABLED)
        self.browser.pack(side=LEFT)
        self.now = ttk.Button(bar, text="立即同步", command=self.sync_now, state=DISABLED)
        self.now.pack(side=LEFT, padx=8)
        ttk.Button(bar, text="退出", command=self.close).pack(side=LEFT)
        self.root.after(100, self.poll)
        self.root.after(1600, self.read_status)
        self.state.set("正在检查本机凭据…")

        def resolve():
            source = credential_source(saved, bundle, self.repo, self.sync_repo, self.api)
            self.events.put(("credentials", source))

        threading.Thread(target=resolve, daemon=True).start()

    def colors(self):
        dark = self.theme.get() == "dark"
        bg, fg, control = ("#242320", "#e9e6dd", "#383630") if dark else ("#f4f2ec", "#302e29", "#e6e2d8")
        self.root.config(bg=bg)
        self.style.configure(".", background=bg, foreground=fg, fieldbackground=control)
        self.style.configure("TButton", background=control, padding=(8, 5))
        self.style.map("TButton", background=[("active", control)], foreground=[("disabled", "#88857e")])
        self.style.configure("TEntry", insertcolor=fg)

    def change_theme(self):
        self.colors()
        atomic_json(self.theme_file, {"theme": self.theme.get()})

    def settings(self):
        if self.dialog and self.dialog.winfo_exists():
            self.dialog.lift()
            return
        dialog = self.dialog = Toplevel(self.root)
        dialog.title("设置")
        dialog.transient(self.root)
        panel = ttk.Frame(dialog, padding=18)
        panel.pack(fill=BOTH)
        fields = {}
        for key, label in (("code", f"代码仓库（只读） · {self.repo}"), ("sync", f"进度仓库（读写） · {self.sync_repo}")):
            ttk.Label(panel, text=label).pack(anchor="w", pady=(6, 2))
            fields[key] = ttk.Entry(panel, show="•", width=48)
            fields[key].insert(0, self.values.get(key, ""))
            fields[key].pack(fill=X)
        ttk.Label(panel, text="两个仓库共用令牌时，第二栏可留空。").pack(anchor="w", pady=4)
        guide = os.environ.get("CODE_DOJO_TOKEN_GUIDE", f"https://github.com/{self.repo}/blob/main/deploy/README.md#在一台新电脑上用")
        ttk.Button(panel, text="如何创建令牌", command=lambda: webbrowser.open(guide)).pack(anchor="w")
        ttk.Separator(panel).pack(fill=X, pady=12)
        found = shutil.which(os.environ.get("CODE_DOJO_CLAUDE_BIN", "claude"))
        ttk.Label(panel, text="已检测到 Claude Code" if found else "AI 助教已关闭。安装 Claude Code 后，打开终端运行 claude，\n按提示登录，再重新打开应用。").pack(anchor="w")
        if not found:
            ttk.Button(panel, text="Claude Code 安装说明",
                       command=lambda: webbrowser.open("https://code.claude.com/docs/en/setup")).pack(anchor="w", pady=4)

        def save():
            values = {k: entry.get().strip() for k, entry in fields.items()}
            if not values["code"]:
                fields["code"].focus_set()
                return
            self.save_credentials(values, dialog)

        ttk.Button(panel, text="保存", command=save).pack(anchor="e", pady=(12, 0))
        fields["code"].focus_set()

    def save_credentials(self, values: dict, dialog: Toplevel):
        try:
            self.values = tokens(self.data, values)
            self.session_notice = ""
        except PermissionError as exc:
            self.values = values
            self.session_notice = str(exc)
        except OSError:
            messagebox.showerror("保存令牌失败", "请检查本机数据目录的写权限。", parent=dialog)
            return
        self.attempts.clear()
        dialog.destroy()
        if self.busy:
            self.note.set("令牌已保存，重新打开应用后生效")
        else:
            self.start()

    def unlock(self):
        if self.dialog and self.dialog.winfo_exists():
            self.dialog.lift()
            return
        dialog = self.dialog = Toplevel(self.root)
        dialog.title("解锁安装包")
        dialog.transient(self.root)
        panel = ttk.Frame(dialog, padding=18)
        panel.pack(fill=BOTH)
        ttk.Label(panel, text="解锁密码").pack(anchor="w")
        field = ttk.Entry(panel, width=32, show="•")
        field.pack(fill=X, pady=(4, 0))
        hint = StringVar()
        ttk.Label(panel, textvariable=hint).pack(anchor="w")
        bar = ttk.Frame(panel)
        bar.pack(fill=X)

        def cooldown():
            remaining = self.attempts.state()[1]
            if remaining:
                hint.set(f"密码不对，请在 {int(remaining) + 1} 秒后重试")
                submit.configure(state=DISABLED)
                dialog.after(250, cooldown)
            else:
                submit.configure(state=NORMAL)
                hint.set("")

        def attempt():
            if submit.instate(["disabled"]) or self.attempts.state()[1]:
                return
            password = field.get()
            field.delete(0, "end")
            try:
                envelope = json.loads((self.bundle / "sealed-tokens.json").read_bytes())
                values = unseal(envelope, password, self.repo, self.sync_repo)
            except InvalidTag:
                self.attempts.failed()
                cooldown()
                if not self.attempts.state()[1]:
                    hint.set("密码不对")
                field.focus_set()
            except (OSError, ValueError):
                hint.set("令牌包无效或仓库不匹配，请改用令牌")
            else:
                self.save_credentials(values, dialog)

        def manual():
            dialog.destroy()
            self.settings()

        self.style.configure("Link.TButton", relief="flat", padding=3)
        self.style.layout("Link.TButton", [("Button.label", {"sticky": "we"})])
        ttk.Button(bar, text="改用令牌", style="Link.TButton", cursor="hand2", command=manual).pack(side=LEFT)
        submit = ttk.Button(bar, text="解锁", command=attempt)
        submit.pack(side="right")
        field.bind("<Return>", lambda _: attempt())
        cooldown()
        field.focus_set()

    def has_payload(self):
        return (self.data / "desktop/current.json").is_file()

    def start(self):
        if self.busy or self.closing:
            return
        if self.prompt == "pending":
            return
        if not self.values.get("code") and not self.has_payload():
            (self.unlock if self.prompt == "sealed" else self.settings)()
            return
        self.busy = True
        self.state.set("正在检查更新…")
        self.note.set("")
        self.download.pack_forget()
        self.now.config(state=DISABLED)
        threading.Thread(target=self.run, daemon=False).start()

    def run(self):
        try:
            updates = Updates(self.data, self.bundle, GitHub(self.repo, self.values.get("code", ""), self.api))
            previous = updates.current()
            result = updates.check()
            self.events.put(("update", result))
            if not result.active or self.closing:
                return
            try:
                self.backend(updates, result.active)
            except StartupError:
                if not previous or previous == result.active or self.closing:
                    raise
                self.events.put(("update", Result(previous, "新版服务启动失败，已恢复上一版本")))
                self.backend(updates, previous)
        except Exception as exc:
            self.events.put(("error", str(exc)))
        finally:
            self.events.put(("finished", None))

    def backend(self, updates, item):
        python = Path(sys.executable)
        if os.name == "nt":
            python = python.with_name("python.exe")
        config = dict(payload=str(item.root), libraries=str(updates.libraries(item.manifest)), data=str(self.data),
                      api=self.api, repo=self.sync_repo, token=self.values.get("sync") or self.values.get("code", ""))
        started = False
        with (updates.root / "backend.log").open("a", encoding="utf-8") as log, subprocess.Popen(
            [str(python), "-I", "-B", "-X", "utf8", str(self.bundle / "start.py"), "--serve"],
            cwd=item.root, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=log, text=True, encoding="utf-8",
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        ) as child:
            child.stdin.write(json.dumps(config) + "\n")
            child.stdin.flush()
            self.child = child
            if self.closing:
                self.command("quit")
            for line in child.stdout:
                event = json.loads(line)
                if "ready" in event:
                    updates.activate(item)
                    started = True
                    self.events.put(("ready", event["ready"]))
                elif "sync" in event:
                    self.events.put(("sync", event["sync"]))
            self.child = None
            status = child.wait()
            if not started:
                raise StartupError(f"本机服务启动失败，请查看 {log.name}")
            if status:
                raise RuntimeError(f"本机服务已退出，请查看 {log.name}")

    def command(self, cmd):
        child = self.child
        if child and child.stdin:
            try:
                child.stdin.write(cmd + "\n")
                child.stdin.flush()
            except (OSError, ValueError):
                pass

    def sync_now(self):
        if self.url:
            self.command("sync")
            self.sync.set("正在同步学习记录…")
        else:
            self.start()

    def read_status(self):
        if self.url and not self.closing:
            self.command("status")
        self.root.after(1600, self.read_status)

    def poll(self):
        while not self.events.empty():
            kind, value = self.events.get_nowait()
            if kind == "credentials" and not self.closing:
                self.prompt, self.values = value
                self.settings_menu.entryconfigure(0, state=NORMAL)
                self.now.configure(state=NORMAL)
                if self.prompt == "sealed":
                    self.state.set("首次使用 · 请解锁安装包")
                    self.unlock()
                else:
                    self.state.set("首次使用 · 请设置 GitHub 令牌")
                    self.start()
            elif kind == "update":
                self.note.set("\n".join(filter(None, (value.message, self.session_notice))))
                if value.active:
                    stamp = datetime.fromisoformat(value.active.updated).astimezone().strftime("%Y-%m-%d %H:%M")
                    self.release.set(f"版本 {value.active.manifest['version']}　·　上次更新 {stamp}")
                    self.state.set("正在启动本机服务…")
                else:
                    self.state.set("尚未安装题库")
                if value.installer:
                    self.download.configure(command=lambda url=value.installer: webbrowser.open(url))
                    self.download.pack(anchor="w")
            elif kind == "ready" and not self.closing:
                self.url = f"http://127.0.0.1:{value}"
                self.state.set(f"正在运行 · 端口 {value}")
                self.now.config(state=NORMAL)
                self.browser.config(state=NORMAL)
                webbrowser.open(self.url)
                self.command("status")
            elif kind == "sync" and not self.closing:
                if not value["enabled"]:
                    self.sync.set("学习记录 · 未开启同步")
                    continue
                stamp = value["last_sync"]
                stamp = datetime.fromisoformat(stamp).astimezone().strftime("%m-%d %H:%M") if stamp else "等待首次同步"
                status = "正在同步…" if value["syncing"] else value["error"] or stamp
                self.sync.set(f"学习记录 · {status}" + (f"　待推送 {value['pending']} 条" if value["pending"] else ""))
            elif kind == "error":
                self.state.set("启动失败")
                self.note.set(value)
            elif kind == "finished":
                self.url = ""
                self.busy = False
                self.now.config(state=NORMAL)
                self.browser.config(state=DISABLED)
        if self.closing and not self.busy:
            self.root.destroy()
        else:
            self.root.after(100, self.poll)

    def close(self):
        self.closing = True
        self.state.set("正在保存学习记录并退出…")
        self.now.config(state=DISABLED)
        self.browser.config(state=DISABLED)
        self.command("quit")


def main(bundle: Path) -> None:
    root = Tk()
    try:
        data = data_directory()
        data.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(data / "desktop.lock", timeout=0) as lock:
            try:
                lock.execute("BEGIN IMMEDIATE")
            except sqlite3.OperationalError:
                messagebox.showinfo("code-dojo", "此数据目录已有运行中的桌面应用", parent=root)
                return
            Window(root, bundle, data)
            root.mainloop()
    except (OSError, ValueError, sqlite3.Error) as exc:
        messagebox.showerror("无法启动 code-dojo", str(exc), parent=root)
