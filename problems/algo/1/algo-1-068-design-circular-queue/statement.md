## 题目

实现 MyCircularQueue(k)。enQueue(value) 加入队尾，deQueue() 移除队首，成功返回 True，已满或已空而无法操作返回 False。Front()、Rear() 分别读首尾，空时返回 -1；isEmpty() 和 isFull() 分别判断空、满。请自行管理容量，不调用内置队列。

样例里的操作、参数、结果按列一一对应。第一项建立对象，同一个用例的后续操作都作用在它上面。null 表示该步没有返回值。

## 示例

**示例 1**

```text
操作 ["MyCircularQueue","enQueue","enQueue","enQueue","deQueue","enQueue","Front","Rear"]
参数 [[2],[6],[4],[7],[],[7],[],[]]
结果 [null,true,true,false,true,true,4,7]
```

前两项已占满两个位置，第三次加入失败。取走 6 后，7 才能从队尾进入。

**示例 2**

```text
操作 ["MyCircularQueue","Rear","deQueue","enQueue","isFull"]
参数 [[1],[],[],[0],[]]
结果 [null,-1,false,true,true]
```

## 约束

1 ≤ k ≤ 1000，每个值 0 至 1000，至多 3000 次操作。
