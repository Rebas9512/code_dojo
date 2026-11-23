## 题目

查出分类（`category`）为 `scifi` 的所有图书的 `book_id` 和书名。

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

| book_id | title |
|---|---|
| 2 | Stars Over Gobi |
| 8 | Quantum Garden |
| 15 | The Clockwork Sea |
| 22 | Orbit of Ashes |
| 28 | The Paper Moon |

（共 5 行。）

## 约束

- 结果两列：`book_id`、`title`。
- 分类的值都是小写英文，例如 `'scifi'`。
- 行的顺序不要求。
- 列名不检查，但列的个数和顺序要和要求一致。
- 提交后还会在几份隐藏数据上运行（比如多了并列、空值、边界值），只对样例凑出结果是不够的。
