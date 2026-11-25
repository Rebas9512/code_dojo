"""学习记录的事件格式、跨机器编号映射和事务日志。调用方持有 SQLite 写事务。"""

from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timedelta, timezone
from itertools import groupby
from pathlib import Path
from uuid import UUID, uuid4, uuid5, NAMESPACE_URL

# 顺序有意义：先给附加题建立编号，再还原引用它的提交和复习。
KEYS = {
    "extra_problems": ("id",), "submissions": ("id",), "chat_messages": ("id",),
    "project_completions": ("project_id",),
    "reviews": ("problem_id",), "study_help": ("problem_id", "attempt"), "settings": ("key",),
    "memory_notes": ("name",),
}
REFS = ("problem_id", "review_source", "rewrite_target", "parent_id")
SCHEMA = """
CREATE TABLE IF NOT EXISTS sync_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS sync_events (
    id TEXT PRIMARY KEY, machine TEXT NOT NULL, timestamp TEXT NOT NULL,
    type TEXT NOT NULL, payload TEXT NOT NULL, exported INTEGER NOT NULL, pushed INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS sync_outbox ON sync_events(machine,exported,pushed);
CREATE INDEX IF NOT EXISTS sync_machine_time ON sync_events(machine,timestamp);
CREATE TABLE IF NOT EXISTS sync_versions (
    type TEXT NOT NULL, entity TEXT NOT NULL, local_id INTEGER, timestamp TEXT NOT NULL, event_id TEXT NOT NULL,
    PRIMARY KEY(type,entity), UNIQUE(type,local_id)
);
CREATE TABLE IF NOT EXISTS sync_offsets (month TEXT PRIMARY KEY, size INTEGER NOT NULL);
"""


def encode(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def meta(conn: sqlite3.Connection, key: str, default: str = "") -> str:
    row = conn.execute("SELECT value FROM sync_meta WHERE key=?", (key,)).fetchone()
    return row[0] if row else default


def set_meta(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute("INSERT OR REPLACE INTO sync_meta VALUES (?,?)", (key, value))


class Journal:
    def __init__(self, conn: sqlite3.Connection, directory: Path):
        self.conn = conn
        self.directory = directory
        self.columns = {t: [r["name"] for r in conn.execute(f"PRAGMA table_info({t})")] for t in KEYS}
        self.machine = meta(conn, "machine")
        if not self.machine:
            self.machine = str(uuid4())
            set_meta(conn, "machine", self.machine)
            for table in KEYS:
                for row in conn.execute(f"SELECT * FROM {table} ORDER BY rowid"):
                    self.capture(table, dict(row))

    def install_triggers(self) -> None:
        # 临时表只记录当前连接在本次写操作中改过的行。导入时不打开捕获开关。
        self.conn.execute("CREATE TEMP TABLE capture_enabled (enabled INTEGER)")
        self.conn.execute("CREATE TEMP TABLE changes (name TEXT, snapshot TEXT, removed INTEGER)")
        for table, cols in self.columns.items():
            for op in ("INSERT", "UPDATE", "DELETE"):
                ref = "OLD" if op == "DELETE" else "NEW"
                fields = ",".join(f"'{c}',{ref}.{c}" for c in cols)
                self.conn.execute(f"""CREATE TEMP TRIGGER capture_{table}_{op} AFTER {op} ON {table}
                    WHEN EXISTS(SELECT 1 FROM capture_enabled)
                    BEGIN INSERT INTO changes VALUES ('{table}',json_object({fields}),{int(op == 'DELETE')}); END""")

    def finish_capture(self) -> None:
        for table, row, removed in self.conn.execute("SELECT * FROM changes ORDER BY rowid"):
            self.capture(table, json.loads(row), bool(removed))
        self.conn.execute("DELETE FROM changes")
        self.conn.execute("DELETE FROM capture_enabled")

    def ref(self, value: str, *, importing: bool) -> str:
        if not value or not value.startswith("x-"):
            return value
        field, target = ("entity", "local_id") if importing else ("local_id", "entity")
        mapped = self.conn.execute(f"SELECT {target} FROM sync_versions WHERE type='extra_problems' AND {field}=?",
                                   (value[2:],)).fetchone()
        if not mapped:
            raise ValueError("事件引用的附加题缺少创建记录")
        return f"x-{mapped[0]}"

    def references(self, row: dict, importing: bool) -> None:
        for field in REFS:
            if row.get(field):
                row[field] = self.ref(row[field], importing=importing)
        if "attempt" in row:
            source, sep, due = row["attempt"].partition("/")
            row["attempt"] = self.ref(source, importing=importing) + sep + due

    def entity(self, table: str, row: dict) -> str:
        if "id" in row:
            mapped = self.conn.execute("SELECT entity FROM sync_versions WHERE type=? AND local_id=?",
                                       (table, row["id"])).fetchone()
            # 数字前缀保留同秒老记录的顺序；即使从同一备份分叉，新记录也各有身份。
            return mapped[0] if mapped else f"{row['id']:020d}:{uuid4()}"
        return encode([row[k] for k in KEYS[table]])

    def capture(self, table: str, row: dict, removed: bool = False) -> None:
        if table == "settings" and row["key"] == "reviews_initialized":
            return
        self.references(row, False)
        key = self.entity(table, row)
        local_id = row.pop("id", None)
        stamp = utc()
        clock = meta(self.conn, "clock")
        if stamp <= clock:
            stamp = (datetime.fromisoformat(clock) + timedelta(microseconds=1)).isoformat(timespec="microseconds")
        event = dict(id=str(uuid4()), machine=self.machine, timestamp=stamp, type=table,
                     payload=dict(entity=key, row=row, removed=removed))
        self.record(event, local=True)
        self.version(event, local_id)

    def record(self, event: dict, local: bool) -> bool:
        cur = self.conn.execute("INSERT INTO sync_events VALUES (?,?,?,?,?,?,?) ON CONFLICT(id) DO NOTHING",
                                (event["id"], event["machine"], event["timestamp"], event["type"],
                                 encode(event["payload"]), int(not local), int(not local)))
        if cur.rowcount and event["timestamp"] > meta(self.conn, "clock"):
            set_meta(self.conn, "clock", event["timestamp"])
        return bool(cur.rowcount)

    def version(self, event: dict, local_id: int | None) -> None:
        self.conn.execute("INSERT OR REPLACE INTO sync_versions VALUES (?,?,?,?,?)",
                          (event["type"], event["payload"]["entity"], local_id, event["timestamp"], event["id"]))

    def apply(self, event: dict, *, local: bool = False) -> bool:
        table = event["type"]
        if table not in KEYS:
            raise ValueError("无法识别的同步事件类型")
        if not self.record(event, local):
            return False
        payload = event["payload"]
        key = payload["entity"]
        row = dict(payload["row"])
        if row.keys() - (set(self.columns[table]) - {"id"}):
            raise ValueError("事件含有未知字段")
        existing = self.conn.execute("SELECT * FROM sync_versions WHERE type=? AND entity=?", (table, key)).fetchone()
        local_id = existing["local_id"] if existing else None
        if existing:
            # 删除是终态。离线应用修改建议或晚到的出题结果都不能复活已删除的内容。
            if table == "chat_messages" and not self.conn.execute(
                    "SELECT 1 FROM chat_messages WHERE id=?", (local_id,)).fetchone():
                return True
            if (existing["timestamp"], existing["event_id"]) >= (event["timestamp"], event["id"]) and not payload["removed"]:
                if table == "extra_problems" and row.get("deleted"):
                    self.conn.execute("UPDATE extra_problems SET deleted=1 WHERE id=?", (local_id,))
                return True
        self.references(row, True)
        if payload["removed"]:
            if table != "chat_messages":
                raise ValueError("无效的删除事件")
            self.conn.execute("DELETE FROM chat_messages WHERE id=?", (local_id,))
        else:
            if table == "extra_problems":
                # 两台离线机器可能都出了「附加题 1」。本机已展示的编号保持稳定。
                extra = self.conn.execute("SELECT seq,deleted FROM extra_problems WHERE id=?", (local_id,)).fetchone()
                if extra:
                    row["seq"] = extra["seq"]
                    row["deleted"] = max(extra["deleted"], row["deleted"])
                elif self.conn.execute("SELECT 1 FROM extra_problems WHERE parent_id=? AND seq=?",
                                       (row["parent_id"], row["seq"])).fetchone():
                    row["seq"] = self.conn.execute("SELECT MAX(seq)+1 FROM extra_problems WHERE parent_id=?",
                                                   (row["parent_id"],)).fetchone()[0]
            if local_id is not None:
                row["id"] = local_id
            cols = ",".join(row)
            params = ",".join("?" for _ in row)
            cur = self.conn.execute(f"INSERT OR REPLACE INTO {table} ({cols}) VALUES ({params})", tuple(row.values()))
            if KEYS[table] == ("id",):
                local_id = cur.lastrowid
        self.version(event, local_id)
        return True

    def flush(self) -> None:
        # 文件先落盘，同一 SQLite 事务再确认偏移。崩溃重试从最后确认的位置续写。
        rows = self.conn.execute("SELECT id,machine,timestamp,type,payload FROM sync_events "
                                 "WHERE machine=? AND exported=0 ORDER BY timestamp,id", (self.machine,))
        directory = self.directory / "events" / self.machine
        for month, group in groupby(rows, key=lambda r: r["timestamp"][:7]):
            directory.mkdir(parents=True, exist_ok=True)
            size = self.conn.execute("SELECT size FROM sync_offsets WHERE month=?", (month,)).fetchone()
            path = directory / f"{month}.jsonl"
            with path.open("a+b") as file:
                offset = size[0] if size else 0
                if file.tell() < offset:
                    raise OSError("本机日志被截断，启动或同步时会从 SQLite 补齐")
                file.truncate(offset)
                for row in group:
                    event = dict(row) | {"payload": json.loads(row["payload"])}
                    file.write((encode(event) + "\n").encode())
                file.flush()
                os.fsync(file.fileno())
                self.conn.execute("INSERT OR REPLACE INTO sync_offsets VALUES (?,?)", (month, file.tell()))
        self.conn.execute("UPDATE sync_events SET exported=1 WHERE machine=? AND exported=0", (self.machine,))

    def recover_exports(self) -> None:
        # SQLite 在线备份可能单独恢复到空目录。按事务日志补写缺失或截断的月份。
        directory = self.directory / "events" / self.machine
        for month, size in self.conn.execute("SELECT month,size FROM sync_offsets").fetchall():
            path = directory / f"{month}.jsonl"
            if not path.is_file() or path.stat().st_size < size:
                self.conn.execute("DELETE FROM sync_offsets WHERE month=?", (month,))
                self.conn.execute("UPDATE sync_events SET exported=0 WHERE machine=? AND substr(timestamp,1,7)=?",
                                  (self.machine, month))


def legacy_events(conn: sqlite3.Connection, machine: str):
    """历史编号以原库首批记录为命名空间；同一份旧库在不同机器导入也有相同事件 ID。"""
    roots = []
    for table in ("submissions", "chat_messages", "extra_problems"):
        row = conn.execute(f"SELECT id,created_at FROM {table} ORDER BY id LIMIT 1").fetchone()
        if row:
            roots.append([table, *row])
    origin = str(uuid5(NAMESPACE_URL, "code-dojo/legacy/" + encode(roots)))
    def ref(value: str) -> str:
        return f"x-{origin}:{int(value[2:]):020d}" if value and value.startswith("x-") else value

    for table, keys in KEYS.items():
        for record in conn.execute(f"SELECT * FROM {table} ORDER BY rowid"):
            row = dict(record)
            if table == "settings" and row["key"] == "reviews_initialized":
                continue
            for field in REFS:
                if row.get(field):
                    row[field] = ref(row[field])
            if "attempt" in row:
                source, sep, due = row["attempt"].partition("/")
                row["attempt"] = ref(source) + sep + due
            key = f"{origin}:{row.pop('id'):020d}" if "id" in row else encode([row[k] for k in keys])
            stamp = row.get("updated_at") or row.get("created_at") or row.get("last_reviewed") or "1970-01-01"
            stamp = datetime.fromisoformat(stamp)
            stamp = (stamp if stamp.tzinfo else stamp.replace(tzinfo=timezone.utc)).astimezone(timezone.utc)
            payload = dict(entity=key, row=row, removed=False)
            yield dict(id=str(uuid5(UUID(origin), table + encode(payload))), machine=machine,
                       timestamp=stamp.isoformat(timespec="microseconds"), type=table, payload=payload)
