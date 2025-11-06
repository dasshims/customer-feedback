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
