## 题目

实现 IndexedRegister()。insert(value) 只在编号首次出现时追加到末尾，返回是否追加。position(value) 交回从 0 算的登记位置；不存在返回 -1。下一次扩展会加入删除和随机抽取。

## 示例

**示例 1**

```text
操作 ["IndexedRegister","insert","insert","insert","position"]
参数 [[],[9],[9],[4],[4]]
结果 [null,true,false,true,1]
```

重复登记 9 没有占新位置，4 的位置是 1。

**示例 2**

```text
操作 ["IndexedRegister","position"]
参数 [[],[8]]
结果 [null,-1]
```

## 约束

至多 30 000 次操作，两个方法均应平均 O(1)。
