"""
Generates an ILLUSTRATIVE 4-unit rental portfolio dataset — sample numbers,
not Jacquelyn's actual financials. Replace data/units.csv and
data/transactions.csv with real figures (rents, expenses, dates) to turn
this into a live analysis of the real portfolio; the SQL and Python below
don't need to change.
"""
import numpy as np, pandas as pd
rng = np.random.default_rng(7)

units = pd.DataFrame({
    'unit_id': [1,2,3,4],
    'unit_name': ['Unit A','Unit B','Unit C','Unit D'],
    'bedrooms': [2,3,2,1],
    'market_rent': [1150, 1450, 1200, 950],
})
units.to_csv('data/units.csv', index=False)

months = pd.date_range('2024-01-01', '2025-12-01', freq='MS')
rows = []
expense_cats = ['repairs','property_tax','insurance','utilities','landscaping','vacancy_loss']
for _, u in units.iterrows():
    occupied = True
    for m in months:
        # small chance of a vacancy month per unit
        if rng.random() < 0.04:
            occupied = False
        elif rng.random() < 0.6:
            occupied = True
        rent_collected = u['market_rent'] * rng.uniform(0.98, 1.03) if occupied else 0
        rows.append({'unit_id': u['unit_id'], 'month': m.strftime('%Y-%m-01'),
                      'category': 'rent_income', 'amount': round(rent_collected, 2)})
        # recurring small expenses every month
        rows.append({'unit_id': u['unit_id'], 'month': m.strftime('%Y-%m-01'),
                      'category': 'property_tax', 'amount': -round(u['market_rent']*0.06, 2)})
        rows.append({'unit_id': u['unit_id'], 'month': m.strftime('%Y-%m-01'),
                      'category': 'insurance', 'amount': -round(45 + rng.uniform(-5,5), 2)})
        if rng.random() < 0.25:
            rows.append({'unit_id': u['unit_id'], 'month': m.strftime('%Y-%m-01'),
                         'category': 'repairs', 'amount': -round(rng.uniform(50, 900), 2)})
        if rng.random() < 0.5:
            rows.append({'unit_id': u['unit_id'], 'month': m.strftime('%Y-%m-01'),
                         'category': 'landscaping', 'amount': -round(rng.uniform(40,120),2)})
        if not occupied:
            rows.append({'unit_id': u['unit_id'], 'month': m.strftime('%Y-%m-01'),
                         'category': 'vacancy_loss', 'amount': -round(u['market_rent']*0.3,2)})

txns = pd.DataFrame(rows)
txns.to_csv('data/transactions.csv', index=False)
print(units)
print(txns.shape)
