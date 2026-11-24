WITH customers AS (
    SELECT COUNT(*) AS customer_versions,
           COUNT(*) - COUNT(valid_to) AS current_customers
    FROM dim_customer
), sales AS (
    SELECT COUNT(*) AS fact_rows, COALESCE(SUM(qty), 0) AS units
    FROM fact_sale
)
SELECT customers.customer_versions, customers.current_customers,
       (SELECT COUNT(*) FROM dim_product) AS products,
       sales.fact_rows, sales.units,
       (SELECT COUNT(*) FROM sale_issues) AS quality_issues
FROM customers
CROSS JOIN sales;
