## 题目

每个箱子输出 bin 和字母升序、去重的标签清单 labels。标签之间用斜杠隔开。

原稿用的是 MySQL。编辑器里保留了原句的注释，下面的 PostgreSQL 译稿有一处意思译错了。

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
