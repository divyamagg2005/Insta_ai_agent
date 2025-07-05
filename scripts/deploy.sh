#!/bin/bash

# Learn2Reel Deployment Script
# This script helps deploy the application to production

set -e  # Exit on any error

echo "🚀 Learn2Reel Deployment Script"
echo "================================"

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

# Check if configuration exists
if [ ! -f learn2reel_config.json ]; then
    echo "⚠️ Configuration not found. No problem! You can configure it in the web interface."
    echo "The application will start and you can configure your API keys in the browser."
fi

# Check if required directories exist
echo "📁 Creating necessary directories..."
mkdir -p output assets

# Check if assets directory has required files
if [ ! -f assets/Montserrat-SemiBold.ttf ]; then
    echo "⚠️ Custom font not found. Downloading Montserrat font..."
    # This would need to be implemented based on font availability
    echo "Please ensure assets/Montserrat-SemiBold.ttf exists"
fi

# Build and start the application
echo "🔨 Building Docker image..."
docker-compose build

echo "🚀 Starting Learn2Reel..."
docker-compose up -d

echo "⏳ Waiting for application to start..."
sleep 10

# Check if application is running
if curl -f http://localhost:8501/_stcore/health &> /dev/null; then
    echo "✅ Learn2Reel is running successfully!"
    echo "🌐 Access the application at: http://localhost:8501"
    echo ""
    echo "📋 Useful commands:"
    echo "   - View logs: docker-compose logs -f"
    echo "   - Stop app: docker-compose down"
    echo "   - Restart app: docker-compose restart"
    echo "   - Update app: docker-compose pull && docker-compose up -d"
else
    echo "❌ Application failed to start. Check logs with: docker-compose logs"
    exit 1
fi 