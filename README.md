# Data Analytics Portfolio — Jacquelyn Little

SQL and Python projects analyzing consumer lending risk and rental
portfolio performance, built to demonstrate analyst-level data work:
normalizing raw data, writing SQL from basic aggregation through CTEs and
window functions, and turning results into charts a non-technical
stakeholder can act on.

**Live portfolio page:** see the published link shared alongside this repo
(or re-publish `../site/index.html` yourself — it's a plain HTML file).

## Projects

- **[`01-lending-risk-analysis/`](01-lending-risk-analysis/)** — default
  rate by grade, vintage, and purpose on a 25,000-loan synthetic dataset
  modeled on the public LendingClub schema.
- **[`02-rental-portfolio-analytics/`](02-rental-portfolio-analytics/)** —
  cash flow, occupancy, and expense analysis for a 4-unit rental portfolio
  (sample data — swap in real numbers to make it live).

## Practice

- **[`sql-python-practice/`](sql-python-practice/)** — a self-paced,
  three-tier SQL and Python curriculum built on the same two datasets,
  with solutions, for building toward the CTE/window-function level tested
  in most analyst technical screens.

## Setup

Requires Python 3 with `pandas`, `numpy`, and `matplotlib`:

```bash
pip install pandas numpy matplotlib
```

SQLite ships with Python (`sqlite3` module); a standalone `sqlite3` CLI is
only needed if you want to run `.sql` files directly from a terminal
instead of through Python.

## License

MIT — see [LICENSE](LICENSE).
