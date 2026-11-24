前三项经营数字、畅销分类、作者贡献和复购人数都已算好。写下整条 WITH 查询的最后一个 SELECT，把店长每月要看的七列放到同一行。

## 输入与输出

`monthly_change(order_month, order_count, revenue, growth_pct)` 每个有有效订单的月一行。`category_ranks(order_month, category, category_revenue, sales_rank)` 每月每类一行。`author_sales(order_month, author_id, author_revenue)` 每月每位署名作者一行。`repeat_buyers(order_month, repeat_count)` 只列有复购的月份。

按以下列名和顺序返回。

`order_month, order_count, revenue, growth_pct, top_categories, top_author_revenue, repeat_count`

## 示例一 · 书店原始订单

2024 年 12 月有 3 单共 218.80 元。`programming` 畅销第一，署名作者的最高月销售额为 123.00 元，有一位读者复购。首行如下。

| order_month | order_count | revenue | growth_pct | top_categories | top_author_revenue | repeat_count |
| --- | ---: | ---: | ---: | --- | ---: | ---: |
| 2024-12-01 | 3 | 218.80 | NULL | programming | 123.00 | 1 |

## 示例二 · 七月加单

新增七月有 2 单，合计 60 元，六月销售额为 322.70 元。`cooking` 和 `fiction` 各卖了 30 元，并列第一。署名作者分别贡献 30 和 24 元，16 号读者当月复购。

| order_month | order_count | revenue | growth_pct | top_categories | top_author_revenue | repeat_count |
| --- | ---: | ---: | ---: | --- | ---: | ---: |
| 2025-07-01 | 2 | 60.00 | -81.41 | cooking, fiction | 30.00 | 1 |

## 约束

每个 `monthly_change` 月份恰好一行，按月从早到晚。并列第一的分类按名称升序，用英文逗号和一个空格连接。月内没有明细时 `top_categories` 为 NULL，没有署名作者时 `top_author_revenue` 为 NULL。没有复购读者时 `repeat_count` 为 0。

只提交最后一条 SELECT，前面的七张中间表由判题器提供。
