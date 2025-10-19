#!/bin/bash

# Hoodie Store API Startup Script

echo "🚀 Starting Hoodie Store API..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please update .env file with your Supabase credentials"
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🌱 Running database seed script..."
python seed.py

echo "🚀 Starting FastAPI server..."
python run.py
