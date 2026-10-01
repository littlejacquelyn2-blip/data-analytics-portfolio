"""
Lending Risk Analysis
Analyst-style exploratory analysis of a consumer loan book: default rate
by grade, vintage, purpose, and risk bucket, plus a pricing sanity check.
Mirrors the kind of portfolio-health monitoring an R&A analyst does.
Run: python3 notebooks/analysis.py   (writes PNGs to ../charts/)
"""
import sqlite3, os
import pandas as pd
import matplotlib.pyplot as plt

con = sqlite3.connect(os.path.join(os.path.dirname(__file__), '..', 'data', 'loans.db'))

RESOLVED = "loan_status != 'Current'"
DEFAULTED = "loan_status IN ('Charged Off','Default')"

def default_rate_by(col):
    q = f"""
        SELECT {col} AS grp,
               COUNT(*) AS n,
               SUM(CASE WHEN {DEFAULTED} THEN 1 ELSE 0 END) AS defaults,
               ROUND(100.0*SUM(CASE WHEN {DEFAULTED} THEN 1 ELSE 0 END) /
                     SUM(CASE WHEN {RESOLVED} THEN 1 ELSE 0 END), 2) AS default_rate_pct
        FROM loans GROUP BY grp ORDER BY grp
    """
    return pd.read_sql(q, con)

plt.rcParams.update({'figure.facecolor': 'white', 'axes.facecolor': 'white',
                      'font.size': 10, 'axes.edgecolor': '#444', 'axes.grid': True,
                      'grid.alpha': 0.25})

# 1. Default rate by grade
by_grade = default_rate_by('grade')
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(by_grade['grp'], by_grade['default_rate_pct'], color='#3B6EA5')
ax.set_title('Default Rate by Loan Grade')
ax.set_xlabel('Grade'); ax.set_ylabel('Default Rate (%)')
for i, v in enumerate(by_grade['default_rate_pct']):
    ax.text(i, v + 0.5, f'{v}%', ha='center', fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(os.path.dirname(__file__), '..', 'charts', 'default_rate_by_grade.png'), dpi=150)
plt.close(fig)

# 2. Default rate by vintage year x grade (small multiples via pivot + line chart)
vintage = pd.read_sql(f"""
    SELECT strftime('%Y', issue_d) AS vintage_year, grade,
           ROUND(100.0*SUM(CASE WHEN {DEFAULTED} THEN 1 ELSE 0 END) /
                 NULLIF(SUM(CASE WHEN {RESOLVED} THEN 1 ELSE 0 END),0), 2) AS default_rate_pct
    FROM loans GROUP BY vintage_year, grade ORDER BY vintage_year, grade
""", con)
pivot = vintage.pivot(index='vintage_year', columns='grade', values='default_rate_pct')
fig, ax = plt.subplots(figsize=(7, 4.5))
for g in ['A','B','C','D','E']:
    if g in pivot.columns:
        ax.plot(pivot.index, pivot[g], marker='o', label=g)
ax.set_title('Default Rate by Vintage Year (Grades A–E)')
ax.set_xlabel('Origination Year'); ax.set_ylabel('Default Rate (%)')
ax.legend(title='Grade', ncol=5, fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(os.path.dirname(__file__), '..', 'charts', 'default_rate_by_vintage.png'), dpi=150)
plt.close(fig)

# 3. Default rate by purpose (horizontal, sorted)
by_purpose = default_rate_by('purpose').sort_values('default_rate_pct')
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.barh(by_purpose['grp'], by_purpose['default_rate_pct'], color='#C0562D')
ax.set_title('Default Rate by Loan Purpose')
ax.set_xlabel('Default Rate (%)')
fig.tight_layout(); fig.savefig(os.path.join(os.path.dirname(__file__), '..', 'charts', 'default_rate_by_purpose.png'), dpi=150)
plt.close(fig)

# 4. DTI bucket vs default rate
dti_q = f"""
    SELECT CASE WHEN dti<10 THEN '<10' WHEN dti<20 THEN '10-20'
                WHEN dti<30 THEN '20-30' ELSE '30+' END AS bucket,
           ROUND(100.0*SUM(CASE WHEN {DEFAULTED} THEN 1 ELSE 0 END) /
                 NULLIF(SUM(CASE WHEN {RESOLVED} THEN 1 ELSE 0 END),0), 2) AS default_rate_pct
    FROM loans GROUP BY bucket
"""
dti_df = pd.read_sql(dti_q, con)
order = ['<10','10-20','20-30','30+']
dti_df['bucket'] = pd.Categorical(dti_df['bucket'], order, ordered=True)
dti_df = dti_df.sort_values('bucket')
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(dti_df['bucket'].astype(str), dti_df['default_rate_pct'], marker='o', color='#3B6EA5', linewidth=2)
ax.set_title('Default Rate by Debt-to-Income Bucket')
ax.set_xlabel('DTI Bucket (%)'); ax.set_ylabel('Default Rate (%)')
fig.tight_layout(); fig.savefig(os.path.join(os.path.dirname(__file__), '..', 'charts', 'default_rate_by_dti.png'), dpi=150)
plt.close(fig)

print("Charts written to ../charts/")
print(by_grade.to_string(index=False))
con.close()
