## 题目

列出每名装订员的 given 和送书总里程 distance，尚未送书记 0。名字唯一。

## 样例输入

`binders`

| badge | given | family |
|---|---|---|
| 11 | Ivo | Lane |
| 12 | Ona | Hall |
| 13 | Teo | Moss |

`route_lengths`

| badge | km |
|---|---|
| 11 | 4 |
| 11 | 6 |
| 13 | 10 |

## 样例结果

| given | distance |
|---|---|
| Ivo | 10 |
| Teo | 10 |
| Ona | 0 |

Ivo 和 Teo 都走了 10 公里，Ivo 排在前面。

按上表的列顺序输出。按 distance 降序，再按 given 升序。
