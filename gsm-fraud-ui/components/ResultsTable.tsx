'use client';

import { PredictionResult } from '@/types';

interface ResultsTableProps {
  results: PredictionResult[];
  isLoading?: boolean;
}

const ResultsTable = ({ results, isLoading = false }: ResultsTableProps) => {
  if (isLoading) {
    return (
      <div className="card">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-300 rounded w-1/4 mb-4"></div>
          <div className="space-y-3">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="h-4 bg-gray-300 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (!results || results.length === 0) {
    return (
      <div className="card text-center py-8">
        <div className="text-gray-500">
          <div className="text-4xl mb-4">📊</div>
          <h3 className="text-lg font-medium mb-2">No Results Yet</h3>
          <p className="text-sm">Upload a CSV file to see fraud detection results</p>
        </div>
      </div>
    );
  }

  const formatProbability = (prob: number) => {
    return `${(prob * 100).toFixed(1)}%`;
  };

  const getBadgeClass = (classification: string) => {
    return classification === 'Fraud' ? 'badge-fraud' : 'badge-legitimate';
  };

  return (
    <div className="card">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900">
          Prediction Results
        </h3>
        <p className="text-sm text-gray-600">
          Showing {Math.min(results.length, 200)} of {results.length} results
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full table-auto">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Subscriber ID
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                IMEI
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Subscriber Type
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Registration Date
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Age
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Income
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Fraud Probability
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Classification
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Location
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Device Switches
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {results.slice(0, 200).map((result, index) => (
              <tr key={index} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-sm font-medium text-gray-900">
                  {result.subscriber_id}
                </td>
                <td className="px-4 py-3 text-sm text-gray-600 font-mono">
                  {result.IMEI}
                </td>
                <td className="px-4 py-3 text-sm text-gray-600">
                  {result.subscriber_type || '-'}
                </td>
                <td className="px-4 py-3 text-sm text-gray-600">
                  {result.registration_date || '-'}
                </td>
                <td className="px-4 py-3 text-sm text-gray-600">
                  {result.age ?? '-'}
                </td>
                <td className="px-4 py-3 text-sm text-gray-600">
                  {result.income ?? '-'}
                </td>
                <td className="px-4 py-3 text-sm text-gray-900">
                  <div className="flex items-center">
                    <span className="font-medium">
                      {formatProbability(result.fraud_probability)}
                    </span>
                    <div className="ml-2 w-16 bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${
                          result.fraud_probability > 0.5 ? 'bg-red-500' : 'bg-green-500'
                        }`}
                        style={{ width: `${result.fraud_probability * 100}%` }}
                      ></div>
                    </div>
                  </div>
                </td>
                <td className="px-4 py-3 text-sm text-gray-600">
                  {Number(result.predicted_fraud) === 1 ? (
                    <span className="px-2 py-1 rounded text-xs bg-red-100 text-red-800">Fraud</span>
                  ) : (
                    <span className="px-2 py-1 rounded text-xs bg-green-100 text-green-800">Legitimate</span>
                  )}
                </td>
                <td className="px-4 py-3 text-sm text-gray-600">
                  {result.location}
                </td>
                <td className="px-4 py-3 text-sm text-gray-600">
                  <span className={`px-2 py-1 rounded text-xs ${
                    result.device_switch_count > 3 
                      ? 'bg-red-100 text-red-800' 
                      : 'bg-gray-100 text-gray-800'
                  }`}>
                    {result.device_switch_count}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {results.length > 200 && (
        <div className="mt-4 text-center text-sm text-gray-500">
          Only showing first 200 results for performance. 
          Download the full results file for complete data.
        </div>
      )}
    </div>
  );
};

export default ResultsTable;