## 题目

库存总值 = 售价 × 库存数量。查出每本书的书名和它的库存总值，第二列起名叫 `stock_value`。

SELECT 里可以直接写表达式，`AS` 给结果列起名字。

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

| title | stock_value |
|---|---|
| The Silent Harbor | 504.00 |
| Stars Over Gobi | 195.00 |
| Python in Practice | 1360.00 |
| A Short History of Tea | 280.00 |
| The Last Lantern | 0.00 |
| Little Cloud | 555.00 |
| Noodles at Midnight | 448.50 |
| Quantum Garden | 315.00 |

（共 30 行，这里只列出前 8 行。）

## 约束

- 结果两列：`title`、`stock_value`。
- 行的顺序不要求。
- 列名不检查，但列的个数和顺序要和要求一致。
- 提交后还会在几份隐藏数据上运行（比如多了并列、空值、边界值），只对样例凑出结果是不够的。
