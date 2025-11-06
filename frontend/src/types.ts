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
