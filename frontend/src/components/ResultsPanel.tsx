import { AnalyzeResponse } from "../types";

interface ResultsPanelProps {
  results: AnalyzeResponse;
  onReset: () => void;
}

const sentimentStyles: Record<string, string> = {
  positive: "sentiment-positive",
  neutral: "sentiment-neutral",
  negative: "sentiment-negative",
};

function ResultsPanel({ results, onReset }: ResultsPanelProps) {
  const { sentiment_stats, summary, improvement_suggestions } = results;

  return (
    <section aria-live="polite">
      <div className="section-card">
        <header style={{ display: "flex", justifyContent: "space-between" }}>
          <h2 style={{ margin: 0 }}>Sentiment Breakdown</h2>
          <button
            type="button"
            className="button"
            onClick={onReset}
            style={{ paddingInline: "1rem", fontSize: "0.9rem" }}
          >
            Analyze Another File
          </button>
        </header>

        <div className="results-grid" style={{ marginTop: "1.5rem" }}>
          {(
            Object.entries(sentiment_stats) as Array<
              [keyof AnalyzeResponse["sentiment_stats"], { count: number; percent: number }]
            >
          ).map(([sentiment, data]) => (
            <article key={sentiment} className="results-card">
              <p className={`sentiment-label ${sentimentStyles[sentiment]}`}>
                {sentiment.charAt(0).toUpperCase() + sentiment.slice(1)}
              </p>
              <p style={{ margin: "0.25rem 0", fontSize: "1.5rem", fontWeight: 700 }}>
                {data.count}
              </p>
              <p style={{ margin: 0, color: "#4a5568", fontWeight: 500 }}>
                {data.percent.toFixed(2)}%
              </p>
            </article>
          ))}
        </div>
      </div>

      <article className="summary-card">
        <h2>Summary of Key Themes</h2>
        <p style={{ margin: 0, fontSize: "1.05rem", lineHeight: 1.6 }}>{summary}</p>
      </article>

      <article className="suggestions-card">
        <h2>Top 2 Improvement Suggestions</h2>
        <ul>
          {improvement_suggestions.map((suggestion, index) => (
            <li key={`${index}-${suggestion.substring(0, 16)}`}>{suggestion}</li>
          ))}
        </ul>
      </article>
    </section>
  );
}

export default ResultsPanel;
