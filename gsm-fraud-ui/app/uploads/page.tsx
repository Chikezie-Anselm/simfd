"use client";

import { useEffect, useState } from 'react';
import { api, API_BASE_URL } from '@/lib/api';

interface UploadRecord {
  results_file: string;
  total: number;
  predicted_frauds: number;
  legit_count: number;
  avg_prob: number;
  note?: string | null;
  created_at?: string | null;
}

export default function UploadsPage() {
  const [uploads, setUploads] = useState<UploadRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    setIsLoading(true);
    api.get('/api/uploads')
      .then(res => {
        if (!mounted) return;
        const data = res.data?.uploads || [];
        setUploads(data);
      })
      .catch(err => {
        console.error('Failed to fetch uploads', err);
        setError('Failed to fetch uploads from backend');
      })
      .finally(() => mounted && setIsLoading(false));

    return () => { mounted = false; };
  }, []);

  if (isLoading) return <div className="max-w-4xl mx-auto"><div className="p-8">Loading uploads...</div></div>;
  if (error) return <div className="max-w-4xl mx-auto"><div className="p-8 text-red-600">{error}</div></div>;

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Saved Uploads</h1>
      {uploads.length === 0 ? (
        <div className="text-gray-600">No uploads recorded yet.</div>
      ) : (
        <div className="overflow-x-auto">
          <table className="table-auto w-full border-collapse">
            <thead>
              <tr className="text-left">
                <th className="px-3 py-2">File</th>
                <th className="px-3 py-2">Total</th>
                <th className="px-3 py-2">Fraud</th>
                <th className="px-3 py-2">Avg Risk</th>
                <th className="px-3 py-2">Note</th>
                <th className="px-3 py-2">Uploaded</th>
                <th className="px-3 py-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {uploads.map((u) => (
                <tr key={u.results_file} className="border-t">
                  <td className="px-3 py-2 align-top break-words max-w-xs">{u.results_file}</td>
                  <td className="px-3 py-2 align-top">{u.total}</td>
                  <td className="px-3 py-2 align-top">{u.predicted_frauds}</td>
                  <td className="px-3 py-2 align-top">{((u.avg_prob || 0) * 100).toFixed(2)}%</td>
                  <td className="px-3 py-2 align-top">{u.note || ''}</td>
                  <td className="px-3 py-2 align-top">{u.created_at || ''}</td>
                  <td className="px-3 py-2 align-top space-x-2">
                    <a className="btn btn-sm btn-outline" href={`${API_BASE_URL}/api/uploads/${encodeURIComponent(u.results_file)}`} target="_blank" rel="noreferrer">View JSON</a>
                    <a className="btn btn-sm btn-outline" href={`${API_BASE_URL}/api/uploads/${encodeURIComponent(u.results_file)}/download`}>Download</a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
