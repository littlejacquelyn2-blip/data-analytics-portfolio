-- ============================================================
-- SQL PRACTICE — TIER 3: ADVANCED
-- CTEs, window functions (RANK, LAG, running totals), self-joins
-- This is the tier closest to a real fintech/analyst technical screen.
-- ============================================================

-- Q1. Using a CTE, compute the default rate (% of resolved loans that are
--     Charged Off or Default) by grade, then in the outer query rank grades
--     from worst to best default rate using RANK().


-- Q2. For each origination month, compute total loan_amnt originated and a
--     running (cumulative) total using a window function.


-- Q3. For each grade, compute each loan's int_rate alongside the average
--     int_rate for that grade, using a window function (no GROUP BY / no
--     self-join) — i.e. AVG(...) OVER (PARTITION BY grade).


-- Q4. Using LAG(), find the month-over-month change in total loan_amnt
--     originated (loans.db, group by issue month).


-- Q5. Self-join challenge: for each state, find how many "peer" states
--     (other states) have a higher average loan_amnt. (Hint: join loans
--     aggregated-by-state to itself on a state != state condition.)


-- Q6. Using a CTE and NTILE(4), split loans into 4 equal-sized buckets by
--     annual_inc (quartiles), then find the default rate for each quartile.


-- Q7. Using the rentals database: for each unit, compute a 3-month rolling
--     average of net monthly cash flow (income + expenses per month per
--     unit), using ROWS BETWEEN 2 PRECEDING AND CURRENT ROW.
