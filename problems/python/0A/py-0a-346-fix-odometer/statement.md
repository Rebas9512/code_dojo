## 题目

Meter(start) 保存里程。advance(k) 应累加 k 并交回新的总里程；read() 随时读取总里程。现在 advance 看起来算对了，但 read 仍读到旧值。

## 示例

**示例 1**

```text
调用：Meter(2) → advance(3) → read()
依次得到：[None, 5, 5]
```

**示例 2**

```text
调用：Meter(0) → advance(0)
依次得到：[None, 0]
```

## 约束

初始值和每次增加量都是非负整数，至多 50 次操作。
