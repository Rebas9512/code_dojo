## 题目

Counter(start) 保存起点。add(step) 把变化量计入当前读数，get() 返回当前读数。补全 add 的更新式；add 本身返回 None。

## 示例

**示例 1**

```text
调用：Counter(3) → add(2) → get()
依次得到：[None, None, 5]
```

**示例 2**

```text
调用：Counter(0) → get()
依次得到：[None, 0]
```

## 约束

每个计数器至多接受 50 次操作，参数为整数。
