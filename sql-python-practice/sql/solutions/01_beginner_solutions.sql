-- SOLUTIONS — TIER 1: BEGINNER

-- Q1
SELECT * FROM loans WHERE grade = 'A' LIMIT 10;

-- Q2
SELECT COUNT(*) FROM loans;

-- Q3
SELECT ROUND(AVG(loan_amnt), 2) FROM loans;

-- Q4
SELECT DISTINCT purpose FROM loans;

-- Q5
SELECT grade, COUNT(*) AS n FROM loans GROUP BY grade ORDER BY n DESC;

-- Q6
SELECT loan_id, loan_amnt, grade FROM loans ORDER BY loan_amnt DESC LIMIT 10;

-- Q7
SELECT * FROM loans WHERE annual_inc > 150000 ORDER BY annual_inc DESC;

-- Q8 (data/rentals.db)
SELECT * FROM units WHERE market_rent > 1000;

-- Q9 (data/rentals.db)
SELECT SUM(amount) FROM transactions WHERE category = 'repairs';

-- Q10
SELECT * FROM loans WHERE purpose IN ('medical', 'car');
