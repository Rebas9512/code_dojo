## 题目

locations 按书名记录架号。补全赋值，将指定书移到 shelf，返回更新后的字典；新书也这样登记。

## 示例

**示例 1**

```text
输入：locations = {'Wind': 2}, title = 'Wind', shelf = 0
输出：{'Wind': 0}
```

**示例 2**

```text
输入：locations = {}, title = 'Rain', shelf = 3
输出：{'Rain': 3}
```

## 约束

书名非空，原字典最多有 50 本书，架号为 0–99。
