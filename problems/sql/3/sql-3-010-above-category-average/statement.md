## 题目

输出标价严格高于本分类平均价的书号、分类和标价。

## 用到的表

书目表 `books(book_id, title, category, price)` 每本书一行，价格单位为元。

## 示例结果

| book_id | category | price |
|---|---|---|
| 1 | fiction | 42 |
| 11 | fantasy | 52 |
| 13 | history | 55 |
| 16 | cooking | 42 |
| 18 | programming | 75 |
| 24 | cooking | 35 |
| 26 | history | 61 |
| 28 | scifi | 45 |

样例共 13 行。这里只列出其中 8 行。

一个分类只有一本书时，它的标价恰等于本类均价。

按上表的列顺序输出。行的顺序不限。
