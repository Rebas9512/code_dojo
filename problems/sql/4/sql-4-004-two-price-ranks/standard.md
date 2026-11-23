## 思路

在每个分类内，把书按价格从高到低排好，未定价的放在末尾。`RANK` 给出的名次等于本档之前的书本数加 1。`DENSE_RANK` 给出的档次等于本档之前的价位数加 1。

## 写法要点

- 如果最高价有两本，竞赛名次是 1、1、3，价格档次是 1、1、2。窗口排序只写价格，才能保留这种并列。

## 进阶写法

两种名次需要完全相同的分区和排序。可以用 `WINDOW` 给这套规则命名，将来调整空价的位置时只改一处。

```sql
SELECT category, book_id,
       RANK() OVER by_price AS place,
       DENSE_RANK() OVER by_price AS tier
FROM shelf
WINDOW by_price AS (PARTITION BY category ORDER BY price DESC NULLS LAST);
```
