## 题目

列出从未订过 red 颜料的工匠 name，包含没有任何订单的人。未署名订单的 maker 为空。

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

| name |
|---|
| Bo |
| Cy |
| Dee |

Bo 只订过蓝墨。另有一张未署名的红墨单，不能归到 Bo 名下。

按上表的列顺序输出。行序不限。
