-- ============================================================
-- Lending Risk Analysis — SQL Queries (SQLite)
-- Table: loans (see ../data/loans.csv for schema)
-- A loan counts as "resolved" for default-rate purposes if its
-- status is Fully Paid, Charged Off, or Default (i.e. not still
-- "Current" / open), since we don't yet know the outcome of an
-- open loan.
-- ============================================================

-- 1) Default rate by grade
-- Basic aggregation: GROUP BY + conditional aggregation.
SELECT
    grade,
    COUNT(*) AS total_loans,
    SUM(CASE WHEN loan_status IN ('Charged Off','Default') THEN 1 ELSE 0 END) AS defaults,
    ROUND(100.0 * SUM(CASE WHEN loan_status IN ('Charged Off','Default') THEN 1 ELSE 0 END)
          / SUM(CASE WHEN loan_status != 'Current' THEN 1 ELSE 0 END), 2) AS default_rate_pct
FROM loans
GROUP BY grade
ORDER BY grade;

-- 2) Default rate by vintage (issue year) and grade
-- strftime for date parts; multi-column GROUP BY.
SELECT
    strftime('%Y', issue_d) AS vintage_year,
    grade,
    COUNT(*) AS total_loans,
    ROUND(100.0 * SUM(CASE WHEN loan_status IN ('Charged Off','Default') THEN 1 ELSE 0 END)
          / NULLIF(SUM(CASE WHEN loan_status != 'Current' THEN 1 ELSE 0 END), 0), 2) AS default_rate_pct
FROM loans
GROUP BY vintage_year, grade
ORDER BY vintage_year, grade;

-- 3) Default rate by loan purpose, ranked worst to best
SELECT
    purpose,
    COUNT(*) AS total_loans,
    ROUND(100.0 * SUM(CASE WHEN loan_status IN ('Charged Off','Default') THEN 1 ELSE 0 END)
          / NULLIF(SUM(CASE WHEN loan_status != 'Current' THEN 1 ELSE 0 END), 0), 2) AS default_rate_pct
FROM loans
GROUP BY purpose
ORDER BY default_rate_pct DESC;

-- 4) Running (cumulative) originations by month — window function
-- Demonstrates a window function with an ORDER BY frame, a common
-- ask in analyst SQL screens.
WITH monthly AS (
    SELECT strftime('%Y-%m', issue_d) AS month, COUNT(*) AS loans_originated,
           SUM(loan_amnt) AS amount_originated
    FROM loans
    GROUP BY month
)
SELECT
    month,
    loans_originated,
    amount_originated,
    SUM(amount_originated) OVER (ORDER BY month) AS cumulative_amount,
    ROUND(AVG(amount_originated) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 0) AS rolling_3mo_avg_amount
FROM monthly
ORDER BY month;

-- 5) DTI (debt-to-income) risk bucket vs default rate — CASE-based bucketing
SELECT
    CASE
        WHEN dti < 10 THEN '1: <10'
        WHEN dti < 20 THEN '2: 10-20'
        WHEN dti < 30 THEN '3: 20-30'
        ELSE '4: 30+'
    END AS dti_bucket,
    COUNT(*) AS total_loans,
    ROUND(100.0 * SUM(CASE WHEN loan_status IN ('Charged Off','Default') THEN 1 ELSE 0 END)
          / NULLIF(SUM(CASE WHEN loan_status != 'Current' THEN 1 ELSE 0 END), 0), 2) AS default_rate_pct
FROM loans
GROUP BY dti_bucket
ORDER BY dti_bucket;

-- 6) Rank each state's default rate against the national rate — window function + CTE
WITH state_stats AS (
    SELECT
        addr_state,
        COUNT(*) AS total_loans,
        ROUND(100.0 * SUM(CASE WHEN loan_status IN ('Charged Off','Default') THEN 1 ELSE 0 END)
              / NULLIF(SUM(CASE WHEN loan_status != 'Current' THEN 1 ELSE 0 END), 0), 2) AS default_rate_pct
    FROM loans
    GROUP BY addr_state
    HAVING COUNT(*) >= 200  -- drop states with too few loans to be meaningful
)
SELECT
    addr_state,
    total_loans,
    default_rate_pct,
    RANK() OVER (ORDER BY default_rate_pct DESC) AS risk_rank
FROM state_stats
ORDER BY risk_rank;

-- 7) Interest rate vs. grade — sanity check that pricing matches risk
SELECT
    grade,
    COUNT(*) AS total_loans,
    ROUND(AVG(int_rate), 2) AS avg_int_rate,
    ROUND(MIN(int_rate), 2) AS min_int_rate,
    ROUND(MAX(int_rate), 2) AS max_int_rate
FROM loans
GROUP BY grade
ORDER BY grade;

-- 8) Self-join style comparison: which sub-grades underperform their letter grade's average?
-- (HAVING + subquery — comparing a group's rate to the parent group's rate)
WITH sub_grade_stats AS (
    SELECT
        grade, sub_grade,
        ROUND(100.0 * SUM(CASE WHEN loan_status IN ('Charged Off','Default') THEN 1 ELSE 0 END)
              / NULLIF(SUM(CASE WHEN loan_status != 'Current' THEN 1 ELSE 0 END), 0), 2) AS sub_default_rate
    FROM loans
    GROUP BY grade, sub_grade
),
grade_stats AS (
    SELECT grade,
           ROUND(100.0 * SUM(CASE WHEN loan_status IN ('Charged Off','Default') THEN 1 ELSE 0 END)
                 / NULLIF(SUM(CASE WHEN loan_status != 'Current' THEN 1 ELSE 0 END), 0), 2) AS grade_default_rate
    FROM loans
    GROUP BY grade
)
SELECT s.grade, s.sub_grade, s.sub_default_rate, g.grade_default_rate,
       ROUND(s.sub_default_rate - g.grade_default_rate, 2) AS gap_vs_grade_avg
FROM sub_grade_stats s
JOIN grade_stats g ON s.grade = g.grade
WHERE s.sub_default_rate > g.grade_default_rate
ORDER BY gap_vs_grade_avg DESC;
