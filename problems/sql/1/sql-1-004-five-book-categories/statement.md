## 题目

馆员给至少有五种书的分类增设书架。输出分类和书目数。现有查询漏掉了正好五种的分类，请修正它。

## 用到的表

`books` 每行一种书。`book_id` 是编号，`category` 是分类，`price` 是单价（元），`stock` 是库存册数。

## 示例结果

| category | book_count |
|---|---|
| fiction | 6 |
| programming | 5 |
| scifi | 5 |

样例共 3 行。

programming 和 scifi 都恰好有五种书。门槛相同时，这两组都要保留。

按上表的列顺序输出。行的顺序不限。
