#!/bin/bash

# GSM Fraud Detection Frontend Setup Script
# This script sets up the Next.js frontend application

echo "🚀 Setting up GSM Fraud Detection Frontend..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    echo "Download from: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Node.js and npm are installed"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create environment file if it doesn't exist
if [ ! -f .env.local ]; then
    echo "🔧 Creating environment configuration..."
    cp .env.example .env.local
    echo "✅ Environment file created (.env.local)"
    echo "💡 You can edit .env.local to customize the backend URL"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p public/images
mkdir -p public/uploads

echo "🎉 Setup complete!"
echo ""
echo "🚀 To start the development server:"
echo "   npm run dev"
echo ""
echo "🌐 The application will be available at:"
echo "   http://localhost:3000"
echo ""
echo "⚙️  Make sure your Flask backend is running on:"
echo "   http://localhost:5000"
echo ""
echo "📖 For more information, see README.md"