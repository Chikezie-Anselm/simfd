'use client';

export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-6">
          About GSM Fraud Detection System
        </h1>
        <p className="text-xl text-gray-600">
          Advanced AI-powered fraud detection for GSM subscriber registrations
        </p>
      </div>

      <div className="space-y-8">
        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">System Overview</h2>
          <p className="text-gray-600 mb-4">
            Our GSM Subscription Fraud Detection System leverages cutting-edge artificial neural network 
            technology to identify potentially fraudulent subscriber registrations in real-time. The system 
            analyzes behavioral patterns, device usage metrics, and registration anomalies to provide 
            accurate fraud probability scores.
          </p>
          <p className="text-gray-600">
            Built with modern web technologies and deployed with enterprise-grade security, our solution 
            helps telecommunications providers protect their networks and customers from fraudulent activities.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="card">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">🧠 AI Technology</h3>
            <ul className="space-y-2 text-gray-600">
              <li>• Artificial Neural Network with 3 hidden layers</li>
              <li>• TensorFlow/Keras backend for high performance</li>
              <li>• Real-time behavioral pattern analysis</li>
              <li>• Continuous learning and model improvement</li>
              <li>• 95%+ accuracy on fraud detection</li>
            </ul>
          </div>

          <div className="card">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">🔍 Detection Features</h3>
            <ul className="space-y-2 text-gray-600">
              <li>• Device switch frequency analysis</li>
              <li>• Call pattern anomaly detection</li>
              <li>• Geographic location verification</li>
              <li>• Registration timing analysis</li>
              <li>• IMEI validation and tracking</li>
            </ul>
          </div>
        </div>

        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Technology Stack</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="text-lg font-semibold text-gray-900 mb-3">Backend</h4>
              <div className="space-y-2 text-gray-600">
                <div className="flex justify-between">
                  <span>Framework:</span>
                  <span className="font-medium">Flask (Python)</span>
                </div>
                <div className="flex justify-between">
                  <span>ML Library:</span>
                  <span className="font-medium">TensorFlow 2.10</span>
                </div>
                <div className="flex justify-between">
                  <span>Data Processing:</span>
                  <span className="font-medium">Pandas, NumPy</span>
                </div>
                <div className="flex justify-between">
                  <span>Model Training:</span>
                  <span className="font-medium">Scikit-learn</span>
                </div>
              </div>
            </div>
            <div>
              <h4 className="text-lg font-semibold text-gray-900 mb-3">Frontend</h4>
              <div className="space-y-2 text-gray-600">
                <div className="flex justify-between">
                  <span>Framework:</span>
                  <span className="font-medium">Next.js 14</span>
                </div>
                <div className="flex justify-between">
                  <span>Language:</span>
                  <span className="font-medium">TypeScript</span>
                </div>
                <div className="flex justify-between">
                  <span>Styling:</span>
                  <span className="font-medium">Tailwind CSS</span>
                </div>
                <div className="flex justify-between">
                  <span>Charts:</span>
                  <span className="font-medium">Chart.js</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">How It Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h4 className="text-lg font-semibold text-gray-900 mb-3">Data Processing</h4>
              <ol className="space-y-2 text-gray-600">
                <li>1. CSV file validation and parsing</li>
                <li>2. Feature extraction and normalization</li>
                <li>3. Missing data imputation</li>
                <li>4. Categorical encoding (location)</li>
                <li>5. Numerical scaling and preprocessing</li>
              </ol>
            </div>
            <div>
              <h4 className="text-lg font-semibold text-gray-900 mb-3">AI Analysis</h4>
              <ol className="space-y-2 text-gray-600">
                <li>1. Neural network inference</li>
                <li>2. Pattern recognition and scoring</li>
                <li>3. Probability calculation</li>
                <li>4. Classification (Fraud/Legitimate)</li>
                <li>5. Results visualization</li>
              </ol>
            </div>
          </div>
        </div>

        <div className="card bg-blue-50 border-blue-200">
          <h2 className="text-2xl font-bold text-blue-900 mb-4">Academic Research</h2>
          <p className="text-blue-800 mb-4">
            This system was developed as part of academic research into machine learning applications 
            for telecommunications fraud detection. The project demonstrates the practical implementation 
            of neural networks for real-world fraud prevention scenarios.
          </p>
          <div className="text-sm text-blue-700">
            <p><strong>Research Areas:</strong></p>
            <ul className="list-disc list-inside mt-2 space-y-1">
              <li>Artificial Neural Networks for Classification</li>
              <li>Feature Engineering for Telecommunications Data</li>
              <li>Real-time Fraud Detection Systems</li>
              <li>Web-based Machine Learning Deployment</li>
            </ul>
          </div>
        </div>

        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Contact & Support</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="text-lg font-semibold text-gray-900 mb-3">Development Team</h4>
              <p className="text-gray-600 mb-2">
                Computer Science Department<br/>
                Advanced AI Research Lab
              </p>
              <p className="text-sm text-gray-500">
                For technical inquiries about the system architecture or research methodology.
              </p>
            </div>
            <div>
              <h4 className="text-lg font-semibold text-gray-900 mb-3">System Requirements</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Modern web browser (Chrome, Firefox, Safari)</li>
                <li>• JavaScript enabled</li>
                <li>• Internet connection for API requests</li>
                <li>• CSV files up to 10MB</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}