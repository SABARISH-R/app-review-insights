"""Load and clean a reviews CSV with configurable column names."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class CleaningSummary:
    rows_in: int
    rows_out: int
    dropped_missing: int
    dropped_bad_rating: int
    dropped_duplicates: int


def load_reviews(
    path: str | Path,
    text_col: str = "review",
    rating_col: str = "rating",
    date_col: str | None = "date",
) -> tuple[pd.DataFrame, CleaningSummary]:
    raw = pd.read_csv(path)
    missing = [c for c in (text_col, rating_col) if c not in raw.columns]
    if missing:
        raise ValueError(f"Columns not found in CSV: {missing}. Available: {list(raw.columns)}")

    df = pd.DataFrame({
        "text": raw[text_col].astype("string"),
        "rating": pd.to_numeric(raw[rating_col], errors="coerce"),
    })
    if date_col and date_col in raw.columns:
        df["date"] = pd.to_datetime(raw[date_col], errors="coerce")
    else:
        df["date"] = pd.NaT

    n_in = len(df)
    df["text"] = df["text"].str.strip()
    before = len(df)
    df = df.dropna(subset=["text", "rating"])
    df = df[df["text"] != ""]
    dropped_missing = before - len(df)

    before = len(df)
    df = df[df["rating"].between(1, 5)]
    dropped_bad_rating = before - len(df)

    before = len(df)
    df = df.drop_duplicates(subset=["text", "rating", "date"])
    dropped_dupes = before - len(df)

    df = df.reset_index(drop=True)
    df["rating"] = df["rating"].astype(float)
    return df, CleaningSummary(n_in, len(df), dropped_missing, dropped_bad_rating, dropped_dupes)
