## 题目

实现 Stack()。push(x) 把编号放到顶部并返回 None；pop() 取走并返回顶部；peek() 只看顶部；size() 返回当前张数。空摞的 pop 和 peek 都返回 None。

## 示例

**示例 1**

```text
调用：Stack() → push(2) → push(5) → peek() → pop() → size()
依次得到：[None, None, None, 5, 5, 1]
```

**示例 2**

```text
调用：Stack() → pop() → peek()
依次得到：[None, None, None]
```

## 约束

至多 100 次操作，编号是任意整数，可重复。
