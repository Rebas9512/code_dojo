"""code-dojo Python 判题程序：在工作目录读取 job.json，输出一行 JSON 结果。

job.json 字段：
  mode: function | class | stdio | predict
  entry: 函数名 / 类名（function、class 模式）
  compare: exact | unordered | float | checker | allclose | frame
  convert: {"args": {"0": "listnode"}, "returns": "listnode"}（可选）
  time_limit_ms: 每个用例的时限
  cases: 用例列表，格式见 docs/problem-format.md
  answer: predict 模式下用户写的预测输出
文件：user.py（用户代码；predict 模式下是要预测的程序），checker.py（可选）。

结果写到 stdout 的最后一行，前缀 RESULT_MARK，避免和用户 print 的内容混在一起。
"""

from __future__ import annotations

import copy
import io
import json
import math
import os
import sys
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, wait
from contextlib import redirect_stdout
from pathlib import Path

# -I 不会自动加入脚本目录。这里只加入随程序发布的 checker 工具。
sys.path.append(os.path.dirname(__file__))

RESULT_MARK = "@@CODE_DOJO_RESULT@@"
USER_FILE = "user.py"
MAX_STDOUT = 4000  # 每个用例最多回传的 print 输出字符数


# ---------- LeetCode 风格的数据结构 ----------

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val})"


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"


def list_to_listnode(values):
    dummy = ListNode()
    cur = dummy
    for v in values or []:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def listnode_to_list(node, limit=100000):
    out = []
    while node is not None and len(out) < limit:
        out.append(node.val)
        node = node.next
    return out


def list_to_treenode(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i, head = 1, 0
    while head < len(queue) and i < len(values):
        node = queue[head]
        head += 1
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def treenode_to_list(root):
    if root is None:
        return []
    out, queue, head = [], [root], 0
    while head < len(queue):
        node = queue[head]
        head += 1
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def to_dataframe(table):
    # 只在数据科学题传表时加载 pandas，普通 Python 镜像也能使用同一入口。
    import pandas as pd

    return pd.DataFrame(table["data"], columns=table["columns"], index=table.get("index"))


TO_NATIVE = {"listnode": list_to_listnode, "treenode": list_to_treenode, "dataframe": to_dataframe}
FROM_NATIVE = {"listnode": listnode_to_list, "treenode": treenode_to_list}


# ---------- 比较 ----------

def normalize(value):
    """把返回值转成可比较、可 JSON 序列化的形式。"""
    if isinstance(value, ListNode):
        return listnode_to_list(value)
    if isinstance(value, TreeNode):
        return treenode_to_list(value)
    if isinstance(value, (tuple, list)):
        return [normalize(v) for v in value]
    if isinstance(value, (set, frozenset)):
        items = [normalize(v) for v in value]
        try:
            return sorted(items)
        except TypeError:
            return items
    if isinstance(value, dict):
        return {str(k): normalize(v) for k, v in value.items()}
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return repr(value)
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    return repr(value)


def _sort_key(v):
    return json.dumps(v, sort_keys=True, ensure_ascii=False)


def float_equal(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=1e-6, abs_tol=1e-6)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(float_equal(x, y) for x, y in zip(a, b))
    return a == b


def values_equal(expected, actual, mode):
    if mode == "float":
        return float_equal(expected, actual)
    if mode == "unordered" and isinstance(expected, list) and isinstance(actual, list):
        return sorted(expected, key=_sort_key) == sorted(actual, key=_sort_key)
    return expected == actual


def normalize_text(text):
    lines = [line.rstrip() for line in (text or "").replace("\r\n", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


# ---------- 运行 ----------

class CaseTimeout(Exception):
    pass


def start_worker():
    # 所有用例共用一个大栈；新建的其他线程仍使用系统默认值。
    previous = threading.stack_size()
    try:
        for mib in range(256, 0, -1):
            try:
                threading.stack_size(mib * 1024 * 1024)
                executor = ThreadPoolExecutor(max_workers=1)
                executor.submit(lambda: None).result()
                return executor
            except (ValueError, RuntimeError):
                if mib == 1 or os.name != "nt":
                    raise
    finally:
        threading.stack_size(previous)


def user_traceback(exc):
    """只保留用户代码里的栈帧，行号对应编辑器里的行。"""
    frames = [f for f in traceback.extract_tb(exc.__traceback__) if f.filename == USER_FILE]
    lines = [f"第 {f.lineno} 行，在 {f.name} 中：{(f.line or '').strip()}" for f in frames[-5:]]
    lines.append(f"{type(exc).__name__}: {exc}")
    return "\n".join(lines)


def run_with_limit(fn, time_limit_ms):
    future = worker.submit(fn)
    done, _ = wait([future], timeout=time_limit_ms / 1000)
    if not done:
        raise CaseTimeout()
    return future.result()


def capture(fn, time_limit_ms, stdin_text=""):
    """运行 fn，捕获 print 输出、耗时和异常。"""
    buf = io.StringIO()
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(stdin_text, newline=None)
    start = time.perf_counter()
    status, value, error = "ok", None, None
    try:
        with redirect_stdout(buf):
            value = run_with_limit(fn, time_limit_ms)
    except CaseTimeout:
        status, error = "timeout", f"超过时限 {time_limit_ms} ms"
    except RecursionError as exc:
        status, error = "runtime_error", user_traceback(exc) + "\n（递归太深）"
    except MemoryError:
        status, error = "runtime_error", "MemoryError：内存超限"
    except BaseException as exc:  # noqa: BLE001 - 用户代码可能抛任何异常，包括 SystemExit
        status, error = "runtime_error", user_traceback(exc)
    finally:
        sys.stdin = old_stdin
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    out = buf.getvalue()
    if len(out) > MAX_STDOUT:
        out = out[:MAX_STDOUT] + "\n…（输出过长已截断）"
    return status, value, error, out, elapsed_ms


def compile_user(source):
    try:
        return compile(source, USER_FILE, "exec"), None
    except SyntaxError as exc:
        caret = ""
        if exc.text:
            caret = "\n" + exc.text.rstrip("\n") + "\n" + " " * max((exc.offset or 1) - 1, 0) + "^"
        return None, f"第 {exc.lineno} 行语法错误：{exc.msg}{caret}"


def fresh_namespace():
    return {
        "__name__": "solution",
        "__builtins__": __builtins__,
        "ListNode": ListNode,
        "TreeNode": TreeNode,
        "Optional": __import__("typing").Optional,
        "List": list,
    }


def load_checker():
    path = Path("checker.py")
    ns = {"__name__": "checker"}
    with open(path, encoding="utf-8") as f:
        exec(compile(f.read(), "checker.py", "exec"), ns)
    if "check_function" in ns:
        return ns["check_function"], True
    return ns["check"], False


def run_cases(cases, judge_one):
    """逐个跑用例；某个用例超时后，其余用例不再运行（每个都会等满时限）。"""
    results = []
    for i, case in enumerate(cases):
        result = judge_one(case)
        results.append(result)
        if result["status"] == "timeout":
            for rest in cases[i + 1:]:
                results.append(case_result(rest, "skipped", None, "前面的用例超时，未运行", "", 0))
            break
    return results


def judge_function(job, code):
    convert = job.get("convert") or {}
    arg_conv = {int(k): v for k, v in (convert.get("args") or {}).items()}
    ret_conv = convert.get("returns")
    checker = None

    def judge_one(case):
        ns = fresh_namespace()
        args = copy.deepcopy(case["args"])

        def call():
            nonlocal checker
            exec(code, ns)
            fn = ns.get(job["entry"])
            if fn is None:
                raise NameError(f"没有找到函数 {job['entry']}")
            expected = case.get("expected")
            if job["compare"] == "checker" and checker is None:
                checker = load_checker()
            if checker and checker[1]:
                try:
                    passed = checker[0](args, expected, fn)
                    return bool(passed), bool(passed), None
                except AssertionError as exc:
                    return False, False, str(exc)
            call_args = [TO_NATIVE[arg_conv[i]](a) if i in arg_conv else a for i, a in enumerate(args)]
            value = fn(*call_args)
            if job["compare"] in ("allclose", "frame"):
                from dojo_compare import compare_result
                actual, reason = compare_result(job["compare"], expected, value, job["compare_options"])
                return normalize(actual), reason is None, reason
            actual = FROM_NATIVE[ret_conv](value) if ret_conv else normalize(value)
            if checker is not None:
                try:
                    passed = checker[0](copy.deepcopy(case["args"]), expected, actual)
                    return actual, bool(passed), None
                except AssertionError as exc:
                    return actual, False, str(exc)
            return actual, values_equal(expected, actual, job["compare"]), None

        status, result, error, out, ms = capture(call, job["time_limit_ms"])
        actual = None
        if status == "ok":
            actual, passed, error = result
            status = "passed" if passed else "wrong_answer"
        return case_result(case, status, actual, error, out, ms)

    return run_cases(job["cases"], judge_one)


def judge_class(job, code):
    def judge_one(case):
        ns = fresh_namespace()
        ops, args = case["ops"], copy.deepcopy(case["args"])

        def run_ops():
            exec(code, ns)
            cls = ns.get(job["entry"])
            if cls is None:
                raise NameError(f"没有找到类 {job['entry']}")
            obj = cls(*args[0])
            outputs = [None]
            first_error = None
            for index, (op, op_args) in enumerate(zip(ops[1:], args[1:]), start=1):
                value = getattr(obj, op)(*op_args)
                if job["compare"] in ("allclose", "frame"):
                    expected = case["expected"][index]
                    error = None
                    if expected is None or value is None:
                        if value is not expected:
                            error = f"期望 {expected!r}，实际 {value!r}"
                    else:
                        from dojo_compare import compare_result
                        value, error = compare_result(job["compare"], expected, value, job["compare_options"])
                    if error and first_error is None:
                        first_error = f"第 {index} 次方法调用 {op}：{error}"
                outputs.append(normalize(value))
            return outputs, first_error

        status, value, error, out, ms = capture(run_ops, job["time_limit_ms"])
        actual = None
        if status == "ok":
            actual, error = value
            expected = case["expected"]
            passed = len(actual) == len(expected) and error is None
            if job["compare"] not in ("allclose", "frame"):
                passed = passed and all(values_equal(e, a, job["compare"]) for e, a in zip(expected, actual))
            status = "passed" if passed else "wrong_answer"
        return case_result(case, status, actual, error, out, ms)

    return run_cases(job["cases"], judge_one)


def judge_stdio(job, code):
    def judge_one(case):
        ns = fresh_namespace()
        ns["__name__"] = "__main__"
        status, _, error, out, ms = capture(lambda: exec(code, ns), job["time_limit_ms"], case.get("stdin", ""))
        actual = out
        if status == "ok":
            passed = normalize_text(out) == normalize_text(case["expected"])
            status = "passed" if passed else "wrong_answer"
        return case_result(case, status, actual, error, "", ms)

    return run_cases(job["cases"], judge_one)


def judge_predict(job, code):
    ns = fresh_namespace()
    ns["__name__"] = "__main__"
    status, _, error, out, ms = capture(lambda: exec(code, ns), job["time_limit_ms"])
    if status == "timeout":
        return [case_result({"answer": job.get("answer", "")}, status, None, error, out, ms)]
    if status != "ok":
        # 程序本身出错时，真实"输出"就是到出错为止打印的内容加上报错类型
        out = out + (error or "")
    passed = normalize_text(job.get("answer", "")) == normalize_text(out)
    case = {"answer": job.get("answer", "")}
    return [case_result(case, "passed" if passed else "wrong_answer", job.get("answer", ""), None, "", ms, expected=out)]


def case_result(case, status, actual, error, stdout, ms, expected=None):
    result = {
        "status": status,
        "input": {k: v for k, v in case.items() if k not in ("expected",)},
        "expected": case.get("expected") if expected is None else expected,
        "actual": actual,
        "error": error,
        "stdout": stdout,
        "time_ms": ms,
    }
    return result


def main():
    global worker
    sys.setrecursionlimit(200000)
    with open(sys.argv[1] if len(sys.argv) > 1 else "job.json", encoding="utf-8") as f:
        job = json.load(f)
    if len(sys.argv) > 2:
        if os.name == "nt":
            from windows_job import join_job
            join_job()
        # 本地 Linux 按地址空间限额，预留工作线程的虚拟栈。
        if sys.platform == "linux" and int(sys.argv[2]) > 0:
            import resource
            limit = int(sys.argv[2]) + 256 * 1024 * 1024
            _, hard = resource.getrlimit(resource.RLIMIT_AS)
            if hard != resource.RLIM_INFINITY:
                limit = min(limit, hard)
            resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
        if job.get("runtime") == "ds":
            sys.path.append(str(Path(__file__).resolve().parents[1] / "ds"))
    worker = start_worker()
    job.setdefault("compare", "exact")
    job.setdefault("compare_options", {})
    job.setdefault("time_limit_ms", 2000)
    with open("user.py", encoding="utf-8") as f:
        source = f.read()

    real_stdout = sys.stdout
    code, compile_error = compile_user(source)
    constraint_error = None
    if job.get("constraints") and not compile_error:
        from dojo_constraints import violation
        constraint_error = violation(source, job["constraints"])
    if compile_error:
        verdict = {"verdict": "compile_error", "error": compile_error, "cases": []}
    elif constraint_error:
        verdict = {"verdict": "constraint_error", "error": constraint_error, "cases": []}
    else:
        handler = {
            "function": judge_function,
            "class": judge_class,
            "stdio": judge_stdio,
            "predict": judge_predict,
        }[job["mode"]]
        cases = handler(job, code)
        statuses = [c["status"] for c in cases]
        if all(s == "passed" for s in statuses):
            verdict_name = "accepted"
        else:
            verdict_name = next(s for s in statuses if s != "passed")
        verdict = {
            "verdict": verdict_name,
            "passed": statuses.count("passed"),
            "total": len(statuses),
            "cases": cases,
        }
    real_stdout.write("\n" + RESULT_MARK + json.dumps(verdict, ensure_ascii=False, default=repr) + "\n")
    real_stdout.flush()
    if any(c["status"] == "timeout" for c in verdict["cases"]):
        os._exit(0)  # 工作线程可能仍在死循环，结果写完立即退出。


if __name__ == "__main__":
    main()
