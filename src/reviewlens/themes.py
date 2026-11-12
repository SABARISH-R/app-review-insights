"""Keyword-based theme tagging. Themes are editable in themes.json."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

DEFAULT_THEMES = Path(__file__).with_name("themes.json")


def load_theme_patterns(path: str | Path = DEFAULT_THEMES) -> dict[str, re.Pattern]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return {name: re.compile("|".join(pats), re.IGNORECASE) for name, pats in raw.items()}


def tag_themes(df: pd.DataFrame, patterns: dict[str, re.Pattern]) -> pd.DataFrame:
    """Return a copy of df with one boolean column per theme."""
    out = df.copy()
    for name, pattern in patterns.items():
        out[name] = out["text"].str.contains(pattern, na=False)
    return out
