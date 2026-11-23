## 题目

编辑器里的 MySQL 查询会在 PostgreSQL 上报错。把它改写成 PostgreSQL 查询，取出的台位应与原稿相同。

先算出每个台位的总张数 `total`，按总张数降序排列，同量时按台位名 `bench` 升序。跳过前两名，只返回第三名的 `bench` 和 `total`。

## 样例输入

`load_slips`

| bench | sheets |
|---|---|
| P | 8 |
| P | 4 |
| Q | 9 |
| R | 5 |
| S | 2 |

## 样例结果

| bench | total |
|---|---|
| R | 5 |

先跳过合计 12 的 P 和合计 9 的 Q，第三名 R 的合计为 5。

按上表的列顺序输出。行序不限。
