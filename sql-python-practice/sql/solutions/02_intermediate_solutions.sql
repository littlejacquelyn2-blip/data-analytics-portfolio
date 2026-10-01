-- SOLUTIONS — TIER 2: INTERMEDIATE

-- Q1
SELECT grade, ROUND(AVG(int_rate), 2) AS avg_int_rate
FROM loans
GROUP BY grade
HAVING COUNT(*) > 500;

-- Q2
SELECT loan_id, grade,
       CASE WHEN grade IN ('A','B') THEN 'low'
            WHEN grade IN ('C','D') THEN 'medium'
            ELSE 'high' END AS risk_tier
FROM loans
LIMIT 20;

-- Q3
SELECT grade, home_ownership, COUNT(*) AS n, SUM(loan_amnt) AS total_amnt
FROM loans
GROUP BY grade, home_ownership
ORDER BY grade, home_ownership;

-- Q4 (rentals.db)
SELECT u.unit_name, ROUND(SUM(t.amount), 2) AS total_rent_income
FROM transactions t
JOIN units u ON u.unit_id = t.unit_id
WHERE t.category = 'rent_income'
GROUP BY u.unit_name;

-- Q5
SELECT * FROM loans
WHERE int_rate > (SELECT AVG(int_rate) FROM loans);

-- Q6
SELECT purpose, MIN(loan_amnt) AS min_amnt, MAX(loan_amnt) AS max_amnt, COUNT(*) AS n
FROM loans
GROUP BY purpose;

-- Q7 (rentals.db)
SELECT month,
       SUM(CASE WHEN category = 'rent_income' THEN amount ELSE 0 END) AS income,
       SUM(CASE WHEN category != 'rent_income' THEN -amount ELSE 0 END) AS expenses
FROM transactions
GROUP BY month
HAVING expenses > income;

-- Q8
SELECT addr_state, SUM(loan_amnt) AS total_amnt
FROM loans
GROUP BY addr_state
ORDER BY total_amnt DESC
LIMIT 3;
