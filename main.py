import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel, Field

from utils.sentiment_utils import (
    build_prompt_payload,
    categorize_sentiment,
    collect_sample_comments,
    compute_sentiment_stats,
    parse_model_response,
    read_feedback_csv,
)

# Load environment variables from .env if present.
load_dotenv()

app = FastAPI(title="Customer Feedback Sentiment Reporter", version="0.1.0")

# Allow local development origins by default.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


class SentimentDetail(BaseModel):
    count: int = Field(..., ge=0)
    percent: float = Field(..., ge=0)


class SentimentStats(BaseModel):
    positive: SentimentDetail
    neutral: SentimentDetail
    negative: SentimentDetail


class AnalysisResponse(BaseModel):
    summary: str
    improvement_suggestions: List[str]
    sentiment_stats: SentimentStats


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_feedback(file: UploadFile = File(...)) -> AnalysisResponse:
    """
    Analyze uploaded CSV feedback, compute sentiment statistics, and
    request AI-generated summaries and improvement suggestions.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    if file.content_type not in {"text/csv", "application/vnd.ms-excel"}:
        raise HTTPException(status_code=400, detail="Unsupported file type. Upload a CSV.")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        dataframe = read_feedback_csv(file_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    dataframe = categorize_sentiment(dataframe)
    stats = compute_sentiment_stats(dataframe)
    samples = collect_sample_comments(dataframe)

    prompt = build_prompt_payload(stats, samples)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an assistant that distills customer feedback into concise "
                        "product insights and actionable improvements."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )
    except Exception as exc:  # pragma: no cover - network/IO errors vary
        raise HTTPException(
            status_code=502,
            detail="Failed to generate summary from language model.",
        ) from exc

    choice = response.choices[0].message.content if response.choices else ""
    summary, suggestions = parse_model_response(choice or "")

    if len(suggestions) < 2:
        raise HTTPException(
            status_code=502,
            detail="Language model did not return the expected suggestions.",
        )

    return AnalysisResponse(
        summary=summary,
        improvement_suggestions=suggestions[:2],
        sentiment_stats=SentimentStats(**stats),
    )


@app.get("/health")
async def health_check() -> dict:
    """Simple health check endpoint useful for uptime monitoring."""
    return {"status": "ok"}
