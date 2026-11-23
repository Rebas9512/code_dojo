SELECT s.sale_id, p.price
FROM counter_sales s
JOIN price_tags p ON p.book_id = s.book_id
                 AND s.sold_on BETWEEN p.starts_on AND p.ends_on;
