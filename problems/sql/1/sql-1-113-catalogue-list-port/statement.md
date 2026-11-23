## 题目

编辑器里是一条 MySQL 查询，在 PostgreSQL 上运行会报错。把它改写成 PostgreSQL 查询，保留原来的标签清单。

每个箱子输出一行，第一列是箱号 `bin`，第二列是清单 `labels`。同一箱里的标签先去重，再按字母升序用斜杠 `/` 拼起来。

## 样例输入

`bin_labels`

| bin | label |
|---|---|
| E | Zed |
| E | Arc |
| E | Arc |
| W | Bay |

## 样例结果

| bin | labels |
|---|---|
| E | Arc/Zed |
| W | Bay |

E 箱有两张 Arc，只印一次；Arc 排在 Zed 前面。

按上表的列顺序输出。行序不限。
