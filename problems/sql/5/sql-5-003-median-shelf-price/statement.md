## 题目

每个分类输出分类和已知价格的中位数。奇数个取中间，偶数个取中间两者的平均。重复价格保留，完全未定价的分类输出 NULL。

## 用到的表

price_survey(book_id,category,price) 是书店盘价快照，价格可为空。

## 示例结果

| category | median_price |
|---|---|
| cooking | 32.45 |
| fantasy | 39 |
| fiction | 31.25 |
| history | 51.5 |
| kids | 15 |
| programming | 59 |
| scifi | 39 |

样例共 7 行。

儿童书三个标价为 12、15、18.5，排在中间的是 15。另一个手写方法见本技能的课。

按上表的列顺序输出。行的顺序不限。
