-- Monthly Sales KPI
SELECT
    strftime('%Y-%m', date) as month,
    COUNT(DISTINCT order_id) as total_orders,
    SUM(amount) as total_revenue,
    AVG(amount) as average_order_value
FROM transactions
GROUP BY
    1
ORDER BY 1;