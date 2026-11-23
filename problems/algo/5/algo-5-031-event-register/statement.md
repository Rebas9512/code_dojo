## 题目

实现 EventCounter。hit(time) 登记一次脉冲并返回 None，count(time) 返回至今登记的总次数。同一秒内可收到多个脉冲。下一次扩展会加入有效时间窗。

## 示例

**示例 1**

```text
操作 ["EventCounter","hit","hit","count"]
参数 [[],[4],[4],[5]]
结果 [null,null,null,2]
```

时刻 4 发生两次，时刻 5 没有新增，累计值仍为 2。

**示例 2**

```text
操作 ["EventCounter","count"]
参数 [[],[1]]
结果 [null,0]
```

## 约束

至多 30 000 次调用，整数秒 time ≥ 1，所有调用时刻非递减。
