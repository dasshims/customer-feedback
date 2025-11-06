# Customer Feedback Sentiment Reporter — Frontend

React + Vite single-page application that uploads customer feedback CSV files to the FastAPI backend and visualizes sentiment insights.

## Prerequisites

- Node.js 18+
- npm (bundled with Node) or pnpm/yarn if preferred

## Setup

```bash
cd frontend
npm install
```

Optionally copy `.env.example` to `.env` and set the backend base URL:

```bash
VITE_API_BASE_URL=http://localhost:8000
```

If omitted, the app defaults to `http://localhost:8000`.

## Running the Dev Server

Start the backend in another terminal:

```bash
uvicorn main:app --reload
```

Then launch the frontend:

```bash
npm run dev
```

Visit the printed URL (default `http://localhost:5173`).

## Using the App

1. Prepare a CSV with columns `feedback_id,text,rating` (see `data/` directory for a sample).
2. Click **Select feedback CSV file** and choose your file.
3. Press **Analyze Feedback** to upload and run the analysis.
4. Review the sentiment breakdown, AI-generated summary, and the top two improvement suggestions that appear after the request completes.

## Building for Production

```bash
npm run build
```

This emits the production bundle in `frontend/dist`. Use `npm run preview` to locally inspect the built output.
