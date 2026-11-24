月报要从每一本卖出的书开始算钱。这一步给有效订单的每条图书明细算成交额，同时带上分类和作者，供后面分组。

## 输入与输出

`valid_orders(order_id, user_id, order_date, order_month)` 已筛好有效单。`order_items(order_id, book_id, quantity, unit_price)` 记录册数和成交单价。`books(book_id, category, author_id, price)` 记录每本书的分类、作者和当前标价。

按以下列名和顺序返回，每行属于中间表 `line_amounts`。

`order_id, book_id, order_month, category, author_id, line_amount`

## 示例一 · 书店原始订单

102 号单里有两册 6 号书，每册实际卖 16.65 元。该行是 `(102, 6, 2024-12-01, kids, 8, 33.30)`。同单的 14 号书另占一行。

## 示例二 · 七月加单

2025 年 7 月的 201 号单买了两册 1 号书，每册 12 元，又买了一册匿名的 25 号书，成交价 6 元。两行分别是 `(201, 1, 2025-07-01, fiction, 1, 24.00)` 和 `(201, 25, 2025-07-01, fiction, NULL, 6.00)`。

## 约束

每个 `(order_id, book_id)` 至多出现一次。只保留有效单里实际存在的明细。作者未知的明细仍有金额，`author_id` 保留 NULL。

只提交 CTE 括号里的查询，省略末尾分号。骨架负责表名、括号和逗号。行序不限。
