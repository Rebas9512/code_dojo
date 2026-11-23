"""将助教和出题格式映射到 Codex 的严格 JSON Schema，并还原答复。"""

from collections import Counter
from typing import Any


def strict_schema(schema: dict[str, Any]) -> dict[str, Any]:
    definitions = schema.get("$defs", {})

    def convert(schema: dict) -> dict:
        if "$ref" in schema:
            return convert(definitions[schema["$ref"].split("/")[-1]])
        # 严格对象不能有任意键。看数据题的误解映射按键值对传输。
        if isinstance(values := schema.get("additionalProperties"), dict):
            return {"type": "array", "items": convert({
                "type": "object", "properties": {"key": {"type": "string"}, "value": values},
                "required": ["key", "value"],
            })}
        # 严格模式支持数组条数约束（如 SQL 附加题的错误写法 1–2 条），字符串长度约束不支持，丢掉。
        result = {k: schema[k] for k in ("type", "description", "enum", "minItems", "maxItems") if k in schema}
        if "const" in schema:
            result["enum"] = [schema["const"]]
        if "enum" in result and "type" not in result:
            result["type"] = "string"  # 题目格式里没有显式类型的枚举都是文本
        if branches := schema.get("oneOf") or schema.get("anyOf"):
            options = [convert(branch) for branch in branches]
            # 对象联合的首键要能区分分支，如 SQL 的 query / probe。
            objects = [option for option in options if option.get("type") == "object"]
            counts = Counter(key for obj in objects for key in obj["properties"])
            for obj in objects:
                props = obj["properties"]
                keys = sorted(props, key=lambda key: counts[key])
                obj.update(properties={key: props[key] for key in keys}, required=keys)
            result["anyOf"] = options
        if "items" in schema:
            result["items"] = convert(schema["items"])
        if schema.get("type") == "object":
            properties = {}
            for key, field in schema.get("properties", {}).items():
                child = convert(field)
                if key not in schema.get("required", ()):
                    variants = child.get("anyOf", [child])
                    if {"type": "null"} not in variants:
                        child = {"anyOf": [*variants, {"type": "null"}]}
                properties[key] = child
            result.update(properties=properties, required=list(properties), additionalProperties=False)
        return result
    return convert(schema)


def restore_result(data: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    def resolve(node: dict) -> dict:
        return schema["$defs"][node["$ref"].split("/")[-1]] if "$ref" in node else node

    def restore(value: Any, node: dict) -> Any:
        if not isinstance(value, (dict, list)):
            return value
        node = resolve(node)
        if branches := node.get("oneOf") or node.get("anyOf"):
            # 现有对象分支由各自的必填字段区分（例如 options / accept、query / probe）。
            for branch in map(resolve, branches):
                if isinstance(value, dict) and branch.get("type") == "object" and set(branch["required"]) <= value.keys():
                    return restore(value, branch)
                if isinstance(value, list) and branch.get("type") == "array":
                    return restore(value, branch)
        if isinstance(values := node.get("additionalProperties"), dict):
            return {pair["key"]: restore(pair["value"], values) for pair in value}
        if isinstance(value, list):
            return [restore(item, node["items"]) for item in value]
        return {key: restore(item, node["properties"][key]) for key, item in value.items()
                if item is not None or key in node.get("required", ())}

    return restore(data, schema)
