## 题目

列出至少买过一本 programming 类图书的读者编号和姓名。取消的订单不算。同名读者按编号区分。

把编辑器里的 `____` 换成缺少的 SQL。

## 用到的表

读者表 `users(user_id, name)` 每人一行。

订单表 `orders(order_id, user_id, order_date, status)` 每单一行，日期可重复。

书目表 `books(book_id, title, category, price)` 每本书一行，价格单位为元。

订单明细 order_items(order_id, book_id, quantity) 连接订单和图书。

## 示例结果

| user_id | name |
|---|---|
| 1 | Li Wei |
| 10 | Emma Davis |
| 19 | Lin Xi |
| 2 | Zhang Min |
| 3 | Alice Brown |
| 5 | Bob Smith |

样例共 6 行。

一个人即使在两张订单里买了编程书，外层名册里也只有一行。

按上表的列顺序输出。行的顺序不限。
