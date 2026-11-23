"""无 Git 客户端时，通过 GitHub Contents API 交换同一份按月事件日志。"""

import base64
import hashlib
from itertools import groupby
from urllib.error import HTTPError, URLError

from .db import Store
from .events import encode
from .sync import MONTH, SyncError, log_path, read_lines


def exchange(client, store: Store) -> None:
    pending = store.pending_events()
    # 不同机器的 PUT 也会竞争同一分支头，冲突后重新读取快照并合并。
    for attempt in range(3):
        try:
            tree = client.json("/git/trees/main?recursive=1")
            if tree.get("truncated"):
                raise SyncError("进度仓库的目录清单不完整")
            blobs = {e["path"]: e["sha"] for e in tree["tree"] if e["type"] == "blob"}
            if "server/pyproject.toml" in blobs:
                raise SyncError("请使用单独的进度仓库")
            revision = tree["sha"]
            if revision == store.imported_revision() and not pending:
                store.confirm_sync([], revision)
                return

            own = store.journal.machine
            months = {f"{own}/{month}.jsonl": list(rows) for month, rows in
                      groupby(pending, key=lambda e: e["timestamp"][:7])}
            records = []
            for relative in sorted(blobs.keys() | months.keys()):
                parts = relative.split("/")
                if len(parts) != 2 or not MONTH.fullmatch(parts[1]):
                    continue
                log_path(store.path.parent / "events", relative)
                raw = b""
                path = "/contents/" + relative
                sha = blobs.get(relative)
                if sha:
                    with client.open(path + "?ref=main", "application/vnd.github.raw+json") as source:
                        raw = source.read()
                    actual = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
                    if actual != sha:
                        break  # 下载期间远端又提交了同月的文件，整轮重读。
                remote = {e["id"]: e for e in read_lines(raw.decode().splitlines(), relative)}
                records.extend(remote.values())
                additions = []
                for e in months.get(relative, []):
                    existing = remote.get(e["id"])
                    if existing and existing != e:
                        raise SyncError("同一事件的内容不同，请检查进度仓库")
                    if existing is None:
                        additions.append(encode(e))
                if additions:
                    prefix = raw if not raw or raw.endswith(b"\n") else raw + b"\n"
                    body = prefix + ("\n".join(additions) + "\n").encode()
                    client.json(path, {"branch": "main", "message": "同步学习记录",
                                       "content": base64.b64encode(body).decode(), **({"sha": sha} if sha else {})})
            else:
                store.import_events(records)
                store.confirm_sync(pending, revision)
                return
        except HTTPError as exc:
            if exc.code in (409, 422) and attempt < 2:
                continue
            raise SyncError(f"进度仓库返回 HTTP {exc.code}，请检查网络、分支和读写权限") from exc
        except URLError as exc:
            raise SyncError("无法连接进度仓库，请检查网络") from exc
    raise SyncError("进度仓库正在变化，请稍后再同步")
