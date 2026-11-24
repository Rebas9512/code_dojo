## 题目

销售到货时只带商品编码 SKU。先按名录给每种商品分配仓库编号，让后续的事实表能引用它。

从 `warehouse_feed.catalog(sku, product_name)` 读取完整名录，创建并填充 `dim_product(product_key, sku, product_name)`。一行代表一个 SKU。

## 示例

- `P01` 和 `P03` 都叫 `Notebook`。两者要得到不同的商品键；尚未售出的 `P04` 也在维度中。
- 单行小账本的名录只有 `('B7', 'Pen')`。维度应有一条对应记录；以后若用 `B7` 再建一个商品，数据库应拒绝写入。

## 约束

`product_key` 为整数 GENERATED ALWAYS AS IDENTITY 主键，具体号码不限。SKU 和品名是必填文字，SKU 唯一。按原文保存编码和品名；名录可以为空。
