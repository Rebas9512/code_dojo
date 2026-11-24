#!/usr/bin/env python3
"""用本机原生 CPython 3.14 跑每道 Python 题的参考解（内容侧的快速自检，不需要 Docker）。

检查项：
  - function / class / stdio：solution.py 通过 tests.json 的全部用例（examples + hidden）；
    用例数量：examples ≥ 2、hidden ≥ 3。
  - predict：solution.py 能运行、有输出、两次运行输出一致；把输出打印出来方便人工核对。
  - fix：starter.py 至少挂一个 examples 用例（让学习者点"运行"就能看到 bug）。
  - complete：starter.py 不能通过全部用例（空没填时必须失败）。
  - 课（problems/<学习线>/lessons/*/lesson.yaml）里的每个 example：带上它的 stdin 能正常运行、有输出。
比较规则和平台判题程序 judge/python/harness.py 保持一致（exact / unordered / float / checker，
stdio 去掉行尾空白和末尾空行）。

用法：
  python3 scripts/curriculum/verify_python.py [--only py-0a-01] [-q]
不是 3.14 时会自动改用：uv run --quiet --no-project --python 3.14 --with pyyaml python <本文件>
"""
from __future__ import annotations

import argparse
import copy
import io
import json
import math
import os
import signal
import sys
from contextlib import redirect_stdout
from pathlib import Path

if sys.version_info[:2] != (3, 14) and not os.environ.get("CODE_DOJO_NO_REEXEC"):
    os.environ["CODE_DOJO_NO_REEXEC"] = "1"
    cmd = ["uv", "run", "--quiet", "--no-project", "--python", "3.14", "--with", "pyyaml",
           "python", str(Path(__file__).resolve()), *sys.argv[1:]]
    os.execvpe("uv", cmd, os.environ)

import yaml  # noqa: E402

from track_files import Track, active_tracks, lesson_files, stage_dirs, verify_projects


# ---------- LeetCode 风格结构（和平台 harness 一致） ----------
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def list_to_listnode(values):
    dummy = cur = ListNode()
    for v in values or []:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def listnode_to_list(node):
    out = []
    while node is not None and len(out) < 100000:
        out.append(node.val)
        node = node.next
    return out


def list_to_treenode(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, i, head = [root], 1, 0
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


TO_NATIVE = {"listnode": list_to_listnode, "treenode": list_to_treenode}
FROM_NATIVE = {"listnode": listnode_to_list, "treenode": treenode_to_list}


def normalize(value):
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
    return value


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
        key = lambda v: json.dumps(v, sort_keys=True, ensure_ascii=False)  # noqa: E731
        return sorted(expected, key=key) == sorted(actual, key=key)
    return expected == actual


def normalize_text(text):
    lines = [line.rstrip() for line in (text or "").replace("\r\n", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


class Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise Timeout()


def run_limited(fn, ms, stdin_text=""):
    """返回 (ok, value_or_error, stdout)。"""
    buf = io.StringIO()
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(stdin_text)
    signal.signal(signal.SIGALRM, _alarm)
    signal.setitimer(signal.ITIMER_REAL, ms / 1000)
    try:
        with redirect_stdout(buf):
            value = fn()
        return True, value, buf.getvalue()
    except Timeout:
        return False, f"超时（>{ms} ms）", buf.getvalue()
    except BaseException as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}", buf.getvalue()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        sys.stdin = old_stdin


def fresh_ns(main=False):
    return {"__name__": "__main__" if main else "solution", "__builtins__": __builtins__,
            "ListNode": ListNode, "TreeNode": TreeNode}


def judge(meta: dict, code_text: str, cases: list[dict], checker=None) -> list[tuple[bool, str]]:
    """对每个用例返回 (是否通过, 说明)。"""
    mode = meta["mode"]
    ms = meta.get("time_limit_ms", 2000)
    try:
        code = compile(code_text, "user.py", "exec")
    except SyntaxError as exc:
        return [(False, f"语法错误：{exc}") for _ in cases]
    results = []
    for case in cases:
        if mode == "function":
            conv = meta.get("convert") or {}
            arg_conv = {int(k): v for k, v in (conv.get("args") or {}).items()}
            ns = fresh_ns()

            def call():
                exec(code, ns)
                fn = ns[meta["entry"]]
                args = copy.deepcopy(case["args"])
                return fn(*[TO_NATIVE[arg_conv[i]](a) if i in arg_conv else a for i, a in enumerate(args)])

            ok, val, _ = run_limited(call, ms)
            if not ok:
                results.append((False, f"args={case['args']} 出错：{val}"))
                continue
            ret = conv.get("returns")
            actual = FROM_NATIVE[ret](val) if ret else normalize(val)
            if checker:
                passed = bool(checker(copy.deepcopy(case["args"]), case.get("expected"), actual))
            else:
                passed = values_equal(case["expected"], actual, meta.get("compare", "exact"))
            results.append((passed, "" if passed else f"args={case['args']} 期望={case['expected']!r} 实际={actual!r}"))
        elif mode == "class":
            ns = fresh_ns()

            def run_ops():
                exec(code, ns)
                obj = ns[meta["entry"]](*copy.deepcopy(case["args"][0]))
                outs = [None]
                for op, a in zip(case["ops"][1:], copy.deepcopy(case["args"][1:])):
                    outs.append(normalize(getattr(obj, op)(*a)))
                return outs

            ok, val, _ = run_limited(run_ops, ms)
            if not ok:
                results.append((False, f"ops={case['ops']} 出错：{val}"))
                continue
            exp = case["expected"]
            passed = len(val) == len(exp) and all(
                values_equal(e, a, meta.get("compare", "exact")) for e, a in zip(exp, val))
            results.append((passed, "" if passed else f"ops={case['ops']} 期望={exp} 实际={val}"))
        elif mode == "stdio":
            ns = fresh_ns(main=True)
            ok, val, out = run_limited(lambda: exec(code, ns), ms, case.get("stdin", ""))
            if not ok:
                results.append((False, f"stdin={case['stdin']!r} 出错：{val}"))
                continue
            passed = normalize_text(out) == normalize_text(case["expected"])
            results.append((passed, "" if passed else f"stdin={case['stdin']!r} 期望={case['expected']!r} 实际={out!r}"))
    return results


def load_checker(d: Path):
    p = d / "checker.py"
    if not p.exists():
        return None
    ns = {"__name__": "checker"}
    exec(compile(p.read_text(encoding="utf-8"), str(p), "exec"), ns)
    return ns["check"]


def verify(d: Path, quiet: bool) -> list[str]:
    meta = yaml.safe_load((d / "problem.yaml").read_text(encoding="utf-8"))
    problems: list[str] = []
    sol = (d / "solution.py").read_text(encoding="utf-8")
    mode = meta["mode"]

    if mode == "predict":
        outs = []
        for _ in range(2):
            ok, val, out = run_limited(lambda: exec(compile(sol, "user.py", "exec"), fresh_ns(main=True)),
                                       meta.get("time_limit_ms", 2000))
            if not ok:
                problems.append(f"展示的程序运行出错：{val}")
                break
            outs.append(out)
        if not problems:
            if not outs[0].strip():
                problems.append("展示的程序没有输出")
            elif outs[0] != outs[1]:
                problems.append("两次运行输出不一致（预测题必须确定）")
            elif not quiet:
                print("      输出：" + " | ".join(normalize_text(outs[0]).split("\n")))
        return problems

    tests = json.loads((d / "tests.json").read_text(encoding="utf-8"))
    examples, hidden = tests.get("examples", []), tests.get("hidden", [])
    if len(examples) < 2 or len(hidden) < 3:
        problems.append(f"用例不够：examples {len(examples)}（至少 2），hidden {len(hidden)}（至少 3）")
    checker = load_checker(d) if meta.get("compare") == "checker" else None
    res = judge(meta, sol, examples + hidden, checker)
    bad = [msg for ok, msg in res if not ok]
    if bad:
        problems.append(f"参考解没通过 {len(bad)}/{len(res)} 个用例：" + "；".join(bad[:3]))

    fmt = meta.get("format")
    if fmt in ("fix", "complete"):
        starter_path = d / "starter.py"
        if not starter_path.exists():
            problems.append(f"{fmt} 题缺少 starter.py")
        else:
            starter = starter_path.read_text(encoding="utf-8")
            ex_res = judge(meta, starter, examples, checker)
            all_res = judge(meta, starter, examples + hidden, checker)
            ex_fail = sum(1 for ok, _ in ex_res if not ok)
            all_fail = sum(1 for ok, _ in all_res if not ok)
            if fmt == "fix" and ex_fail == 0:
                problems.append("fix 题的 starter 在 examples 上全部通过——学习者点\"运行\"看不到 bug")
            if all_fail == 0:
                problems.append(f"{fmt} 题的 starter 居然全部通过")
            if not quiet and not problems:
                print(f"      starter 挂掉 {all_fail}/{len(all_res)} 个用例（examples 里 {ex_fail} 个）")
    return problems


def verify_lessons(tracks: list[Track], quiet: bool) -> tuple[int, int]:
    """运行每个 lesson 示例，返回（示例数, 失败数）。"""
    total = failed = 0
    for yml in lesson_files(tracks):
        lesson = yaml.safe_load(yml.read_text(encoding="utf-8")) or {}
        for i, st in enumerate(lesson.get("steps") or [], 1):
            if (st or {}).get("type") != "example" or "data" in st:
                continue
            total += 1
            code = st.get("code") or ""
            try:
                compiled = compile(code, "example.py", "exec")
            except SyntaxError as exc:
                failed += 1
                print(f"✗ {yml.parent.name} 第 {i} 步（{st.get('skill')}）语法错误：{exc}")
                continue
            ok, val, out = run_limited(lambda: exec(compiled, fresh_ns(main=True)), 2000, st.get("stdin") or "")
            if not ok or not out.strip():
                failed += 1
                print(f"✗ {yml.parent.name} 第 {i} 步（{st.get('skill')}）{'运行出错：' + str(val) if not ok else '没有输出'}")
            elif not quiet:
                print(f"  {yml.parent.name} 第 {i:>2} 步 {st.get('skill'):<24} 输出：" + " | ".join(normalize_text(out).split("\n"))[:110])
    return total, failed


def ensure_deep_stack() -> None:
    """和判题镜像一致：栈 256 MB（docker --ulimit stack=256MB）+ 递归上限 200000（harness.py）。
    主线程的栈大小在进程启动时就定了，所以调高软上限后重新 exec 自己一次；超时靠 SIGALRM，必须留在主线程。"""
    import resource
    want = 256 * 1024 * 1024
    soft, hard = resource.getrlimit(resource.RLIMIT_STACK)
    if os.environ.get("CODE_DOJO_DEEP_STACK") != "1" and soft != resource.RLIM_INFINITY and soft < want:
        new = want if hard == resource.RLIM_INFINITY else min(want, hard)
        if new > soft:
            resource.setrlimit(resource.RLIMIT_STACK, (new, hard))
            os.environ["CODE_DOJO_DEEP_STACK"] = "1"
            os.execv(sys.executable, [sys.executable, *sys.argv])
    sys.setrecursionlimit(200000)


def main() -> int:
    ensure_deep_stack()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", default="", help="只校验 id 以此开头的题")
    ap.add_argument("-q", "--quiet", action="store_true", help="不打印预测题输出等细节")
    args = ap.parse_args()
    print(f"Python {sys.version.split()[0]}（{sys.executable}）")
    dirs = []
    # 只查跑在普通 Python 镜像里的线；runtime: ds（numpy/pandas/torch）的题和课示例由 verify_bank.py 在 DS 镜像里跑
    python_tracks = active_tracks("python")
    tracks = [t for t in python_tracks if t.runtime == "python"]
    for sd in stage_dirs(tracks):
        if sd.exists():
            metas = []
            for d in sd.iterdir():
                if (d / "problem.yaml").exists() and d.name.startswith(args.only):
                    meta = yaml.safe_load((d / "problem.yaml").read_text(encoding="utf-8"))
                    if meta.get("format") != "inspect":
                        metas.append((meta.get("order", 0), d))
            dirs += [d for _, d in sorted(metas)]
    failed = 0
    for d in dirs:
        issues = verify(d, args.quiet)
        mark = "✗" if issues else "✓"
        if issues or not args.quiet:
            print(f"{mark} {d.name}")
        for i in issues:
            print(f"      {i}")
        failed += bool(issues)
    print(f"\n{len(dirs) - failed}/{len(dirs)} 道题通过")
    n_ex, bad_ex = verify_lessons(tracks, args.quiet)
    print(f"课的示例：{n_ex - bad_ex}/{n_ex} 个能正常运行")
    project_errors = verify_projects("python", python_tracks, args.only)
    return int(bool(failed or bad_ex or project_errors))


if __name__ == "__main__":
    sys.exit(main())
