import io
import json
from typing import Dict, List, Tuple

import pandas as pd

EXPECTED_COLUMNS = ["feedback_id", "text", "rating"]
SENTIMENT_ORDER = ["positive", "neutral", "negative"]


def read_feedback_csv(file_bytes: bytes) -> pd.DataFrame:
    """
    Load the uploaded CSV into a pandas DataFrame and validate its structure.
    Raises ValueError with a human-friendly message on invalid input.
    """
    try:
        dataframe = pd.read_csv(io.BytesIO(file_bytes))
    except Exception as exc:  # pragma: no cover - pandas will raise varied exceptions
        raise ValueError("Unable to parse CSV file. Ensure it is a valid CSV.") from exc

    missing_columns = [col for col in EXPECTED_COLUMNS if col not in dataframe.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}.")

    # Coerce ratings to numeric values and validate that none are missing.
    dataframe["rating"] = pd.to_numeric(dataframe["rating"], errors="coerce")
    if dataframe["rating"].isna().any():
        raise ValueError("Column 'rating' contains non-numeric values.")

    dataframe["text"] = dataframe["text"].astype(str).str.strip()
    if dataframe["text"].eq("").any():
        raise ValueError("Column 'text' contains empty entries.")

    return dataframe


def categorize_sentiment(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Annotate the dataframe with sentiment labels based on rating thresholds.
    Positive: rating >= 4, Neutral: rating == 3, Negative: rating < 3.
    """
    def label_row(rating: float) -> str:
        if rating >= 4:
            return "positive"
        if rating == 3:
            return "neutral"
        return "negative"

    dataframe = dataframe.copy()
    dataframe["sentiment"] = dataframe["rating"].apply(label_row)
    return dataframe


def compute_sentiment_stats(dataframe: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Generate counts and percentages per sentiment bucket.
    """
    total = len(dataframe.index)
    sentiment_counts = dataframe["sentiment"].value_counts().to_dict()

    stats = {}
    for sentiment in SENTIMENT_ORDER:
        count = int(sentiment_counts.get(sentiment, 0))
        percent = round((count / total) * 100, 2) if total else 0.0
        stats[sentiment] = {"count": count, "percent": percent}
    return stats


def collect_sample_comments(
    dataframe: pd.DataFrame, limit: int = 3
) -> Dict[str, List[str]]:
    """
    Collect up to `limit` sample comments for each sentiment label.
    """
    samples: Dict[str, List[str]] = {}
    for sentiment in SENTIMENT_ORDER:
        sample_series = (
            dataframe.loc[dataframe["sentiment"] == sentiment, "text"]
            .dropna()
            .head(limit)
        )
        samples[sentiment] = sample_series.tolist()
    return samples


def build_prompt_payload(
    stats: Dict[str, Dict[str, float]], samples: Dict[str, List[str]]
) -> str:
    """
    Construct the user prompt supplied to the language model.
    """
    stat_summary = ", ".join(
        f"{details['percent']}% {name}" for name, details in stats.items()
    )

    sample_blocks = []
    for sentiment, comments in samples.items():
        if comments:
            block = f"{sentiment.title()} samples:\n- " + "\n- ".join(comments)
        else:
            block = f"{sentiment.title()} samples:\n- None provided"
        sample_blocks.append(block)

    prompt = (
        f"Sentiment distribution: {stat_summary}.\n\n"
        "Sample customer comments:\n"
        + "\n\n".join(sample_blocks)
        + "\n\n"
        "Summarize the key customer sentiment themes and recommend exactly two "
        "product improvement actions. Respond as JSON with the following keys:\n"
        '{"summary": "<string>", "improvement_suggestions": ["<string>", "<string>"]}'
    )
    return prompt


def parse_model_response(content: str) -> Tuple[str, List[str]]:
    """
    Parse the JSON response from the language model.
    Falls back to a minimal best-effort extraction if parsing fails.
    """
    try:
        payload = json.loads(content)
        summary = str(payload.get("summary", "")).strip()
        suggestions = payload.get("improvement_suggestions", [])
        if not isinstance(suggestions, list):
            raise TypeError("improvement_suggestions must be a list.")
        suggestions = [str(item).strip() for item in suggestions if str(item).strip()]
        return summary, suggestions
    except (json.JSONDecodeError, TypeError, ValueError):
        cleaned_lines = [line.strip("-• ").strip() for line in content.splitlines()]
        cleaned_lines = [line for line in cleaned_lines if line]
        summary = cleaned_lines[0] if cleaned_lines else ""
        suggestions = cleaned_lines[1:3] if len(cleaned_lines) > 1 else []
        return summary, suggestions
