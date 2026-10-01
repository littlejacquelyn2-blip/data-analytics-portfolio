"""
PYTHON PRACTICE — TIER 1: BEGINNER (pandas fundamentals)
Data: ../data/loans.csv, ../data/units.csv, ../data/transactions.csv
Write your code under each question, run this file, and check your output
against solutions/01_beginner_solutions.py
"""
import pandas as pd

loans = pd.read_csv('../data/loans.csv')
units = pd.read_csv('../data/units.csv')
transactions = pd.read_csv('../data/transactions.csv')

# Q1. Print the shape of `loans` (rows, columns) and its column names.


# Q2. Filter `loans` to only grade 'A' loans and print the first 5 rows.


# Q3. Find the average loan_amnt across all loans (a single number).


# Q4. Count how many loans exist for each grade (use value_counts()).


# Q5. Sort `loans` by loan_amnt descending and print the top 10
#     (loan_id, loan_amnt, grade columns only).


# Q6. Find all loans where annual_inc > 150000, sorted by annual_inc descending.


# Q7. Add a new column `high_dti` to `loans` that is True when dti > 25,
#     else False. Print how many loans have high_dti == True.


# Q8. From `units`, filter to units with market_rent > 1000.


# Q9. From `transactions`, filter to category == 'repairs' and sum the amount column.


# Q10. Find all loans where purpose is 'medical' or 'car' (use .isin()).
