SELECT g.label, s.sale_year, s.price
FROM sales s
JOIN goods g ON g.goods_id = s.goods_id;
