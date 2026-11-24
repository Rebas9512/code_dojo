-- 学习者在空的 public 模式建表。项目来料单独存放。
CREATE SCHEMA warehouse_feed;

CREATE TABLE warehouse_feed.sales (
    batch_no integer,
    line_id integer,
    sold_on date,
    customer_code text,
    sku text,
    qty integer
);

CREATE TABLE warehouse_feed.customers (
    batch_no integer,
    customer_code text,
    valid_from date,
    tier text
);

CREATE TABLE warehouse_feed.catalog (
    sku text,
    product_name text
);
