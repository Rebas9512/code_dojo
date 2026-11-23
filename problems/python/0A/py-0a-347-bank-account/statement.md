## 题目

实现 Account(start)。deposit(amount) 存款后返回 None；withdraw(amount) 余额足够时扣款并返回 True，否则保留余额并返回 False；balance() 返回余额。

## 示例

**示例 1**

```text
调用：Account(5) → deposit(2) → withdraw(7) → balance()
依次得到：[None, None, True, 0]
```

**示例 2**

```text
调用：Account(1) → withdraw(3) → balance()
依次得到：[None, False, 1]
```

## 约束

金额和初始余额为非负整数，至多 50 次操作。
