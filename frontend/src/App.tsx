import { useCallback, useState } from "react";
import FileUpload from "./components/FileUpload";
import ResultsPanel from "./components/ResultsPanel";
import { AnalyzeResponse } from "./types";

const API_URL = import.meta.env.VITE_API_BASE_URL
  ? `${import.meta.env.VITE_API_BASE_URL}/analyze`
  : "http://localhost:8000/analyze";

function App() {
  const [results, setResults] = useState<AnalyzeResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = useCallback(async (file: File) => {
    setIsLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(API_URL, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const detail = await response
          .json()
          .catch(() => ({ detail: "Unknown error" }));
        throw new Error(
          detail?.detail || "Failed to analyze feedback. Please try again."
        );
      }

      const payload = (await response.json()) as AnalyzeResponse;
      setResults(payload);
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "Failed to analyze feedback. Please try again.";
      setError(message);
      setResults(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  return (
    <div className="app-shell">
      <h1 className="app-title">Customer Feedback Sentiment Reporter</h1>
      <p className="app-subtitle">
        Upload a CSV of customer feedback to uncover sentiment trends, key
        themes, and the top two improvement opportunities.
      </p>

      <section className="section-card">
        <FileUpload onSubmit={handleSubmit} isLoading={isLoading} />

        {isLoading && (
          <p className="loading" role="status">
            ⏳ Analyzing feedback...
          </p>
        )}
      </section>

      {error && (
        <div className="error-banner" role="alert">
          {error}
        </div>
      )}

      {results && !error && (
        <ResultsPanel results={results} onReset={() => setResults(null)} />
      )}
    </div>
  );
}

export default App;
