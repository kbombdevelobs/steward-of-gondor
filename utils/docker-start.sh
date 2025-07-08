#!/bin/bash

# DeepSeek Chatbot API Docker Startup Script

echo "🐳 Starting DeepSeek Chatbot API with Docker..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create logs directory if it doesn't exist
mkdir -p logs

echo "🔨 Building Docker image..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed!"
    exit 1
fi

echo "🚀 Starting the container..."
echo "📡 API will be available at: http://localhost:5001"
echo "🔍 Health check: http://localhost:5001/health"
echo ""
echo "📋 Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop container: docker-compose down"
echo "  - Restart: docker-compose restart"
echo "  - Test API: python docker-test-client.py"
echo ""
echo "⏳ The first startup may take a while as the model downloads..."
echo ""

# Start the container in detached mode
docker-compose up -d

# Wait a moment for the container to start
sleep 5

# Show logs
echo "📋 Container logs:"
docker-compose logs --tail=20

echo ""
echo "✅ Container started! You can now test the API."
echo "💡 Run 'python docker-test-client.py' to test the API" 