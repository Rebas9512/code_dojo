## 题目

从 13 号库房向上追溯至根，输出每个严格上级的 unit 及要经过的边数 distance，不含 13 本身。关系是一棵树。

## 样例输入

`archive_units`

| unit | parent | label | budget |
|---|---|---|---|
| 10 | NULL | Atrium | 20 |
| 11 | 10 | Birch | 6 |
| 12 | 10 | Cedar | 7 |
| 13 | 11 | Dune | 9 |

## 样例结果

| unit | distance |
|---|---|
| 11 | 1 |
| 10 | 2 |

13 → 11 → 10，走两条边才到根。

按上表的列顺序输出。行序不限。
