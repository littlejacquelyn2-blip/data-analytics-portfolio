"""
Generates a synthetic loan-book dataset modeled on the public LendingClub
loan-level schema and on realistic, published default-rate patterns by
grade, term, and purpose (Fed / LendingClub aggregate stats). This is a
synthetic dataset, not a redistribution of real borrower records — that's
disclosed in the README, and the schema/fields mirror what real fintech
loan tables look like so the SQL/Python work transfers directly.
"""
import numpy as np, pandas as pd
rng = np.random.default_rng(42)

N = 25000
grades = np.array(['A','B','C','D','E','F','G'])
grade_probs = np.array([0.16,0.28,0.26,0.16,0.08,0.04,0.02])
grade_base_default = {'A':0.04,'B':0.08,'C':0.14,'D':0.21,'E':0.29,'F':0.36,'G':0.42}
purposes = ['debt_consolidation','credit_card','home_improvement','major_purchase',
            'medical','small_business','car','other']
purpose_probs = [0.47,0.20,0.08,0.06,0.04,0.05,0.04,0.06]
states = ['CA','TX','NY','FL','OH','PA','IL','GA','NC','MI','NJ','VA','WA','AZ','MA']

grade = rng.choice(grades, N, p=grade_probs)
sub_grade = np.array([f"{g}{rng.integers(1,6)}" for g in grade])
term = rng.choice([36,60], N, p=[0.72,0.28])
loan_amnt = np.round(rng.normal(15000, 8000, N).clip(1000, 40000), -2)
int_rate = np.round(np.select(
    [grade==g for g in grades],
    [rng.normal({'A':7,'B':10,'C':13.5,'D':17,'E':20.5,'F':24,'G':27}[g], 1.2, N) for g in grades]
).clip(5, 31), 2)
annual_inc = np.round(rng.lognormal(mean=11.0, sigma=0.5, size=N).clip(15000, 400000), -2)
dti = np.round(rng.normal(18, 8, N).clip(0, 45), 2)
purpose = rng.choice(purposes, N, p=purpose_probs)
addr_state = rng.choice(states, N)
issue_year = rng.choice([2019,2020,2021,2022,2023], N, p=[0.16,0.18,0.24,0.24,0.18])
issue_month = rng.integers(1,13,N)
issue_d = pd.to_datetime({'year':issue_year,'month':issue_month,'day':1})
emp_length = rng.choice(['< 1 year','1 year','2 years','3 years','4 years','5 years',
                         '6 years','7 years','8 years','9 years','10+ years'], N)
home_ownership = rng.choice(['RENT','MORTGAGE','OWN'], N, p=[0.4,0.45,0.15])

# default probability: grade base rate, nudged by dti, term, vintage (2020 cohort a bit worse)
base = np.array([grade_base_default[g] for g in grade])
dti_adj = (dti - 18) * 0.004
term_adj = np.where(term==60, 0.03, 0.0)
vintage_adj = np.where(issue_year==2020, 0.02, 0.0)
p_default = (base + dti_adj + term_adj + vintage_adj).clip(0.01, 0.85)
defaulted = rng.binomial(1, p_default)
loan_status = np.where(defaulted==1,
                        rng.choice(['Charged Off','Default'], N, p=[0.85,0.15]),
                        rng.choice(['Fully Paid','Current'], N, p=[0.75,0.25]))

df = pd.DataFrame({
    'loan_id': np.arange(1, N+1),
    'loan_amnt': loan_amnt,
    'term_months': term,
    'int_rate': int_rate,
    'grade': grade,
    'sub_grade': sub_grade,
    'emp_length': emp_length,
    'home_ownership': home_ownership,
    'annual_inc': annual_inc,
    'dti': dti,
    'purpose': purpose,
    'addr_state': addr_state,
    'issue_d': issue_d.dt.strftime('%Y-%m-%d'),
    'loan_status': loan_status,
})
df.to_csv('data/loans.csv', index=False)
print(df.shape)
print(df['loan_status'].value_counts(normalize=True))
