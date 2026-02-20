// Mock data for testing the frontend without backend
export const mockPredictionResults = [
  {
    subscriber_id: "SUB001",
    IMEI: "356938035643809",
    registration_date: "2024-01-15",
    location: "New York",
    initial_call_count: 25,
    average_call_duration: 180,
    device_switch_count: 1,
    fraud_probability: 0.15,
    predicted_fraud: 0,
    classification: "Legitimate" as const,
  },
  {
    subscriber_id: "SUB002", 
    IMEI: "356938035643810",
    registration_date: "2024-01-16",
    location: "Los Angeles",
    initial_call_count: 3,
    average_call_duration: 45,
    device_switch_count: 5,
    fraud_probability: 0.85,
    predicted_fraud: 1,
    classification: "Fraud" as const,
  },
  {
    subscriber_id: "SUB003",
    IMEI: "356938035643811", 
    registration_date: "2024-01-17",
    location: "Chicago",
    initial_call_count: 15,
    average_call_duration: 120,
    device_switch_count: 2,
    fraud_probability: 0.35,
    predicted_fraud: 0,
    classification: "Legitimate" as const,
  },
  {
    subscriber_id: "SUB004",
    IMEI: "356938035643812",
    registration_date: "2024-01-18", 
    location: "Miami",
    initial_call_count: 2,
    average_call_duration: 30,
    device_switch_count: 8,
    fraud_probability: 0.92,
    predicted_fraud: 1,
    classification: "Fraud" as const,
  },
  {
    subscriber_id: "SUB005",
    IMEI: "356938035643813",
    registration_date: "2024-01-19",
    location: "Seattle", 
    initial_call_count: 20,
    average_call_duration: 200,
    device_switch_count: 0,
    fraud_probability: 0.08,
    predicted_fraud: 0,
    classification: "Legitimate" as const,
  }
];

export const mockSummary = {
  total: 5,
  predicted_frauds: 2,
  legit_count: 3,
  avg_prob: 0.47
};

export const mockResponse = {
  predictions: mockPredictionResults,
  summary: mockSummary
};