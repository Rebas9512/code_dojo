## 题目

查出每本书的书名和打八折后的价格（原价 × 0.8），第二列起名 `sale_price`。把 `____` 换成计算式。

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

| title | sale_price |
|---|---|
| The Silent Harbor | 33.600 |
| Stars Over Gobi | 31.200 |
| Python in Practice | 54.400 |
| A Short History of Tea | 28.000 |
| The Last Lantern | 31.200 |
| Little Cloud | 14.800 |
| Noodles at Midnight | 23.920 |
| Quantum Garden | 36.000 |

（共 30 行，这里只列出前 8 行。）

## 约束

- 结果两列：`title`、`sale_price`。
- 行的顺序不要求。
- 列名不检查，但列的个数和顺序要和要求一致。
- 提交后还会在几份隐藏数据上运行（比如多了并列、空值、边界值），只对样例凑出结果是不够的。
