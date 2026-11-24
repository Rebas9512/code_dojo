# 小数仓的两批来料

数据为 code-dojo 原创的文具店教学样本。客户、商品、日期和数量均为虚构。两批样本和边界数据按 CC0 1.0 提供，可复制、修改及再分发。

`schema.sql` 在 `warehouse_feed` 模式建立三个来源表。`seed.sql` 给出首批销售、首批客户等级记录和完整商品目录。默认的 `public` 模式留给练习建表。

| 来源表 | 一行的含义 |
| --- | --- |
| `sales(batch_no, line_id, sold_on, customer_code, sku, qty)` | 一个批次中一条销售明细的快照。跨批重报同一行时，以新快照覆盖。 |
| `customers(batch_no, customer_code, valid_from, tier)` | 一个客户在生效日期登记的等级。次批也可能重报原等级。 |
| `catalog(sku, product_name)` | 商品名录的一项。SKU 唯一，品名可以相同。 |

下载数据得到首批工作库；再执行导出的 `warehouse.sql`。脚本在第一批事实装好后插入第二批补丁，重现两次到货的顺序。补丁和八个代码位置都在[项目骨架](../../8/1/scaffold.sql)。独立判题用同一份补丁；[边界数据](../../8/1/datasets/)涵盖空仓、版本切换、迟到更正和无法匹配的来料。
