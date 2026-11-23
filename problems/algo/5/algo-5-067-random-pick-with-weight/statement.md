## 题目

实现 WeightedPicker(weights) 和 pickIndex()。下标 i 被选中的概率应为 weights[i] 除以所有权重之和。每次重新抽取，权重保持不变。样例中的 PickTrial.sample(次数) 统计一批抽取，检查下标和频率是否符合权重，返回布尔值。

请实现 `WeightedPicker`。起始代码的 `PickTrial` 负责转换样例和读取结果，提交时保留它。

## 示例

**示例 1**

```text
操作 ["PickTrial","sample"]
参数 [[[1,3,6]],[16000]]
结果 [null,true]
```

权重 1、3、6 将十份机会分给三个下标，不能给每个下标同样多的机会。

**示例 2**

```text
操作 ["PickTrial","pickIndex"]
参数 [[[9]],[]]
结果 [null,0]
```

## 约束

1 至 10 000 个正整数权重，每项至多 100 000。初始化后应能在 O(log n) 或更短时间完成一次抽取。
