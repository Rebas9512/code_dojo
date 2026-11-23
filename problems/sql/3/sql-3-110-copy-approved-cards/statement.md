## 题目

用一条 INSERT … SELECT 将所有 pass 的 slip 和 sheets 加入 proof_archive。队列表的编号尚未入档，归档表里原有的记录继续保留。

## 样例输入

`proof_queue`

| slip | verdict | sheets |
|---|---|---|
| 21 | pass | 8 |
| 22 | hold | 5 |
| 23 | pass | 12 |

`proof_archive`

| slip | sheets |
|---|---|
| 9 | 4 |

## 修改后的表

| slip | sheets |
|---|---|
| 9 | 4 |
| 21 | 8 |
| 23 | 12 |

9 号是旧档，21 和 23 是本次新增的档案。
