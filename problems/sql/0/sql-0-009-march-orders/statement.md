## 题目

查出 **2025 年 3 月**下的所有订单的 `order_id`、`user_id`、`order_date`。

`order_date` 是 DATE 类型（只有日期，没有时间），可以直接和 `'2025-03-01'` 这样的字符串比较。

用到的表（书店练习数据库）：

**orders**（订单）

| 列 | 类型 | 说明 |
|---|---|---|
| order_id | integer | 主键 |
| user_id | integer | 下单用户 |
| order_date | date | 下单日期 |
| status | text | paid / shipped / delivered / cancelled |
| coupon_code | text | 优惠码，可能为空 |

## 示例

在书店样例数据上，正确结果是：

| order_id | user_id | order_date |
|---|---|---|
| 113 | 2 | 2025-03-01 |
| 114 | 10 | 2025-03-03 |
| 115 | 1 | 2025-03-15 |
| 116 | 11 | 2025-03-18 |
| 117 | 6 | 2025-03-31 |

（共 5 行。）

## 约束

- 结果三列：`order_id`、`user_id`、`order_date`（日期按 `YYYY-MM-DD` 比较）。
- 行的顺序不要求。
- 列名不检查，但列的个数和顺序要和要求一致。
- 提交后还会在几份隐藏数据上运行（比如多了并列、空值、边界值），只对样例凑出结果是不够的。
