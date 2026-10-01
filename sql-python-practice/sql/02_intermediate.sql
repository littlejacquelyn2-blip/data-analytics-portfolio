-- ============================================================
-- SQL PRACTICE — TIER 2: INTERMEDIATE
-- Joins, GROUP BY + HAVING, CASE, subqueries, multi-table logic
-- ============================================================

-- Q1. For each grade, find the average interest rate (int_rate), rounded to 2
--     decimals, but only include grades with more than 500 loans (HAVING).


-- Q2. Using CASE, create a column `risk_tier` that labels each loan:
--     grade A/B = 'low', C/D = 'medium', E/F/G = 'high'. Return loan_id,
--     grade, risk_tier for the first 20 rows.


-- Q3. Find the number of loans and the total loan_amnt for each combination
--     of grade and home_ownership.


-- Q4. Using the rentals database: JOIN `transactions` to `units` and find
--     the total rent_income collected per unit_name.


-- Q5. Find all loans whose int_rate is above the overall average int_rate
--     (use a subquery — don't hardcode the average).


-- Q6. For each purpose, find the minimum and maximum loan_amnt, and the
--     count of loans, in one query.


-- Q7. Using rentals: find every month where total expenses (all categories
--     except rent_income) exceeded total rent_income for that month
--     (JOIN or subquery + GROUP BY month, compare two aggregates).


-- Q8. Find the top 3 states (addr_state) by total loan_amnt originated,
--     along with that total.
