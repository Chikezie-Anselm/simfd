export interface Subscriber {
  subscriber_id: string;
  subscriber_type?: string;
  IMEI: string;
  registration_date: string;
  age: number;
  income: number;
  location: string;
  initial_call_count?: number;
  average_call_duration?: number;
  device_switch_count: number;
  is_fraud?: number;
}

export interface PredictionResult extends Subscriber {
  fraud_probability: number;
  predicted_fraud: number;
  classification: 'Fraud' | 'Legitimate';
  classification_badge?: string;
  fraud_probability_pct?: string;
}

export interface ApiResponse {
  success: boolean;
  message?: string;
  data?: {
    predictions: PredictionResult[];
    summary: {
      total: number;
      predicted_frauds: number;
      legit_count: number;
      avg_prob: number;
    };
  };
  error?: string;
}

export interface UploadResponse {
  table_html?: string;
  total: number;
  avg_prob: number;
  predicted_frauds: number;
  legit_count: number;
  results_file: string;
}

export interface ChartData {
  labels: string[];
  datasets: {
    data: number[];
    backgroundColor: string[];
    borderColor?: string[];
    borderWidth?: number;
  }[];
}