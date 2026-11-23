## 题目

实现 MemoryStore。set(key, value) 写入整数，重写覆盖；get(key) 读取，缺失时返回 None；delete(key) 删除并返回删除前是否存在。 除标明结果的方法，其余方法返回 None。

## 示例

**示例 1**

```text
操作 ["MemoryStore","set","get","delete","delete"]
参数 [[],["r",0],["r"],["r"],["r"]]
结果 [null,null,0,true,false]
```

写入的 0 可以读回。第一次删除成功，第二次已没有这个键。

**示例 2**

```text
操作 ["MemoryStore","get"]
参数 [[],["?"]]
结果 [null,null]
```

## 约束

每组至多 30 000 次调用；键为非空字符串，ttl 为正整数。
