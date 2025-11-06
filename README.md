# Customer Feedback Sentiment Reporter (MVP)

Backend FastAPI service that ingests customer feedback CSV files, computes sentiment metrics, and generates AI-assisted summaries with improvement recommendations.

## Prerequisites

- Python 3.11
- An OpenAI API key with access to Chat Completions models

## Setup

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example` and add your OpenAI credentials.

## Running Locally

```bash
source .venv/bin/activate
uvicorn main:app --reload
```

Once running, the API is available at `http://localhost:8000`.

## Endpoint

- `POST /analyze` — Upload a CSV file with columns `feedback_id,text,rating` to receive sentiment statistics and AI-generated insights.

## Example Request

```bash
curl -X POST -F "file=@feedback.csv" http://localhost:8000/analyze
```

## Example Response

```json
{
  "summary": "Customers appreciate the intuitive design but want better reporting features.",
  "improvement_suggestions": [
    "Prioritize enhancing analytics dashboards for deeper insights.",
    "Improve in-app guidance to shorten the onboarding learning curve."
  ],
  "sentiment_stats": {
    "positive": {"count": 42, "percent": 58.33},
    "neutral": {"count": 18, "percent": 25.0},
    "negative": {"count": 12, "percent": 16.67}
  }
}
```

## Health Check

`GET /health` returns `{ "status": "ok" }` for uptime monitoring.
