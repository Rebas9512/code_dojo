## 题目

一行是一次整批交易。按纸种 paper 返回净收益 gain，卖出收款减去买入支出，亏损保留负数。

## 样例输入

`paper_trades`

| paper | side | coins |
|---|---|---|
| L | buy | 18 |
| L | sell | 24 |
| M | buy | 12 |
| M | sell | 9 |

## 样例结果

| paper | gain |
|---|---|
| L | 6 |
| M | -3 |

M 花 12 又收 9，净收益为 -3。

按上表的列顺序输出。行序不限。
