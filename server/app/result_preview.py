"""判题完成后才生成显示用摘要，完整值留给判题器。"""

import json
import re
from typing import Any


def syntax_error(result: dict) -> bool:
    # Python 判题器捕获 SyntaxError（包括 IndentationError）后返回 compile_error。
    if result.get("verdict") == "compile_error":
        return True
    errors = [result.get("error"), *(c.get("error") for c in result.get("cases", []))]
    return any(re.search(r"(?m)^(SyntaxError|IndentationError):", e) for e in errors if isinstance(e, str))


def preview(value: Any, hidden: bool) -> tuple[Any, bool]:
    if value is None or value == "":
        return value, False
    raw = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    encoded = raw.encode("utf-8")
    if not hidden and len(encoded) <= 2048:
        return value, False
    prefix = encoded[:96 if hidden else 1984].decode("utf-8", errors="ignore")
    if hidden:
        prefix = prefix[:max(0, len(raw) // 2)]
    return f"{prefix} … （共 {len(raw)} 字符）", True


def compact_result(result: dict) -> dict:
    out = result.copy()
    for key in ("error", "stdout"):
        if key in out:
            out[key], _ = preview(out[key], False)
    if "cases" in out:
        out["cases"] = []
        for original in result["cases"]:
            case = original.copy()
            hidden = bool(case.get("hidden"))
            for key in ("input", "expected", "actual", "stdout", "error", "difference"):
                if key in case:
                    case[key], clipped = preview(case[key], hidden and key != "error")
                    if clipped:
                        case["preview"] = True
            out["cases"].append(case)
    return out
