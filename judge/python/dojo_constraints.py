"""题目声明的静态写法约束，检查循环、导入和直接调用。"""

import ast


def dotted(node, aliases):
    if isinstance(node, ast.Name):
        return aliases.get(node.id, node.id)
    if isinstance(node, ast.Attribute):
        return f"{dotted(node.value, aliases)}.{node.attr}"
    return ""


class Visitor(ast.NodeVisitor):
    def __init__(self, rules):
        self.rules = rules
        self.aliases = {}
        self.errors = []

    def report(self, node, message):
        self.errors.append((node.lineno, message))

    def visit_Module(self, node):
        # 函数里的全局名字在调用时查找，模块末尾的 import 同样生效。
        for statement in node.body:
            if isinstance(statement, (ast.Import, ast.ImportFrom)):
                self.visit(statement)
        self.generic_visit(node)

    def visit(self, node):
        if self.rules.get("no_loops") and isinstance(node, (ast.For, ast.AsyncFor, ast.While, ast.ListComp,
                                                             ast.DictComp, ast.SetComp, ast.GeneratorExp)):
            self.report(node, "本题要求向量化，请去掉循环或推导式")
        return super().visit(node)

    def visit_FunctionDef(self, node):
        outer = self.aliases
        self.aliases = outer.copy()
        for arg in ast.walk(node.args):
            if isinstance(arg, ast.arg):
                self.aliases.pop(arg.arg, None)
        self.generic_visit(node)
        self.aliases = outer

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Import(self, node):
        for item in node.names:
            self.check_import(node, item.name)
            root = item.name.split(".")[0]
            self.aliases[item.asname or root] = item.name if item.asname else root

    def visit_ImportFrom(self, node):
        for item in node.names:
            name = f"{node.module}.{item.name}"
            self.check_import(node, name)
            if item.name == "*":
                prefix = f"{node.module}."
                for call in self.rules.get("forbid_calls", []):
                    if call.startswith(prefix):
                        bound = call[len(prefix):].split(".")[0]
                        self.aliases[bound] = prefix + bound
            else:
                self.aliases[item.asname or item.name] = name

    def check_import(self, node, name):
        for module in self.rules.get("forbid_imports", []):
            if name == module or name.startswith(module + "."):
                self.report(node, f"本题不能导入 {module}")

    def visit_Assign(self, node):
        self.visit(node.value)
        name = dotted(node.value, self.aliases)
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.aliases[target.id] = name or target.id
            self.visit(target)

    def visit_Call(self, node):
        name = dotted(node.func, self.aliases)
        if name in self.rules.get("forbid_calls", []):
            self.report(node, f"本题需要手写实现，不能调用 {name}")
        self.generic_visit(node)


def violation(source, rules):
    visitor = Visitor(rules)
    visitor.visit(ast.parse(source))
    if visitor.errors:
        line, reason = min(visitor.errors, key=lambda error: error[0])
        return f"第 {line} 行：{reason}"
    return None
