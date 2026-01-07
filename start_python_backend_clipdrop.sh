#!/bin/bash

echo "🎨 Starting AleaArt Python Backend (Clipdrop API Version)..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/update requirements
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install flask flask-cors pymongo requests python-dotenv

echo "✅ Dependencies installed successfully!"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "📄 Creating .env file from env.example..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✅ Created .env file. Please edit it with your actual values:"
        echo "   nano .env"
        echo ""
    else
        echo "❌ env.example file not found. Please create a .env file manually."
        exit 1
    fi
fi

# Load environment variables from .env file
echo "🔍 Loading environment variables from .env file..."
export $(grep -v '^#' .env | xargs)

# Check for required environment variables
echo "🔍 Checking environment variables..."

if [ -z "$CLIPDROP_API_KEY" ] || [ "$CLIPDROP_API_KEY" = "your_clipdrop_api_key_here" ]; then
    echo "⚠️ CLIPDROP_API_KEY not set in .env file. Please add your Clipdrop API key:"
    echo "   Get your API key from: https://clipdrop.co/apis"
    echo "   Then edit the .env file: nano .env"
fi

if [ -z "$MONGODB_URI" ] || [ "$MONGODB_URI" = "mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority" ]; then
    echo "⚠️ MONGODB_URI not set in .env file. Please add your MongoDB connection string."
    echo "   Edit the .env file: nano .env"
fi

if [ -z "$PINATA_JWT" ] || [ "$PINATA_JWT" = "your_pinata_jwt_token_here" ]; then
    echo "⚠️ PINATA_JWT not set in .env file. IPFS uploads will be skipped."
    echo "   Get your JWT from: https://app.pinata.cloud/developers/api-keys"
    echo "   Edit the .env file: nano .env"
fi

echo ""
echo "🚀 Starting the server..."
echo "📡 Server will be available at: http://localhost:5001"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Start the Flask app with a different port to avoid conflicts
PORT=5001 python3 python_backend_clipdrop.py
