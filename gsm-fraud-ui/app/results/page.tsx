'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import ResultsTable from '@/components/ResultsTable';
import SummaryChart from '@/components/SummaryChart';
import LoadingSpinner from '@/components/LoadingSpinner';
import AlertMessage from '@/components/AlertMessage';
import { PredictionResult } from '@/types';

interface ResultsData {
  predictions: PredictionResult[];
  summary: {
    total: number;
    predicted_frauds: number;
    legit_count: number;
    avg_prob: number;
  };
}

export default function ResultsPage() {
  const [results, setResults] = useState<ResultsData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [note, setNote] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    // Try to get results from sessionStorage first
    const storedResults = sessionStorage.getItem('fraudDetectionResults');
    
    if (storedResults) {
      try {
        const parsedResults = JSON.parse(storedResults);
        // Transform the data to match our expected format
        if (parsedResults && typeof parsedResults === 'object') {
          // If it's the Flask response format, adapt it
          if (parsedResults.total !== undefined) {
            const adaptedResults: ResultsData = {
              predictions: (parsedResults.sample || []).map((r: any) => ({
                ...r,
                fraud_probability: Number(r.fraud_probability) || 0,
                predicted_fraud: Number(r.predicted_fraud) || 0,
              })),
              summary: {
                total: parsedResults.total || 0,
                predicted_frauds: parsedResults.predicted_frauds || 0,
                legit_count: parsedResults.legit_count || 0,
                avg_prob: parsedResults.avg_prob || 0,
              }
            };
            setResults(adaptedResults);
            if (parsedResults.note) setNote(parsedResults.note);
          } else {
            setResults(parsedResults);
          }
        }
      } catch (err) {
        console.error('Error parsing stored results:', err);
        setError('Error loading results data');
      }
    } else {
      setError('No results found. Please upload a file first.');
    }
    
    setIsLoading(false);
  }, []);

  const handleNewUpload = () => {
    sessionStorage.removeItem('fraudDetectionResults');
    router.push('/upload');
  };

  if (isLoading) {
    return <LoadingSpinner text="Loading results..." />;
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto">
        <AlertMessage type="error" message={error} />
        <div className="text-center mt-8">
          <button onClick={handleNewUpload} className="btn-primary">
            Upload New File
          </button>
        </div>
      </div>
    );
  }

  if (!results) {
    return (
      <div className="max-w-4xl mx-auto text-center">
        <div className="card">
          <div className="text-gray-500">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-lg font-medium mb-2">No Results Available</h3>
            <p className="text-sm mb-6">Upload a CSV file to see fraud detection results</p>
            <button onClick={handleNewUpload} className="btn-primary">
              Upload File
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Fraud Detection Results
          </h1>
          <p className="text-gray-600">
            Analysis complete - Review the detected patterns and risk scores below
          </p>
          {note && (
            <div className="mt-3">
              <div className="inline-block bg-yellow-50 border border-yellow-200 text-yellow-800 px-3 py-1 rounded">
                {note}
              </div>
            </div>
          )}
        </div>
        <button onClick={handleNewUpload} className="btn-secondary">
          Upload New File
        </button>
      </div>

      <div className="space-y-8">
        {/* Summary Statistics */}
        <SummaryChart
          fraudCount={results.summary.predicted_frauds}
          legitimateCount={results.summary.legit_count}
          totalCount={results.summary.total}
        />

        {/* Quick Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="card text-center">
            <div className="text-2xl font-bold text-gray-900">
              {results.summary.total}
            </div>
            <div className="text-sm text-gray-600 font-medium">Total Records</div>
          </div>
          
          <div className="card text-center">
            <div className="text-2xl font-bold text-red-600">
              {results.summary.predicted_frauds}
            </div>
            <div className="text-sm text-gray-600 font-medium">Fraudulent</div>
            <div className="text-xs text-red-600">
              {results.summary.total > 0 
                ? ((results.summary.predicted_frauds / results.summary.total) * 100).toFixed(1)
                : '0'
              }%
            </div>
          </div>
          
          <div className="card text-center">
            <div className="text-2xl font-bold text-green-600">
              {results.summary.legit_count}
            </div>
            <div className="text-sm text-gray-600 font-medium">Legitimate</div>
            <div className="text-xs text-green-600">
              {results.summary.total > 0 
                ? ((results.summary.legit_count / results.summary.total) * 100).toFixed(1)
                : '0'
              }%
            </div>
          </div>
          
          <div className="card text-center">
            <div className="text-2xl font-bold text-blue-600">
              {(results.summary.avg_prob * 100).toFixed(1)}%
            </div>
            <div className="text-sm text-gray-600 font-medium">Avg Risk Score</div>
          </div>
        </div>

        {/* Results Table */}
        <ResultsTable 
          results={results.predictions || []} 
          isLoading={false}
        />

        {/* Additional Information */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              Detection Summary
            </h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span>Detection Threshold:</span>
                <span className="font-medium">50%</span>
              </div>
              <div className="flex justify-between">
                <span>High Risk (&gt;70%):</span>
                <span className="font-medium text-red-600">
                  {results.predictions ? 
                    results.predictions.filter(p => p.fraud_probability > 0.7).length : 0
                  }
                </span>
              </div>
              <div className="flex justify-between">
                <span>Medium Risk (30-70%):</span>
                <span className="font-medium text-yellow-600">
                  {results.predictions ? 
                    results.predictions.filter(p => p.fraud_probability >= 0.3 && p.fraud_probability <= 0.7).length : 0
                  }
                </span>
              </div>
              <div className="flex justify-between">
                <span>Low Risk (&lt;30%):</span>
                <span className="font-medium text-green-600">
                  {results.predictions ? 
                    results.predictions.filter(p => p.fraud_probability < 0.3).length : 0
                  }
                </span>
              </div>
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              Next Steps
            </h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li className="flex items-start">
                <span className="text-red-500 mr-2">•</span>
                Review high-risk subscribers for manual verification
              </li>
              <li className="flex items-start">
                <span className="text-yellow-500 mr-2">•</span>
                Monitor medium-risk accounts for suspicious activity
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">•</span>
                Low-risk subscribers can proceed normally
              </li>
              <li className="flex items-start">
                <span className="text-blue-500 mr-2">•</span>
                Export results for further analysis or reporting
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}