## 题目

结账时，旧交易仍要算在客户当时的等级下。给每段等级历史分配自己的仓库编号，这个编号称为代理键。

首批登记在 `warehouse_feed.customers(batch_no, customer_code, valid_from, tier)`。创建并填充 `dim_customer(customer_key, customer_code, tier, valid_from, valid_to)`。业务属性 `customer_code`、`tier` 是文字，两端日期为 date。只处理第一批。

## 示例

- `C01` 在 1 月 1 日登记为 `base`，2 月 1 日改为 `silver`。旧版本的结束日填 `2025-02-01`；从这一天起使用新版本，新版本的结束日为 NULL。
- 单行小账本只有 `Solo` 从 `2025-01-01` 起的 `base` 记录。这个版本的结束日为 NULL，即使这位客户从未购物也要建档。

## 约束

`customer_key` 用整数 GENERATED ALWAYS AS IDENTITY 主键，自增号码的具体值不限。除 `valid_to` 外各列必填，`(customer_code, valid_from)` 唯一。首批的每次登记都是一次真实等级变化，同一客户同日最多一条；来源的行序没有时间含义。有效期含起始日，止于同一客户下一次变化当日之前。
