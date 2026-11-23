## 题目

给每本书打一个价位标签，查出书名、价格和标签：

| 价格 | 标签 |
|---|---|
| 低于 30 元 | `budget` |
| 30 元及以上、低于 50 元 | `standard` |
| 50 元及以上 | `premium` |

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

| title | price | price_band |
|---|---|---|
| The Silent Harbor | 42.00 | standard |
| Stars Over Gobi | 39.00 | standard |
| Python in Practice | 68.00 | premium |
| A Short History of Tea | 35.00 | standard |
| The Last Lantern | 39.00 | standard |
| Little Cloud | 18.50 | budget |
| Noodles at Midnight | 29.90 | budget |
| Quantum Garden | 45.00 | standard |

（共 30 行，这里只列出前 8 行。）

## 约束

- 结果三列：`title`、`price`、标签。
- 行的顺序不要求。
- 列名不检查，但列的个数和顺序要和要求一致。
- 提交后还会在几份隐藏数据上运行（比如多了并列、空值、边界值），只对样例凑出结果是不够的。
