# SQL & Python Practice

A self-paced curriculum built around the same two datasets used in the
portfolio projects (`data/loans.db` / `loans.csv` and `data/rentals.db` /
`units.csv` + `transactions.csv`), so what you practice here transfers
directly to the projects and to a real analyst technical screen.

## How to use this

1. Work through each tier's question file — write your answer directly
   under the question, run it, and see if the output makes sense before
   checking the solution.
2. Don't peek at `solutions/` first. Getting it wrong and figuring out why
   is most of the value.
3. SQL: run queries with `sqlite3 ../data/loans.db` (interactive shell) or
   from Python with `pandas.read_sql`. Python: run each file with
   `python3 01_beginner.py` etc. from inside the `python/` folder.

## Order (do SQL and Python side by side, tier by tier)

| Tier | SQL | Python | Focus |
|---|---|---|---|
| 1 — Beginner | `sql/01_beginner.sql` | `python/01_beginner.py` | SELECT/WHERE/ORDER BY, filtering, value_counts, basic aggregation |
| 2 — Intermediate | `sql/02_intermediate.sql` | `python/02_intermediate.py` | GROUP BY + HAVING, CASE/map, JOIN/merge, subqueries, pivot tables |
| 3 — Advanced | `sql/03_advanced.sql` | `python/03_advanced.py` | CTEs, window functions (RANK, LAG, NTILE, rolling averages), groupby+transform, row-wise apply |

Tier 3 is the level Affirm's posting (and most fintech/analyst screens) test
for: CTEs and window functions in SQL, groupby/merge/apply fluency in
Python. If you can do Tier 3 comfortably without the solutions, you're in
good shape for a live SQL screen.

## After this

- Redo the queries in `../01-lending-risk-analysis/sql/analysis_queries.sql`
  and `../02-rental-portfolio-analytics/sql/analysis_queries.sql` from
  scratch, without looking at the finished versions — that's the real test
  of whether Tier 3 stuck.
- For more reps in the same style: DataLemur and StrataScratch both have
  free SQL questions modeled on real company interviews (cohort analysis,
  funnel analysis, window functions) that match this tier well.
