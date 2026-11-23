## 题目

输入是一棵树，根为第 1 层。每个库房输出 label、level、所有直接或间接下级的个数 reports 及含本库预算在内的整棵子树预算 funds。库名唯一。

## 样例输入

`archive_units`

| unit | parent | label | budget |
|---|---|---|---|
| 10 | NULL | Atrium | 20 |
| 11 | 10 | Birch | 6 |
| 12 | 10 | Cedar | 7 |
| 13 | 11 | Dune | 9 |

## 样例结果

| label | level | reports | funds |
|---|---|---|---|
| Atrium | 1 | 3 | 42 |
| Birch | 2 | 1 | 15 |
| Cedar | 2 | 0 | 7 |
| Dune | 3 | 0 | 9 |

Atrium 管理三处下级，自己的 20 与三处预算相加为 42。

按上表的列顺序输出。先按 level 升序，再按 funds 降序，最后按 label 升序。
