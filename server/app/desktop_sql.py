"""桌面动态 SQL 任务交给已打开的浏览器，沿用与 Node 相同的 PGlite 校验器。"""

from concurrent.futures import Future, TimeoutError
from threading import Lock
from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/desktop/sql")
lock = Lock()
waiting: dict[str, dict] = {}
replies: dict[str, Future] = {}


class Reply(BaseModel):
    tables: list | None = None
    error: str | None = None


def execute(job: dict) -> list:
    key = str(uuid4())
    future = Future()
    with lock:
        waiting[key] = job
        replies[key] = future
    try:
        reply = future.result(timeout=50)
        if reply.error or reply.tables is None:
            raise ValueError(reply.error or "浏览器没有返回 SQL 结果")
        return reply.tables
    except TimeoutError as exc:
        raise ValueError("等待浏览器验证 SQL 超时，请打开练习页面并重试") from exc
    finally:
        with lock:
            waiting.pop(key, None)
            replies.pop(key, None)


@router.post("/next")
def take():
    with lock:
        if waiting:
            key = next(iter(waiting))
            return {"id": key, "job": waiting.pop(key)}
    return None


@router.post("/{key}")
def finish(key: str, reply: Reply):
    with lock:
        if (future := replies.get(key)) and not future.done():
            future.set_result(reply)
