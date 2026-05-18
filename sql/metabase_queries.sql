SELECT COUNT(DISTINCT order_id) AS total_orders
FROM mci_orders.orders;

SELECT COUNT(*) AS total_order_items
FROM mci_orders.orders;

SELECT
    ROUND(COUNT(*) / COUNT(DISTINCT order_id), 2) AS avg_items_per_order
FROM mci_orders.orders;

SELECT
    ROUND(100.0 * SUM(reordered) / COUNT(*), 2) AS reorder_rate_percent
FROM mci_orders.orders;

-- Top 10 Most Ordered Products
SELECT
    product_name,
    COUNT(*) AS total_ordered
FROM mci_orders.orders
GROUP BY product_name
ORDER BY total_ordered DESC
LIMIT 10;

-- Top 10 reordered
SELECT
    product_name,
    COUNT(*) AS reordered_count
FROM mci_orders.orders
WHERE reordered = 1
GROUP BY product_name
ORDER BY reordered_count DESC
LIMIT 10;

-- orders by departement
SELECT
    department,
    COUNT(*) AS total_items
FROM mci_orders.orders
GROUP BY department
ORDER BY total_items DESC;

-- average basket size
SELECT
    department,
    ROUND(COUNT(*) / COUNT(DISTINCT order_id), 2) AS avg_items_per_order
FROM mci_orders.orders
GROUP BY department
ORDER BY avg_items_per_order DESC;

-- order by hours of a day
SELECT
    concat(toString(order_hour_of_day), ':00') AS hour_label,
    COUNT(DISTINCT order_id) AS total_orders
FROM mci_orders.orders
GROUP BY order_hour_of_day, hour_label
ORDER BY order_hour_of_day;

-- order by day a week
SELECT
    CASE order_dow
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END AS day_name,
    COUNT(DISTINCT order_id) AS total_orders
FROM mci_orders.orders
GROUP BY order_dow, day_name
ORDER BY order_dow;

-- reorder vs first
SELECT
    CASE
        WHEN reordered = 1 THEN 'Reordered'
        ELSE 'First-Time Ordered'
    END AS order_type,
    COUNT(*) AS total_items
FROM mci_orders.orders
GROUP BY order_type
ORDER BY total_items DESC;

-- avg days since prior
SELECT
    ROUND(AVG(days_since_prior_order), 2) AS avg_days_since_prior_order
FROM mci_orders.orders
WHERE days_since_prior_order IS NOT NULL;