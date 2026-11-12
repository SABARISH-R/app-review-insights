"""Pain-point scoring. See docs/METHODOLOGY.md for definitions and limitations."""
from __future__ import annotations

import pandas as pd


def theme_metrics(df: pd.DataFrame, themes: list[str], min_mentions: int = 30) -> pd.DataFrame:
    """Rank themes by estimated rating impact.

    impact = share_of_reviews * (overall_avg_rating - avg_rating_when_mentioned)
    i.e. roughly how many rating points the average review loses because of the theme.
    """
    total = len(df)
    overall = df["rating"].mean()
    low = df["rating"] <= 2
    n_low = int(low.sum())
    rows = []
    for theme in themes:
        mask = df[theme]
        n = int(mask.sum())
        if n == 0:
            continue
        avg = df.loc[mask, "rating"].mean()
        rows.append({
            "theme": theme,
            "mentions": n,
            "share_of_reviews": n / total,
            "share_of_low_rated": (int((mask & low).sum()) / n_low) if n_low else 0.0,
            "avg_rating_when_mentioned": avg,
            "rating_gap": overall - avg,
            "impact": (n / total) * (overall - avg),
            "reliable": n >= min_mentions,
        })
    cols = ["theme", "mentions", "share_of_reviews", "share_of_low_rated",
            "avg_rating_when_mentioned", "rating_gap", "impact", "reliable"]
    out = pd.DataFrame(rows, columns=cols)
    return out.sort_values("impact", ascending=False).reset_index(drop=True)


def monthly_trends(df: pd.DataFrame, themes: list[str]) -> pd.DataFrame:
    """Monthly review volume, average rating, and share of reviews mentioning each theme."""
    dated = df.dropna(subset=["date"]).copy()
    if dated.empty:
        return pd.DataFrame()
    dated["month"] = dated["date"].dt.to_period("M").dt.to_timestamp()
    grouped = dated.groupby("month")
    out = pd.DataFrame({
        "reviews": grouped.size(),
        "avg_rating": grouped["rating"].mean(),
    })
    for theme in themes:
        out[f"{theme}_share"] = grouped[theme].mean()
    return out.reset_index()


def rating_distribution(df: pd.DataFrame) -> pd.Series:
    return df["rating"].round().astype(int).value_counts().reindex(range(1, 6), fill_value=0).sort_index()
