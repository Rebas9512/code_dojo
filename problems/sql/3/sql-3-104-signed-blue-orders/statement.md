## 题目

输出至少有一张蓝墨订单的 maker。未署名的订单没有工匠编号。

## 样例输入

`makers`

| maker | name |
|---|---|
| 1 | Ari |
| 2 | Bo |
| 3 | Cy |
| 4 | Dee |

`ink_orders`

| ticket | maker | pigment |
|---|---|---|
| 11 | 1 | red |
| 12 | 1 | blue |
| 13 | 2 | blue |
| 14 | NULL | red |

## 样例结果

| maker |
|---|
| 1 |
| 2 |

1 号有两种颜色的订单，其中一张蓝墨单就足以使他入选。

按上表的列顺序输出。行序不限。
