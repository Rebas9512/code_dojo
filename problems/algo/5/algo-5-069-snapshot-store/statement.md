## 题目

实现 MemoryStore。set(key, value) 写入整数，重写覆盖；get(key) 读取，缺失时返回 None；delete(key) 删除并返回删除前是否存在。 scan(prefix) 按字典序返回以 prefix 开头的全部可见键，空前缀匹配所有键。 时钟从 0 开始，advance(now) 将它移到不早于当前的整数时刻。set_ttl(key, value, ttl) 的写入在当前时刻起生效，到当前时刻加 ttl 恰好失效。set 的普通写入永久有效并取消旧期限。 backup() 保存当前可见键和各自的剩余寿命，替换旧快照；restore() 将最近快照恢复到当前时刻，恢复后寿命从此刻继续计。恢复前保证做过备份。 除标明结果的方法，其余方法返回 None。

起始代码保留上一级的实现。实现备份与恢复，尤其留意恢复时已经过去的时间。

## 示例

**示例 1**

```text
操作 ["MemoryStore","set_ttl","advance","backup","advance","restore","advance","get","advance","get"]
参数 [[],["x",7,5],[2],[],[10],[],[12],["x"],[13],["x"]]
结果 [null,null,null,null,null,null,null,7,null,null]
```

备份时还剩 3 个时间单位，时刻 10 恢复后可读到时刻 13 之前。

**示例 2**

```text
操作 ["MemoryStore","backup","set","restore","get"]
参数 [[],[],["k",1],[],["k"]]
结果 [null,null,null,null,null]
```

## 约束

每组至多 30 000 次调用；键为非空字符串，ttl 为正整数。
