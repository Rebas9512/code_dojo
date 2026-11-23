## 题目

打印订单抬头。每笔订单一行，列出订单编号和下单人的姓名。取消的订单也有抬头。

把编辑器里的 `____` 换成缺少的 SQL。

## 用到的表

`orders(order_id, user_id, order_date, status)` 每笔订单一行，分别记录订单号、用户号、下单日期和状态。

`users(user_id, name)` 每位读者一行，编号唯一，姓名可以重复。

## 示例结果

| order_id | name |
|---|---|
| 101 | Li Wei |
| 102 | Zhang Min |
| 103 | Li Wei |
| 104 | Alice Brown |
| 105 | Wang Fang |
| 106 | Bob Smith |
| 107 | Li Wei |
| 108 | Chen Jie |

样例共 33 行。这里只列出其中 8 行。

101 和 103 是两笔订单，都由编号为 1 的 Li Wei 下单，结果里应分别出现。

按上表的列顺序输出。行的顺序不限。
