## 题目

ChannelCounter(width) 建立宽度为 width 秒的窗口。hit(channel,time) 登记该频道一次脉冲并返回 None。count(channel,time) 返回该频道在 (time−width,time] 的次数，未知频道为 0。

## 示例

**示例 1**

```text
操作 ["ChannelCounter","hit","hit","count","count"]
参数 [[3],["a",1],["b",2],["a",2],["a",4]]
结果 [null,null,null,1,0]
```

b 的脉冲不能算给 a；到了时刻 4，a 在时刻 1 的脉冲恰好过期。

**示例 2**

```text
操作 ["ChannelCounter","count"]
参数 [[8],["z",5]]
结果 [null,0]
```

## 约束

width 为正整数，最多 30 000 次调用；全局记录和查询的时间非递减，频道名非空。
