## 题目

查出**不是** Harbor Press 出版的图书的书名和出版社。出版社未知（`publisher` 为空）的书也算"不是 Harbor Press 出版的"，要包含在结果里。

用到的表（书店练习数据库）：

**books**（图书）

| 列 | 类型 | 说明 |
|---|---|---|
| book_id | integer | 主键 |
| title | text | 书名；不同版本可能同名 |
| author_id | integer | 作者，可能为空 |
| category | text | 分类：fiction / scifi / fantasy / history / programming / kids / cooking |
| price | numeric(6,2) | 售价（元） |
| stock | integer | 库存，0 表示售罄 |
| publisher | text | 出版社，可能为空 |
| published_on | date | 出版日期，可能为空 |
| pages | integer | 页数 |

## 示例

在书店样例数据上，正确结果是：

| title | publisher |
|---|---|
| Stars Over Gobi | Blue Kite |
| Python in Practice | Northwind |
| The Last Lantern | Blue Kite |
| Little Cloud | NULL |
| Noodles at Midnight | Northwind |
| Quantum Garden | Blue Kite |
| SQL for Curious Minds | Northwind |
| Dragons of the North | Blue Kite |

（共 23 行，这里只列出前 8 行。）

## 约束

- 结果两列：`title`、`publisher`（为空的显示为 NULL）。
- 行的顺序不要求。
- 列名不检查，但列的个数和顺序要和要求一致。
- 提交后还会在几份隐藏数据上运行（比如多了并列、空值、边界值），只对样例凑出结果是不够的。
