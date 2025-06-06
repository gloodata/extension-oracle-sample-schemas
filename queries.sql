-- ENUMS FOR FILTERS
-- List of product categories
-- name: product_category_enum
-- This query retrieves distinct product categories for filter dropdowns
SELECT DISTINCT prod_category as "key", prod_category as "label"
FROM products
WHERE (:value IS NULL OR LOWER(prod_category) LIKE LOWER(:value))
ORDER BY prod_category
FETCH FIRST :limit ROWS ONLY

-- List of countries
-- name: country_enum
-- This query retrieves distinct countries for geographic filtering
SELECT DISTINCT country_name as "key", country_name as "label"
FROM countries
WHERE (:value IS NULL OR LOWER(country_name) LIKE LOWER(:value))
ORDER BY country_name
FETCH FIRST :limit ROWS ONLY

-- List of channels
-- name: channel_enum
-- This query retrieves distinct sales channels for filtering
SELECT DISTINCT channel_desc as "key", channel_desc as "label"
FROM channels
WHERE (:value IS NULL OR LOWER(channel_desc) LIKE LOWER(:value))
ORDER BY channel_desc
FETCH FIRST :limit ROWS ONLY

-- List of customer segments
-- name: customer_segment_enum
-- This query retrieves distinct customer segments for filtering
SELECT DISTINCT cust_income_level as "key", cust_income_level as "label"
FROM customers
WHERE (:value IS NULL OR LOWER(cust_income_level) LIKE LOWER(:value))
ORDER BY cust_income_level
FETCH FIRST :limit ROWS ONLY

-- 1. Sales by product category
-- name: sales_by_category
-- This query shows total sales amount by product category with optional filters
SELECT 
    p.prod_category as category,
    ROUND(SUM(s.amount_sold), 2) as total_sales
FROM sales s
JOIN products p ON s.prod_id = p.prod_id
JOIN customers c ON s.cust_id = c.cust_id
JOIN countries co ON c.country_id = co.country_id
WHERE (:country IS NULL OR co.country_name = :country)
  AND (s.time_id BETWEEN :start_date AND :end_date)
GROUP BY p.prod_category
ORDER BY total_sales DESC

-- 2. Sales by channel
-- name: sales_by_channel
-- This query shows total sales amount by sales channel with filtering options
SELECT 
    ch.channel_desc as channel,
    ROUND(SUM(s.amount_sold), 2) as total_sales
FROM sales s
JOIN channels ch ON s.channel_id = ch.channel_id
JOIN products p ON s.prod_id = p.prod_id
JOIN customers c ON s.cust_id = c.cust_id
WHERE (:product_category IS NULL OR p.prod_category = :product_category)
  AND (:customer_segment IS NULL OR c.cust_income_level = :customer_segment)
  AND (s.time_id BETWEEN :start_date AND :end_date)
GROUP BY ch.channel_desc
ORDER BY total_sales DESC

-- 3. Customer Density by Region
-- name: customer_density
-- This query shows customer count by geographic region for density mapping
SELECT 
    co.country_region as region,
    COUNT(DISTINCT c.cust_id) as customer_count
FROM customers c
JOIN countries co ON c.country_id = co.country_id
JOIN sales s ON c.cust_id = s.cust_id
WHERE (:customer_segment IS NULL OR c.cust_income_level = :customer_segment)
  AND (s.time_id BETWEEN :start_date AND :end_date)
GROUP BY co.country_region
HAVING COUNT(DISTINCT c.cust_id) > 0
ORDER BY customer_count DESC

-- 4. Monthly Sales Trend by Category
-- name: monthly_sales_trend
-- This query shows monthly sales trends by product category over time
SELECT 
    calendar_month_desc,
    p.prod_category as category,
    ROUND(SUM(s.amount_sold), 2) as total_sales
FROM sales s
JOIN products p ON s.prod_id = p.prod_id
JOIN times t ON s.time_id = t.time_id
JOIN customers c ON s.cust_id = c.cust_id
JOIN countries co ON c.country_id = co.country_id
WHERE (:country IS NULL OR co.country_name = :country)
  AND (:product_category IS NULL OR p.prod_category = :product_category)
  AND (s.time_id BETWEEN :start_date AND :end_date)
GROUP BY t.calendar_month_desc, p.prod_category
ORDER BY t.calendar_month_desc, category

-- 5. Quarterly Sales by Channel
-- name: quarterly_sales_by_channel
-- This query shows quarterly sales performance by channel over time
SELECT 
    t.calendar_quarter_desc,
    ch.channel_desc as category,
    ROUND(SUM(s.amount_sold), 2) as total_sales
FROM sales s
JOIN channels ch ON s.channel_id = ch.channel_id
JOIN times t ON s.time_id = t.time_id
JOIN customers c ON s.cust_id = c.cust_id
WHERE (:customer_segment IS NULL OR c.cust_income_level = :customer_segment)
  AND (:min_amount IS NULL OR s.amount_sold >= :min_amount)
  AND (s.time_id BETWEEN :start_date AND :end_date)
GROUP BY t.calendar_quarter_desc, ch.channel_desc
ORDER BY t.calendar_quarter_desc, category

-- 6. Comprehensive Sales Analysis Table
-- name: sales_analysis
-- This table shows detailed sales metrics with multiple dimensions
SELECT 
    p.prod_category as category,
    co.country_name as country,
    ROUND(SUM(s.amount_sold), 2) as total_sales,
    ROUND(SUM(s.quantity_sold), 0) as total_quantity,
    COUNT(DISTINCT s.cust_id) as unique_customers,
    ROUND(AVG(s.amount_sold), 2) as avg_sale_amount,
    ROUND(SUM(s.amount_sold) / SUM(s.quantity_sold), 2) as avg_unit_price
FROM sales s
JOIN products p ON s.prod_id = p.prod_id
JOIN customers c ON s.cust_id = c.cust_id
JOIN countries co ON c.country_id = co.country_id
WHERE (:product_category IS NULL OR p.prod_category = :product_category)
  AND (:country IS NULL OR co.country_name = :country)
  AND (s.time_id BETWEEN :start_date AND :end_date)
GROUP BY p.prod_category, co.country_name
ORDER BY total_sales DESC

-- 7. Sales by Country (Geographic)
-- name: sales_by_country
-- This query provides sales data by country for geographic visualization
SELECT 
    co.country_name as region,
    ROUND(SUM(s.amount_sold), 2) as total_sales
FROM sales s
JOIN customers c ON s.cust_id = c.cust_id
JOIN countries co ON c.country_id = co.country_id
JOIN products p ON s.prod_id = p.prod_id
WHERE (:product_category IS NULL OR p.prod_category = :product_category)
  AND (s.time_id BETWEEN :start_date AND :end_date)
  AND (:min_sales IS NULL OR s.amount_sold >= :min_sales)
GROUP BY co.country_name
ORDER BY total_sales DESC
