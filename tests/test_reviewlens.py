import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from reviewlens.load import load_reviews  # noqa: E402
from reviewlens.metrics import monthly_trends, rating_distribution, theme_metrics  # noqa: E402
from reviewlens.themes import load_theme_patterns, tag_themes  # noqa: E402


def small_frame():
    return pd.DataFrame({
        "text": ["App crashes on start", "Too many ads", "Love it", "crash again and slow",
                 "Great design", "Login error, cannot sign in", "ok", "Ads ads ads", "Fine", "Nice"],
        "rating": [1, 2, 5, 1, 5, 1, 4, 2, 4, 5],
        "date": pd.to_datetime(["2026-01-05"] * 5 + ["2026-02-10"] * 5),
    })


class LoadTests(unittest.TestCase):
    def test_cleaning_counts(self):
        csv = "review,rating,date\nGood app,5,2026-01-01\nGood app,5,2026-01-01\n,3,2026-01-02\nBad,9,2026-01-03\nSlow,2,not-a-date\n"
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "r.csv"
            p.write_text(csv)
            df, s = load_reviews(p)
        self.assertEqual(s.rows_in, 5)
        self.assertEqual(s.dropped_duplicates, 1)
        self.assertEqual(s.dropped_missing, 1)
        self.assertEqual(s.dropped_bad_rating, 1)
        self.assertEqual(s.rows_out, 2)

    def test_missing_column_error(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "r.csv"
            p.write_text("a,b\n1,2\n")
            with self.assertRaises(ValueError):
                load_reviews(p)


class ThemeTests(unittest.TestCase):
    def test_tags_expected_themes(self):
        tagged = tag_themes(small_frame(), load_theme_patterns())
        self.assertTrue(tagged.loc[0, "crashes_bugs"])
        self.assertTrue(tagged.loc[1, "ads"])
        self.assertTrue(tagged.loc[3, "performance"])
        self.assertTrue(tagged.loc[5, "login_account"])
        self.assertFalse(tagged.loc[2, "crashes_bugs"])

    def test_ui_does_not_match_inside_words(self):
        df = pd.DataFrame({"text": ["quite quiet", "the ui is nice"], "rating": [3, 4], "date": pd.NaT})
        tagged = tag_themes(df, load_theme_patterns())
        self.assertEqual(list(tagged["ui_ux"]), [False, True])


class MetricTests(unittest.TestCase):
    def test_impact_matches_hand_calculation(self):
        tagged = tag_themes(small_frame(), load_theme_patterns())
        m = theme_metrics(tagged, ["crashes_bugs"], min_mentions=2).iloc[0]
        # crashes_bugs: rows 0 (1 star), 3 (1 star), 5 (1 star) -> 3 mentions
        self.assertEqual(m["mentions"], 3)
        overall = tagged["rating"].mean()  # 3.0
        self.assertAlmostEqual(overall, 3.0)
        self.assertAlmostEqual(m["avg_rating_when_mentioned"], 1.0)
        self.assertAlmostEqual(m["impact"], 0.3 * (3.0 - 1.0))
        self.assertTrue(m["reliable"])

    def test_monthly_trends_and_distribution(self):
        tagged = tag_themes(small_frame(), load_theme_patterns())
        t = monthly_trends(tagged, ["ads"])
        self.assertEqual(list(t["reviews"]), [5, 5])
        self.assertEqual(int(rating_distribution(tagged).sum()), 10)


if __name__ == "__main__":
    unittest.main()
