## 题目

列出一起完成过至少三单的装订员 binder 与裁纸员 cutter。一行代表一次合作。

## 样例输入

`binding_jobs`

| binder | cutter |
|---|---|
| A | X |
| A | X |
| A | X |
| A | Y |
| B | X |

## 样例结果

| binder | cutter |
|---|---|
| A | X |

A 和 X 合作三次。A 换成与 Y 搭档时应重新计数。

按上表的列顺序输出。行序不限。
