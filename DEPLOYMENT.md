# 🚀 Learn2Reel Deployment Guide

This guide covers deploying Learn2Reel to various production environments.

## 📋 Prerequisites

- Docker and Docker Compose installed
- API keys for Gemini and ElevenLabs
- FFmpeg (handled by Docker)
- At least 2GB RAM and 10GB disk space

## 🐳 Docker Deployment (Recommended)

### Quick Start
```bash
# Clone and setup
git clone <your-repo>
cd learn2reel
cp env.example .env
# Edit .env with your API keys

# Deploy
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

### Manual Docker Deployment
```bash
# Build the image
docker-compose build

# Start the application
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Production Docker Configuration

For production environments, consider these optimizations:

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  learn2reel:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./output:/app/output
      - ./.env:/app/.env
      - ./assets:/app/assets
    environment:
      - PYTHONUNBUFFERED=1
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
```

## ☁️ Cloud Deployment

### AWS EC2

1. **Launch EC2 Instance:**
   - Ubuntu 20.04 LTS
   - t3.medium or larger
   - Security group: Allow port 8501

2. **Install Docker:**
```bash
sudo apt update
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
```

3. **Deploy Application:**
```bash
git clone <your-repo>
cd learn2reel
cp env.example .env
# Edit .env
docker-compose up -d
```

### Google Cloud Run

1. **Build and Push:**
```bash
# Build image
docker build -t gcr.io/YOUR_PROJECT/learn2reel .

# Push to Google Container Registry
docker push gcr.io/YOUR_PROJECT/learn2reel
```

2. **Deploy to Cloud Run:**
```bash
gcloud run deploy learn2reel \
  --image gcr.io/YOUR_PROJECT/learn2reel \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8501
```

### Azure Container Instances

```bash
# Deploy to Azure
az container create \
  --resource-group myResourceGroup \
  --name learn2reel \
  --image your-registry/learn2reel:latest \
  --ports 8501 \
  --environment-variables \
    GEMINI_API_KEY=your_key \
    ELEVENLABS_API_KEY=your_key
```

## 🔧 Environment Configuration

### Required Environment Variables

```bash
# API Keys (Required)
GEMINI_API_KEY=your_gemini_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=EXAVITQu4vr4xnSDxMaL

# Optional Instagram Integration
IG_USERNAME=your_instagram_username
IG_PASSWORD=your_instagram_password

# Video Settings
VIDEO_WIDTH=1080
VIDEO_HEIGHT=1920
VIDEO_FPS=24

# Subtitle Settings
SUBTITLE_ENABLED=true
SUBTITLE_FONT_SIZE=50
SUBTITLE_FONT_COLOR=white
SUBTITLE_BACKGROUND_COLOR=black@0.7
```

### Security Best Practices

1. **Use Secrets Management:**
   - AWS Secrets Manager
   - Google Secret Manager
   - Azure Key Vault

2. **Environment-specific configs:**
```bash
# Development
cp env.example .env.dev

# Production
cp env.example .env.prod

# Staging
cp env.example .env.staging
```

## 📊 Monitoring and Health Checks

### Health Check Endpoint
```bash
# Check application health
curl http://localhost:8501/_stcore/health

# Run comprehensive health check
python utils/health_check.py
```

### Logging Configuration
```python
# Add to your application
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('learn2reel.log'),
        logging.StreamHandler()
    ]
)
```

### Monitoring with Prometheus/Grafana

Create `monitoring/prometheus.yml`:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'learn2reel'
    static_configs:
      - targets: ['localhost:8501']
```

## 🔒 Security Considerations

### Network Security
- Use HTTPS in production
- Configure firewall rules
- Implement rate limiting

### Application Security
- Rotate API keys regularly
- Use environment variables for secrets
- Implement proper error handling
- Add input validation

### Data Security
- Encrypt sensitive data at rest
- Use secure file permissions
- Implement proper backup strategies

## 📈 Scaling Considerations

### Horizontal Scaling
```yaml
# docker-compose.scale.yml
version: '3.8'
services:
  learn2reel:
    build: .
    deploy:
      replicas: 3
    environment:
      - REDIS_URL=redis://redis:6379
```

### Load Balancing
```nginx
# nginx.conf
upstream learn2reel {
    server learn2reel:8501;
}

server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://learn2reel;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🚨 Troubleshooting

### Common Issues

1. **FFmpeg not found:**
```bash
# Inside container
apt-get update && apt-get install -y ffmpeg
```

2. **Permission denied:**
```bash
# Fix file permissions
chmod -R 755 output/
chmod -R 755 assets/
```

3. **API key errors:**
```bash
# Check environment variables
docker-compose exec learn2reel env | grep API
```

4. **Memory issues:**
```bash
# Increase Docker memory limit
docker-compose down
docker system prune -a
docker-compose up -d
```

### Debug Commands
```bash
# Check container logs
docker-compose logs -f learn2reel

# Access container shell
docker-compose exec learn2reel bash

# Check resource usage
docker stats

# Health check
python utils/health_check.py
```

## 📝 Deployment Checklist

- [ ] API keys configured
- [ ] Environment variables set
- [ ] FFmpeg installed (Docker handles this)
- [ ] Font files present in assets/
- [ ] Output directory writable
- [ ] Health checks passing
- [ ] Logs configured
- [ ] Monitoring set up
- [ ] Backup strategy defined
- [ ] Security measures implemented

## 🆘 Support

For deployment issues:
1. Check the health check: `python utils/health_check.py`
2. Review logs: `docker-compose logs -f`
3. Verify environment: `docker-compose exec learn2reel env`
4. Test API connectivity manually

# Deployment Guide for Learn2Reel

## 🎯 Quick Start - Hugging Face Spaces (Recommended)

### Why Hugging Face Spaces?
- Perfect for ML/AI projects
- Free tier available
- Automatic Docker builds
- Easy integration with ML models
- Great for showcasing AI projects

### Steps to Deploy on HF Spaces:

1. **Create a Hugging Face Account**
   - Go to [huggingface.co](https://huggingface.co)
   - Sign up for a free account

2. **Create a New Space**
   - Click "New Space" on your profile
   - Choose a name (e.g., "learn2reel")
   - Select "Docker" as the SDK
   - Choose "Public" or "Private"

3. **Upload Your Files**
   Your project already has all the required files:
   - ✅ `Dockerfile` - Defines the container
   - ✅ `requirements.txt` - Python dependencies
   - ✅ `README.md` - Project documentation
   - ✅ `ui/streamlit_app.py` - Main application

4. **Automatic Deployment**
   - HF Spaces will automatically detect your Dockerfile
   - It will build and deploy your container
   - Your app will be available at `https://huggingface.co/spaces/YOUR_USERNAME/learn2reel`

### Configuration for HF Spaces

Your current Dockerfile is already optimized for deployment. The key settings:

```dockerfile
# These settings work perfectly for HF Spaces
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
EXPOSE 8501
```

## 🚀 Alternative Deployment Options

### Railway (Simple & Fast)
1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Railway auto-detects your Dockerfile
4. Deploy with one click

### Render (Free Tier Available)
1. Create account on [render.com](https://render.com)
2. Create new "Web Service"
3. Connect your GitHub repo
4. Set build command: `docker build -t learn2reel .`
5. Set start command: `docker run -p 8501:8501 learn2reel`

### Google Cloud Run (Production)
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT/learn2reel

# Deploy to Cloud Run
gcloud run deploy learn2reel \
  --image gcr.io/YOUR_PROJECT/learn2reel \
  --platform managed \
  --allow-unauthenticated \
  --port 8501
```

### AWS ECS/Fargate (Enterprise)
```bash
# Build and push to Amazon ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker tag learn2reel:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/learn2reel:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/learn2reel:latest
```

## 🔧 Environment Variables

For production deployments, you might want to set these environment variables:

```bash
# API Keys (if needed)
OPENAI_API_KEY=your_openai_key
ELEVENLABS_API_KEY=your_elevenlabs_key

# App Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

## 📊 Monitoring & Health Checks

Your Dockerfile includes a health check:
```dockerfile
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1
```

This ensures your app is running properly and can be monitored by deployment platforms.

## 🐛 Troubleshooting

### Common Issues:

1. **Port Issues**
   - Ensure port 8501 is exposed in Dockerfile
   - Check that STREAMLIT_SERVER_ADDRESS=0.0.0.0

2. **Memory Issues**
   - Your app uses FFmpeg and ML models
   - Consider increasing memory limits on deployment platforms

3. **Build Failures**
   - Check that all dependencies are in requirements.txt
   - Ensure Dockerfile installs system dependencies (ffmpeg)

### Debug Commands:
```bash
# Test locally first
docker build -t learn2reel .
docker run -p 8501:8501 learn2reel

# Check container logs
docker logs <container_id>

# Enter container for debugging
docker exec -it <container_id> /bin/bash
```

## 🎉 Success!

Once deployed, your Learn2Reel app will be accessible via web browser and can:
- Generate AI-powered content
- Create videos with voiceovers
- Process images and text
- All through a beautiful Streamlit interface

The Docker containerization ensures consistent behavior across all deployment platforms! 