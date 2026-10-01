"""Run from inside python/solutions/: python3 01_beginner_solutions.py"""
import pandas as pd

loans = pd.read_csv('../../data/loans.csv')
units = pd.read_csv('../../data/units.csv')
transactions = pd.read_csv('../../data/transactions.csv')

# Q1
print(loans.shape)
print(loans.columns.tolist())

# Q2
print(loans[loans['grade'] == 'A'].head())

# Q3
print(loans['loan_amnt'].mean())

# Q4
print(loans['grade'].value_counts())

# Q5
print(loans.sort_values('loan_amnt', ascending=False)[['loan_id', 'loan_amnt', 'grade']].head(10))

# Q6
print(loans[loans['annual_inc'] > 150000].sort_values('annual_inc', ascending=False))

# Q7
loans['high_dti'] = loans['dti'] > 25
print(loans['high_dti'].sum())

# Q8
print(units[units['market_rent'] > 1000])

# Q9
print(transactions[transactions['category'] == 'repairs']['amount'].sum())

# Q10
print(loans[loans['purpose'].isin(['medical', 'car'])])
