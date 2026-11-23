## 题目

用带子查询的一条 DELETE 从 paper_claims 删除列在 void_slips 的单据。清单可能重复、有 NULL 或有未登记的单号。核对剩余的 claim、sheets。

## 样例输入

`paper_claims`

| claim | sheets |
|---|---|
| 1 | 8 |
| 2 | 5 |
| 3 | 11 |
| 4 | 3 |

`void_slips`

| claim |
|---|
| 2 |
| 4 |
| NULL |

## 修改后的表

| claim | sheets |
|---|---|
| 1 | 8 |
| 3 | 11 |

清单中的 2 和 4 均需删除，空白清单行不指向任何单据。
