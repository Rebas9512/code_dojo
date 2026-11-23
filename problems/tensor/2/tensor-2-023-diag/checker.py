"""坐标题传入整数张量，允许生成坐标、读形状、索引及逐元素运算。"""
import ast
from pathlib import Path

import torch
from dojo_compare import allclose


def check_notation():
    tree = ast.parse(Path("user.py").read_text(encoding="utf-8"))
    # 接受常用导入别名。len 与 size 只用于读取形状。
    modules = {"torch"}
    ranges = set()
    helpers = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(a.asname or "torch" for a in node.names if a.name == "torch")
        if isinstance(node, ast.ImportFrom) and node.module == "torch":
            ranges.update(a.asname or "arange" for a in node.names if a.name == "arange")
    for node in ast.walk(tree):
        if isinstance(node, ast.MatMult):
            raise AssertionError("请用坐标、广播与索引完成计算。")
        if isinstance(node, ast.Attribute) and node.attr in ("T", "mT", "H", "mH"):
            raise AssertionError("请用行列坐标和索引表达轴的移动。")
        if isinstance(node, ast.Call):
            name = ast.unparse(node.func)
            allowed = name in ranges or name in helpers or name == "len"
            if isinstance(node.func, ast.Attribute):
                allowed |= (node.func.attr == "arange" and ast.unparse(node.func.value) in modules)
                allowed |= node.func.attr in ("size", "numel")
            assert allowed, f"第 {node.lineno} 行使用了 {name}，本题只用 arange、形状、逐项运算和索引。"


def check_function(args, expected, fn):
    check_notation()
    inputs = [torch.tensor(v, dtype=torch.int64) if isinstance(v, list) else v for v in args]
    result = fn(*inputs)
    assert isinstance(result, torch.Tensor), "请返回整数张量。"
    reason = allclose(torch.tensor(expected, dtype=torch.int64), result, rtol=0, atol=0)
    assert reason is None, reason
    return True
