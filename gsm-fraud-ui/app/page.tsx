'use client';

import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="max-w-4xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
          GSM Subscription Fraud Detection System
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          Advanced AI-powered fraud detection using artificial neural networks to identify 
          potentially fraudulent GSM subscriber registrations in real-time.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/upload" className="btn-primary text-lg px-8 py-3">
            Start Detection
          </Link>
          <Link href="/about" className="btn-secondary text-lg px-8 py-3">
            Learn More
          </Link>
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
        <div className="card text-center">
          <div className="text-4xl mb-4">🧠</div>
          <h3 className="text-lg font-semibold mb-2">AI-Powered Detection</h3>
          <p className="text-gray-600 text-sm">
            Neural network model trained on behavioral patterns to identify fraudulent registrations
          </p>
        </div>
        
        <div className="card text-center">
          <div className="text-4xl mb-4">📊</div>
          <h3 className="text-lg font-semibold mb-2">Real-time Analytics</h3>
          <p className="text-gray-600 text-sm">
            Instant results with detailed probability scores and visual analytics dashboard
          </p>
        </div>
        
        <div className="card text-center">
          <div className="text-4xl mb-4">🔒</div>
          <h3 className="text-lg font-semibold mb-2">Secure Processing</h3>
          <p className="text-gray-600 text-sm">
            Enterprise-grade security for sensitive subscriber data processing and analysis
          </p>
        </div>
      </div>

      {/* How it Works */}
      <div className="card">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-600 text-white rounded-full flex items-center justify-center font-bold text-lg mx-auto mb-3">
              1
            </div>
            <h4 className="font-semibold mb-2">Upload CSV</h4>
            <p className="text-sm text-gray-600">
              Upload your subscriber data in CSV format
            </p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-600 text-white rounded-full flex items-center justify-center font-bold text-lg mx-auto mb-3">
              2
            </div>
            <h4 className="font-semibold mb-2">AI Analysis</h4>
            <p className="text-sm text-gray-600">
              Neural network analyzes patterns and behaviors
            </p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-600 text-white rounded-full flex items-center justify-center font-bold text-lg mx-auto mb-3">
              3
            </div>
            <h4 className="font-semibold mb-2">Risk Scoring</h4>
            <p className="text-sm text-gray-600">
              Generate fraud probability for each subscriber
            </p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-600 text-white rounded-full flex items-center justify-center font-bold text-lg mx-auto mb-3">
              4
            </div>
            <h4 className="font-semibold mb-2">View Results</h4>
            <p className="text-sm text-gray-600">
              Review detailed analytics and take action
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="text-center mt-12">
        <div className="card bg-primary-50 border-primary-200">
          <h3 className="text-xl font-semibold text-primary-900 mb-4">
            Ready to detect fraud in your subscriber data?
          </h3>
          <p className="text-primary-700 mb-6">
            Upload your CSV file and get instant fraud detection results powered by AI
          </p>
          <Link href="/upload" className="btn-primary">
            Get Started Now
          </Link>
        </div>
      </div>
    </div>
  );
}