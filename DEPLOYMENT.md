# 🚀 Deployment Guide

## Deploy Your Bengali Hate Speech Classifier

This guide shows you how to deploy your Flask app to various platforms.

---

## Option 1: Heroku (Recommended for Beginners)

### Prerequisites
- Heroku account (free tier available)
- Heroku CLI installed

### Steps

1. **Create Procfile**
```bash
echo "web: gunicorn app:app" > Procfile
```

2. **Update requirements.txt**
Add gunicorn:
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

3. **Initialize Git**
```bash
git init
git add .
git commit -m "Initial commit"
```

4. **Create Heroku App**
```bash
heroku create your-app-name
```

5. **Deploy**
```bash
git push heroku main
```

6. **Open App**
```bash
heroku open
```

### Cost
- Free tier available (with limitations)
- Hobby tier: $7/month

---

## Option 2: Railway

### Prerequisites
- Railway account
- GitHub account

### Steps

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin your-github-repo-url
git push -u origin main
```

2. **Deploy on Railway**
- Go to railway.app
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your repository
- Railway auto-detects Flask and deploys

### Cost
- $5 free credit per month
- Pay as you go after that

---

## Option 3: Render

### Prerequisites
- Render account
- GitHub account

### Steps

1. **Create render.yaml**
```yaml
services:
  - type: web
    name: bengali-classifier
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

2. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git push
```

3. **Deploy on Render**
- Go to render.com
- Click "New Web Service"
- Connect GitHub repository
- Render auto-deploys

### Cost
- Free tier available
- Paid plans start at $7/month

---

## Option 4: AWS EC2

### Prerequisites
- AWS account
- Basic Linux knowledge

### Steps

1. **Launch EC2 Instance**
- Choose Ubuntu 22.04 LTS
- t2.micro (free tier eligible)
- Configure security group (allow port 80, 443, 22)

2. **Connect via SSH**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Install Dependencies**
```bash
sudo apt update
sudo apt install python3-pip nginx
```

4. **Upload Code**
```bash
scp -i your-key.pem -r * ubuntu@your-ec2-ip:~/app/
```

5. **Install Python Packages**
```bash
cd ~/app
pip3 install -r requirements.txt
pip3 install gunicorn
```

6. **Run with Gunicorn**
```bash
gunicorn --bind 0.0.0.0:8000 app:app
```

7. **Configure Nginx** (optional, for production)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Cost
- Free tier: 750 hours/month for 12 months
- After free tier: ~$10-20/month

---

## Option 5: Google Cloud Run

### Prerequisites
- Google Cloud account
- gcloud CLI installed

### Steps

1. **Create Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
```

2. **Build and Deploy**
```bash
gcloud builds submit --tag gcr.io/your-project-id/bengali-classifier
gcloud run deploy --image gcr.io/your-project-id/bengali-classifier --platform managed
```

### Cost
- Free tier: 2 million requests/month
- Pay per use after that

---

## Option 6: DigitalOcean App Platform

### Prerequisites
- DigitalOcean account
- GitHub account

### Steps

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git push
```

2. **Deploy on DigitalOcean**
- Go to cloud.digitalocean.com
- Click "Create" → "Apps"
- Connect GitHub repository
- Choose Python environment
- Deploy

### Cost
- Basic plan: $5/month
- Professional: $12/month

---

## Production Considerations

### 1. Environment Variables
Store sensitive data in environment variables:
```python
import os
HF_TOKEN = os.getenv('HF_TOKEN')
```

### 2. WSGI Server
Use Gunicorn instead of Flask dev server:
```bash
gunicorn --workers 4 --bind 0.0.0.0:8000 app:app
```

### 3. Caching
Cache model files to avoid re-downloading:
```python
import os
os.environ['HF_HOME'] = '/path/to/cache'
```

### 4. Rate Limiting
Add rate limiting to prevent abuse:
```python
from flask_limiter import Limiter

limiter = Limiter(app, default_limits=["100 per hour"])
```

### 5. HTTPS
Always use HTTPS in production (most platforms provide this automatically)

### 6. Monitoring
Add logging and monitoring:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### 7. Error Handling
Improve error handling for production:
```python
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500
```

---

## Recommended Setup for Production

```python
# app.py (production version)
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

app = Flask(__name__)
CORS(app)

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ... rest of your code ...

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
```

---

## Cost Comparison

| Platform | Free Tier | Paid Plans | Best For |
|----------|-----------|------------|----------|
| Heroku | Limited | $7/mo | Beginners |
| Railway | $5 credit | Pay-as-go | Small apps |
| Render | Yes | $7/mo | Simple deploy |
| AWS EC2 | 12 months | $10-20/mo | Full control |
| GCP Cloud Run | 2M req/mo | Pay-as-go | Scalability |
| DigitalOcean | No | $5/mo | Simplicity |

---

## Quick Deploy Checklist

- [ ] Update requirements.txt with gunicorn
- [ ] Create Procfile (for Heroku)
- [ ] Set up environment variables
- [ ] Test locally with gunicorn
- [ ] Push to GitHub
- [ ] Choose deployment platform
- [ ] Deploy and test
- [ ] Set up custom domain (optional)
- [ ] Enable HTTPS
- [ ] Set up monitoring

---

## Need Help?

- Check platform-specific documentation
- Test locally before deploying
- Use environment variables for secrets
- Monitor logs after deployment
- Start with free tier, scale as needed

Happy deploying! 🚀
