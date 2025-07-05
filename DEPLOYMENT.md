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