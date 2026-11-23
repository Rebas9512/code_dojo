## 题目

列出没有任何展品记录的 hall。work 是非空作品编号，memo 是可空备注。

## 样例输入

`galleries`

| hall | label |
|---|---|
| 1 | Cove |
| 2 | Arch |
| 3 | Bay |
| 4 | Glen |

`exhibits`

| work | hall | memo |
|---|---|---|
| 31 | 1 | NULL |
| 32 | 3 | set |
| 33 | 3 | NULL |

## 样例结果

| hall |
|---|
| 2 |
| 4 |

1 号厅的作品还没写备注，这仍然是有展品的厅。

按上表的列顺序输出。行序不限。
