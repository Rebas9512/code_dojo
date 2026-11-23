## 题目

目录是一棵树。输出每个 node 的 role：没有父节点标 root，有父且有子节点标 branch，其余标 leaf。

## 样例输入

`collection_nodes`

| node | parent |
|---|---|
| 10 | NULL |
| 15 | 10 |
| 18 | 10 |
| 22 | 15 |

## 样例结果

| node | role |
|---|---|
| 10 | root |
| 15 | branch |
| 18 | leaf |
| 22 | leaf |

10 是根；15 既有父节点，又是 22 的父节点。

按上表的列顺序输出。行序不限。
