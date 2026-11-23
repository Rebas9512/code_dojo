## 题目

每人每项分别统计，忽略无日期的试卷，同日按 trial 升序。以最早和最晚的两次成绩为准，两端都已知且末次严格提高才列出 reader、topic、first_score、last_score。

## 样例输入

`proof_trials`

| trial | reader | topic | day | score |
|---|---|---|---|---|
| 1 | A | ink | 2025-01-01 | 4 |
| 2 | A | ink | 2025-02-01 | 8 |
| 3 | A | wax | 2025-01-01 | 9 |
| 4 | B | ink | 2025-01-01 | 5 |
| 5 | B | ink | 2025-02-01 | 5 |
| 6 | C | wax | 2025-01-01 | NULL |

## 样例结果

| reader | topic | first_score | last_score |
|---|---|---|---|
| A | ink | 4 | 8 |

A 的 ink 从 4 提高到 8，B 的两次 5 分持平。

按上表的列顺序输出。按 reader、topic 依次升序。
