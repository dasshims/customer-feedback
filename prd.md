# **Product Requirements Document (PRD)**

## **Project Name:** Customer Feedback Sentiment Reporter (MVP)

---

### **Project Overview**

The **Customer Feedback Sentiment Reporter** is an AI-powered analytics tool that processes a CSV of customer feedback, categorizes sentiments (positive, neutral, negative) based on numeric ratings, and uses the **OpenAI Chat Completions API** to generate a concise summary of key themes and top improvement suggestions.

The app is designed as a lightweight MVP that works entirely **in-memory** (no database persistence) and runs as a **FastAPI backend** with a minimal **frontend dashboard** (optional) built in Node.js or any JS framework like Vite + React.

The goal is to help product teams and customer-success managers quickly identify sentiment trends and actionable insights from raw feedback without setting up complex data pipelines or analytics stacks.

---

### **Level:**

MVP

### **Type of Project:**

AI Development, Sentiment Analytics, Feedback Summarization

---

### **Skills Required**

1. **Python CSV & Metrics Data Processing** — read and process structured CSV data in real-time.
2. **OpenAI Chat Completions API (official `openai` library)** — generate summaries and improvement recommendations from sentiment data.
3. **UI Development (Node.js or React/Vite)** — simple interface for file upload and displaying summary statistics and AI-generated insights.

---

### **Key Features**

#### 1. **CSV File Upload and Parsing**

* Accepts a CSV file in the format:

  ```
  feedback_id,text,rating
  1,"Love the interface, but app crashes sometimes.",4
  2,"Very slow response time and confusing error messages.",2
  3,"Smooth login and dashboard experience.",5
  ```
* Reads the file on the fly (no database storage).
* Validates consistent format and basic schema integrity.

#### 2. **Sentiment Categorization**

* Computes sentiment categories directly from ratings:

  * **Positive:** rating ≥ 4
  * **Neutral:** rating = 3
  * **Negative:** rating < 3
* Returns aggregate counts and percentages (e.g., 50% positive, 25% neutral, 25% negative).

#### 3. **AI-Generated Insights**

* Sends a formatted prompt to the **OpenAI Chat Completions API** (using `openai` Python library) such as:

  ```
  Given 50% positive, 25% neutral, 25% negative feedback, summarize key themes from the following sample comments and recommend two product improvement actions.
  ```
* Uses a small set of representative feedback snippets for context (e.g., 2–3 per category).
* Displays returned summary and recommendations in readable text format.

#### 4. **Simple Interactive UI**

* Single-page app (React/Vite or minimal HTML form) to:

  * Upload CSV file
  * View sentiment counts/percentages
  * Display AI summary & improvement suggestions

#### 5. **Lightweight Deployment**

* Backend: **FastAPI** with `/analyze` endpoint (accepts file upload, returns JSON results).
* Frontend: minimal UI consuming the API.
* Configurable OpenAI API key loaded securely via `.env` using **python-dotenv**.

---

### **End Users**

1. **Product Managers** – to identify patterns and user sentiment for roadmap prioritization.
2. **Customer Success Teams** – to quickly summarize client feedback before stakeholder reviews.
3. **UX Researchers** – to track user satisfaction and spot recurring pain points.
4. **Startup Founders / Analysts** – to get lightweight sentiment intelligence without full-blown analytics tooling.

---

### **Technical Guidelines**

1. **Use the official `openai` Python package** — avoid direct REST API calls.
2. **Use `Chat Completions` endpoint**, *not* the newer `Responses` API.
3. **Store OpenAI API key in `.env` file** and load via `dotenv`.
4. **Add `README.md`** including:

   * Setup instructions (`pip install -r requirements.txt`)
   * Running local FastAPI server (`uvicorn main:app --reload`)
   * Example CSV input and output
   * Optional frontend setup and usage

---

### **Success Criteria**

* The app correctly categorizes sentiment based on ratings.
* AI summary meaningfully reflects the tone of user feedback.
* All processing is done in-memory (no persistence layer).
* The system runs locally with minimal dependencies.
