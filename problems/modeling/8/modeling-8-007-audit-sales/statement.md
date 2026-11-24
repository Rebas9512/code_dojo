## 题目

仓库要能回答两类问题：某客户版本在一段日期内卖了什么，以及哪些来料因找不到维度而没有装入事实表。为前者建索引，为后者保存可重复读取的质量检查。

在 `fact_sale` 建普通 B-tree 索引 `fact_customer_day_idx`，键依次为 `customer_key`、`sold_on`，都升序。创建普通视图 `sale_issues(batch_no, line_id, issue)`，逐条检查 `raw_sale` 中两个批次的快照：

- 按 `customer_code` 在 `dim_customer` 中找交易日有效的版本。找不到则报告 `customer_gap`。
- 按 `sku` 在 `dim_product` 中找商品。找不到则报告 `unknown_sku`。

## 示例

- 若客户 `C09` 的首个版本在 2 月 1 日生效，首批来料 `301` 却在 1 月 31 日成交，商品已登记，返回 `(1, 301, 'customer_gap')`。若交易恰在 2 月 1 日，则通过这一项检查。
- 次批的 `304` 同时引用陌生客户和陌生 SKU，应返回两行，原因分别是 `customer_gap` 和 `unknown_sku`。项目的正常两批和单行小账本都没有异常，视图返回零行。

## 约束

客户有效期含 `valid_from`、不含 `valid_to`，结束日为 NULL 时一直有效。以原始层为检查对象，即使该行未写入事实表也要能发现。按每条快照、每种命中的原因各报一行，行序不限。索引覆盖全表且非唯一，只用给出的两个键。
