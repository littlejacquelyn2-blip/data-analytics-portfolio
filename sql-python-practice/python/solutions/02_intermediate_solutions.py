"""Run from inside python/solutions/: python3 02_intermediate_solutions.py"""
import pandas as pd

loans = pd.read_csv('../../data/loans.csv')
units = pd.read_csv('../../data/units.csv')
transactions = pd.read_csv('../../data/transactions.csv')

# Q1
print(loans.groupby('grade')['int_rate'].mean().round(2))

# Q2
print(loans.groupby('purpose')['loan_amnt'].agg(['count', 'sum']))

# Q3
risk_map = {'A': 'low', 'B': 'low', 'C': 'medium', 'D': 'medium',
            'E': 'high', 'F': 'high', 'G': 'high'}
loans['risk_tier'] = loans['grade'].map(risk_map)
# equivalent with apply:
# loans['risk_tier'] = loans['grade'].apply(lambda g: risk_map[g])
print(loans[['grade', 'risk_tier']].drop_duplicates())

# Q4
merged = transactions.merge(units, on='unit_id')
rent_by_unit = merged[merged['category'] == 'rent_income'].groupby('unit_name')['amount'].sum()
print(rent_by_unit)

# Q5
filtered = loans[(loans['grade'].isin(['A', 'B'])) & (loans['dti'] > 20) & (loans['term_months'] == 60)]
print(filtered.shape)

# Q6
print(loans.groupby('grade')['loan_amnt'].agg(['min', 'max']))

# Q7
merged = transactions.merge(units, on='unit_id')
expenses = merged[merged['category'] != 'rent_income']
by_month = expenses.groupby('month')['amount'].sum().abs()  # amounts are negative
print(by_month.idxmax(), by_month.max())

# Q8
pivot = pd.pivot_table(loans, index='purpose', columns='grade', values='int_rate', aggfunc='mean').round(2)
print(pivot)
