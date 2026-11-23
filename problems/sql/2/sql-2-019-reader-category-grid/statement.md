## 题目

运营要一张完整的读者 × 图书分类清单。每个读者和书目中出现的每个分类的组合占一行，依次输出用户编号、分类和该用户购买该类书的不同订单数。一单买同类两种书记一单；没买过填 0。

把编辑器里的 `____` 换成缺少的 SQL。

## 用到的表

`users(user_id, name)` 每位读者一行，编号唯一，姓名可以重复。

书店随题提供 `categories(category)`，每个目录分类恰好一行（含售罄图书的分类）。

`purchases(user_id, category, order_id)` 也是随题提供的清单，每行代表一笔未取消订单中的一种书。同一订单号和分类可出现多次。

## 示例结果

| user_id | category | order_count |
|---|---|---|
| 1 | cooking | 0 |
| 1 | fantasy | 0 |
| 1 | fiction | 0 |
| 1 | history | 0 |
| 1 | kids | 0 |
| 1 | programming | 3 |
| 1 | scifi | 2 |
| 10 | cooking | 0 |

样例共 140 行。这里只列出其中 8 行。

101 号单里有两种 programming 图书，给 1 号读者的这个格子只加 1 单。

按上表的列顺序输出。行的顺序不限。
