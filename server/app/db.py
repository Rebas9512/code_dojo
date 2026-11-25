"""SQLite 存储：提交、复习日程、设置与助教记录。"""

from __future__ import annotations

import json
import logging
import sqlite3
import threading
from contextlib import closing, contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import events
from .ai.memory import BODY_LIMIT, DESCRIPTION_LIMIT, NAME_LIMIT, MemorySnapshot, ReviewBatch, ReviewEvidence
from .mastery import independent, local_day, schedule
from .result_preview import compact_result, syntax_error


class ReviewConflict(ValueError):
    """其他页面已交卷、未到期或当天复习名额已用完。"""


SCHEMA = """
CREATE TABLE IF NOT EXISTS submissions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    problem_id  TEXT NOT NULL,
    track       TEXT NOT NULL,
    kind        TEXT NOT NULL,            -- run | submit | review
    code        TEXT NOT NULL,
    verdict     TEXT NOT NULL,
    passed      INTEGER,
    total       INTEGER,
    elapsed_ms  INTEGER,                  -- 从打开题目到这次提交的用时（前端上报）
    hints_used  INTEGER NOT NULL DEFAULT 0,
    ai_lines    INTEGER NOT NULL DEFAULT 0, -- 代码里应用过的 AI 修改建议行数（前端上报）
    review_source TEXT,                   -- 本轮复习所归属的原题
    solution_seen INTEGER NOT NULL DEFAULT 0,
    syntax_error INTEGER NOT NULL DEFAULT 0,
    result_json TEXT NOT NULL,
    created_at  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_submissions_problem ON submissions(problem_id, created_at);

CREATE TABLE IF NOT EXISTS project_completions (project_id TEXT PRIMARY KEY, created_at TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS reviews (
    problem_id TEXT PRIMARY KEY,
    step INTEGER NOT NULL,
    rounds INTEGER NOT NULL DEFAULT 0,
    rewrite_target TEXT,
    due TEXT,
    result TEXT NOT NULL,
    last_reviewed TEXT
);
CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS memory_notes (
    name TEXT PRIMARY KEY, type TEXT, description TEXT, scope TEXT, as_of TEXT, body TEXT,
    deleted INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS study_help (
    problem_id TEXT NOT NULL,
    attempt TEXT NOT NULL,
    author_hints INTEGER NOT NULL DEFAULT 0,
    ai_hints INTEGER NOT NULL DEFAULT 0,
    solution_seen INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY(problem_id, attempt)
);

CREATE TABLE IF NOT EXISTS chat_messages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    problem_id  TEXT NOT NULL,
    role        TEXT NOT NULL,            -- user | assistant
    content     TEXT NOT NULL,
    edit_json   TEXT,                     -- 助教对共享编辑框的修改 [{old, new, why}, ...]
    applied     INTEGER NOT NULL DEFAULT 0,
    notes       TEXT,                     -- 回复来源与重试记录（旧版仅存重试列表）
    created_at  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_chat_problem ON chat_messages(problem_id, id);

CREATE TABLE IF NOT EXISTS extra_problems (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id   TEXT NOT NULL,
    seq         INTEGER NOT NULL,            -- 附加题编号：每道原题从 1 开始，删了不复用
    practice_skill TEXT,
    request     TEXT NOT NULL DEFAULT '',    -- 出题要求（学生或助教说的）
    status      TEXT NOT NULL,               -- generating | ready | failed
    spec_json   TEXT,                        -- 验证通过的题目内容
    error       TEXT,
    notes       TEXT,                        -- 重试记录
    deleted     INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_extra_parent ON extra_problems(parent_id, seq);
"""

MIGRATIONS = [
    ("extra_problems", "practice_skill", "ALTER TABLE extra_problems ADD COLUMN practice_skill TEXT"),
    ("submissions", "review_source", "ALTER TABLE submissions ADD COLUMN review_source TEXT"),
    ("submissions", "solution_seen", "ALTER TABLE submissions ADD COLUMN solution_seen INTEGER NOT NULL DEFAULT 0"),
    ("submissions", "syntax_error", "ALTER TABLE submissions ADD COLUMN syntax_error INTEGER NOT NULL DEFAULT 0"),
    ("submissions", "ai_lines", "ALTER TABLE submissions ADD COLUMN ai_lines INTEGER NOT NULL DEFAULT 0"),
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def migrate(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    conn.execute("BEGIN IMMEDIATE")
    for table, column, sql in MIGRATIONS:
        cols = {r["name"] for r in conn.execute(f"PRAGMA table_info({table})")}
        if column not in cols:
            conn.execute(sql)
    if conn.execute("PRAGMA user_version").fetchone()[0] < 1:
        for row in conn.execute("SELECT id, result_json FROM submissions"):
            result = json.loads(row["result_json"])
            conn.execute("UPDATE submissions SET result_json=?, syntax_error=? WHERE id=?",
                         (json.dumps(compact_result(result), ensure_ascii=False), syntax_error(result), row["id"]))
        conn.execute("PRAGMA user_version=1")
    conn.commit()


class Store:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._lock = threading.Lock()
        with self._lock:
            migrate(self._conn)
            self._conn.executescript(events.SCHEMA)
            with self._conn:
                self._conn.execute("BEGIN IMMEDIATE")
                self.journal = events.Journal(self._conn, path.parent)
                self.journal.install_triggers()
                if not self._conn.execute("SELECT 1 FROM sync_meta WHERE key='memory_review_cursor'").fetchone():
                    self._reset_review_cursor()
            self._flush_locked(recover=True)
        self.path = path
        self._reviews_ready = False
        self.version = 0  # 每次写入后加一，供 main.learning() 判断缓存是否过期

    @contextmanager
    def _write(self):
        with self._lock:
            with self._conn:
                self._conn.execute("BEGIN IMMEDIATE")
                self._conn.execute("INSERT INTO capture_enabled VALUES (1)")
                yield
                self.journal.finish_capture()
            self.version += 1
            self._flush_locked()

    def _flush_locked(self, *, recover: bool = False) -> None:
        try:
            with self._conn:
                self._conn.execute("BEGIN IMMEDIATE")
                if recover:
                    self.journal.recover_exports()
                self.journal.flush()
        except OSError:
            logging.exception("本机日志暂未写出，事件已保存在数据库，下次重试")

    def import_events(self, records: list[dict]) -> int:
        with self._lock, self._conn:
            self._conn.execute("BEGIN IMMEDIATE")
            ordered = sorted(records, key=lambda e: (e["type"] != "extra_problems", e["timestamp"], e["id"]))
            self.version += 1
            setting = self._memory_setting()
            count = sum(self.journal.apply(e) for e in ordered)
            if self._memory_setting() != setting:
                self._reset_review_cursor()
            return count

    def import_legacy(self, directory: Path) -> int:
        source = (directory / "code_dojo.db").resolve()
        if source == self.path.resolve():
            raise ValueError("旧库和目标库必须在不同目录")
        marker = f"legacy:{source}"
        # 在内存快照上升级列和结果摘要；源库仅以只读模式打开。
        with closing(sqlite3.connect(source.as_uri() + "?mode=ro", uri=True)) as old, \
                closing(sqlite3.connect(":memory:")) as snapshot:
            old.backup(snapshot)
            snapshot.row_factory = sqlite3.Row
            migrate(snapshot)
            with self._lock:
                with self._conn:
                    self._conn.execute("BEGIN IMMEDIATE")
                    if events.meta(self._conn, marker):
                        return 0
                    setting = self._memory_setting()
                    count = sum(self.journal.apply(e, local=True)
                                for e in events.legacy_events(snapshot, self.journal.machine))
                    if self._memory_setting() != setting:
                        self._reset_review_cursor()
                    events.set_meta(self._conn, marker, "1")
                    self.version += 1
                    # 让旧库里只有通过提交的题也能按历史日期补排。已有日程由事件保留。
                    if count:
                        self._conn.execute("DELETE FROM settings WHERE key='reviews_initialized'")
                        self._reviews_ready = False
                self._flush_locked()
                return count

    def pending_events(self) -> list[dict]:
        with self._lock:
            self._flush_locked(recover=True)
            rows = self._conn.execute("SELECT id,machine,timestamp,type,payload FROM sync_events "
                                      "WHERE machine=? AND pushed=0 ORDER BY timestamp,id", (self.journal.machine,))
            return [dict(r) | {"payload": json.loads(r["payload"])} for r in rows]

    def sync_status(self) -> tuple[int, str]:
        with self._lock:
            count = self._conn.execute("SELECT COUNT(*) FROM sync_events WHERE machine=? AND pushed=0",
                                       (self.journal.machine,)).fetchone()[0]
            return count, events.meta(self._conn, "last_sync")

    def imported_revision(self) -> str:
        with self._lock:
            return events.meta(self._conn, "imported_revision")

    def confirm_sync(self, records: list[dict], revision: str) -> None:
        with self._lock, self._conn:
            self._conn.executemany("UPDATE sync_events SET pushed=1 WHERE id=?", ((e["id"],) for e in records))
            events.set_meta(self._conn, "last_sync", events.utc())
            events.set_meta(self._conn, "imported_revision", revision)

    def study_rows(self) -> list[dict]:
        with self._lock:
            return [dict(r) for r in self._conn.execute(
                "SELECT id, problem_id, kind, verdict, elapsed_ms, hints_used, ai_lines, solution_seen, "
                "syntax_error, created_at, review_source FROM submissions LEFT JOIN sync_versions v ON v.type='submissions' AND v.local_id=id "
                "WHERE kind IN ('submit','review') ORDER BY created_at,v.entity,id")]

    def extra_catalog(self) -> list[dict]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT 'x-' || id AS id, parent_id, deleted, json_extract(spec_json,'$.title') AS title, "
                "json_extract(spec_json,'$.mode') AS mode, json_extract(spec_json,'$.practice_skill') AS practice_skill, "
                "json_extract(spec_json,'$.review_format') AS review_format, json_extract(spec_json,'$.review_skills') "
                "AS review_skills FROM extra_problems WHERE status='ready' ORDER BY id")
            return [dict(r) | {"review_skills": json.loads(r["review_skills"]) if r["review_skills"] else None}
                    for r in rows]

    def initialize_reviews(self, counted: set[str]) -> None:
        if self._reviews_ready:
            return
        with self._write():
            if not self._conn.execute("INSERT OR IGNORE INTO settings VALUES ('reviews_initialized',1)").rowcount:
                self._reviews_ready = True
                return
            # 旧库可能先失败后通过；按原始日期排期，保留已经到期的练习。
            existing = {r[0] for r in self._conn.execute("SELECT problem_id FROM reviews")}
            seen = set()
            rows = self._conn.execute("SELECT problem_id, verdict, hints_used, ai_lines, solution_seen, created_at "
                                      "FROM submissions LEFT JOIN sync_versions v ON v.type='submissions' AND v.local_id=id "
                                      "WHERE kind='submit' ORDER BY created_at,v.entity,id")
            for r in rows:
                pid = r["problem_id"]
                if pid not in existing and r["verdict"] == "accepted" and (pid in counted or r["ai_lines"]):
                    result = "new" if pid not in seen and independent(r) else "rewrite"
                    self._enroll(pid, r["created_at"], result, reset=bool(r["ai_lines"] or r["solution_seen"]))
                seen.add(pid)
        self._reviews_ready = True

    def review_rows(self) -> list[dict]:
        with self._lock:
            return [dict(r) for r in self._conn.execute("SELECT * FROM reviews")]

    def _limit(self) -> int:
        row = self._conn.execute("SELECT value FROM settings WHERE key='daily_limit'").fetchone()
        return row[0] if row else 5

    def daily_limit(self) -> int:
        with self._lock:
            return self._limit()

    def set_limit(self, value: int) -> None:
        with self._write():
            self._conn.execute("INSERT OR REPLACE INTO settings VALUES ('daily_limit', ?)", (value,))

    def _enroll(self, pid: str, stamp: str, result: str, reset: bool = False) -> None:
        _, due = schedule(local_day(stamp), 0, False)
        self._conn.execute("INSERT OR IGNORE INTO reviews(problem_id,step,due,result) VALUES (?,0,?,?)",
                           (pid, due, result))
        if reset:
            self._conn.execute("UPDATE reviews SET step=0,rounds=0,rewrite_target=NULL,due=?,result='rewrite' WHERE problem_id=?", (due, pid))

    def _check_review(self, source: str, due: str, stamp: str) -> sqlite3.Row:
        day = local_day(stamp).isoformat()
        row = self._conn.execute("SELECT * FROM reviews WHERE problem_id=?", (source,)).fetchone()
        done = self._conn.execute("SELECT COUNT(*) FROM reviews WHERE last_reviewed=?", (day,)).fetchone()[0]
        if not row or row["due"] != due or due > day or done >= self._limit():
            raise ReviewConflict("这轮复习已结束或未到期，请返回今日计划。")
        return row

    def record_help(self, pid: str, *, solution: bool, source: str = "", due: str = "", author: int = 0) -> None:
        stamp = now()
        with self._write():
            if source:
                self._check_review(source, due, stamp)
            self._conn.execute(
                "INSERT INTO study_help(problem_id, attempt, author_hints, ai_hints, solution_seen) VALUES (?,?,?,?,?) "
                "ON CONFLICT(problem_id,attempt) DO UPDATE SET author_hints=MAX(author_hints,excluded.author_hints), "
                "ai_hints=ai_hints+excluded.ai_hints, solution_seen=MAX(solution_seen,excluded.solution_seen)",
                (pid, f"{source}/{due}", author, int(not solution and not author), int(solution)))
            if solution:
                self._enroll(source or pid, stamp, "rewrite")
                _, tomorrow = schedule(local_day(stamp), 0, False)
                self._conn.execute("UPDATE reviews SET step=0,rounds=0,rewrite_target=?,due=?,result='rewrite', "
                                   "last_reviewed=CASE WHEN ? THEN ? ELSE last_reviewed END WHERE problem_id=?",
                                   (pid, tomorrow, bool(source), local_day(stamp).isoformat(), source or pid))

    # ---------- 提交 ----------

    def add_submission(
        self,
        *,
        problem_id: str,
        track: str,
        kind: str,
        code: str,
        result: dict[str, Any],
        elapsed_ms: int | None,
        hints_used: int,
        ai_lines: int = 0,
        counted: bool = False,
        review_source: str = "",
        review_due: str = "",
    ) -> int:
        stamp = now()
        with self._write():
            # 日程和交卷记录在同一写事务内提交；跨连接的重复交卷也只能推进一次。
            review = self._check_review(review_source, review_due, stamp) if review_source else None
            help_row = self._conn.execute("SELECT * FROM study_help WHERE problem_id=? AND attempt=?",
                                          (problem_id, f"{review_source}/{review_due}")).fetchone()
            solution = bool(help_row and help_row["solution_seen"])
            if help_row:
                hints_used = max(hints_used, help_row["author_hints"]) + help_row["ai_hints"]
            verdict = result["verdict"]
            first = not self._conn.execute("SELECT 1 FROM submissions WHERE problem_id=? AND kind='submit' LIMIT 1",
                                           (problem_id,)).fetchone()
            cur = self._conn.execute(
                "INSERT INTO submissions (problem_id,track,kind,code,verdict,passed,total,elapsed_ms,hints_used,"
                "ai_lines,solution_seen,syntax_error,review_source,result_json,created_at) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (problem_id, track, kind, code, verdict, result.get("passed"), result.get("total"), elapsed_ms,
                 hints_used, ai_lines, solution, syntax_error(result), review_source or None,
                 json.dumps(result, ensure_ascii=False), stamp),
            )
            clean = verdict == "accepted" and not (solution or hints_used or ai_lines)
            if kind == "review" and review:
                rewriting = review["result"] == "rewrite" or bool(review["rewrite_target"])
                step, due = schedule(local_day(stamp), review["step"], clean, rewriting)
                rounds = 0 if rewriting else review["rounds"] + 1
                # 看过答案或有协助时，次日仍要求写回实际做过的那道变式。
                retry = problem_id if not clean and (rewriting or ai_lines or hints_used or solution) else None
                self._conn.execute("UPDATE reviews SET step=?,rounds=?,rewrite_target=?,due=?,result=?,last_reviewed=? "
                                   "WHERE problem_id=?", (step, rounds, retry, due if counted or not clean else None,
                                   "passed" if clean else "failed", local_day(stamp).isoformat(), review_source))
            elif kind == "submit" and verdict == "accepted" and (counted or solution or ai_lines):
                self._enroll(problem_id, stamp, "new" if clean and first else "rewrite", reset=bool(ai_lines or solution))
            return int(cur.lastrowid)

    def submissions(self, problem_id: str, limit: int = 50) -> list[dict[str, Any]]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT id, kind, code, verdict, passed, total, elapsed_ms, hints_used, ai_lines, created_at"
                " FROM submissions LEFT JOIN sync_versions v ON v.type='submissions' AND v.local_id=id"
                " WHERE problem_id = ? AND kind IN ('submit','review') ORDER BY created_at DESC,v.entity DESC,id DESC LIMIT ?",
                (problem_id, limit),
            ).fetchall()
        return [dict(r) for r in rows]

    def project_answers(self, part_ids: list[str]) -> dict[str, str]:
        slots = ",".join("?" for _ in part_ids)
        with self._lock:
            rows = self._conn.execute(f"""
                SELECT problem_id, code FROM (
                    SELECT problem_id, code, ROW_NUMBER() OVER (
                        PARTITION BY problem_id ORDER BY created_at DESC, v.entity DESC, id DESC
                    ) AS rank FROM submissions
                    LEFT JOIN sync_versions v ON v.type='submissions' AND v.local_id=id
                    WHERE problem_id IN ({slots}) AND kind IN ('submit','review') AND verdict='accepted'
                ) WHERE rank=1""", part_ids)
            return dict(rows)

    def complete_project(self, project_id: str) -> None:
        with self._write():
            self._conn.execute("INSERT OR IGNORE INTO project_completions VALUES (?,?)", (project_id, now()))

    def project_completed(self, project_id: str) -> bool:
        with self._lock:
            return self._conn.execute("SELECT 1 FROM project_completions WHERE project_id=?", (project_id,)).fetchone() is not None

    def latest_result(self, problem_id: str) -> dict[str, Any] | None:
        """最近一次运行或提交的判题结果（给 AI 助教当上下文）。"""
        with self._lock:
            row = self._conn.execute(
                "SELECT result_json FROM submissions LEFT JOIN sync_versions v ON v.type='submissions' AND v.local_id=id "
                "WHERE problem_id = ? ORDER BY created_at DESC,v.entity DESC,id DESC LIMIT 1", (problem_id,)
            ).fetchone()
        return json.loads(row["result_json"]) if row else None

    def last_active_by_track(self) -> dict[str, str]:
        """附加题的运行和提交也使用原题的 track。"""
        with self._lock:
            return dict(self._conn.execute("SELECT track, MAX(created_at) FROM submissions GROUP BY track"))

    def has_passed(self, problem_id: str) -> bool:
        with self._lock:
            return self._conn.execute(
                "SELECT 1 FROM submissions WHERE problem_id=? AND kind IN ('submit','review') AND verdict='accepted' LIMIT 1",
                (problem_id,),
            ).fetchone() is not None

    def status_by_problem(self, track: str) -> dict[str, str]:
        """solved：有不靠 AI 修改的通过；assisted：只有用过 AI 修改的通过；attempted：提交过没通过。"""
        with self._lock:
            rows = self._conn.execute(
                "SELECT problem_id,"
                " MAX(verdict = 'accepted' AND ai_lines = 0) AS solo,"
                " MAX(verdict = 'accepted') AS any_ok"
                " FROM submissions WHERE track = ? AND kind IN ('submit','review') GROUP BY problem_id",
                (track,),
            ).fetchall()
        out = {}
        for r in rows:
            out[r["problem_id"]] = "solved" if r["solo"] else ("assisted" if r["any_ok"] else "attempted")
        return out

    # ---------- AI 对话 ----------

    def _memory_setting(self) -> tuple[bool, str | None]:
        row = self._conn.execute(
            "SELECT value,event_id FROM settings LEFT JOIN sync_versions "
            "ON type='settings' AND entity=json_array(key) WHERE key='memory_enabled'"
        ).fetchone()
        return (bool(row["value"]), row["event_id"]) if row else (True, None)

    def memory_enabled(self) -> bool:
        with self._lock:
            return self._memory_setting()[0]

    def set_memory_enabled(self, enabled: bool) -> None:
        with self._write():
            if self._memory_setting()[0] != enabled:
                self._conn.execute("INSERT OR REPLACE INTO settings VALUES ('memory_enabled', ?)", (enabled,))
                self._reset_review_cursor()

    def _memory_snapshot(self, setting_version: str | None) -> MemorySnapshot:
        rows = self._conn.execute(
            "SELECT n.*,v.event_id FROM memory_notes n JOIN sync_versions v "
            "ON v.type='memory_notes' AND v.entity=json_array(n.name)"
        )
        notes, versions = [], {}
        for row in rows:
            versions[row["name"]] = row["event_id"]
            if not row["deleted"]:
                notes.append(dict(row))
        return MemorySnapshot(notes, versions, setting_version, self._clear_generation())

    def memory_snapshot(self) -> MemorySnapshot | None:
        with self._lock, self._conn:
            self._conn.execute("BEGIN")
            enabled, version = self._memory_setting()
            return self._memory_snapshot(version) if enabled else None

    def latest_progress_body(self, skills: set[str]) -> str | None:
        slots = ",".join("?" for _ in skills)
        with self._lock:
            row = self._conn.execute(
                f"SELECT body FROM memory_notes WHERE deleted=0 AND type='progress' AND scope IN ({slots}) "
                "AND COALESCE((SELECT value FROM settings WHERE key='memory_enabled'),1) "
                "ORDER BY as_of DESC,name LIMIT 1", tuple(skills)).fetchone()
            return row[0] if row else None

    def _delete_memory(self, name: str | None = None) -> None:
        sql = "UPDATE memory_notes SET deleted=1,type=NULL,description=NULL,scope=NULL,as_of=NULL,body=NULL WHERE deleted=0"
        if name is None:
            self._conn.execute(sql)
        else:
            self._conn.execute(sql + " AND name=?", (name,))

    def _clear_generation(self) -> int:
        return int(events.meta(self._conn, "memory_clear_generation", "0"))

    def clear_memory(self) -> None:
        with self._write():
            self._delete_memory()
            self._reset_review_cursor()
            events.set_meta(self._conn, "memory_clear_generation", str(self._clear_generation() + 1))

    def _apply_memory(self, snapshot: MemorySnapshot, operations: list[dict], *, review_day: str = "") -> bool:
        if self._clear_generation() != snapshot.clear_generation or self._memory_setting() != (True, snapshot.setting_version):
            return False
        # 同一答复的操作依次执行。本事务的事件在 finish_capture 时才登记。
        for op in operations:
            name, note = op["name"], op["note"]
            if len(name) > NAME_LIMIT or (note is not None and (
                len(note["description"]) > DESCRIPTION_LIMIT or len(note["body"]) > BODY_LIMIT
            )):
                continue
            row = self._conn.execute("SELECT v.event_id,n.type,n.as_of FROM sync_versions v JOIN memory_notes n "
                                     "ON n.name=? WHERE v.type='memory_notes' AND v.entity=?",
                                     (name, events.encode([name]))).fetchone()
            if (row["event_id"] if row else None) != snapshot.versions.get(name):
                continue
            if review_day:
                if note is not None and note["type"] != "progress":
                    continue
                evidence_day = min(review_day, note["as_of"]) if note else review_day
                if row and row["type"] and (row["type"] != "progress" or row["as_of"] > evidence_day):
                    continue
            if note is None:
                self._delete_memory(name)
            else:
                self._conn.execute(
                    "INSERT OR REPLACE INTO memory_notes(name,type,description,scope,as_of,body) VALUES (?,?,?,?,?,?)",
                    (name, note["type"], " ".join(note["description"].splitlines()), note["scope"], note["as_of"], note["body"]),
                )
        return True

    def _reset_review_cursor(self) -> None:
        tail = self._conn.execute("SELECT MAX(timestamp) FROM sync_events WHERE machine=?",
                                  (self.journal.machine,)).fetchone()[0]
        events.set_meta(self._conn, "memory_review_cursor", tail or "")

    def _review_evidence(self, event: sqlite3.Row) -> ReviewEvidence:
        row = json.loads(event["payload"])["row"]
        pid = self.journal.ref(row["problem_id"], importing=True)
        skills = None
        if pid.startswith("x-"):
            pid, practice, refs = self._conn.execute(
                "SELECT parent_id,COALESCE(json_extract(spec_json,'$.practice_skill'), practice_skill),"
                "json_extract(spec_json,'$.review_skills') FROM extra_problems WHERE id=?",
                (pid[2:],)).fetchone()
            if practice:
                skills = [practice]
            elif refs:
                refs = json.loads(refs)
                skills = ([refs["introduces"]] if refs["introduces"] else []) + refs["requires"]

        flags = []
        if row.get("hints_used") or row.get("author_hints") or row.get("ai_hints"):
            flags.append("提示")
        if row.get("ai_lines"):
            flags.append("AI改码")
        if row["solution_seen"]:
            flags.append("题解")
        if event["type"] == "submissions":
            result = json.loads(row["result_json"])
            outcome = " ".join([row["verdict"], *(flags or ["独立"])])
            if mistake := result.get("misconception"):
                outcome += " " + mistake["id"]
        else:
            outcome = "求助 " + " ".join(flags)
        day = local_day(row.get("created_at") or event["timestamp"])
        return ReviewEvidence(pid, day.isoformat(), outcome, row.get("track", ""), skills)

    def claim_memory_review(self, day: str, *, after_submit: bool) -> ReviewBatch | None:
        with self._lock, self._conn:
            self._conn.execute("BEGIN IMMEDIATE")
            enabled, version = self._memory_setting()
            if not enabled or events.meta(self._conn, "memory_review_day") >= day:
                return None
            # 历史库导入的 UUIDv5 也挂在本机名下。回顾只取本机正常采集的事件。
            where = "FROM sync_events WHERE machine=? AND timestamp>? AND substr(id,15,1)!='5' AND "
            params = (self.journal.machine, events.meta(self._conn, "memory_review_cursor"))
            formal = "(type='submissions' AND json_extract(payload,'$.row.kind') IN ('submit','review'))"
            if after_submit and not self._conn.execute("SELECT 1 " + where + formal + " LIMIT 1 OFFSET 3", params).fetchone():
                return None
            rows = self._conn.execute("SELECT timestamp,type,payload " + where + "(type='study_help' OR " + formal +
                                      ") ORDER BY timestamp LIMIT 24", params).fetchall()
            if not rows:
                return None
            events.set_meta(self._conn, "memory_review_day", day)
            return ReviewBatch(self._memory_snapshot(version), [self._review_evidence(r) for r in rows], rows[-1]["timestamp"])

    def finish_memory_review(self, batch: ReviewBatch, operations: list[dict]) -> None:
        with self._write():
            if self._apply_memory(batch.snapshot, operations, review_day=max(e.day for e in batch.evidence)):
                events.set_meta(self._conn, "memory_review_cursor", batch.through)

    @staticmethod
    def _chat_row(r: sqlite3.Row) -> dict[str, Any]:
        edits = json.loads(r["edit_json"]) if r["edit_json"] else []
        if isinstance(edits, dict):  # 早期单条修改建议的存法
            edits = [edits]
        for edit in edits:
            edit.setdefault("target", "answer")  # 旧记录只改答案
        agent = None
        if r["role"] == "assistant":
            notes = json.loads(r["notes"]) if r["notes"] else None
            agent = notes["agent"] if isinstance(notes, dict) else "claude"
        return {
            "id": r["id"],
            "role": r["role"],
            "agent": agent,
            "content": r["content"],
            "edits": edits,
            "applied": bool(r["applied"]),
            "created_at": r["created_at"],
        }

    def add_chat(
        self, problem_id: str, role: str, content: str, edits: list[dict[str, Any]] | None = None,
        notes: list[str] | None = None, *, agent: str | None = None,
        snapshot: MemorySnapshot | None = None, memory: list[dict] | None = None,
    ) -> dict[str, Any]:
        metadata = {"agent": agent, "notes": notes or []} if agent else notes
        with self._write():
            cur = self._conn.execute(
                "INSERT INTO chat_messages (problem_id, role, content, edit_json, notes, created_at)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                (
                    problem_id, role, content,
                    json.dumps(edits, ensure_ascii=False) if edits else None,
                    json.dumps(metadata, ensure_ascii=False) if metadata else None,
                    now(),
                ),
            )
            row = self._conn.execute("SELECT * FROM chat_messages WHERE id = ?", (cur.lastrowid,)).fetchone()
            if snapshot is not None and memory:
                self._apply_memory(snapshot, memory)
        return self._chat_row(row)

    def chat(self, problem_id: str) -> list[dict[str, Any]]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT m.* FROM chat_messages m LEFT JOIN sync_versions v ON v.type='chat_messages' AND v.local_id=m.id "
                "WHERE problem_id = ? ORDER BY created_at,v.entity,m.id", (problem_id,)
            ).fetchall()
        return [self._chat_row(r) for r in rows]

    def mark_applied(self, problem_id: str, message_id: int) -> bool:
        with self._write():
            cur = self._conn.execute(
                "UPDATE chat_messages SET applied = 1 WHERE id = ? AND problem_id = ? AND edit_json IS NOT NULL",
                (message_id, problem_id),
            )
            return cur.rowcount == 1

    def applied_count(self, problem_id: str) -> int:
        with self._lock:
            row = self._conn.execute(
                "SELECT COUNT(*) AS n FROM chat_messages WHERE problem_id = ? AND applied = 1", (problem_id,)
            ).fetchone()
        return int(row["n"])

    # ---------- 附加题 ----------

    @staticmethod
    def _extra_row(r: sqlite3.Row) -> dict[str, Any]:
        spec = json.loads(r["spec_json"]) if r["spec_json"] else None
        return {
            "id": f"x-{r['id']}",
            "row_id": r["id"],
            "parent_id": r["parent_id"],
            "seq": r["seq"],
            "title": spec["title"] if spec else None,
            "request": r["request"],
            "practice_skill": r["practice_skill"],
            "status": r["status"],
            "error": r["error"],
            "spec": spec,
            "deleted": bool(r["deleted"]),
            "created_at": r["created_at"],
        }

    def create_extra(self, parent_id: str, request: str, practice_skill: str | None = None) -> dict[str, Any]:
        with self._write():
            row = self._conn.execute(
                "SELECT COALESCE(MAX(seq), 0) AS m FROM extra_problems WHERE parent_id = ?", (parent_id,)
            ).fetchone()
            cur = self._conn.execute(
                "INSERT INTO extra_problems (parent_id, seq, request, practice_skill, status, created_at, updated_at)"
                " VALUES (?, ?, ?, ?, 'generating', ?, ?)",
                (parent_id, int(row["m"]) + 1, request, practice_skill, now(), now()),
            )
            r = self._conn.execute("SELECT * FROM extra_problems WHERE id = ?", (cur.lastrowid,)).fetchone()
        return self._extra_row(r)

    def finish_extra(self, row_id: int, spec: dict[str, Any], notes: list[str]) -> None:
        with self._write():
            self._conn.execute(
                "UPDATE extra_problems SET status = 'ready', spec_json = ?, notes = ?, updated_at = ? WHERE id = ?",
                (json.dumps(spec, ensure_ascii=False), json.dumps(notes, ensure_ascii=False), now(), row_id),
            )

    def fail_extra(self, row_id: int, error: str) -> None:
        with self._write():
            self._conn.execute(
                "UPDATE extra_problems SET status = 'failed', error = ?, updated_at = ? WHERE id = ?",
                (error[:2000], now(), row_id),
            )

    def extras(self, parent_id: str) -> list[dict[str, Any]]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT * FROM extra_problems WHERE parent_id = ? AND deleted = 0 ORDER BY seq", (parent_id,)
            ).fetchall()
        return [self._extra_row(r) for r in rows]

    def get_extra(self, row_id: int) -> dict[str, Any] | None:
        with self._lock:
            r = self._conn.execute("SELECT * FROM extra_problems WHERE id = ?", (row_id,)).fetchone()
        return self._extra_row(r) if r else None

    def delete_extra(self, parent_id: str, seq: int) -> bool:
        with self._write():
            cur = self._conn.execute(
                "UPDATE extra_problems SET deleted = 1, updated_at = ? WHERE parent_id = ? AND seq = ? AND deleted = 0",
                (now(), parent_id, seq),
            )
            return cur.rowcount == 1

    def clear_chat(self, problem_id: str) -> None:
        with self._write():
            self._conn.execute("DELETE FROM chat_messages WHERE problem_id = ?", (problem_id,))
