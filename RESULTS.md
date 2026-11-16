# Results

Produced on 2026-11-16 with Python 3.12.3.

## Unit tests
`PYTHONPATH=src python -m unittest discover -s tests`

```
----------------------------------------------------------------------
Ran 6 tests in 0.045s

OK
```

The tests verify data cleaning counts, theme matching (including word-boundary handling) and the impact formula against hand calculations.

## Findings on real data
Not yet available. This repository has not been run on a real review dataset. After running it on one product's reviews, add here: the dataset source and size, the top three pain points with their impact scores, and the precision of the theme tags on a 100-review hand-labelled sample.

## Sample output (synthetic demo data)
The charts below come from **generated** reviews and show only what the tool produces. They are **not findings**. Regenerate with `PYTHONPATH=src python scripts/make_demo.py`. Open `docs/demo/report.md` for the full sample report and the CSVs you can load into Power BI or Tableau.

![Top pain points, synthetic demo](docs/demo/top_pain_points.png)

![Rating distribution, synthetic demo](docs/demo/rating_distribution.png)
