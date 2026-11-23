## 题目

查出最便宜的 3 本书（book_id、书名、价格），从便宜到贵；同价时 book_id 小的在前。排序已经写好了，补全最后一行。

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

| book_id | title | price |
|---|---|---|
| 23 | Count with Panda | 12.00 |
| 14 | Moon Rabbit | 15.00 |
| 6 | Little Cloud | 18.50 |

（共 3 行。）

## 约束

- 结果三列：`book_id`、`title`、`price`，恰好 3 行。
- 结果要按题目要求的顺序排列。
- 列名不检查，但列的个数和顺序要和要求一致。
- 提交后还会在几份隐藏数据上运行（比如多了并列、空值、边界值），只对样例凑出结果是不够的。
