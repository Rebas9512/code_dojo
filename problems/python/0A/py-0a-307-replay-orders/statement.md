## 题目

返回一本能按客人名字查的点单簿，每人对应逐次点过的菜；查询者要能辨认先后、也能看出连点两次同一道菜。输入每行是 [客人, 菜名]。

## 示例

**示例 1**

```text
输入：rows = [['Lin', 'noodles'], ['Ye', 'porridge'], ['Lin', 'noodles']]
输出：{'Lin': ['noodles', 'noodles'], 'Ye': ['porridge']}
```

**示例 2**

```text
输入：rows = [['Yu', 'tea'], ['Yu', 'soup']]
输出：{'Yu': ['tea', 'soup']}
```

## 约束

记录有 0–100 行，客人和菜名都是非空字符串。
