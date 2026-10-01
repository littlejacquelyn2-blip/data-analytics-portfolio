"""
PYTHON PRACTICE — TIER 3: ADVANCED
Multi-step analysis, groupby + transform, rolling windows, basic charting —
the level closest to real analyst work and to the projects in this repo.
Data: ../data/loans.csv, ../data/units.csv, ../data/transactions.csv
"""
import pandas as pd

loans = pd.read_csv('../data/loans.csv')
loans['issue_d'] = pd.to_datetime(loans['issue_d'])
units = pd.read_csv('../data/units.csv')
transactions = pd.read_csv('../data/transactions.csv')

# Q1. Compute the default rate (%) by grade. A loan is a default if
#     loan_status is 'Charged Off' or 'Default'; only count loans whose
#     status is NOT 'Current' in the denominator. (This is the Python
#     version of SQL practice Tier 3, Q1 — compare your two answers.)


# Q2. Using groupby('grade')['int_rate'].transform('mean'), add a column
#     `grade_avg_rate` to `loans` showing each loan's grade average next to
#     its own int_rate, without collapsing the DataFrame (no merge needed).


# Q3. Extract the origination month (YYYY-MM) into a new column, then compute
#     total loan_amnt per month and its cumulative sum over time.


# Q4. Bucket loans into income quartiles using pd.qcut on annual_inc, then
#     compute the default rate for each quartile (same logic as Q1, grouped
#     by quartile instead of grade).


# Q5. For the rentals data: compute monthly net cash flow per unit (merge
#     transactions -> units, group by unit + month, sum amount), then use
#     .rolling(3).mean() (after sorting by month, grouped by unit) to get a
#     3-month rolling average per unit.


# Q6. Write a function `flag_high_risk(row)` that returns True if
#     (grade in ['E','F','G']) OR (dti > 30 AND term_months == 60), and apply
#     it row-wise to create a `high_risk_flag` column. Report how many loans
#     are flagged.


# Q7. Bonus (matplotlib): plot default rate by grade as a bar chart and save
#     it to a file. (You already have a working example in
#     ../../01-lending-risk-analysis/notebooks/analysis.py — write your own
#     version from scratch without looking at it first, then compare.)
