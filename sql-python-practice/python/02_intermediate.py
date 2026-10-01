"""
PYTHON PRACTICE — TIER 2: INTERMEDIATE
groupby, merge, apply/lambda, multi-condition filters
Data: ../data/loans.csv, ../data/units.csv, ../data/transactions.csv
"""
import pandas as pd

loans = pd.read_csv('../data/loans.csv')
units = pd.read_csv('../data/units.csv')
transactions = pd.read_csv('../data/transactions.csv')

# Q1. Using groupby, find the average int_rate per grade, rounded to 2 decimals.


# Q2. Using groupby + agg, find both the count and total loan_amnt for each purpose
#     in a single call (hint: .agg({'loan_amnt': ['count','sum']})).


# Q3. Create a `risk_tier` column using a lambda/apply: grade A/B -> 'low',
#     C/D -> 'medium', E/F/G -> 'high'. (Try it with .map() using a dict, too.)


# Q4. Merge `transactions` with `units` on unit_id, then find total rent_income
#     (category == 'rent_income') grouped by unit_name.


# Q5. Filter loans where (grade in ['A','B']) AND (dti > 20) AND (term_months == 60).


# Q6. Using groupby, find the min and max loan_amnt per grade in one call.


# Q7. Using merge + groupby, find which month (across the whole rentals portfolio)
#     had the largest total expense (category != 'rent_income').


# Q8. Create a pivot table: rows = purpose, columns = grade, values = average int_rate
#     (use pd.pivot_table).
