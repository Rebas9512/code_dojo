## 题目

查出书名以单词 **The** 开头的图书的书名。注意要的是单词 The：后面紧跟一个空格，
像 *Theory of Tides* 这样只是字母 The 开头的不算。

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

| title |
|---|
| The Silent Harbor |
| The Last Lantern |
| The Map Maker |
| The Clockwork Sea |
| The Glass Fox |
| The Paper Moon |

（共 6 行。）

## 约束

- 结果一列：`title`。
- 区分大小写：只算大写 T 开头的 `The`。
- 行的顺序不要求。
- 列名不检查，但列的个数和顺序要和要求一致。
- 提交后还会在几份隐藏数据上运行（比如多了并列、空值、边界值），只对样例凑出结果是不够的。
