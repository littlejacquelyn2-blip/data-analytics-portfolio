# Lending Risk Analysis

Analyst-style exploratory analysis of a consumer loan book, built to mirror the
kind of portfolio-health monitoring a risk & analytics analyst does day to day:
measuring default rates, spotting which segments carry the most risk, and
sanity-checking that pricing matches that risk.

## Dataset

`data/loans.csv` (25,000 rows) is a **synthetic dataset** — it is not real
borrower data. It's generated (`generate_data.py`) with a schema modeled on
the public LendingClub loan-level dataset, and with default rates calibrated
to realistic, published patterns (default rate rising with loan grade, DTI,
and 60-month terms; a worse-performing 2020 vintage). This keeps the project
self-contained and reproducible without redistributing anyone's real
financial records, while the schema, SQL, and analysis are exactly what you'd
run against a real loan book.

Fields: `loan_id, loan_amnt, term_months, int_rate, grade, sub_grade,
emp_length, home_ownership, annual_inc, dti, purpose, addr_state, issue_d,
loan_status`.

## What's here

- `generate_data.py` — builds the dataset
- `data/loans.db` — the same data loaded into SQLite
- `sql/analysis_queries.sql` — 8 queries, ordered from basic aggregation to
  CTEs, window functions (`RANK`, running totals, rolling averages), and a
  self-join-style comparison
- `notebooks/analysis.py` — runs the queries via `pandas.read_sql`, builds
  the charts in `charts/`, and prints a summary table
- `charts/` — output PNGs

## Key findings

- **Default rate rises monotonically with grade**, from ~8% (A) to ~53% (G) —
  confirms the grading system is doing its job.
- **2020-issued loans default at a higher rate** than surrounding vintages
  across every grade, consistent with a macro shock hitting a cohort
  regardless of underwriting quality — the kind of pattern a "flag anomalies
  to senior team members" analyst would surface.
- **Small-business and debt-consolidation loans default more than
  car or medical loans** — purpose carries real signal beyond grade alone.
- **Default rate climbs sharply above a 30% DTI** — a natural underwriting
  cutoff to test.

## Run it yourself

```bash
python3 generate_data.py           # rebuild data/loans.csv + loads it below
python3 -c "import sqlite3,pandas as pd; \
  pd.read_csv('data/loans.csv').to_sql('loans', sqlite3.connect('data/loans.db'), if_exists='replace', index=False)"
sqlite3 data/loans.db < sql/analysis_queries.sql   # or open in any SQLite client
cd notebooks && python3 analysis.py
```

Requires `pandas`, `numpy`, `matplotlib` (`pip install pandas numpy matplotlib`).
