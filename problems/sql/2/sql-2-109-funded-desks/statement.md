## 题目

流水 coins 有正有负。返回余额严格大于 100 的员工名字 given 与余额 balance。每人的账户由 badge 标识。

## 样例输入

`binders`

| badge | given | family |
|---|---|---|
| 11 | Ivo | Lane |
| 12 | Ona | Hall |
| 13 | Teo | Moss |

`credit_moves`

| badge | coins |
|---|---|
| 11 | 70 |
| 11 | 45 |
| 12 | 140 |
| 12 | -40 |
| 13 | 35 |

## 样例结果

| given | balance |
|---|---|
| Ivo | 115 |

Ona 收到 140 又支出 40，余额恰好 100。

按上表的列顺序输出。行序不限。
