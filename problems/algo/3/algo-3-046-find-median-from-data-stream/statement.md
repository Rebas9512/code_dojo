## 题目

实现 MedianFinder。addNum(num) 把整数加入集合，findMedian() 返回当前中位数。偶数项时取居中两项的平均值。

操作与参数逐项对应。第一步创建实例，之后共用这个实例，null 表示该步没有返回值。

## 示例

**示例 1**

```text
操作 ["MedianFinder","addNum","addNum","findMedian"]
参数 [[],[8],[3],[]]
结果 [null,null,null,5.5]
```

3、8 排好后都在中间，平均为 5.5。

**示例 2**

```text
操作 ["MedianFinder","addNum","findMedian"]
参数 [[],[-2],[]]
结果 [null,null,-2]
```

## 约束

最多 50 000 次调用，查询前至少已加入一项。
