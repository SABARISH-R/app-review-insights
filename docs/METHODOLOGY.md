# Methodology

## Data cleaning
Rows are dropped if the text or rating is missing, if the rating is outside 1-5, or if the (text, rating, date) combination is an exact duplicate. The report states how many rows were dropped for each reason so the analysis is auditable.

## Theme tagging
Each theme is a list of regular expressions in `src/reviewlens/themes.json`. A review mentions a theme if any pattern matches (case-insensitive). A review can mention several themes. Edit the file to add themes or refine keywords for your product.

## Metrics per theme
| Metric | Definition |
|---|---|
| mentions | Reviews matching the theme |
| share_of_reviews | mentions / all reviews |
| share_of_low_rated | Share of all 1-2 star reviews that mention the theme |
| avg_rating_when_mentioned | Mean rating of reviews mentioning the theme |
| rating_gap | Overall mean rating minus avg_rating_when_mentioned |
| impact | share_of_reviews x rating_gap |
| reliable | mentions >= `--min-mentions` (default 30) |

Impact is a prioritisation heuristic, not a causal estimate. A crash that appears in 5% of reviews and drags those reviews 2 points below average scores 0.10.

## Limitations
1. **Keyword matching** misses paraphrases and sarcasm and can match unrelated uses of a word. Validate precision on a hand-labelled sample before trusting a ranking.
2. **Praise vs complaint:** "great design" and "confusing design" both match ui_ux. Read the rating gap: a negative gap means the theme appears mostly in happy reviews.
3. **Selection bias:** people who review are not typical users. Do not generalise to all users.
4. **Correlation, not causation:** low ratings that mention a theme do not prove the theme caused the rating.
5. **Small counts:** themes below the minimum mention count are flagged unreliable.

## Suggested validation
Hand-label 100 random reviews for each of your top 3 themes, compute precision (labelled correct / tagged) and recall on a separate sample, and report both in your write-up.
