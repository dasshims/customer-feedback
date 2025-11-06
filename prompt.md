## 🧠 **Prompt: FastAPI Backend — Customer Feedback Sentiment Reporter (MVP)**

You are an expert full-stack engineer.
Build the **backend FastAPI server** for the following app end-to-end with clean, production-ready code, clear comments, and a minimal but complete repo structure.

---

### **App Name**

Customer Feedback Sentiment Reporter (MVP)

---

### **Goal**

Read a CSV file containing customer feedback `(feedback_id, text, rating)`, compute positive/neutral/negative sentiment counts, and call **OpenAI Chat Completions API** to generate a summary of key themes and two improvement recommendations — all computed **in-memory** (no DB storage).

---

### **Backend Requirements**

#### 1. **Tech Stack**

* Python 3.11
* FastAPI
* Uvicorn
* Pandas
* Python-dotenv
* Official `openai` Python library (use Chat Completions endpoint)
* Pydantic for response models
* python-multipart for file upload handling

#### 2. **Endpoints**

* `POST /analyze`

  * Accepts a CSV file upload (`multipart/form-data`).
  * Reads the file in-memory using Pandas.
  * Validates consistent format (`feedback_id,text,rating`).
  * Categorizes sentiment:

    * Positive ≥ 4
    * Neutral = 3
    * Negative < 3
  * Computes counts & percentages for each category.
  * Selects 2–3 sample comments per category.
  * Calls the **OpenAI Chat Completions API** with a formatted prompt such as:

    ```
    Given 50% positive, 25% neutral, 25% negative feedback,
    summarize key themes from the following sample comments
    and recommend two product improvement actions.
    ```
  * Returns JSON response:

    ```json
    {
      "summary": "AI-generated summary text...",
      "improvement_suggestions": ["...", "..."],
      "sentiment_stats": {
        "positive": {"count": X, "percent": Y},
        "neutral": {...},
        "negative": {...}
      }
    }
    ```

#### 3. **Environment & Configuration**

* Load the OpenAI API key from a `.env` file using `python-dotenv`.
* Use the official `openai.chat.completions.create` method (not Responses API).
* Enable CORS for localhost frontend testing.

#### 4. **Repo Structure**

```
/feedback-sentiment-reporter
│
├── main.py                # FastAPI app with /analyze endpoint
├── requirements.txt       # all dependencies
├── .env.example           # example of required environment variables
├── README.md              # setup & run instructions
└── utils/
    └── sentiment_utils.py # helper functions for parsing & sentiment logic
```

#### 5. **README.md should include**

* Setup instructions

  ```
  pip install -r requirements.txt
  ```
* Running locally

  ```
  uvicorn main:app --reload
  ```
* Example curl test:

  ```
  curl -X POST -F "file=@feedback.csv" http://localhost:8000/analyze
  ```
* Example JSON output

---

### **Implementation Guidelines**

* Keep the code modular and commented.
* Handle common errors gracefully (missing columns, bad data types, invalid CSV).
* No persistence — everything runs in memory.
* Return clean, structured JSON responses.
* Ensure CORS is enabled for the upcoming frontend phase.

---

### **Final Output**

Generate:

1. `main.py`
2. `requirements.txt`
3. `.env.example`
4. `utils/sentiment_utils.py`
5. `README.md`

All files should be self-contained and runnable locally.


### Prompt Phase 2

## 🧠 Prompt: Frontend UI (Phase 2) — Customer Feedback Sentiment Reporter (MVP)

You are an expert frontend engineer.
Build the **frontend UI** for the app described below, assuming the backend FastAPI server already exists.

---

### App Name

Customer Feedback Sentiment Reporter (MVP)

---

### Context (Backend Already Implemented)

Assume there is a running **FastAPI backend** with this endpoint:

* `POST http://localhost:8000/analyze`

  * Accepts `multipart/form-data` with a CSV file field named `file`.
  * Returns JSON in this shape:

    ```json
    {
      "summary": "AI-generated summary text...",
      "improvement_suggestions": ["Suggestion 1", "Suggestion 2"],
      "sentiment_stats": {
        "positive": { "count": 10, "percent": 50.0 },
        "neutral":  { "count": 5,  "percent": 25.0 },
        "negative": { "count": 5,  "percent": 25.0 }
      }
    }
    ```

The backend:

* Reads CSV with columns: `feedback_id,text,rating`
* Computes sentiment based on `rating` (>=4 positive, 3 neutral, <3 negative)
* Calls **OpenAI Chat Completions API** using the official Python `openai` library.
* Uses `.env` + `python-dotenv` for secrets.
* Frontend must **not** talk to OpenAI directly — only to the backend REST API.

---

### Goal of the Frontend

Create a **simple, clean single-page web UI** that allows a user to:

1. Upload a CSV file of feedback (`feedback_id,text,rating`).
2. Send it to `POST /analyze` on the backend.
3. Display:

   * Sentiment stats (counts + percentages for positive/neutral/negative).
   * AI-generated **summary**.
   * The top **two improvement suggestions** as a list.

This is an MVP, so prioritize clarity and UX over visual fanciness.

---

### Tech Stack (Frontend)

Use the following stack:

* **Node.js** (for tooling)
* **React 18 + Vite**
* **TypeScript**
* Optional minimal styling with CSS or simple utility classes (no need for a full design system).

Do **not** integrate any OpenAI SDK in the frontend.

---

### Frontend Requirements

#### 1. Project Structure

Create the frontend in a `frontend/` directory inside the project root:

```
/feedback-sentiment-reporter
│
├── main.py               # (already exists, backend)
├── requirements.txt
├── .env.example
├── README.md             # root README
└── frontend/
    ├── index.html
    ├── package.json
    ├── tsconfig.json
    ├── vite.config.ts
    ├── src/
    │   ├── main.tsx
    │   ├── App.tsx
    │   ├── components/
    │   │   ├── FileUpload.tsx
    │   │   └── ResultsPanel.tsx
    │   └── types.ts
    └── README.md         # frontend-specific instructions
```

You can adjust internal file names as needed, but keep a clean, modular structure.

---

#### 2. UI Behavior

**Main layout (App.tsx):**

* A centered container with:

  * App title: `Customer Feedback Sentiment Reporter`
  * Short subtitle describing what the app does.
  * A card/section containing:

    * File upload + “Analyze Feedback” button.
    * Loading state while request is in progress.
    * Error message area (for network/server/validation errors).
    * Results section that appears after a successful response.

**File Upload Flow:**

* `FileUpload` component:

  * Contains:

    * `<input type="file" accept=".csv" />`
    * “Analyze Feedback” button.
  * Validations:

    * Require a file to be selected before enabling the button.
    * Only allow `.csv` files.
  * On submit:

    * Use `FormData` and `fetch` POST to `http://localhost:8000/analyze`.
    * Handle async/await and error cases.
    * Expose success/error callbacks up to `App` via props.

**Loading & Error States:**

* While waiting for backend:

  * Disable the upload button.
  * Show a simple "Analyzing feedback..." loading indicator.
* If an error occurs:

  * Display a clear error message (e.g., “Failed to analyze feedback. Please check the CSV format and try again.”).
  * Allow user to retry.

---

#### 3. Results Display

When the backend responds successfully, show a **ResultsPanel** with:

* **Sentiment Stats Section**

  * Show positive/neutral/negative counts and percents in a neat layout, e.g.:

    | Sentiment | Count | Percent |
    | --------- | ----- | ------- |
    | Positive  | 10    | 50%     |
    | Neutral   | 5     | 25%     |
    | Negative  | 5     | 25%     |

  * Use data from `sentiment_stats` in the response.

  * Optional: small bar visualization using plain CSS (no heavy chart library required).

* **AI Summary Section**

  * Heading: “Summary of Key Themes”
  * Show the `summary` text from the backend.

* **Improvement Suggestions Section**

  * Heading: “Top 2 Improvement Suggestions”
  * Render `improvement_suggestions` as a bullet list.

The UI should update dynamically whenever a new file is analyzed.

---

#### 4. Types & API Layer

* Create a `types.ts` file for TypeScript interfaces, such as:

  ```ts
  export interface SentimentBucket {
    count: number;
    percent: number;
  }

  export interface SentimentStats {
    positive: SentimentBucket;
    neutral: SentimentBucket;
    negative: SentimentBucket;
  }

  export interface AnalyzeResponse {
    summary: string;
    improvement_suggestions: string[];
    sentiment_stats: SentimentStats;
  }
  ```
* Use these types in your React components for strong typing.
* Keep the fetch logic in a small helper or inside `App.tsx`.

---

#### 5. Environment Configuration

* For simplicity, hardcode the backend URL as `http://localhost:8000/analyze` in the frontend, **or** expose it via a Vite env variable like `VITE_API_BASE_URL`.
* If you use env vars:

  * Add an example to `frontend/README.md` (e.g., `.env` with `VITE_API_BASE_URL=http://localhost:8000`).

---

#### 6. Frontend README

Create `frontend/README.md` with:

* Prerequisites:

  * Node.js + npm or pnpm
* Setup:

  ```bash
  cd frontend
  npm install
  ```
* Run dev server:

  ```bash
  npm run dev
  ```
* Note that the backend must also be running:

  ```bash
  uvicorn main:app --reload
  ```
* Explain how to:

  * Upload `feedback.csv`
  * Interpret the displayed results.

---

### Implementation Style

* Use functional React components and hooks (`useState`, `useEffect` where needed).
* Keep components small, focused, and well-commented.
* Prioritize a clean UX:

  * Clearly labeled sections.
  * Good spacing and readable fonts.
* No need for routing — single-page experience is fine.

---

### Final Output

Generate **all necessary frontend files** under the `frontend/` directory:

1. `package.json`
2. `tsconfig.json`
3. `vite.config.ts`
4. `index.html`
5. `src/main.tsx`
6. `src/App.tsx`
7. `src/components/FileUpload.tsx`
8. `src/components/ResultsPanel.tsx`
9. `src/types.ts`
10. `frontend/README.md`
11. Any minimal CSS files if needed.

All code should be complete, runnable, and wired together so that:

* Running `npm install && npm run dev` in `frontend/`
* And running the FastAPI backend on `http://localhost:8000`
* Produces a working end-to-end **Customer Feedback Sentiment Reporter** UI.