-- ============================================================
-- Rental Portfolio Analytics — SQL Queries (SQLite)
-- Tables: units (unit_id, unit_name, bedrooms, market_rent)
--         transactions (unit_id, month, category, amount)
--         amount is signed: positive = income, negative = expense
-- ============================================================

-- 1) Net cash flow per unit, all time — JOIN + aggregation
SELECT
    u.unit_name,
    ROUND(SUM(t.amount), 2) AS net_cash_flow
FROM transactions t
JOIN units u ON u.unit_id = t.unit_id
GROUP BY u.unit_name
ORDER BY net_cash_flow DESC;

-- 2) Monthly net cash flow across the whole portfolio, with running total — window function
WITH monthly AS (
    SELECT month, SUM(amount) AS net_amount
    FROM transactions
    GROUP BY month
)
SELECT
    month,
    ROUND(net_amount, 2) AS net_amount,
    ROUND(SUM(net_amount) OVER (ORDER BY month), 2) AS cumulative_net
FROM monthly
ORDER BY month;

-- 3) Expense breakdown by category, portfolio-wide
SELECT
    category,
    ROUND(SUM(-amount), 2) AS total_expense
FROM transactions
WHERE category != 'rent_income'
GROUP BY category
ORDER BY total_expense DESC;

-- 4) Occupancy rate per unit (months with rent collected / total months)
SELECT
    u.unit_name,
    COUNT(DISTINCT t.month) AS months_tracked,
    SUM(CASE WHEN t.category = 'rent_income' AND t.amount > 0 THEN 1 ELSE 0 END) AS months_occupied,
    ROUND(100.0 * SUM(CASE WHEN t.category = 'rent_income' AND t.amount > 0 THEN 1 ELSE 0 END)
          / COUNT(DISTINCT t.month), 1) AS occupancy_rate_pct
FROM transactions t
JOIN units u ON u.unit_id = t.unit_id
GROUP BY u.unit_name
ORDER BY occupancy_rate_pct DESC;

-- 5) Rent collected vs. market rent, per unit — comparing actual to benchmark
SELECT
    u.unit_name,
    u.market_rent,
    ROUND(AVG(CASE WHEN t.amount > 0 THEN t.amount END), 2) AS avg_rent_collected_when_occupied,
    ROUND(AVG(CASE WHEN t.amount > 0 THEN t.amount END) - u.market_rent, 2) AS variance_vs_market
FROM transactions t
JOIN units u ON u.unit_id = t.unit_id
WHERE t.category = 'rent_income'
GROUP BY u.unit_name;

-- 6) Month-over-month change in net cash flow — LAG window function
WITH monthly AS (
    SELECT month, SUM(amount) AS net_amount
    FROM transactions GROUP BY month
)
SELECT
    month,
    ROUND(net_amount, 2) AS net_amount,
    ROUND(net_amount - LAG(net_amount) OVER (ORDER BY month), 2) AS change_vs_prior_month
FROM monthly
ORDER BY month;

-- 7) Which unit had the single worst month (biggest net loss)?
SELECT
    u.unit_name, t.month,
    ROUND(SUM(t.amount), 2) AS unit_month_net
FROM transactions t
JOIN units u ON u.unit_id = t.unit_id
GROUP BY u.unit_name, t.month
ORDER BY unit_month_net ASC
LIMIT 5;
