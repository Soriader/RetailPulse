--Revenue per day
USE RetailPulse;
GO

CREATE OR ALTER VIEW vw_kpi_revenue_daily AS
SELECT
    CAST(o.order_datetime AS DATE) AS order_date,
    SUM(oi.qty * oi.unit_price) AS revenue
FROM raw_orders o
JOIN raw_order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY CAST(o.order_datetime AS DATE);
GO

--Top product
CREATE OR ALTER VIEW vw_kpi_top_products AS
SELECT
    p.product_name,
    SUM(oi.qty) AS sold_qty,
    SUM(oi.qty * oi.unit_price) AS revenue
FROM raw_order_items oi
JOIN raw_products p ON p.product_id = oi.product_id
JOIN raw_orders o ON o.order_id = oi.order_id
WHERE o.status = 'completed'
GROUP BY p.product_name;
GO

--AOV (Average Order Value)
CREATE OR ALTER VIEW vw_kpi_aov AS
WITH order_totals AS (
    SELECT
        o.order_id,
        SUM(oi.qty * oi.unit_price) AS order_value
    FROM raw_orders o
    JOIN raw_order_items oi ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY o.order_id
)
SELECT AVG(order_value) AS aov
FROM order_totals;
GO

