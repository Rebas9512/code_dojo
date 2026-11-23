## 题目

每笔借用占一件模具，back 为空表示尚未归还。列出全部现有副本都借出的 design、在借数 on_loan。每种模具至少有一件。

## 样例输入

`mould_stock`

| design | copies |
|---|---|
| Elm | 2 |
| Ash | 1 |
| Oak | 2 |

`mould_loans`

| design | slip | back |
|---|---|---|
| Elm | 1 | NULL |
| Elm | 2 | NULL |
| Elm | 3 | 2025-02-01 |
| Ash | 4 | NULL |
| Oak | 5 | NULL |

## 样例结果

| design | on_loan |
|---|---|
| Elm | 2 |
| Ash | 1 |

Elm 曾借出三次，其中两件还在外面，正好等于副本数。

按上表的列顺序输出。按 on_loan 降序，再按 design 升序。
