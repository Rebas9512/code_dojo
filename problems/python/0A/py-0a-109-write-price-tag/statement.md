## 题目

给商品名 `name` 和价格 `price`，返回价签文字，格式是 `name：price yuan`，价格保留两位小数。
例如 `("apple", 3.5)` → `"apple：3.50 yuan"`。注意冒号是中文冒号 `：`，小写的 `yuan` 前面有一个空格。

## 示例

**示例 1**

```
输入：name = "apple", price = 3.5
输出："apple：3.50 yuan"
```

**示例 2**

```
输入：name = "notebook", price = 12
输出："notebook：12.00 yuan"
```

## 约束

- `0 <= price <= 10^6`
