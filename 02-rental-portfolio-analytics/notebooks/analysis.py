"""
Rental Portfolio Analytics
Run: python3 notebooks/analysis.py  (writes PNGs to ../charts/)
"""
import sqlite3, os
import pandas as pd
import matplotlib.pyplot as plt

DB = os.path.join(os.path.dirname(__file__), '..', 'data', 'rentals.db')
CHARTS = os.path.join(os.path.dirname(__file__), '..', 'charts')
con = sqlite3.connect(DB)

plt.rcParams.update({'figure.facecolor': 'white', 'axes.facecolor': 'white',
                      'font.size': 10, 'axes.edgecolor': '#444', 'axes.grid': True,
                      'grid.alpha': 0.25})

# 1. Net cash flow by unit
by_unit = pd.read_sql("""
    SELECT u.unit_name, ROUND(SUM(t.amount),2) AS net_cash_flow
    FROM transactions t JOIN units u ON u.unit_id = t.unit_id
    GROUP BY u.unit_name ORDER BY net_cash_flow DESC
""", con)
fig, ax = plt.subplots(figsize=(6,4))
ax.bar(by_unit['unit_name'], by_unit['net_cash_flow'], color='#3B6EA5')
ax.set_title('Net Cash Flow by Unit (2024–2025)')
ax.set_ylabel('Net Cash Flow ($)')
fig.tight_layout(); fig.savefig(os.path.join(CHARTS, 'net_cash_flow_by_unit.png'), dpi=150)
plt.close(fig)

# 2. Portfolio cumulative net cash flow over time
monthly = pd.read_sql("""
    SELECT month, SUM(amount) AS net_amount FROM transactions GROUP BY month ORDER BY month
""", con)
monthly['cumulative'] = monthly['net_amount'].cumsum()
fig, ax = plt.subplots(figsize=(7,4.5))
ax.plot(monthly['month'], monthly['cumulative'], color='#3B6EA5', linewidth=2)
ax.set_title('Cumulative Portfolio Net Cash Flow')
ax.set_ylabel('Cumulative Net ($)')
ax.set_xticks(ax.get_xticks()[::3])
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
fig.tight_layout(); fig.savefig(os.path.join(CHARTS, 'cumulative_cash_flow.png'), dpi=150)
plt.close(fig)

# 3. Expense breakdown
exp = pd.read_sql("""
    SELECT category, ROUND(SUM(-amount),2) AS total_expense
    FROM transactions WHERE category != 'rent_income'
    GROUP BY category ORDER BY total_expense DESC
""", con)
fig, ax = plt.subplots(figsize=(6,4))
ax.barh(exp['category'], exp['total_expense'], color='#C0562D')
ax.set_title('Total Expenses by Category (2024–2025)')
ax.set_xlabel('Total ($)')
fig.tight_layout(); fig.savefig(os.path.join(CHARTS, 'expense_breakdown.png'), dpi=150)
plt.close(fig)

# 4. Occupancy rate by unit
occ = pd.read_sql("""
    SELECT u.unit_name,
           ROUND(100.0*SUM(CASE WHEN t.category='rent_income' AND t.amount>0 THEN 1 ELSE 0 END)
                 / COUNT(DISTINCT t.month), 1) AS occupancy_rate_pct
    FROM transactions t JOIN units u ON u.unit_id=t.unit_id
    GROUP BY u.unit_name ORDER BY occupancy_rate_pct DESC
""", con)
fig, ax = plt.subplots(figsize=(6,4))
ax.bar(occ['unit_name'], occ['occupancy_rate_pct'], color='#3B6EA5')
ax.set_ylim(0, 100)
ax.set_title('Occupancy Rate by Unit')
ax.set_ylabel('Occupancy Rate (%)')
for i, v in enumerate(occ['occupancy_rate_pct']):
    ax.text(i, v + 1.5, f'{v}%', ha='center', fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(CHARTS, 'occupancy_by_unit.png'), dpi=150)
plt.close(fig)

print("Charts written.")
print(by_unit.to_string(index=False))
con.close()
