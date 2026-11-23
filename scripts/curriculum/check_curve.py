#!/usr/bin/env python3
"""code-dojo 学习曲线平滑性检查（内容侧）。

检查什么（规则的说明见 docs/curriculum.md 第 5 节）：
  技能图   skills.yaml 里 id 唯一、前缀正确、前置技能都存在、整张图无环。
  学习顺序 按 stage 顺序 + stage 内 order 升序走一遍所有题：
           - 每题 requires 的技能都已被前面的题引入；
           - 每题最多引入 1 个技能，且这个技能之前没被引入过；
           - 引入技能 X 时，X 在技能图里的前置都已被引入；
           - 活跃线中，技能所在阶段已有题、整条线却没有题引入它时，报警告。
  参考解   Python 用 AST、SQL 用正则扫描参考解，识别用到的语法 / 函数 / 库，映射成技能；
           识别出的技能必须落在"requires ∪ {introduces} 及它们的全部前置"之内（掌握一个技能
           意味着已经掌握它的前置）。--strict 时只允许 requires ∪ {introduces} 本身。
  课       problems/<track>/lessons/*/lesson.yaml（docs/problem-format.md v1.2：题和课合在一起）：
           文件格式正确（id / title / track / skills / steps，步骤只有 read / example / quiz）；
           每一步的 skill 存在且属于该文件的 skills；每个技能最多在一个文件里讲；
           每个被某道题 introduces 的技能，都至少有一段 read 和一个 example。
  选修     必修技能不能以选修技能为前置；必修题不能用到选修内容才引入的技能。
  计划覆盖 docs/curriculum.md 里的题单计划要恰好覆盖 NeetCode 250（+ 热题 100 补充 + 阶段 5）和 SQL 50。
           活跃学习线中，已有题的阶段要在题目文件的 leetcode 字段里覆盖本阶段计划表列出的骨架题。

识别规则都是下面的数据表，扩展时只改表：
  Python：PY_NODE_SKILLS / PY_CALLS / PY_METHODS_DEFAULT / PY_METHODS_BY_TYPE / PY_IMPORTS / PY_ATTRS
  SQL：  SQL_RULES（正则）+ SQL_FUNC_RULES（函数式检测）

用法：
  python3 scripts/curriculum/check_curve.py            # 检查全部学习线
  python3 scripts/curriculum/check_curve.py -v         # 逐题打印识别到的技能
  python3 scripts/curriculum/check_curve.py --track sql --strict
没有 PyYAML 时：uv run --with pyyaml python3 scripts/curriculum/check_curve.py
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from graphlib import CycleError, TopologicalSorter
from pathlib import Path

from track_files import ROOT, Track, load_tracks, normalize_stage
from app.inspect_data import InspectExercise, data_block

try:
    import yaml
except ImportError:  # pragma: no cover
    print("需要 PyYAML：uv run --with pyyaml python3 scripts/curriculum/check_curve.py", file=sys.stderr)
    sys.exit(2)

PROBLEMS = ROOT / "problems"
PLAN_DOC = ROOT / "docs" / "curriculum.md"
LISTS_JSON = ROOT / "docs" / "research_notes" / "2026 技术面试 高频题单 调研" / "lists.json"

FORMATS = {"predict", "complete", "fix", "write", "variant", "combine", "inspect"}
STEP_TYPES = {"read", "example", "quiz"}
LESSON_KEYS = {"id", "title", "track", "skills", "steps"}
SCAFFOLD_FORMATS = {"predict", "complete"}
# NeetCode 250 里的 7 道 LeetCode 会员题（replaces_premium 只能写这些）
PREMIUM_SLUGS = {
    "encode-and-decode-strings", "graph-valid-tree", "number-of-connected-components-in-an-undirected-graph",
    "walls-and-gates", "meeting-rooms", "meeting-rooms-ii", "alien-dictionary",
}

# =====================================================================
# Python：语法结构 → 技能（改这里扩展）
# =====================================================================

# 结构性检测：键是检测器内部的构造名，值是技能 id（None 表示识别但不计技能）
PY_NODE_SKILLS: dict[str, str | None] = {
    "assign": "py.var-arith",            # x = ...
    "aug-assign": "py.var-arith",        # x += ...
    "arith": "py.var-arith",             # + - * / ** 和一元负号
    "floordiv-mod": "py.floordiv-mod",   # // %
    "bit-op": "algo.bit-ops",              # & | ^ << >> ~
    "str-percent-format": "py.fstring",  # "%d" % x（老式格式化，归入格式化）
    "compare": "py.compare-bool",        # == != < > <= >=
    "compare-in": "py.in-membership",    # in / not in
    "compare-is": "py.none",             # is / is not
    "bool-const": "py.value-types",      # True / False
    "none-const": "py.value-types",      # None
    "bool-op": "py.bool-ops",            # and / or
    "not": "py.bool-ops",                # not
    "if": "py.if-else",
    "elif": "py.elif",
    "ternary": "py.ternary",             # a if c else b
    "for-range": "py.for-range",         # for i in range(...)
    "for-each": "py.for-each",           # for x in seq
    "while": "py.while",
    "break-continue": "py.break-continue",
    "nested-loop": "py.nested-loop",     # 循环里再套循环（不算推导式）
    "fstring": "py.fstring",
    "index": "py.index-len",             # s[i]
    "slice": "py.slice",                 # s[a:b]
    "double-index": "py.nested-list",    # grid[i][j]
    "list-literal": "py.list-basics",    # [..]
    "list-item-store": "py.list-basics", # nums[i] = v
    "dict-literal": "py.dict-basics",    # {k: v}
    "dict-item": "py.dict-basics",       # d[k] 读写（d 推断为字典时）
    "set-literal": "py.set-basics",      # {a, b}
    "list-repeat-concat": "py.list-concat-repeat",  # [0] * n、[x] + rest
    "tuple-unpack-assign": "py.multi-assign",       # a, b = b, a
    "tuple-literal": "py.tuple",         # return a, b / (r, c)
    "list-comp": "py.list-comp",
    "dict-comp": "py.dict-set-comp",
    "set-comp": "py.dict-set-comp",
    "genexp": "py.genexp",
    "lambda": "py.sort-key",
    "key-kwarg": "py.sort-key",          # sorted(..., key=...)
    "reverse-kwarg": "py.sorted",        # sorted(..., reverse=True)
    "return": "py.func-return",          # 函数体最外层的 return
    "early-return": "py.early-return",   # 嵌在 if / 循环里的 return
    "entry-def": "py.func-return",       # function 模式题目给定的入口函数；predict / stdio 程序里的第一个函数
    "helper-def": "py.helper-func",      # 第二个及以后的顶层函数（把问题拆成多个函数）
    "nested-def": "algo.nested-func",      # 函数里定义函数
    "default-arg": "py.default-args",
    "recursion": "py.recursion",
    "multi-recursion": "py.recursion-multi",  # 两处以上自调用，或在循环里自调用
    "class-def": "py.class-basic",
    "method-def": "py.class-methods",    # __init__ 以外的方法
    "try": "algo.try-except",
    "yield": "algo.generator",
    "nonlocal": "algo.nested-func",
    "global": "algo.nested-func",
}

# 内置函数调用
PY_CALLS: dict[str, str | None] = {
    "bytes": "llm.utf8",
    "norm": None, "branch": None, "norm1": None, "norm2": None, "attention": None, "mlp": None,  # 题目传入的可调用层
    "model": None, "layer": None,  # 题目传入或示例创建的可调用模型
    "guess": "algo.binary-search",        # 猜数题提供的三向比较函数
    "lower_bound": "algo.binary-search",  # 手写查找第一个达标位置的辅助函数
    "print": "py.print", "input": "py.stdio-input",
    "int": "py.type-convert", "str": "py.type-convert", "float": "py.type-convert", "bool": "py.type-convert",
    "len": "py.index-len", "range": "py.for-range",
    "abs": "py.minmax-abs", "round": "py.minmax-abs",
    "sum": "py.list-builtins",
    "ord": "py.ord-chr", "chr": "py.ord-chr",
    "enumerate": "py.enumerate", "zip": "py.zip",
    "sorted": "py.sorted", "reversed": "py.sorted",
    "list": "py.list-basics", "dict": "py.dict-basics", "set": "py.set-basics",
    "frozenset": "py.set-basics", "tuple": "py.tuple",
    "any": "py.genexp", "all": "py.genexp",
    "map": "py.list-comp", "filter": "py.list-comp",
    "divmod": "py.tuple", "pow": "py.var-arith",
    "isinstance": "py.class-basic", "type": "py.value-types", "super": "algo.class-design",
    "iter": "algo.generator", "next": "algo.generator",
    "hash": None, "id": None,
    # 判题平台提供的类型
    "ListNode": "py.node-class", "TreeNode": "algo.tree-basics",
}
# min / max：一个参数（作用于序列）和多个参数（比较几个值）是两个技能
PY_MINMAX_ONE_ARG = "py.list-builtins"
PY_MINMAX_MULTI_ARG = "py.minmax-abs"

_STR_METHODS = [
    "strip", "lstrip", "rstrip", "lower", "upper", "title", "capitalize", "swapcase", "casefold",
    "replace", "find", "rfind", "index", "rindex", "count", "startswith", "endswith",
    "isdigit", "isalpha", "isalnum", "isspace", "isupper", "islower", "isnumeric", "isdecimal",
    "zfill", "center", "ljust", "rjust", "format", "partition", "rpartition",
]
# 接收者类型未知时按方法名映射（取最先教的那个技能）
PY_METHODS_DEFAULT: dict[str, str | None] = {
    "encode": "llm.utf8", "decode": "llm.utf8", "from_pretrained": "llm.embedding",
    "project": None, "finish": None,  # 缓存题提供的投影与读出接口
    "manual_seed": "train.shuffle",  # 生成器实例的抽签起点
    "SGD": "train.loop", "zero_grad": "train.loop", "step": "train.loop", "loss": "train.loop",
    "CrossEntropyLoss": "train.ce", "Adam": "train.adam", "StepLR": "train.schedule",
    "clip_grad_norm_": "train.clip", "Dropout": "train.dropout",
    "train": "train.evaluate", "eval": "train.evaluate", "evaluating": "train.evaluate",
    "Identity": None, "seek": None, "long": "tensor.create",
    "default_rng": None,  # 按指定种子创建 NumPy 随机数生成器
    "tanh": None,  # 标量节点或张量的双曲正切
    "permutation": None,  # 取得洗牌后的行号
    "next": "algo.generator", "hasNext": "algo.generator",  # 搜索树迭代器的读取和探询接口
    "getstate": None,  # 随机设计题的校验器固定抽样起点
    "__init__": "py.class-basic",  # 通过 super 初始化父类状态
    "view": "tensor.reshape",
    "permute": "tensor.axes", "transpose": "tensor.axes",
    "contiguous": "tensor.axes", "is_contiguous": "tensor.axes",
    "unsqueeze": "tensor.singleton", "squeeze": "tensor.singleton",
    "masked_fill": "tensor.mask",
    "diagonal": "tensor.relabel",
    "backward": "tensor.backward", "requires_grad_": "tensor.backward",
    "item": None,  # 单个数值取为 Python 标量
    "detach": "tensor.boundary", "add_": "tensor.boundary", "copy_": "tensor.boundary",
    "linear": "tensor.linear", "numel": "tensor.create",
    "parameters": "tensor.state", "state_dict": "tensor.state", "load_state_dict": "tensor.state",
    "clone": None,  # 独立复制张量
    "tolist": None,  # 数组或列转成便于阅读的 Python 列表
    "reshape": "wrangle.reshape",
    "sort_values": "wrangle.filter-sort",
    "isna": "wrangle.missing", "dropna": "wrangle.missing", "fillna": "wrangle.missing",
    "astype": "wrangle.cast",
    "groupby": "wrangle.group", "agg": "wrangle.group", "reset_index": "wrangle.group",
    "merge": "wrangle.merge", "pivot_table": "wrangle.pivot", "melt": "wrangle.melt",
    "value_counts": "wrangle.frequency", "apply": "wrangle.apply",
    "drop_duplicates": "wrangle.projection",
    "isin": "py.in-membership", "eq": "py.compare-bool",
    "rank": "wrangle.window", "cumcount": "wrangle.window", "cumsum": "wrangle.cumsum",
    "serialize": "algo.tree-basics", "deserialize": "algo.tree-basics",  # 二叉树编解码接口
    "root": "algo.union-find", "merge_sets": "algo.union-find",  # 查代表、合并两个集合
    "length": "py.index-len",             # 山脉数组接口提供的长度
    "deposit": "py.class-methods",  # 账户示例：在实例上调用存款方法
    **{m: "py.str-methods" for m in _STR_METHODS},
    "split": "py.split-join", "rsplit": "py.split-join", "splitlines": "py.split-join", "join": "py.split-join",
    "append": "py.list-append", "extend": "py.list-append",
    "pop": "py.list-pop", "insert": "py.list-pop", "remove": "py.list-pop", "clear": "py.list-pop",
    "sort": "py.sorted", "reverse": "py.sorted",
    "copy": "py.aliasing",
    "get": "py.dict-get", "setdefault": "py.dict-get",
    "popitem": "py.dict-basics",         # 字典取出并删除一项
    "contains": "algo.class-design",     # 设计题的集合查询接口
    "items": "py.dict-iter", "keys": "py.dict-iter", "values": "py.dict-iter",
    "update": "py.dict-basics",
    "add": "py.set-basics", "discard": "py.set-basics", "union": "py.set-basics",
    "intersection": "py.set-basics", "difference": "py.set-basics", "issubset": "py.set-basics",
    "issuperset": "py.set-basics", "symmetric_difference": "py.set-basics",
    "popleft": "py.deque", "appendleft": "py.deque", "rotate": "py.deque",
    "most_common": "algo.counter", "elements": "algo.counter",
}
# 接收者类型推断得出时的覆盖映射
PY_METHODS_BY_TYPE: dict[str, dict[str, str | None]] = {
    "list": {"index": "py.list-basics", "count": "py.list-builtins"},
    "dict": {"pop": "py.dict-basics", "clear": "py.dict-basics"},
    "set": {"pop": "py.set-basics", "remove": "py.set-basics", "clear": "py.set-basics", "update": "py.set-basics"},
    "deque": {"append": "py.deque", "pop": "py.deque", "extend": "py.deque", "clear": "py.deque"},
}
# import：模块或 模块.名字
PY_IMPORTS: dict[str, str | None] = {
    "torch.nn.functional.gelu": "llm.mlp", "torch.nn.Embedding.from_pretrained": "llm.embedding",
    "torch.utils.data.Dataset": "train.dataset", "torch.utils.data.DataLoader": "train.batch",
    "torch.nn.utils.rnn.pad_sequence": "train.pad", "io.BytesIO": "train.checkpoint",
    "torch.save": "train.checkpoint", "torch.load": "train.checkpoint",
    "numpy.linalg.solve": "ml.normal",
    "math.tanh": None,  # 纯 Python 的标量激活值
    "random.randrange": None, "random.Random": None, "random.setstate": None,  # 抽签及判题端的可复现抽样
    "torch.tensor": "tensor.create", "torch.arange": "tensor.create",
    "torch.sum": "tensor.reduce", "torch.mean": "tensor.reduce",
    "torch.gather": "tensor.route", "torch.scatter": "tensor.route",
    "torch.where": "tensor.where", "torch.topk": "tensor.rank", "torch.argmax": "tensor.rank",
    "torch.einsum": "tensor.contract", "torch.bmm": "tensor.batch-contract",
    "torch.no_grad": "tensor.boundary", "torch.nn.Parameter": "tensor.parameter",
    "torch.nn.Linear": "tensor.linear",
    "numpy.array": "wrangle.array",
    "numpy.sum": "wrangle.axis", "numpy.mean": "wrangle.axis",
    "numpy.array_equal": "wrangle.vectorize", "numpy.where": "wrangle.where",
    "numpy.cumsum": "wrangle.cumsum",
    "numpy.argsort": "wrangle.rank-index", "numpy.argmax": "wrangle.rank-index",
    "pandas.DataFrame": "wrangle.table", "pandas.Series": "wrangle.table",
    "pandas.read_csv": "wrangle.csv", "io.StringIO": "wrangle.csv",
    "pandas.to_datetime": "wrangle.dates",
    "numpy": None,
    "pandas": None,
    "torch": None,
    "heapq": "algo.heapq",
    "collections": None,
    "collections.deque": "py.deque",
    "collections.Counter": "algo.counter",
    "collections.defaultdict": "algo.defaultdict",
    "collections.OrderedDict": "algo.class-design",
    "functools": None,
    "functools.cache": "algo.memo-cache",
    "functools.lru_cache": "algo.memo-cache",
    "functools.cmp_to_key": "py.sort-key",
    "bisect": "algo.binary-search",
    "math": "algo.math-module",
    "math.exp": "math.exp",
    "math.log": "math.log",
    "random.seed": "math.frequency",
    "random.randint": "math.frequency",
    "time": "py.big-o",
    "sys": "py.recursion",
    "string": "py.str-methods",
    "typing": None,
    "__future__": None,
}
# 属性访问（不是方法调用时）
PY_ATTRS: dict[str, str] = {
    "next": "py.node-class",
    "val": "py.node-class",
    "left": "algo.tree-basics",
    "right": "algo.tree-basics",
    "prev": "algo.doubly-linked",
}


def _ann_type(node: ast.AST | None) -> str | None:
    if node is None:
        return None
    text = ast.unparse(node).replace(" ", "")
    for prefix, t in (("list[list", "list2d"), ("list[str]", "list_str"), ("list", "list"), ("List", "list"),
                      ("dict", "dict"), ("Dict", "dict"), ("set", "set"), ("Set", "set"), ("str", "str"),
                      ("deque", "deque")):
        if text.startswith(prefix):
            return t
    return None


@dataclass
class Detection:
    skill: str
    construct: str
    line: int


class PyDetector(ast.NodeVisitor):
    """扫描一份 Python 源码，收集用到的构造（类型标注不扫描）。"""

    def __init__(self, mode: str, entry: str | None):
        self.mode = mode
        self.entry = entry
        self.found: list[Detection] = []
        self.unknown: list[str] = []
        self.types: dict[str, str] = {}
        self.modules: dict[str, str] = {}      # 本地名字 → 模块全名
        self.imported_names: set[str] = set()
        self.defined_funcs: set[str] = set()
        self.loop_depth = 0
        self.func_stack: list[ast.FunctionDef] = []
        self.class_depth = 0
        self.script_defs = 0                   # predict / stdio 程序里已经见过的顶层函数个数
        self._tuple_rhs: set[int] = set()

    # ---------- helpers ----------
    def hit(self, construct: str, node: ast.AST):
        skill = PY_NODE_SKILLS.get(construct, construct)
        if skill:
            self.found.append(Detection(skill, construct, getattr(node, "lineno", 0)))

    def hit_skill(self, skill: str | None, construct: str, node: ast.AST):
        if skill:
            self.found.append(Detection(skill, construct, getattr(node, "lineno", 0)))

    def type_of(self, node: ast.AST) -> str | None:
        if isinstance(node, ast.Name):
            return self.types.get(node.id)
        if isinstance(node, (ast.List, ast.ListComp)):
            if isinstance(node, ast.List) and node.elts and all(isinstance(e, ast.List) for e in node.elts):
                return "list2d"
            return "list"
        if isinstance(node, (ast.Dict, ast.DictComp)):
            return "dict"
        if isinstance(node, (ast.Set, ast.SetComp)):
            return "set"
        if isinstance(node, ast.JoinedStr) or (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            return "str"
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Mult, ast.Add)):
            for t in (self.type_of(node.left), self.type_of(node.right)):
                if t in ("list", "list2d", "str"):
                    return t
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Name):
                name = f.id
                if name in ("list", "sorted"):
                    return "list"
                if name in ("dict", "defaultdict", "Counter", "OrderedDict"):
                    return "dict"
                if name in ("set", "frozenset"):
                    return "set"
                if name == "str":
                    return "str"
                if name == "deque":
                    return "deque"
            if isinstance(f, ast.Attribute):
                if f.attr in ("split", "rsplit", "splitlines"):
                    return "list_str"
                if f.attr in ("join", "strip", "lower", "upper", "replace"):
                    return "str"
                full = self._module_attr(f)
                if full in ("collections.defaultdict", "collections.Counter"):
                    return "dict"
                if full == "collections.deque":
                    return "deque"
        if isinstance(node, ast.Subscript):
            base = self.type_of(node.value)
            if isinstance(node.slice, ast.Slice):
                return base
            if base == "list2d":
                return "list"
            if base in ("list_str", "str"):
                return "str"
        return None

    def _module_attr(self, attr: ast.Attribute) -> str | None:
        if isinstance(attr.value, ast.Name) and attr.value.id in self.modules:
            return f"{self.modules[attr.value.id]}.{attr.attr}"
        return None

    # ---------- imports ----------
    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.modules[alias.asname or alias.name] = alias.name
            self._import(alias.name, node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        mod = node.module or ""
        for alias in node.names:
            full = f"{mod}.{alias.name}"
            self.imported_names.add(alias.asname or alias.name)
            self._import(full if full in PY_IMPORTS else mod, node)

    def _import(self, name: str, node: ast.AST):
        root = name.split(".")[0]
        if name not in PY_IMPORTS and root in ("numpy", "pandas", "torch"):
            name = root
        if name in PY_IMPORTS:
            self.hit_skill(PY_IMPORTS[name], f"import {name}", node)
        else:
            self.unknown.append(f"第 {node.lineno} 行：未登记的 import {name}（在 PY_IMPORTS 里加映射）")

    # ---------- definitions ----------
    def visit_FunctionDef(self, node: ast.FunctionDef):
        in_class = self.class_depth > 0 and not self.func_stack
        if self.func_stack:
            self.hit("nested-def", node)
        elif in_class:
            if node.name != "__init__":
                self.hit("method-def", node)
        elif self.mode == "function" and node.name == self.entry:
            self.hit("entry-def", node)
        elif self.mode in ("predict", "stdio") and self.script_defs == 0:
            self.script_defs += 1
            self.hit("entry-def", node)        # 读懂"定义一个函数再调用它"属于 func-return
        else:
            self.hit("helper-def", node)
        if node.args.defaults or any(d is not None for d in node.args.kw_defaults):
            self.hit("default-arg", node)
        for a in node.args.args + node.args.kwonlyargs:
            t = _ann_type(a.annotation)
            if t:
                self.types[a.arg] = t
        self._check_recursion(node)
        self._classify_returns(node)
        for d in node.decorator_list:
            self.visit(d)
        for d in node.args.defaults + [d for d in node.args.kw_defaults if d is not None]:
            self.visit(d)
        self.func_stack.append(node)
        saved_depth, self.loop_depth = self.loop_depth, 0
        for stmt in node.body:
            self.visit(stmt)
        self.loop_depth = saved_depth
        self.func_stack.pop()

    visit_AsyncFunctionDef = visit_FunctionDef

    def _classify_returns(self, fn: ast.FunctionDef):
        top = {id(s) for s in fn.body if isinstance(s, ast.Return)}
        stack = list(fn.body)
        while stack:
            n = stack.pop()
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
                continue
            if isinstance(n, ast.Return):
                self.hit("return" if id(n) in top else "early-return", n)
            stack.extend(ast.iter_child_nodes(n))

    def _check_recursion(self, fn: ast.FunctionDef):
        calls, in_loop = 0, False

        def walk(n: ast.AST, looping: bool):
            nonlocal calls, in_loop
            for child in ast.iter_child_nodes(n):
                lp = looping or isinstance(child, (ast.For, ast.While, ast.comprehension))
                if isinstance(child, ast.Call):
                    f = child.func
                    if (isinstance(f, ast.Name) and f.id == fn.name) or (
                        isinstance(f, ast.Attribute) and f.attr == fn.name
                        and isinstance(f.value, ast.Name) and f.value.id == "self"
                    ):
                        calls += 1
                        in_loop = in_loop or lp
                walk(child, lp)

        walk(fn, False)
        if calls:
            self.hit("recursion", fn)
            if calls >= 2 or in_loop:
                self.hit("multi-recursion", fn)

    def visit_ClassDef(self, node: ast.ClassDef):
        self.hit("class-def", node)
        self.class_depth += 1
        saved = self.func_stack
        self.func_stack = []
        for stmt in node.body:
            self.visit(stmt)
        self.func_stack = saved
        self.class_depth -= 1

    def visit_Lambda(self, node: ast.Lambda):
        self.hit("lambda", node)
        self.visit(node.body)

    def visit_AnnAssign(self, node: ast.AnnAssign):
        self.hit("assign", node)
        t = _ann_type(node.annotation)
        if isinstance(node.target, ast.Name) and t:
            self.types[node.target.id] = t
        self.visit(node.target)
        if node.value is not None:
            self.visit(node.value)

    # ---------- statements ----------
    def visit_Assign(self, node: ast.Assign):
        self.hit("assign", node)
        for t in node.targets:
            if isinstance(t, (ast.Tuple, ast.List)):
                self.hit("tuple-unpack-assign", node)
                if isinstance(node.value, ast.Tuple):
                    self._tuple_rhs.add(id(node.value))
            elif isinstance(t, ast.Name):
                vt = self.type_of(node.value)
                if vt:
                    self.types[t.id] = vt
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign):
        self.hit("aug-assign", node)
        self._binop(node.op, node, left_type=self.type_of(node.target))
        self.generic_visit(node)

    def visit_If(self, node: ast.If):
        self.hit("if", node)
        self.visit(node.test)
        for s in node.body:
            self.visit(s)
        orelse = node.orelse
        if len(orelse) == 1 and isinstance(orelse[0], ast.If) and orelse[0].col_offset == node.col_offset:
            self.hit("elif", orelse[0])
        for s in orelse:
            self.visit(s)

    def visit_IfExp(self, node: ast.IfExp):
        self.hit("ternary", node)
        self.generic_visit(node)

    def _enter_loop(self, node: ast.AST):
        if self.loop_depth > 0:
            self.hit("nested-loop", node)
        self.loop_depth += 1

    def visit_For(self, node: ast.For):
        it = node.iter
        is_range = isinstance(it, ast.Call) and isinstance(it.func, ast.Name) and it.func.id == "range"
        self.hit("for-range" if is_range else "for-each", node)
        it_type = self.type_of(it)
        if isinstance(node.target, ast.Name):
            if it_type in ("str", "list_str"):
                self.types[node.target.id] = "str"
            elif it_type == "list2d":
                self.types[node.target.id] = "list"
        self.visit(it)
        self._enter_loop(node)
        for s in node.body + node.orelse:
            self.visit(s)
        self.loop_depth -= 1

    visit_AsyncFor = visit_For

    def visit_While(self, node: ast.While):
        self.hit("while", node)
        self.visit(node.test)
        self._enter_loop(node)
        for s in node.body + node.orelse:
            self.visit(s)
        self.loop_depth -= 1

    def visit_Break(self, node):
        self.hit("break-continue", node)

    visit_Continue = visit_Break

    def visit_Try(self, node):
        self.hit("try", node)
        self.generic_visit(node)

    visit_TryStar = visit_Try

    def visit_Yield(self, node):
        self.hit("yield", node)
        self.generic_visit(node)

    visit_YieldFrom = visit_Yield

    def visit_Nonlocal(self, node):
        self.hit("nonlocal", node)

    def visit_Global(self, node):
        self.hit("global", node)

    # ---------- expressions ----------
    def _binop(self, op: ast.operator, node: ast.AST, left_type: str | None = None, right_type=None):
        if isinstance(op, (ast.FloorDiv, ast.Mod)):
            if isinstance(op, ast.Mod) and left_type == "str":
                self.hit("str-percent-format", node)
            else:
                self.hit("floordiv-mod", node)
        elif isinstance(op, (ast.BitAnd, ast.BitOr, ast.BitXor, ast.LShift, ast.RShift)):
            self.hit("bit-op", node)
        else:
            self.hit("arith", node)
            if isinstance(op, (ast.Mult, ast.Add)) and "list" in (left_type, right_type):
                self.hit("list-repeat-concat", node)

    def visit_BinOp(self, node: ast.BinOp):
        lt = "list" if isinstance(node.left, ast.List) else self.type_of(node.left)
        rt = "list" if isinstance(node.right, ast.List) else None
        if lt == "list2d":
            lt = "list"
        self._binop(node.op, node, lt, rt)
        self.generic_visit(node)

    def visit_UnaryOp(self, node: ast.UnaryOp):
        if isinstance(node.op, ast.Not):
            self.hit("not", node)
        elif isinstance(node.op, ast.Invert):
            self.hit("bit-op", node)
        else:
            self.hit("arith", node)
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        self.hit("bool-op", node)
        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare):
        for op in node.ops:
            if isinstance(op, (ast.In, ast.NotIn)):
                self.hit("compare-in", node)
            elif isinstance(op, (ast.Is, ast.IsNot)):
                self.hit("compare-is", node)
            else:
                self.hit("compare", node)
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant):
        if node.value is None:
            self.hit("none-const", node)
        elif isinstance(node.value, bool):
            self.hit("bool-const", node)

    def visit_JoinedStr(self, node):
        self.hit("fstring", node)
        self.generic_visit(node)

    def visit_List(self, node: ast.List):
        if isinstance(node.ctx, ast.Load):
            self.hit("list-literal", node)
        self.generic_visit(node)

    def visit_Tuple(self, node: ast.Tuple):
        if isinstance(node.ctx, ast.Load) and id(node) not in self._tuple_rhs:
            self.hit("tuple-literal", node)
        self.generic_visit(node)

    def visit_Dict(self, node):
        self.hit("dict-literal", node)
        self.generic_visit(node)

    def visit_Set(self, node):
        self.hit("set-literal", node)
        self.generic_visit(node)

    def visit_ListComp(self, node):
        self.hit("list-comp", node)
        self.generic_visit(node)

    def visit_DictComp(self, node):
        self.hit("dict-comp", node)
        self.generic_visit(node)

    def visit_SetComp(self, node):
        self.hit("set-comp", node)
        self.generic_visit(node)

    def visit_GeneratorExp(self, node):
        self.hit("genexp", node)
        self.generic_visit(node)

    def visit_comprehension(self, node: ast.comprehension):
        # 推导式里的 for 不算 for 循环，target 也不算元组字面量
        if isinstance(node.target, ast.Name) and self.type_of(node.iter) in ("str", "list_str"):
            self.types[node.target.id] = "str"
        self.visit(node.iter)
        for cond in node.ifs:
            self.visit(cond)

    def visit_Subscript(self, node: ast.Subscript):
        base_type = self.type_of(node.value)
        if isinstance(node.slice, ast.Slice):
            self.hit("slice", node)
        elif base_type == "dict":
            self.hit("dict-item", node)
        else:
            self.hit("index", node)
            if isinstance(node.ctx, (ast.Store, ast.Del)):
                self.hit("list-item-store", node)
            inner = node.value
            if isinstance(inner, ast.Subscript) and not isinstance(inner.slice, ast.Slice):
                if self.type_of(inner.value) not in ("list_str", "str", "dict"):
                    self.hit("double-index", node)
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        if node.attr in PY_ATTRS and isinstance(node.ctx, (ast.Load, ast.Store)):
            self.hit_skill(PY_ATTRS[node.attr], f".{node.attr}", node)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        f = node.func
        for kw in node.keywords:
            if kw.arg == "key":
                self.hit("key-kwarg", node)
            elif kw.arg == "reverse":
                self.hit("reverse-kwarg", node)
        if isinstance(f, ast.Name):
            name = f.id
            if name in ("min", "max"):
                one = len(node.args) == 1 and not isinstance(node.args[0], ast.Starred)
                self.hit_skill(PY_MINMAX_ONE_ARG if one else PY_MINMAX_MULTI_ARG, f"{name}()", node)
            elif name in PY_CALLS:
                self.hit_skill(PY_CALLS[name], f"{name}()", node)
            elif name not in self.defined_funcs and name not in self.imported_names:
                self.unknown.append(f"第 {node.lineno} 行：未登记的调用 {name}()（在 PY_CALLS 里加映射）")
            self.generic_visit(node)
            return
        if isinstance(f, ast.Attribute):
            full = self._module_attr(f)
            if full is not None:
                if full in PY_IMPORTS:
                    self.hit_skill(PY_IMPORTS[full], full, node)
            else:
                recv_type = self.type_of(f.value)
                if recv_type in ("list2d", "list_str"):
                    recv_type = "list"
                by_type = PY_METHODS_BY_TYPE.get(recv_type or "", {})
                if f.attr in by_type:
                    self.hit_skill(by_type[f.attr], f".{f.attr}()", node)
                elif f.attr in PY_METHODS_DEFAULT:
                    self.hit_skill(PY_METHODS_DEFAULT[f.attr], f".{f.attr}()", node)
                elif not (isinstance(f.value, ast.Name) and f.value.id == "self"):
                    self.unknown.append(
                        f"第 {node.lineno} 行：未登记的方法 .{f.attr}()（在 PY_METHODS_DEFAULT 里加映射）"
                    )
            # 只访问接收者和参数，不把 .attr 当成属性访问
            self.visit(f.value)
            for a in node.args:
                self.visit(a)
            for kw in node.keywords:
                self.visit(kw.value)
            return
        self.generic_visit(node)


def detect_python(source: str, mode: str, entry: str | None) -> tuple[list[Detection], list[str]]:
    tree = ast.parse(source)
    det = PyDetector(mode, entry)
    det.defined_funcs = {
        n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    }
    det.visit(tree)
    return det.found, det.unknown


# =====================================================================
# SQL：语法结构 → 技能（改这里扩展）。在规范化后的 SQL 上匹配：
# 去注释、字符串字面量换成 ''、转大写、空白压成一个空格、括号两边不留空格。
# =====================================================================

SQL_RULES: list[tuple[str, str, str]] = [
    # (正则, 技能, 说明)
    (r"\bSELECT\s*\*", "sql.select-star", "SELECT *"),
    (r"\bSELECT\b(?!\s*\*)", "sql.select-basic", "SELECT 列"),
    (r"\bWHERE\b", "sql.where", "WHERE"),
    (r"\bIN\((?!SELECT\b)", "sql.in-list", "IN (列表)"),
    (r"\bBETWEEN\b", "sql.between", "BETWEEN"),
    (r"\bI?LIKE\b", "sql.like", "LIKE / ILIKE"),
    (r"!?~\*?|\bSIMILAR TO\b|\bREGEXP_\w+\(", "sql.regex", "正则匹配"),
    (r"\bIS (NOT )?NULL\b|\bIS (NOT )?DISTINCT FROM\b", "sql.is-null", "IS NULL"),
    (r"\bCOALESCE\(", "sql.coalesce", "COALESCE"),
    (r"\bNULLIF\(", "sql.nullif", "NULLIF"),
    (r"\bORDER BY\b", "sql.order-by", "ORDER BY"),
    (r"\bLIMIT\b|\bOFFSET\b|\bFETCH (FIRST|NEXT)\b", "sql.limit", "LIMIT / OFFSET"),
    (r"\bSELECT DISTINCT\b", "sql.distinct", "SELECT DISTINCT"),
    (r"\bCASE\b", "sql.case", "CASE"),
    (r"\|\||\b(LENGTH|CHAR_LENGTH|UPPER|LOWER|INITCAP|SUBSTRING|SUBSTR|LEFT|RIGHT|TRIM|LTRIM|RTRIM|"
     r"CONCAT|CONCAT_WS|REPLACE|POSITION|STRPOS|SPLIT_PART|LPAD|RPAD|REVERSE)\(", "sql.string-funcs", "字符串函数"),
    (r"\b(EXTRACT|DATE_TRUNC|DATE_PART|TO_CHAR|TO_DATE|AGE|NOW|MAKE_DATE)\(|\bCURRENT_DATE\b|\bINTERVAL\b",
     "sql.date-funcs", "日期函数"),
    (r"\b(ROUND|CAST|CEIL|CEILING|FLOOR|ABS|TRUNC|MOD|POWER|SQRT)\(|::", "sql.round-cast", "数值函数 / 类型转换"),
    (r"\bCOUNT\(", "sql.count", "COUNT"),
    (r"\b(SUM|AVG|MIN|MAX)\(", "sql.sum-avg", "SUM / AVG / MIN / MAX"),
    (r"\bGROUP BY\b", "sql.group-by", "GROUP BY"),
    (r"\bHAVING\b", "sql.having", "HAVING"),
    (r"\b(COUNT|SUM|AVG)\(DISTINCT\b", "sql.count-distinct", "聚合里的 DISTINCT"),
    (r"\b(SUM|COUNT|AVG|MAX|MIN)\(CASE\b|\bFILTER\(WHERE\b", "sql.conditional-agg", "条件聚合"),
    (r"\bBOOL_OR\(", "sql.conditional-agg", "组内是否有一行满足条件"),
    (r"\b(STRING_AGG|ARRAY_AGG)\(", "sql.string-agg", "STRING_AGG"),
    (r"\b(LEFT|RIGHT|FULL)( OUTER)? JOIN\b", "sql.left-join", "外连接"),
    (r"\bCROSS JOIN\b", "sql.cross-join", "CROSS JOIN"),
    (r"\b(FROM|JOIN)\(SELECT\b", "sql.derived-table", "FROM 子查询"),
    (r"\bIN\(SELECT\b", "sql.subquery-in", "IN (子查询)"),
    (r"\bEXISTS\(", "sql.exists", "EXISTS"),
    (r"^WITH\b", "sql.cte", "WITH"),
    (r"^WITH RECURSIVE\b", "sql.recursive-cte", "WITH RECURSIVE"),
    (r"\b(UNION|INTERSECT|EXCEPT)\b", "sql.set-ops", "集合运算"),
    (r"^(DELETE|UPDATE|INSERT)\b", "sql.dml", "DML 语句"),
    # 把 DML 命令作为清理清单交付时，FORMAT 的美元引号模板内就是待执行的 SQL。
    (r"\bFORMAT\(\$([A-Z_][A-Z_0-9]*|)\$\s*(?:DELETE FROM|UPDATE|INSERT INTO)\s+\w+[^$]*\$\1\$",
     "sql.dml", "生成 DML 命令"),
    (r"\bOVER\(", "sql.window-agg", "窗口 OVER"),
    (r"\bROW_NUMBER\(", "sql.row-number", "ROW_NUMBER"),
    (r"\bPARTITION BY\b", "sql.partition-by", "PARTITION BY"),
    (r"\b(RANK|DENSE_RANK|PERCENT_RANK|NTILE)\(", "sql.rank", "RANK / DENSE_RANK"),
    (r"\b(LAG|LEAD|FIRST_VALUE|LAST_VALUE|NTH_VALUE)\(", "sql.lag-lead", "LAG / LEAD"),
    (r"\b(SUM|COUNT|AVG)\([^()]*\) OVER\([^)]*ORDER BY", "sql.running-total", "累计聚合"),
    (r"\b(ROWS|RANGE|GROUPS) BETWEEN\b", "sql.window-frame", "窗口框架"),
    (r"\bPERCENTILE_(CONT|DISC)\b|\bWITHIN GROUP\b", "sql.median", "分位数"),
    (r"\bGENERATE_SERIES\(", "sql.generate-series", "generate_series"),
]

_CLAUSE_END = r"\b(WHERE|GROUP BY|ORDER BY|HAVING|LIMIT|UNION|JOIN|LEFT|RIGHT|FULL|INNER|CROSS|ON)\b|\)|$"


def _blank_parens_after(sql: str, keyword: str) -> str:
    """把 KEYWORD( ... ) 的括号内容换成空格（按括号配对），避免 CAST(x AS int) 的 AS 被当成别名。"""
    out = list(sql)
    for m in re.finditer(rf"\b{keyword}\(", sql):
        depth, i = 0, m.end() - 1
        while i < len(sql):
            if sql[i] == "(":
                depth += 1
            elif sql[i] == ")":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        for k in range(m.end(), min(i, len(sql))):
            out[k] = " "
    return "".join(out)


def _sql_alias(sql: str) -> bool:
    s = _blank_parens_after(sql, "CAST")
    return re.search(r"\bAS (?!\(|MATERIALIZED\b|NOT MATERIALIZED\b)", s) is not None


def _sql_arith(sql: str) -> bool:
    s = re.sub(r"\bCOUNT\(\*\)", "COUNT(X)", sql)
    s = re.sub(r"(\bSELECT( DISTINCT)?|,) ?\*", r"\1 X", s)
    s = re.sub(r"\.\*", ".X", s)
    s = s.replace("::", " ")
    return re.search(r"[\w')] ?[-+*/%] ?[\w'(]", s) is not None


def _sql_bool(sql: str) -> bool:
    s = re.sub(r"\bBETWEEN\b(.*?)\bAND\b", r"BETWEEN\1BAND", sql)
    if re.search(r"\b(AND|OR)\b", s):
        return True
    return re.search(r"(?<!\bIS )\bNOT\b(?! ?(IN|LIKE|ILIKE|BETWEEN|EXISTS|NULL|DISTINCT|MATERIALIZED)\b)",
                     s) is not None


def _sql_tables_by_depth(sql: str) -> dict[int, list[str]]:
    by_depth: dict[int, list[str]] = defaultdict(list)
    depth = 0
    for m in re.finditer(r"\(|\)|\b(FROM|JOIN) ([A-Z_][A-Z0-9_]*)", sql):
        tok = m.group(0)
        if tok == "(":
            depth += 1
        elif tok == ")":
            depth -= 1
        else:
            by_depth[depth].append(m.group(2))
    return by_depth


def _sql_self_join(sql: str) -> bool:
    return any(len(t) != len(set(t)) for t in _sql_tables_by_depth(sql).values())


def _sql_inner_join(sql: str) -> bool:
    return re.search(r"(?<!LEFT )(?<!RIGHT )(?<!FULL )(?<!OUTER )(?<!CROSS )\bJOIN\b", sql) is not None


def _sql_multi_join(sql: str) -> bool:
    return len(re.findall(r"\bJOIN\b", sql)) >= 2


def _sql_anti_join(sql: str) -> bool:
    return bool(re.search(r"\b(LEFT|RIGHT)( OUTER)? JOIN\b", sql)) and bool(
        re.search(r"\bWHERE\b[^;]*?\bIS NULL\b", sql)
    )


def _sql_join_conditions(sql: str) -> bool:
    for m in re.finditer(r"\bON\b", sql):
        rest = sql[m.end():]
        end = re.search(_CLAUSE_END, rest[1:])
        clause = rest[: end.start() + 1] if end else rest
        if re.search(r"\bAND\b|\bBETWEEN\b|<|>", clause):
            return True
    return False


def _sql_join_aggregate(sql: str) -> bool:
    return bool(re.search(r"\bJOIN\b", sql)) and bool(re.search(r"\bGROUP BY\b", sql))


def _sql_scalar_subquery(sql: str) -> bool:
    for m in re.finditer(r"\(SELECT\b", sql):
        before = sql[: m.start()].rstrip()
        if not re.search(r"(\b(IN|EXISTS|FROM|JOIN|AS|ANY|ALL|SOME|UNION|INTERSECT|EXCEPT)|\(|^)$", before):
            return True
    return False


SQL_FUNC_RULES: list[tuple[object, str, str]] = [
    (_sql_alias, "sql.select-expr", "AS 别名"),
    (_sql_arith, "sql.select-expr", "算术表达式"),
    (_sql_bool, "sql.and-or", "AND / OR / NOT"),
    (_sql_inner_join, "sql.inner-join", "JOIN"),
    (_sql_multi_join, "sql.multi-join", "两个以上 JOIN"),
    (_sql_self_join, "sql.self-join", "同一张表出现两次"),
    (_sql_anti_join, "sql.anti-join", "LEFT JOIN + IS NULL"),
    (_sql_join_conditions, "sql.join-conditions", "ON 里有多个条件 / 范围"),
    (_sql_join_aggregate, "sql.join-aggregate", "连接后聚合"),
    (_sql_scalar_subquery, "sql.subquery-scalar", "标量子查询"),
]


def normalize_sql(sql: str) -> str:
    sql = re.sub(r"--[^\n]*", " ", sql)
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)
    sql = re.sub(r"'(?:[^']|'')*'", "''", sql)
    sql = sql.upper()
    sql = re.sub(r"\s+", " ", sql).strip().rstrip(";").strip()
    sql = re.sub(r" ?\( ?", "(", sql)   # 括号两边不留空格：COUNT ( * ) → COUNT(*)
    sql = re.sub(r" \)", ")", sql)
    return sql


def detect_sql(source: str) -> list[Detection]:
    sql = normalize_sql(source)
    found = []
    for pattern, skill, label in SQL_RULES:
        if re.search(pattern, sql):
            found.append(Detection(skill, label, 0))
    for fn, skill, label in SQL_FUNC_RULES:
        if fn(sql):  # type: ignore[operator]
            found.append(Detection(skill, label, 0))
    return found


# =====================================================================
# 题库加载与检查
# =====================================================================

@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    info: list[str] = field(default_factory=list)

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)


def load_skills(track: Track, rep: Report) -> dict[str, dict]:
    path = PROBLEMS / track.id / "skills.yaml"
    if not path.exists():
        rep.err(f"缺少 {path.relative_to(PROBLEMS)}")
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if data.get("track") != track.id:
        rep.err(f"{track.id}/skills.yaml 的 track 字段应为 {track.id}")
    skills: dict[str, dict] = {}
    prefix = track.skill_prefix + "."
    for raw in data.get("skills", []):
        sid = raw.get("id", "")
        if sid in skills:
            rep.err(f"技能 id 重复：{sid}")
        if not re.fullmatch(re.escape(prefix) + r"[a-z0-9]+(-[a-z0-9]+)*", sid):
            rep.err(f"技能 id 不合规范：{sid!r}（应为 {prefix}<kebab>）")
        raw["stage"] = normalize_stage(raw.get("stage", ""))
        if raw["stage"] not in track.stages:
            rep.err(f"技能 {sid} 的 stage {raw['stage']!r} 不存在")
        if not raw.get("name"):
            rep.err(f"技能 {sid} 缺少 name")
        if not (raw.get("card") or "").strip():
            rep.err(f"技能 {sid} 缺少知识卡 card")
        elif len(raw["card"].rstrip().splitlines()) > 20:
            rep.warn(f"技能 {sid} 的知识卡超过 20 行")
        raw["prereqs"] = list(raw.get("prereqs") or [])
        raw["track"] = track.id
        if not isinstance(raw.get("optional", False), bool):
            rep.err(f"技能 {sid} 的 optional 必须是 true / false")
        skills[sid] = raw
    return skills


def check_prereqs(track: Track, own: dict, skills: dict, ancestors: set[str], rep: Report) -> None:
    stages = list(track.stages)
    for sid, s in own.items():
        for pid in s["prereqs"]:
            pre = skills.get(pid)
            if pre is None:
                rep.err(f"技能 {sid} 的前置 {pid} 不存在")
                continue
            if pre["track"] != track.id and pre["track"] not in ancestors:
                rep.err(f"技能 {sid} 的前置 {pid} 不在本线或前置线中")
            if pre["track"] == track.id and pre["stage"] in stages and s["stage"] in stages:
                if stages.index(pre["stage"]) > stages.index(s["stage"]):
                    rep.warn(f"技能 {sid} 的前置 {pid} 属于更晚的阶段 {pre['stage']}")
            if pre.get("optional") and not s.get("optional"):
                rep.err(f"必修技能 {sid} 的前置 {pid} 是选修技能")
    # 无环检查（三色 DFS）
    color: dict[str, int] = {}

    def dfs(u: str, path: list[str]):
        color[u] = 1
        for v in skills[u]["prereqs"]:
            if v not in own:
                continue
            if color.get(v) == 1:
                rep.err("技能图有环：" + " → ".join(path[path.index(v):] + [v]))
            elif color.get(v) is None:
                dfs(v, path + [v])
        color[u] = 2

    for sid in own:
        if color.get(sid) is None:
            dfs(sid, [sid])


def closure(skills: dict[str, dict], roots) -> set[str]:
    seen: set[str] = set()
    stack = [r for r in roots if r]
    while stack:
        u = stack.pop()
        if u in seen or u not in skills:
            continue
        seen.add(u)
        stack.extend(skills[u]["prereqs"])
    return seen


def load_problems(track: Track, rep: Report) -> list[dict]:
    out = []
    for yml in sorted((PROBLEMS / track.id).glob("*/*/problem.yaml")):
        stage_dir = yml.parent.parent.name
        if stage_dir.startswith("_"):
            continue
        meta = yaml.safe_load(yml.read_text(encoding="utf-8"))
        meta["_dir"] = yml.parent
        meta["stage"] = normalize_stage(meta.get("stage"))
        pid = meta.get("id")
        if pid != yml.parent.name:
            rep.err(f"{yml.parent.relative_to(PROBLEMS)}：id {pid!r} 和文件夹名不一致")
        if meta["stage"] != normalize_stage(stage_dir):
            rep.err(f"{pid}：stage {meta['stage']} 和所在文件夹 {stage_dir} 不一致")
        if meta["stage"] not in track.stages:
            rep.err(f"{pid}：未知 stage {meta['stage']}")
            continue
        if meta.get("track") != track.id:
            rep.err(f"{pid}：track 字段应为 {track.id}")
        prefix = f"{track.skill_prefix}-{meta['stage'].lower()}-"
        if not re.fullmatch(re.escape(prefix) + r"\d{3}-[a-z0-9]+(-[a-z0-9]+)*", pid or ""):
            rep.err(f"{pid}：id 应为 {prefix}<三位序号>-<slug>")
        if meta.get("format") not in FORMATS:
            rep.err(f"{pid}：format {meta.get('format')!r} 不合法")
        if meta.get("starter_dialect") is not None and (
            meta["starter_dialect"] != "mysql" or track.language != "sql"
            or meta.get("format") != "fix" or meta.get("mode") is not None
        ):
            rep.err(f"{pid}：starter_dialect 只用于 SQL 改错查询，取值为 mysql")
        d = yml.parent
        if meta.get("format") == "inspect":
            try:
                InspectExercise.load(meta, d)
            except (ValueError, OSError) as exc:
                rep.err(f"{pid}：{exc}")
        elif track.language == "none" or meta.get("mode") == "inspect":
            rep.err(f"{pid}：看数据作答题的 format 和 mode 都应为 inspect")
        elif track.language == "python":
            mode = meta.get("mode")
            if (meta.get("format") == "predict") != (mode == "predict"):
                rep.err(f"{pid}：format predict 和 mode predict 必须同时出现")
            if meta.get("format") in ("complete", "fix") and not (d / "starter.py").exists():
                rep.err(f"{pid}：{meta['format']} 题必须有 starter.py")
            if mode != "predict" and not (d / "tests.json").exists():
                rep.err(f"{pid}：缺少 tests.json")
            if mode == "function" and not (meta.get("entry") and meta.get("signature")):
                rep.err(f"{pid}：function 模式必须有 entry 和 signature")
            if not (d / "solution.py").exists():
                rep.err(f"{pid}：缺少 solution.py")
        else:
            if not (d / "solution.sql").exists():
                rep.err(f"{pid}：缺少 solution.sql")
            if meta.get("format") in ("complete", "fix") and not (d / "starter.sql").exists():
                rep.err(f"{pid}：{meta['format']} 题必须有 starter.sql")
            if not meta.get("datasets"):
                rep.err(f"{pid}：SQL 题至少要有一个数据集")
            if meta.get("mode") == "dml":
                if not isinstance(meta.get("check_query"), str) or not meta["check_query"].strip():
                    rep.err(f"{pid}：dml 模式必须有非空的 check_query")
            elif meta.get("mode") == "script":
                if not meta.get("checks") or meta.get("check_query") is not None:
                    rep.err(f"{pid}：script 模式使用非空的 checks")
            elif meta.get("mode") is not None or meta.get("check_query") is not None:
                rep.err(f"{pid}：SQL 查询题省略 mode 和 check_query")
        if not (d / "statement.md").exists():
            rep.err(f"{pid}：缺少 statement.md")
        if "week" in meta and (type(meta["week"]) is not int or meta["week"] < 1):
            rep.err(f"{pid}：week 应为正整数")
        diff = meta.get("difficulty")
        if not isinstance(diff, int) or not 1 <= diff <= 100:
            rep.err(f"{pid}：difficulty 应为 1–100 的整数")
        if not isinstance(meta.get("optional", False), bool):
            rep.err(f"{pid}：optional 必须是 true / false")
        prem = meta.get("replaces_premium")
        if prem is not None:
            if prem not in PREMIUM_SLUGS:
                rep.err(f"{pid}：replaces_premium {prem!r} 不是 NeetCode 250 里的会员题")
            if meta.get("source") != "original":
                rep.err(f"{pid}：替代会员题的原创题 source 应为 original")
        wrong = meta.get("wrong_examples")
        if wrong is not None:
            key = "code" if track.language == "python" else "sql"
            if meta.get("format") == "inspect" and isinstance(wrong, list):
                valid = all(isinstance(w, dict) and w.get("why") and
                            (w.get(key) or isinstance(w.get("answer"), (str, int))) for w in wrong)
                if not valid:
                    rep.err(f"{pid}：典型误答需要 why 和 answer")
            elif not isinstance(wrong, list) or not all(isinstance(w, dict) and w.get("why") and w.get(key) for w in wrong):
                rep.err(f"{pid}：wrong_examples 每一项都要有 why 和 {key}")
        out.append(meta)
    stages = list(track.stages)
    out.sort(key=lambda m: (stages.index(m["stage"]), m.get("order", 0), m["id"]))
    seen_order: dict[tuple, str] = {}
    for m in out:
        key = (m["stage"], m.get("order"))
        if key in seen_order:
            rep.err(f"{m['id']}：order {m.get('order')} 和 {seen_order[key]} 重复")
        seen_order[key] = m["id"]
    return out


def detectable_skills(track: Track) -> set[str]:
    if track.language == "python":
        vals = list(PY_NODE_SKILLS.values()) + list(PY_CALLS.values()) + list(PY_METHODS_DEFAULT.values())
        vals += [v for d in PY_METHODS_BY_TYPE.values() for v in d.values()]
        vals += list(PY_IMPORTS.values()) + list(PY_ATTRS.values()) + [PY_MINMAX_ONE_ARG, PY_MINMAX_MULTI_ARG]
    else:
        vals = [s for _, s, _ in SQL_RULES] + [s for _, s, _ in SQL_FUNC_RULES]
    return {v for v in vals if v}


def load_lessons(track: Track, rep: Report, skills: dict[str, dict]) -> dict[str, dict]:
    """读 v1.2 的 lesson 文件，返回 技能 → {lesson, read, example, quiz} 的统计。"""
    taught: dict[str, dict] = {}
    for yml in sorted((PROBLEMS / track.id / "lessons").glob("*/lesson.yaml")):
        where = yml.parent.name
        try:
            meta = yaml.safe_load(yml.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            rep.err(f"课 {where}：lesson.yaml 解析失败 {exc}")
            continue
        lid = meta.get("id")
        if lid != where:
            rep.err(f"课 {where}：id {lid!r} 和文件夹名不一致")
        stage_ids = "|".join(re.escape(s.lower()) for s in track.stages)
        pattern = rf"{re.escape(track.skill_prefix)}-(?:{stage_ids})-l\d{{2}}-[a-z0-9]+(?:-[a-z0-9]+)*"
        if not re.fullmatch(pattern, lid or ""):
            rep.err(f"课 {lid}：id 应为 {track.skill_prefix}-<stage>-l<两位序号>-<slug>")
        extra = sorted(set(meta) - LESSON_KEYS)
        if extra:
            rep.err(f"课 {lid}：v1.2 的 lesson 只有 {sorted(LESSON_KEYS)}，多出了 {extra}（v1.1 的独立课字段已取消）")
        if meta.get("track") != track.id:
            rep.err(f"课 {lid}：track 字段应为 {track.id}")
        if not meta.get("title"):
            rep.err(f"课 {lid}：缺少 title")
        own = meta.get("skills")
        if not isinstance(own, list) or not own:
            rep.err(f"课 {lid}：skills 必须是非空列表")
            own = []
        for sid in own:
            if sid not in skills:
                rep.err(f"课 {lid}：skills 里的 {sid} 不在技能图里")
            elif sid in taught:
                rep.err(f"课 {lid}：{sid} 已经在 {taught[sid]['lesson']} 里讲过，每个技能只能在一个文件里讲")
            else:
                taught[sid] = {"lesson": lid, "read": 0, "example": 0, "quiz": 0, "examples": []}
        steps = meta.get("steps")
        if not isinstance(steps, list) or not steps:
            rep.err(f"课 {lid}：没有 steps")
            steps = []
        for i, st in enumerate(steps, 1):
            st = st or {}
            t = st.get("type")
            if t not in STEP_TYPES:
                rep.err(f"课 {lid} 第 {i} 步：type {t!r} 不合法（v1.2 只有 read / example / quiz）")
                continue
            sid = st.get("skill")
            if sid not in own:
                rep.err(f"课 {lid} 第 {i} 步：skill {sid!r} 不在这个文件的 skills 里")
                continue
            if t == "read":
                md = (st.get("md") or "").strip()
                if not md:
                    rep.err(f"课 {lid} 第 {i} 步：read 缺少 md")
                elif not 100 <= len(md) <= 900:
                    rep.warn(f"课 {lid} 第 {i} 步（{sid}）：讲解 {len(md)} 字，一般 150–500 字")
            elif t == "example":
                if "data" in st:
                    try:
                        data_block(st["data"], yml.parent)
                    except (ValueError, OSError) as exc:
                        rep.err(f"课 {lid} 第 {i} 步：{exc}")
                    if "code" in st:
                        rep.err(f"课 {lid} 第 {i} 步：example 的 code 和 data 必须二选一")
                elif not (st.get("code") or "").strip():
                    rep.err(f"课 {lid} 第 {i} 步：example 缺少 code")
                elif track.language == "sql":
                    db = st.get("db")
                    if not db or not (PROBLEMS / track.id / "_db" / str(db)).exists():
                        rep.err(f"课 {lid} 第 {i} 步：SQL 示例要写存在的 db（如 bookstore），现在是 {db!r}")
                elif "# ①" not in (st.get("code") or ""):
                    rep.warn(f"课 {lid} 第 {i} 步（{sid}）：示例代码没有用 # ① 这样的注释标出步骤名")
            elif t == "quiz":
                opts = st.get("options") or []
                ans = st.get("answer")
                if not st.get("q") or len(opts) < 2:
                    rep.err(f"课 {lid} 第 {i} 步：quiz 需要 q 和至少 2 个 options")
                if not isinstance(ans, int) or isinstance(ans, bool) or not 0 <= ans < len(opts):
                    rep.err(f"课 {lid} 第 {i} 步：quiz 的 answer 超出选项范围")
                if not (st.get("explain") or "").strip():
                    rep.warn(f"课 {lid} 第 {i} 步：quiz 没有 explain")
            if sid in taught and taught[sid]["lesson"] == lid:
                taught[sid][t] += 1
                if t == "example" and (st.get("code") or "").strip():
                    taught[sid]["examples"].append((i, st["code"]))
        if steps and (steps[0] or {}).get("type") != "read":
            rep.warn(f"课 {lid}：第一步建议是 read（先讲是什么、为什么）")
        for sid in own:
            if sid in taught and taught[sid]["lesson"] == lid:
                t = taught[sid]
                if not t["read"] and not t["example"]:
                    rep.err(f"课 {lid}：skills 里列了 {sid}，但没有任何步骤讲它")
                if t["quiz"] > 2:
                    rep.warn(f"课 {lid}：{sid} 有 {t['quiz']} 道小测，每个技能 0–2 道")
    return taught


def check_track(track: Track, problems: list[dict], own: dict, skills: dict, inherited: set[str], lessons: dict,
                taught: dict, strict: bool, verbose: bool, rep: Report) -> None:
    stages = list(track.stages)
    detectable = detectable_skills(track)
    for m in problems:
        if "in_lesson" in m:
            rep.err(f"{m['id']}：in_lesson 在 v1.2 里已取消（题目都在题目列表里，课按技能自动拼出来）")

    introduced: dict[str, str] = dict.fromkeys(sorted(inherited), "前置学习线")
    optional_skills = {s for s in inherited if skills[s].get("optional")}
    stage_max_diff: dict[str, tuple[int, str]] = {}
    for m in problems:
        pid = m["id"]
        sk = m.get("skills") or {}
        requires = sk.get("requires") or []
        intro = sk.get("introduces")
        if not isinstance(requires, list):
            rep.err(f"{pid}：skills.requires 必须是列表")
            requires = []
        if isinstance(intro, list):
            rep.err(f"{pid}：introduces 只能是一个技能（或 null），现在是列表 {intro}")
            intro = intro[0] if intro else None
        for r in requires:
            if r not in skills:
                rep.err(f"{pid}：requires 里的 {r} 不在技能图里")
            elif r not in introduced:
                rep.err(f"{pid}：requires {r}，但前面没有题引入过它")
        if intro:
            if intro not in own:
                rep.err(f"{pid}：introduces {intro} 不在本线技能图里")
            elif intro in introduced:
                rep.err(f"{pid}：{intro} 已经在 {introduced[intro]} 引入过，不能重复引入")
            else:
                missing = [p for p in skills[intro]["prereqs"] if p not in introduced]
                if missing:
                    rep.err(f"{pid}：引入 {intro} 时，它的前置 {', '.join(missing)} 还没被引入")
                if skills[intro]["stage"] != m["stage"]:
                    rep.warn(f"{pid}：引入的 {intro} 在技能图里属于阶段 {skills[intro]['stage']}，题目在阶段 {m['stage']}")
            if intro in requires:
                rep.err(f"{pid}：{intro} 同时出现在 requires 和 introduces 里")
            if intro in skills:
                t = lessons.get(intro)
                if not t:
                    rep.err(f"{pid}：引入的 {intro} 还没有任何 lesson 文件讲它（需要 read + example）")
                elif not (t["read"] and t["example"]):
                    rep.err(f"{pid}：引入的 {intro} 在 {t['lesson']} 里缺少 "
                            + "、".join(k for k in ("read", "example") if not t[k]))

        declared = set(requires) | ({intro} if intro else set())
        allowed = declared if strict else closure(skills, declared)
        found: list[Detection] = []
        try:
            if m.get("format") != "inspect" and track.language == "python":
                src = (m["_dir"] / "solution.py").read_text(encoding="utf-8")
                found, unknown = detect_python(src, m.get("mode", "function"), m.get("entry"))
                for u in unknown:
                    rep.warn(f"{pid}：{u}")
            elif m.get("format") != "inspect" and track.language == "sql":
                found = detect_sql((m["_dir"] / "solution.sql").read_text(encoding="utf-8"))
        except FileNotFoundError:
            pass
        except SyntaxError as exc:
            rep.err(f"{pid}：参考解语法错误 {exc}")
        used = {d.skill for d in found}
        for s in sorted(used - allowed):
            where = sorted({d.construct + (f"@{d.line}" if d.line else "") for d in found if d.skill == s})
            rep.err(f"{pid}：参考解用到 {s}（{', '.join(where)}），不在 requires ∪ introduces"
                    + ("" if strict else " 及其前置") + " 里")
        for s in sorted(used - set(skills)):
            rep.err(f"{pid}：识别出的技能 {s} 不在技能图里（检查映射表）")
        if m.get("format") != "inspect" and intro and intro in detectable and intro not in used:
            rep.warn(f"{pid}：引入的 {intro} 是可识别的语法，但参考解里没有用到")

        # 选修：必修题不能依赖选修内容引入的技能
        is_optional = bool(m.get("optional"))
        if intro:
            if is_optional:
                optional_skills.add(intro)
                if intro in skills and not skills[intro].get("optional"):
                    rep.warn(f"{pid}：{intro} 在选修题里引入，skills.yaml 里也应标 optional: true")
            elif intro in skills and skills[intro].get("optional"):
                rep.warn(f"{pid}：{intro} 在 skills.yaml 里标了选修，却由必修题引入")
        if not is_optional:
            for s in sorted((declared | used) & optional_skills):
                rep.err(f"{pid}：必修题用到了选修内容才引入的技能 {s}")
        if verbose:
            print(f"  {pid:<44} +{intro or '-':<24} 识别：{', '.join(sorted(used))}")

        # 难度在阶段内大致递增（预测 / 补全是脚手架，不参与）
        if m.get("format") not in SCAFFOLD_FORMATS:
            diff = m.get("difficulty") or 0
            best = stage_max_diff.get(m["stage"])
            if best and diff < best[0] - 6:
                rep.warn(f"{pid}：难度 {diff} 比本阶段前面的 {best[1]}（{best[0]}）低很多")
            if not best or diff > best[0]:
                stage_max_diff[m["stage"]] = (diff, pid)
        if intro and intro not in introduced:
            introduced[intro] = pid

    # 示例代码只能用"这个技能 + 它的前置 + 学习顺序里更早引入的技能"
    pos = {s: i for i, s in enumerate(introduced)}
    for sid, t in taught.items():
        here = pos.get(sid, len(pos))
        allowed = closure(skills, {sid}) | {s for s, p in pos.items() if p < here}
        for i, code in t["examples"]:
            try:
                found = detect_python(code, "predict", None)[0] if track.language == "python" else detect_sql(code)
            except SyntaxError as exc:
                rep.err(f"课 {t['lesson']} 第 {i} 步（{sid} 的示例）：语法错误 {exc}")
                continue
            for s in sorted({d.skill for d in found} - allowed):
                rep.err(f"课 {t['lesson']} 第 {i} 步（{sid} 的示例）用到了这时还没教的 {s}")

    by_stage: dict[str, int] = defaultdict(int)
    for m in problems:
        by_stage[m["stage"]] += 1
    for sid, skill in own.items():
        if skill["stage"] in by_stage and sid not in introduced:
            rep.warn(f"技能 {sid} 所在的阶段 {skill['stage']} 已有题，但没有题引入它")
    stage_txt = "，".join(f"{s}: {by_stage[s]}" for s in stages if by_stage[s])
    n_files = len({t["lesson"] for t in taught.values()})
    rep.info.append(f"{len(own)} 个技能，{len(problems)} 道题（{stage_txt or '无'}）")
    rep.info.append(f"已引入 {len(introduced.keys() & own.keys())}/{len(own)} 个技能")
    rep.info.append(f"课：{n_files} 个 lesson 文件讲了 {len(taught)} 个技能"
                    f"（{sum(t['read'] for t in taught.values())} 段讲解、"
                    f"{sum(t['example'] for t in taught.values())} 个示例、{sum(t['quiz'] for t in taught.values())} 道小测）")


def check_curriculum(selected: str, strict: bool, verbose: bool, *, with_plan: bool = False) -> list[tuple[str, Report]]:
    tracks, errors = load_tracks(PROBLEMS)
    config = Report(errors=[f"{e.path}：{e.message}" for e in errors])
    reports = [("学习线", config)]
    deps = {t.id: set(t.requires) for t in tracks.values()}
    for tid, requires in deps.items():
        for missing in sorted(requires - tracks.keys()):
            config.err(f"{tid} 的前置学习线 {missing} 不存在")
    if selected != "all" and selected not in tracks:
        config.err(f"没有这条学习线：{selected}")
    try:
        order = list(TopologicalSorter(deps).static_order())
    except CycleError as exc:
        config.err("学习线有环：" + " → ".join(exc.args[1]))
        return reports
    if config.errors:
        return reports
    ancestors: dict[str, set[str]] = {}
    for tid in order:
        ancestors[tid] = deps[tid].union(*(ancestors[pre] for pre in deps[tid]))
    selected_ids = set(order) if selected == "all" else {selected}
    needed = selected_ids.union(*(ancestors[t] for t in selected_ids))
    local = {}
    skills = {}
    by_track = {}
    for tid in order:
        if tid not in needed:
            continue
        rep = by_track[tid] = Report()
        if tid in selected_ids:
            reports.append((tid, rep))
        track = tracks[tid]
        if track.status == "planned":
            rep.info.append("规划中")
            continue
        own = local[tid] = load_skills(track, rep)
        for duplicate in skills.keys() & own.keys():
            rep.err(f"技能 id 跨线重复：{duplicate}")
        skills.update(own)
    lessons = {}
    taught = {}
    for tid in local:
        rep = by_track[tid]
        check_prereqs(tracks[tid], local[tid], skills, ancestors[tid], rep)
        taught[tid] = load_lessons(tracks[tid], rep, skills)
        for duplicate in lessons.keys() & taught[tid].keys():
            rep.err(f"技能 {duplicate} 已经在另一条线的课里讲过")
        lessons.update(taught[tid])
    problems_by_track = {}
    for tid in local:
        if tid not in selected_ids:
            continue
        track = tracks[tid]
        mapped = detectable_skills(track)
        if selected != "all":
            mapped = {sid for sid in mapped if sid.startswith(track.skill_prefix + ".")}
        for sid in sorted(mapped - skills.keys()):
            by_track[tid].err(f"检测表里的技能 {sid} 不在技能图里")
        inherited = {sid for pre in ancestors[tid] for sid in local.get(pre, {})}
        problems = problems_by_track[tid] = load_problems(track, by_track[tid])
        check_track(track, problems, local[tid], skills, inherited, lessons, taught[tid], strict, verbose, by_track[tid])
    for tid in needed - selected_ids:
        config.errors.extend(by_track[tid].errors)
    if with_plan:
        reports.append(("plan", check_plan(tracks, problems_by_track)))
    return reports


# ---------------------------------------------------------------------
# 计划覆盖：基础、算法和 SQL 的计划区块分别对应它们的学习线。
# ---------------------------------------------------------------------

def plan_by_stage(block: str, first_stage: str) -> dict[str, list[str]]:
    """按阶段读题单列。0A 的区块从阶段标题下方开始，算法阶段 5 的一行列有多题。"""
    entries: dict[str, list[str]] = defaultdict(list)
    stage = first_stage
    column = None
    for line in block.splitlines():
        if line.startswith("#"):
            heading = re.search(r"(?:阶段\s+|^#+\s+(?:[\d.]+\s+)?)(\d+[A-Z]?)(?=[\s：:（(]|$)", line)
            if heading:
                stage = normalize_stage(heading.group(1))
        if not line.startswith("|"):
            column = None
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if column is None:
            for title in ("LeetCode", "标题", "题目 / 阶梯题", "题目"):
                if title in cells:
                    column = cells.index(title)
                    break
        elif cells[0] != "桥" and column < len(cells):
            entries[stage].extend(re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)*)`", cells[column]))
    return entries


def check_plan(tracks: dict[str, Track], problems_by_track: dict[str, list[dict]]) -> Report:
    rep = Report()
    if not PLAN_DOC.exists() or not LISTS_JSON.exists():
        rep.warn("没有找到 docs/curriculum.md 或 lists.json，跳过计划覆盖检查")
        return rep
    lists = json.loads(LISTS_JSON.read_text(encoding="utf-8"))
    doc = PLAN_DOC.read_text(encoding="utf-8")
    nc250 = set(lists["NC250"])
    extras = set(lists["top-100-liked"]) - nc250
    stage5 = (set(lists["Grind169"]) | set(lists["top-interview-150"])) - nc250 - extras
    sql50 = set(lists["top-sql-50"])
    blocks = dict(re.findall(r"<!-- plan:([\w-]+) -->(.*?)<!-- /plan:\1 -->", doc, re.S))
    for tid, problems in problems_by_track.items():
        if tid not in blocks:
            continue
        plan = plan_by_stage(blocks[tid], next(iter(tracks[tid].stages)))
        actual: dict[str, set[str]] = defaultdict(set)
        for meta in problems:
            slugs = actual[meta["stage"]]
            if isinstance(meta.get("leetcode"), str):
                slugs.add(meta["leetcode"])
        covered = set()
        for stage, planned in plan.items():
            if not planned or stage not in actual:
                continue
            wanted = set(planned)
            found = wanted & actual[stage]
            covered.update(found)
            rep.info.append(f"{tid} 阶段 {stage} 实际覆盖 {len(found)}/{len(wanted)} 道计划题")
            missing = sorted(wanted - found)
            if missing:
                rep.err(f"{tid} 阶段 {stage} 的题目缺少 leetcode：{', '.join(missing)}")
        if tid == "sql":
            rep.info.append(f"SQL 50 实际覆盖 {len(covered & sql50)}/{len(sql50)} 道")

    expectations = {("python", "algo"): nc250 | extras | stage5, ("sql",): sql50}
    for track_ids, expected in expectations.items():
        slugs = []
        for tid in track_ids:
            if tid not in blocks:
                rep.err(f"curriculum.md 缺少 <!-- plan:{tid} --> 区块")
                continue
            entries = re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)*)`", blocks[tid])
            slugs.extend(entries)
            if tid == "algo":
                missing_nc = sorted(nc250 - set(entries))
                if missing_nc:
                    rep.err(f"算法与数据结构的计划缺少 NeetCode 题：{', '.join(missing_nc)}")
                rep.info.append(f"算法与数据结构覆盖 NeetCode {len(nc250) - len(missing_nc)}/{len(nc250)} 道")
        track = " + ".join(track_ids)
        counted = [s for s in slugs if s in expected]
        dup = sorted({s for s in counted if counted.count(s) > 1})
        missing = sorted(expected - set(counted))
        if dup:
            rep.err(f"{track} 计划里重复出现：{', '.join(dup)}")
        if missing:
            rep.err(f"{track} 计划漏掉 {len(missing)} 道：{', '.join(missing)}")
        rep.info.append(f"{track} 计划覆盖 {len(set(counted))}/{len(expected)} 道骨架题")
    return rep


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--track", default="all")
    ap.add_argument("--strict", action="store_true", help="参考解只能用 requires ∪ introduces 本身（不展开前置）")
    ap.add_argument("-v", "--verbose", action="store_true", help="逐题打印识别到的技能")
    ap.add_argument("--no-plan", action="store_true", help="跳过 curriculum.md 计划覆盖检查")
    args = ap.parse_args()

    reports = check_curriculum(args.track, args.strict, args.verbose, with_plan=not args.no_plan)
    total_err = total_warn = 0
    for name, rep in reports:
        print("== 计划覆盖（docs/curriculum.md）" if name == "plan" else f"== {name}")
        for line in rep.info:
            print(f"   {line}")
        for e in rep.errors:
            print(f"   ✗ {e}")
        for w in rep.warnings:
            print(f"   ! {w}")
        if not rep.errors:
            print("   ✓ 没有错误")
        total_err += len(rep.errors)
        total_warn += len(rep.warnings)
    print(f"\n合计：错误 {total_err}，警告 {total_warn}")
    return 1 if total_err else 0


if __name__ == "__main__":
    sys.exit(main())
