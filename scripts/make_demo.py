"""Create a DEMO report from synthetic reviews so you can see what the tool produces.
The data is generated, NOT real. Run from the repo root:
   PYTHONPATH=src python scripts/make_demo.py
"""
import random
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from reviewlens.load import load_reviews  # noqa: E402
from reviewlens.metrics import monthly_trends, rating_distribution, theme_metrics  # noqa: E402
from reviewlens.report import write_report  # noqa: E402
from reviewlens.themes import load_theme_patterns, tag_themes  # noqa: E402

random.seed(11)
pool = [
    ("The app crashes every time I open it", [1, 1, 2]),
    ("Very slow and laggy on my phone", [1, 2, 2, 3]),
    ("Too many ads, cannot use it properly", [1, 2, 2]),
    ("Login keeps failing, otp never arrives", [1, 1, 2]),
    ("Subscription is expensive for what it offers", [2, 2, 3]),
    ("Love the clean design and layout", [4, 5, 5]),
    ("Great app, works well", [4, 5, 5, 5]),
    ("Please add a dark mode feature", [3, 4]),
    ("Battery drain after the latest update", [2, 2, 3]),
    ("Customer support never replied to my complaint", [1, 1, 2]),
    ("Does what I need, simple and fast", [4, 5]),
]
weights = [8, 10, 9, 6, 7, 14, 18, 6, 5, 4, 13]
rows = []
for i in range(1500):
    text, ratings = random.choices(pool, weights)[0]
    month = random.randint(1, 9)
    rows.append((f"{text} #{i}", random.choice(ratings), f"2026-{month:02d}-{random.randint(1, 28):02d}"))
csv = ROOT / "data" / "_demo_synthetic.csv"
pd.DataFrame(rows, columns=["review", "rating", "date"]).to_csv(csv, index=False)

df, summary = load_reviews(csv)
patterns = load_theme_patterns()
tagged = tag_themes(df, patterns)
themes = list(patterns)
out = ROOT / "docs" / "demo"
path = write_report(out, tagged, summary, theme_metrics(tagged, themes), monthly_trends(tagged, themes),
                    rating_distribution(tagged), 30, title_suffix=" [SYNTHETIC DEMO DATA]",
                    banner="> **SYNTHETIC DEMO DATA. These are generated reviews used to show the output format. They are not real findings.**")
csv.unlink()
print("Demo report written to", path)
