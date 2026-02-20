'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import FileUpload from '@/components/FileUpload';
import AlertMessage from '@/components/AlertMessage';

export default function UploadPage() {
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [uploadData, setUploadData] = useState<any>(null);
  const router = useRouter();

  const handleUploadSuccess = (data: any) => {
    setUploadData(data);
    setUploadSuccess(true);
    
    // Store results in sessionStorage for the results page
    sessionStorage.setItem('fraudDetectionResults', JSON.stringify(data));
    
    // Redirect to results page after a short delay
    setTimeout(() => {
      router.push('/results');
    }, 2000);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Upload Subscriber Data
        </h1>
        <p className="text-lg text-gray-600">
          Upload your CSV file containing GSM subscriber data for fraud detection analysis
        </p>
      </div>

      {uploadSuccess && (
        <div className="mb-6">
          <AlertMessage 
            type="success" 
            message="Upload successful! Processing complete. Redirecting to results..." 
          />
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <FileUpload onUploadSuccess={handleUploadSuccess} />
        </div>
        
        <div className="space-y-6">
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Required CSV Format
            </h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="font-medium">subscriber_id</span>
                <span className="text-gray-600">Unique ID</span>
              </div>
              <div className="flex justify-between">
                <span className="font-medium">IMEI</span>
                <span className="text-gray-600">Device identifier</span>
              </div>
              <div className="flex justify-between">
                <span className="font-medium">registration_date</span>
                <span className="text-gray-600">YYYY-MM-DD</span>
              </div>
              <div className="flex justify-between">
                <span className="font-medium">location</span>
                <span className="text-gray-600">Geographic area</span>
              </div>
              <div className="flex justify-between">
                <span className="font-medium">initial_call_count</span>
                <span className="text-gray-600">Number</span>
              </div>
              <div className="flex justify-between">
                <span className="font-medium">average_call_duration</span>
                <span className="text-gray-600">Seconds</span>
              </div>
              <div className="flex justify-between">
                <span className="font-medium">device_switch_count</span>
                <span className="text-gray-600">Number</span>
              </div>
            </div>
          </div>

          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Detection Process
            </h3>
            <div className="space-y-3 text-sm text-gray-600">
              <div className="flex items-start">
                <span className="w-6 h-6 bg-primary-600 text-white rounded-full flex items-center justify-center text-xs font-bold mr-3 mt-0.5">
                  1
                </span>
                <span>File validation and preprocessing</span>
              </div>
              <div className="flex items-start">
                <span className="w-6 h-6 bg-primary-600 text-white rounded-full flex items-center justify-center text-xs font-bold mr-3 mt-0.5">
                  2
                </span>
                <span>AI model analysis of behavioral patterns</span>
              </div>
              <div className="flex items-start">
                <span className="w-6 h-6 bg-primary-600 text-white rounded-full flex items-center justify-center text-xs font-bold mr-3 mt-0.5">
                  3
                </span>
                <span>Fraud probability calculation</span>
              </div>
              <div className="flex items-start">
                <span className="w-6 h-6 bg-primary-600 text-white rounded-full flex items-center justify-center text-xs font-bold mr-3 mt-0.5">
                  4
                </span>
                <span>Results generation and visualization</span>
              </div>
            </div>
          </div>

          <div className="card bg-yellow-50 border-yellow-200">
            <h3 className="text-lg font-semibold text-yellow-800 mb-2">
              ⚠️ Important Notes
            </h3>
            <ul className="text-sm text-yellow-700 space-y-1">
              <li>• Ensure your backend server is running on localhost:5000</li>
              <li>• File size limit: 10MB maximum</li>
              <li>• Processing time varies with file size</li>
              <li>• All data is processed securely and temporarily</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}