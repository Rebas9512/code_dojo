## 题目

实现 MemoryStore。set(key, value) 写入整数，重写覆盖；get(key) 读取，缺失时返回 None；delete(key) 删除并返回删除前是否存在。 scan(prefix) 按字典序返回以 prefix 开头的全部可见键，空前缀匹配所有键。 时钟从 0 开始，advance(now) 将它移到不早于当前的整数时刻。set_ttl(key, value, ttl) 的写入在当前时刻起生效，到当前时刻加 ttl 恰好失效。set 的普通写入永久有效并取消旧期限。 除标明结果的方法，其余方法返回 None。

起始代码保留上一级的实现。为记录增加失效时刻，并让单键操作和前缀查询遵守同一时钟。

## 示例

**示例 1**

```text
操作 ["MemoryStore","set_ttl","advance","get","advance","get"]
参数 [[],["x",7,3],[2],["x"],[3],["x"]]
结果 [null,null,null,7,null,null]
```

时刻 2 仍能读到 7，时刻 3 刚好失效。

**示例 2**

```text
操作 ["MemoryStore","set_ttl","set","advance","get"]
参数 [[],["a",0,1],["a",6],[2],["a"]]
结果 [null,null,null,null,6]
```

## 约束

每组至多 30 000 次调用；键为非空字符串，ttl 为正整数。
