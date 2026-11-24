## 题目

第二批来料中既有新销售，也有对旧销售的更正。把它并入已经装好首批的仓库，保留旧客户版本和原始快照。

本题直接提供首批仓库及次批来料，按下面三个步骤写一段增量 SQL。

1. 从 `valid_sales(batch_no, line_id, sold_on, customer_code, sku, qty)` 把批号 2 的记录写入同列的 `raw_sale`。原始层以 `(batch_no, line_id)` 为键，同批重放保留已有快照。
2. 从 `warehouse_feed.customers(batch_no, customer_code, valid_from, tier)` 读次批登记。客户换等级时，旧当前版本的 `valid_to` 填新生效日，再追加新版本；新客户直接建档；重报当前等级保留原版本。`dim_customer(customer_key, customer_code, tier, valid_from, valid_to)` 自动分配代理键，当前行的结束日为 NULL。
3. `keyed_sale(batch_no, line_id, sold_on, customer_key, product_key, qty)` 会用更新后的维度换键。把其中次批行按 `line_id` 合并进 `fact_sale(line_id, sold_on, customer_key, product_key, qty)`。新行插入，已有行按新快照覆盖全部业务列。可用 ON CONFLICT 或 MERGE。

## 示例

- `C01` 在 3 月 1 日从 `silver` 升成 `gold`。次批的 `105` 在升档日成交，归 `gold`；同批迟到的 `106` 在 2 月 28 日成交，仍归 `silver`。`102` 的件数从 `1` 更正到 `3`，最终只有一条事实，数量是 `3`。
- `C02` 重报 `base`，版本数仍为一；新客户 `C03` 登记 `base`，得到首个版本。若像单行小账本一样次批完全为空，首批的一条事实和一个客户版本照常保留。

## 约束

次批每位客户至多一条等级登记。已有客户的新生效日晚于其首批交易和版本起始日。两批内各自行号唯一，次批可以改变旧行的日期、客户、商品或件数。只合并能够换出两个维度键的销售。重复处理同一份次批时，维度历史和销售结果应一致。
