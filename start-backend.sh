#!/bin/bash

echo "🚀 Starting Sales Coach Backend..."
echo ""

# Navigate to backend directory
cd "$(dirname "$0")/backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "=" * 60
echo "🎯 Backend Server Starting..."
echo "=" * 60
echo ""

# Run the application
python app.py
