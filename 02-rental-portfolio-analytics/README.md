# Rental Portfolio Analytics

Cash-flow, occupancy, and expense analysis for a small residential rental
portfolio — the same kind of unit-level P&L tracking used to guide pricing,
budgeting, and capital-improvement decisions.

## Dataset

**`data/units.csv` and `data/transactions.csv` contain illustrative sample
numbers, not real financials.** The schema (4 units, monthly rent and
expense line items) mirrors a real rental portfolio's books. To turn this
into a live analysis, replace the two CSVs with real numbers (same column
names) and rerun — none of the SQL or Python needs to change.

- `units`: unit_id, unit_name, bedrooms, market_rent
- `transactions`: unit_id, month, category, amount (signed: + = income, − = expense)

## What's here

- `generate_data.py` — builds the sample dataset
- `data/rentals.db` — same data loaded into SQLite (2 tables)
- `sql/analysis_queries.sql` — 7 queries: joins, running totals, `LAG`
  month-over-month deltas, and a rent-vs-market-benchmark comparison
- `notebooks/analysis.py` — runs the queries, builds charts in `charts/`

## Key findings (on the sample data)

- Net cash flow varies meaningfully by unit even before financing costs —
  useful for deciding where the next capital dollar goes.
- Occupancy rate differs by unit, and even a short vacancy month has an
  outsized effect on that unit's annual return.
- Expense categories are dominated by property tax and insurance, with
  repairs the most variable and least predictable line.

## Run it yourself

```bash
python3 generate_data.py
python3 -c "import sqlite3,pandas as pd; con=sqlite3.connect('data/rentals.db'); \
  pd.read_csv('data/units.csv').to_sql('units',con,if_exists='replace',index=False); \
  pd.read_csv('data/transactions.csv').to_sql('transactions',con,if_exists='replace',index=False)"
sqlite3 data/rentals.db < sql/analysis_queries.sql
cd notebooks && python3 analysis.py
```
