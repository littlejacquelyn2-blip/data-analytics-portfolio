"""Run from inside python/solutions/: python3 03_advanced_solutions.py"""
import pandas as pd
import matplotlib.pyplot as plt

loans = pd.read_csv('../../data/loans.csv')
loans['issue_d'] = pd.to_datetime(loans['issue_d'])
units = pd.read_csv('../../data/units.csv')
transactions = pd.read_csv('../../data/transactions.csv')

DEFAULT_STATUSES = ['Charged Off', 'Default']

def default_rate(df):
    resolved = df[df['loan_status'] != 'Current']
    return round(100 * resolved['loan_status'].isin(DEFAULT_STATUSES).mean(), 2)

# Q1
print(loans.groupby('grade').apply(default_rate, include_groups=False))

# Q2
loans['grade_avg_rate'] = loans.groupby('grade')['int_rate'].transform('mean').round(2)
print(loans[['loan_id', 'grade', 'int_rate', 'grade_avg_rate']].head())

# Q3
loans['month'] = loans['issue_d'].dt.strftime('%Y-%m')
by_month = loans.groupby('month')['loan_amnt'].sum().sort_index()
cumulative = by_month.cumsum()
print(cumulative.tail())

# Q4
loans['income_quartile'] = pd.qcut(loans['annual_inc'], 4, labels=[1, 2, 3, 4])
print(loans.groupby('income_quartile', observed=True).apply(default_rate, include_groups=False))

# Q5
merged = transactions.merge(units, on='unit_id')
monthly_net = merged.groupby(['unit_name', 'month'])['amount'].sum().reset_index()
monthly_net = monthly_net.sort_values(['unit_name', 'month'])
monthly_net['rolling_3mo'] = monthly_net.groupby('unit_name')['amount'].transform(
    lambda s: s.rolling(3, min_periods=1).mean().round(2)
)
print(monthly_net.head(10))

# Q6
def flag_high_risk(row):
    return (row['grade'] in ['E', 'F', 'G']) or (row['dti'] > 30 and row['term_months'] == 60)

loans['high_risk_flag'] = loans.apply(flag_high_risk, axis=1)
print(loans['high_risk_flag'].sum())

# Q7
rates = loans.groupby('grade').apply(default_rate, include_groups=False)
fig, ax = plt.subplots()
ax.bar(rates.index, rates.values)
ax.set_title('Default Rate by Grade')
ax.set_ylabel('Default Rate (%)')
fig.savefig('q7_default_rate_by_grade.png', dpi=150)
print("Saved q7_default_rate_by_grade.png")
