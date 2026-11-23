## 题目

输出每位装订员的 given、family、room、wing。名册每人一行，工位表每人至多一行；还没有工位时，后两列为空。

## 样例输入

`binders`

| badge | given | family |
|---|---|---|
| 11 | Ivo | Lane |
| 12 | Ona | Hall |
| 13 | Teo | Moss |

`desk_map`

| badge | room | wing |
|---|---|---|
| 11 | Reed | N |
| 13 | Pine | S |

## 样例结果

| given | family | room | wing |
|---|---|---|---|
| Ivo | Lane | Reed | N |
| Ona | Hall | NULL | NULL |
| Teo | Moss | Pine | S |

Ona 在名册里，但还没有领到工位。

按上表的列顺序输出。行序不限。
