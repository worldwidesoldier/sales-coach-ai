#!/bin/bash

echo "🚀 Starting Sales Coach Frontend..."
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies (this may take a few minutes)..."
    npm install
fi

echo ""
echo "=" * 60
echo "🎯 Frontend Server Starting..."
echo "=" * 60
echo ""

# Run development server
npm run dev
