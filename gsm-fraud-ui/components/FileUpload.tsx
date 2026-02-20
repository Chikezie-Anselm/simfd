'use client';

import { useState, useRef } from 'react';
import { api } from '@/lib/api';
import LoadingSpinner from './LoadingSpinner';
import AlertMessage from './AlertMessage';

interface FileUploadProps {
  onUploadSuccess: (data: any) => void;
}

const FileUpload = ({ onUploadSuccess }: FileUploadProps) => {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFiles = async (files: FileList | null) => {
    if (!files || files.length === 0) return;

    const file = files[0];
    
    // Validate file type
    if (!file.name.toLowerCase().endsWith('.csv')) {
      setError('Please select a CSV file');
      return;
    }

    // Validate file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      setError('File size must be less than 10MB');
      return;
    }

    setError(null);
    setIsUploading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);

      // Do not set Content-Type header here; the browser will add the correct
      // multipart/form-data boundary when using FormData.
  const response = await api.post('/upload', formData);

      // The backend now returns JSON with a summary and sample rows when called via AJAX.
      const payload = response.data;
      // Basic validation: we expect a total or a sample array
      if (payload && (typeof payload.total === 'number' || Array.isArray(payload.sample))) {
        onUploadSuccess(payload);
      } else {
        // Unexpected response shape (maybe HTML or error). Surface an error instead of redirecting to an empty results page.
        setError('Unexpected response from backend. Please check the server logs or try again.');
      }
    } catch (err: any) {
      console.error('Upload error:', err);
      if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else if (err.code === 'ECONNREFUSED') {
        setError('Cannot connect to backend server. Please ensure the Flask API is running on http://localhost:5000');
      } else {
        setError('Upload failed. Please try again.');
      }
    } finally {
      setIsUploading(false);
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    handleFiles(e.dataTransfer.files);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    handleFiles(e.target.files);
  };

  const openFileDialog = () => {
    fileInputRef.current?.click();
  };

  if (isUploading) {
    return <LoadingSpinner text="Uploading and processing your file..." />;
  }

  return (
    <div className="w-full max-w-2xl mx-auto">
      {error && (
        <div className="mb-4">
          <AlertMessage type="error" message={error} onClose={() => setError(null)} />
        </div>
      )}
      
      <div
        className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-colors duration-200 ${
          dragActive
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          onChange={handleInputChange}
          className="hidden"
        />
        
        <div className="space-y-4">
          <div className="text-6xl text-gray-400">📄</div>
          <div>
            <h3 className="text-lg font-medium text-gray-900">
              Upload CSV File
            </h3>
            <p className="text-sm text-gray-600 mt-2">
              Drag and drop your CSV file here, or click to browse
            </p>
          </div>
          
          <button
            onClick={openFileDialog}
            className="btn-primary"
          >
            Select CSV File
          </button>
          
          <div className="text-xs text-gray-500">
            <p>Supported format: CSV files only</p>
            <p>Maximum file size: 10MB</p>
            <p>Required columns: subscriber_id, IMEI, registration_date, location, initial_call_count, average_call_duration, device_switch_count</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FileUpload;