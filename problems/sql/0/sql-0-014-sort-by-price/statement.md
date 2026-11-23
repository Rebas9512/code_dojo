## 题目

列出所有图书的书名和价格，按价格**从高到低**排列；价格相同时，按书名的字母顺序（A → Z）排列。

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

| title | price |
|---|---|
| Algorithms, Gently | 75.00 |
| Python in Practice | 68.00 |
| Rivers and Kings | 61.00 |
| SQL for Curious Minds | 59.00 |
| Data at Dawn | 55.00 |
| Silk Road Letters | 55.00 |
| Dragons of the North | 52.00 |
| Data at Dawn | 49.00 |

（共 30 行，这里只列出前 8 行。）

## 约束

- 结果两列：`title`、`price`。
- 结果要按题目要求的顺序排列。
- 列名不检查，但列的个数和顺序要和要求一致。
- 提交后还会在几份隐藏数据上运行（比如多了并列、空值、边界值），只对样例凑出结果是不够的。
