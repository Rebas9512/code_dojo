## 题目

一条销售事实代表一条销售明细。这里把来料中的客户编号和 SKU 换成仓库键，让每笔销售永久指向交易日适用的客户版本。

已提供 `raw_sale(batch_no, line_id, sold_on, customer_code, sku, qty)`、`dim_customer(customer_key, customer_code, tier, valid_from, valid_to)` 和 `dim_product(product_key, sku, product_name)`。

建立普通视图 `keyed_sale(batch_no, line_id, sold_on, customer_key, product_key, qty)`，对所有批次换键。建表 `fact_sale(line_id, sold_on, customer_key, product_key, qty)`，将视图中首批的明细载入。

## 示例

- `C01` 在 `2025-02-01` 从 `base` 升为 `silver`。1 月 31 日的销售 `101` 引用旧版本，2 月 1 日的销售 `102` 只引用新版本。
- 单行小账本里，`Solo` 的首个版本在 `2025-01-01` 生效，当日买了一件 `B7`。事实表应有一行：行号 `7`、该日、这个版本的键、`B7` 的键、件数 `1`。

## 约束

事实表以整数 `line_id` 作主键，交易日为 date，两侧键和件数为整数，各列必填。两个维度键分别建外键，引用对应维度的主键。

有效期含起始日，不含结束日，NULL 结束日表示仍有效。找不到当天客户版本或找不到 SKU 的来料留在原始层。数据保证同一客户的有效期互不重叠。
