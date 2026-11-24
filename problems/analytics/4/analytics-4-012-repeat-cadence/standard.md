## 思路

先从正金额流水中为每人配出相邻两笔购买。去掉每人的第一笔后，按人求日期差的平均数，自然只留下买过至少两次的人。

## 写法要点

- 三笔购买只有两个相邻间隔，给首笔填零会多出一个间隔，把均值拉低。

## 进阶写法

只求平均值时，中间的日期会在相邻差之和里抵消，留下末次日期减去首次日期。用这段总天数除以间隔个数，数据库只需按人汇总，无须为每笔购买找上一笔。

```sql
SELECT user_id,
       ROUND((MAX(paid_at::date) - MIN(paid_at::date))::numeric / (COUNT(*) - 1), 2) AS mean_days
FROM payments
WHERE amount > 0
GROUP BY user_id
HAVING COUNT(*) >= 2
ORDER BY user_id;
```
