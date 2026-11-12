"""Usage:
  PYTHONPATH=src python -m reviewlens.cli --input data/reviews.csv \
      --text-col content --rating-col score --date-col at --out reports
"""
from __future__ import annotations

import argparse

from .load import load_reviews
from .metrics import monthly_trends, rating_distribution, theme_metrics
from .report import write_report
from .themes import DEFAULT_THEMES, load_theme_patterns, tag_themes


def main() -> None:
    p = argparse.ArgumentParser(description="Rank product pain points from app reviews.")
    p.add_argument("--input", required=True, help="Path to reviews CSV")
    p.add_argument("--text-col", default="review")
    p.add_argument("--rating-col", default="rating")
    p.add_argument("--date-col", default="date")
    p.add_argument("--themes", default=str(DEFAULT_THEMES), help="Path to themes JSON")
    p.add_argument("--min-mentions", type=int, default=30)
    p.add_argument("--out", default="reports")
    args = p.parse_args()

    df, summary = load_reviews(args.input, args.text_col, args.rating_col, args.date_col)
    patterns = load_theme_patterns(args.themes)
    tagged = tag_themes(df, patterns)
    themes = list(patterns)
    metrics = theme_metrics(tagged, themes, args.min_mentions)
    trends = monthly_trends(tagged, themes)
    path = write_report(args.out, tagged, summary, metrics, trends, rating_distribution(tagged), args.min_mentions)
    print(f"Analysed {summary.rows_out} reviews. Report written to {path}")


if __name__ == "__main__":
    main()
