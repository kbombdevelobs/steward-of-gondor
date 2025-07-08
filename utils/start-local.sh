#!/bin/bash

# DeepSeek Chatbot API with Local Model Startup Script

echo "🏠 Starting DeepSeek Chatbot API with Local Model..."

# Check if models directory exists
if [ ! -d "models" ]; then
    echo "📁 Creating models directory..."
    mkdir -p models
fi

# Check if any models are available
if [ -z "$(ls -A models 2>/dev/null)" ]; then
    echo "❌ No local models found in ./models directory"
    echo ""
    echo "💡 To download a model locally:"
    echo "   1. Run: python download_model.py"
    echo "   2. Select a model to download"
    echo "   3. Wait for download to complete"
    echo ""
    echo "📁 Or manually place model files in ./models/ directory"
    exit 1
fi

echo "📂 Available local models:"
ls -la models/

echo ""
echo "🔧 To use a specific local model, update app.py or use the /load-model endpoint"
echo ""

# Start the Docker container
echo "🐳 Starting Docker container..."
docker-compose down
docker-compose build
docker-compose up -d

echo ""
echo "✅ Container started!"
echo "📡 API available at: http://localhost:5001"
echo "🔍 Health check: http://localhost:5001/health"
echo ""
echo "💡 To load a local model, use:"
echo "   curl -X POST http://localhost:5001/load-model \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"model_name\": \"./models/deepseek-coder-1.3b-instruct\"}'" 