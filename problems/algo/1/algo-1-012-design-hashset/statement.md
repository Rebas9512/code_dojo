## 题目

实现 MyHashSet()。add(key) 登记，remove(key) 注销，contains(key) 返回是否仍登记。重复登记、注销不存在的号码都允许。前两个操作无返回值；请自己实现集合，勿调用内置集合或字典。

样例里的操作、参数、结果按列一一对应。第一项建立对象，同一个用例的后续操作都作用在它上面。null 表示该步没有返回值。

## 示例

**示例 1**

```text
操作 ["MyHashSet","add","remove","contains"]
参数 [[],[9],[9],[9]]
结果 [null,null,null,false]
```

先登记 9 再注销 9，最后查询时它已经不在登记簿里。

**示例 2**

```text
操作 ["MyHashSet","contains","add","contains"]
参数 [[],[0],[0],[0]]
结果 [null,false,null,true]
```

## 约束

0 ≤ key ≤ 1 000 000，至多 10 000 次操作。
