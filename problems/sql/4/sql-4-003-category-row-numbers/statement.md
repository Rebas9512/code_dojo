## 题目

每个分类独立编号，价格从高到低，NULL 在末尾，同价按书号升序。输出分类、书号和组内序号。

把编辑器里的 `____` 换成缺少的 SQL。

## 用到的表

shelf(book_id, category, price) 是书店本次盘价的快照，每本书一行。未定价记为 NULL。

## 样例数据（节选）

| book_id | category | price |
|---|---|---|
| 18 | programming | 75.00 |
| 8 | scifi | 45.00 |
| 28 | scifi | 45.00 |
| 2 | scifi | 39.00 |
| 22 | scifi | 39.00 |
| 15 | scifi | 33.00 |

## 示例结果

| category | book_id | position |
|---|---|---|
| programming | 18 | 1 |
| scifi | 8 | 1 |
| scifi | 28 | 2 |
| scifi | 2 | 3 |
| scifi | 22 | 4 |
| scifi | 15 | 5 |

样例共 30 行，上表列出科幻类全组和编程类榜首。

编程类的 18 号书和科幻类最贵的书都能排在各自组的第 1 位。

按上表的列顺序输出。行的顺序不限。
