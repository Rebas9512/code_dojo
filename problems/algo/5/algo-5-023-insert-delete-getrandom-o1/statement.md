## 题目

实现 RandomizedSet。insert(val) 和 remove(val) 返回集合是否发生了变化。getRandom() 在非空集合里等概率抽出一个现存编号，不把它删掉。三个方法都应平均 O(1)。样例中 SetTrial 的 sample(当前成员列表,次数) 连续调用 getRandom，检查结果的范围与频数，返回是否通过。

请实现 `RandomizedSet`。起始代码的 `SetTrial` 负责转换样例和读取结果，提交时保留它。

## 示例

**示例 1**

```text
操作 ["SetTrial","insert","insert","sample","remove","getRandom"]
参数 [[],[7],[3],[[7,3],4096],[7],[]]
结果 [null,true,true,true,true,3]
```

登记 7 和 3 后抽取应覆盖两者；删除 7 后只能抽到 3。

**示例 2**

```text
操作 ["SetTrial","remove","insert","insert"]
参数 [[],[8],[-2],[-2]]
结果 [null,false,true,false]
```

## 约束

不在空集合上抽取，至多 50 000 次更新或抽取。
