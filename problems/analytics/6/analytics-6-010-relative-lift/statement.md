## 题目

只看 cover，同组重报取首次入组时刻，跨组者剔除。首次入组起七个整日内（含起点、不含终点）有正向收款即成功，每人至多一次。输出 B 相对 A 的提升 (pB−pA)/pA，对照比例为零时输出 NULL。结果比例、百分点或 z 保留 4 位小数。两组均有合格读者。

## 用到的表

payments(payment_id, user_id, paid_at, amount) 图书交易流水，收款为正，退款为负。金额单位为元。

assignments(assignment_id, experiment, user_id, arm, assigned_at) 每次分组一行。组别为 A 或 B，可能重复上报或跨组。

## 示例结果

| lift |
|---|
| -0.2857 |

两组分母都为 17，比较 (10/17−14/17)/(14/17)，结果为负。

样例共 1 行。按示例列顺序输出，行序不限。
