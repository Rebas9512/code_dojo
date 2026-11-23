## 题目

实现 MemoryStore。set(key, value) 写入整数，重写覆盖；get(key) 读取，缺失时返回 None；delete(key) 删除并返回删除前是否存在。 scan(prefix) 按字典序返回以 prefix 开头的全部可见键，空前缀匹配所有键。 除标明结果的方法，其余方法返回 None。

起始代码保留上一级的实现。增加前缀查询，让已有读写继续工作。

## 示例

**示例 1**

```text
操作 ["MemoryStore","set","set","set","scan"]
参数 [[],["bb",2],["ba",0],["c",4],["b"]]
结果 [null,null,null,null,["ba","bb"]]
```

ba 和 bb 都以 b 开头，输出按键排序。

**示例 2**

```text
操作 ["MemoryStore","scan"]
参数 [[],[""]]
结果 [null,[]]
```

## 约束

每组至多 30 000 次调用；键为非空字符串，ttl 为正整数。
