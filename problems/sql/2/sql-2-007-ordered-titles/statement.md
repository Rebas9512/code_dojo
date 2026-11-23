## 题目

打印逐项装箱单。每一条订单明细输出订单号、下单日期、书名和本次订购册数。多本同名书属于不同明细时，保留各自的一行。所有状态都列出。

把编辑器里的 `____` 换成缺少的 SQL。

## 用到的表

`orders(order_id, user_id, order_date, status)` 每笔订单一行，分别记录订单号、用户号、下单日期和状态。

`order_items(order_id, book_id, quantity, unit_price)` 每笔订单的每种书一行，记录订购册数和当时的成交单价。

`books(book_id, title, author_id, price, category)` 每种书一行，记录书名、作者编号、当前标价和分类；不同版本可以同名。

## 示例结果

| order_id | order_date | title | quantity |
|---|---|---|---|
| 101 | 2024-12-02 | Data at Dawn | 1 |
| 101 | 2024-12-02 | Python in Practice | 1 |
| 102 | 2024-12-15 | Little Cloud | 2 |
| 102 | 2024-12-15 | Moon Rabbit | 1 |
| 103 | 2024-12-31 | SQL for Curious Minds | 1 |
| 104 | 2025-01-01 | Rainy Season | 2 |
| 104 | 2025-01-01 | The Map Maker | 1 |
| 104 | 2025-01-01 | The Silent Harbor | 1 |

样例共 47 行。这里只列出其中 8 行。

102 号订单买了两册 Little Cloud 和一册 Moon Rabbit。装箱单有两行，每种书一行。

按上表的列顺序输出。行的顺序不限。
