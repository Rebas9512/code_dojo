## 题目

原表每种纸一行，把 east、west、pier 三列价格展开为 paper、counter、price。跳过空价格，保留零价和不同柜台的同价。

## 样例输入

`quote_board`

| paper | east | west | pier |
|---|---|---|---|
| Ash | 4 | NULL | 8 |
| Elm | NULL | 0 | NULL |
| Oak | 3 | 3 | 3 |

## 样例结果

| paper | counter | price |
|---|---|---|
| Ash | east | 4 |
| Oak | east | 3 |
| Elm | west | 0 |
| Oak | west | 3 |
| Ash | pier | 8 |
| Oak | pier | 3 |

Oak 虽然三柜同价，展开后仍有三行。Elm 西柜报价为 0。

按上表的列顺序输出。行序不限。
