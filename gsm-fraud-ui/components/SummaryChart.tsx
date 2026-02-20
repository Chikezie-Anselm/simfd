'use client';

import { useEffect, useRef } from 'react';

interface SummaryChartProps {
  fraudCount: number;
  legitimateCount: number;
  totalCount: number;
}

const SummaryChart = ({ fraudCount, legitimateCount, totalCount }: SummaryChartProps) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
  if (!canvasRef.current || !(window as any).Chart) return;

    const ctx = canvasRef.current.getContext('2d');
    if (!ctx) return;

    // Destroy existing chart if it exists
    if ((canvasRef.current as any).chart) {
      (canvasRef.current as any).chart.destroy();
    }

    const chart = new (window as any).Chart(ctx, {
      type: 'pie',
      data: {
        labels: ['Legitimate', 'Fraud'],
        datasets: [{
          data: [legitimateCount, fraudCount],
          backgroundColor: ['#10b981', '#ef4444'],
          borderColor: ['#059669', '#dc2626'],
          borderWidth: 2,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom' as const,
          },
          tooltip: {
            callbacks: {
              label: function(context: any) {
                const percentage = ((context.parsed / totalCount) * 100).toFixed(1);
                return `${context.label}: ${context.parsed} (${percentage}%)`;
              }
            }
          }
        }
      }
    });

    // Store chart instance
    (canvasRef.current as any).chart = chart;

    return () => {
      chart.destroy();
    };
  }, [fraudCount, legitimateCount, totalCount]);

  const fraudPercentage = totalCount > 0 ? ((fraudCount / totalCount) * 100).toFixed(1) : '0';
  const legitimatePercentage = totalCount > 0 ? ((legitimateCount / totalCount) * 100).toFixed(1) : '0';

  return (
    <div className="card">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Summary Statistics
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <div className="space-y-4">
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="text-sm font-medium text-gray-600">Total Records</span>
              <span className="text-lg font-bold text-gray-900">{totalCount}</span>
            </div>
            
            <div className="flex justify-between items-center p-3 bg-green-50 rounded-lg">
              <span className="text-sm font-medium text-green-600">Legitimate</span>
              <div className="text-right">
                <div className="text-lg font-bold text-green-800">{legitimateCount}</div>
                <div className="text-xs text-green-600">{legitimatePercentage}%</div>
              </div>
            </div>
            
            <div className="flex justify-between items-center p-3 bg-red-50 rounded-lg">
              <span className="text-sm font-medium text-red-600">Fraudulent</span>
              <div className="text-right">
                <div className="text-lg font-bold text-red-800">{fraudCount}</div>
                <div className="text-xs text-red-600">{fraudPercentage}%</div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="flex justify-center items-center">
          <div className="relative w-64 h-64">
            <canvas ref={canvasRef}></canvas>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SummaryChart;