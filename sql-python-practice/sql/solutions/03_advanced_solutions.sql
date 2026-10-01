-- SOLUTIONS — TIER 3: ADVANCED

-- Q1
WITH grade_default AS (
    SELECT grade,
           ROUND(100.0 * SUM(CASE WHEN loan_status IN ('Charged Off','Default') THEN 1 ELSE 0 END)
                 / NULLIF(SUM(CASE WHEN loan_status != 'Current' THEN 1 ELSE 0 END), 0), 2) AS default_rate_pct
    FROM loans
    GROUP BY grade
)
SELECT grade, default_rate_pct,
       RANK() OVER (ORDER BY default_rate_pct DESC) AS worst_to_best_rank
FROM grade_default;

-- Q2
WITH monthly AS (
    SELECT strftime('%Y-%m', issue_d) AS month, SUM(loan_amnt) AS amount
    FROM loans GROUP BY month
)
SELECT month, amount,
       SUM(amount) OVER (ORDER BY month) AS cumulative_amount
FROM monthly
ORDER BY month;

-- Q3
SELECT loan_id, grade, int_rate,
       ROUND(AVG(int_rate) OVER (PARTITION BY grade), 2) AS grade_avg_int_rate,
       ROUND(int_rate - AVG(int_rate) OVER (PARTITION BY grade), 2) AS diff_from_grade_avg
FROM loans;

-- Q4
WITH monthly AS (
    SELECT strftime('%Y-%m', issue_d) AS month, SUM(loan_amnt) AS amount
    FROM loans GROUP BY month
)
SELECT month, amount,
       amount - LAG(amount) OVER (ORDER BY month) AS change_vs_prior_month
FROM monthly
ORDER BY month;

-- Q5
WITH state_avg AS (
    SELECT addr_state, AVG(loan_amnt) AS avg_amnt
    FROM loans GROUP BY addr_state
)
SELECT a.addr_state, a.avg_amnt,
       (SELECT COUNT(*) FROM state_avg b WHERE b.avg_amnt > a.avg_amnt) AS n_states_higher
FROM state_avg a
ORDER BY n_states_higher;

-- Q6
WITH quartiles AS (
    SELECT *, NTILE(4) OVER (ORDER BY annual_inc) AS income_quartile
    FROM loans
)
SELECT income_quartile,
       ROUND(100.0 * SUM(CASE WHEN loan_status IN ('Charged Off','Default') THEN 1 ELSE 0 END)
             / NULLIF(SUM(CASE WHEN loan_status != 'Current' THEN 1 ELSE 0 END), 0), 2) AS default_rate_pct
FROM quartiles
GROUP BY income_quartile
ORDER BY income_quartile;

-- Q7 (rentals.db)
WITH monthly_net AS (
    SELECT unit_id, month, SUM(amount) AS net_amount
    FROM transactions
    GROUP BY unit_id, month
)
SELECT unit_id, month, net_amount,
       ROUND(AVG(net_amount) OVER (PARTITION BY unit_id ORDER BY month
             ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS rolling_3mo_avg
FROM monthly_net
ORDER BY unit_id, month;
