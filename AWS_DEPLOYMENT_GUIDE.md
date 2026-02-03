# 📘 AWS App Runner Deployment Guide
## Sentiment Analysis API - Complete Step-by-Step Tutorial

---

## 🎯 Overview

This guide will help you deploy your Sentiment Analysis API to AWS App Runner.

**Time Required**: ~10 minutes  
**Cost**: ~$20-30/month (low traffic)  
**Difficulty**: Beginner-friendly

---

## ✅ Prerequisites Checklist

Before starting, make sure you have:

- [ ] AWS Account (free tier works!)
- [ ] GitHub Account
- [ ] Git installed on your computer
- [ ] Project files downloaded

---

## 📋 Step 1: Push Code to GitHub (3 minutes)

### 1.1 Create a new repository on GitHub

1. Go to https://github.com
2. Click the **"+"** icon → **"New repository"**
3. Repository name: `sentiment-api`
4. Description: "Sentiment Analysis API with FastAPI"
5. Choose: **Public** (or Private if you have GitHub Pro)
6. **DO NOT** initialize with README (we already have one)
7. Click **"Create repository"**

### 1.2 Push your code

Open terminal/command prompt in your project folder:

```bash
# Navigate to your project
cd sentiment-api

# Initialize git (if not done already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Sentiment Analysis API"

# Add your GitHub repository
git remote add origin https://github.com/YOUR-USERNAME/sentiment-api.git

# Push to GitHub
git push -u origin main
```

**✅ Checkpoint**: Verify your code is on GitHub by visiting your repository URL

---

## ☁️ Step 2: Create App Runner Service (7 minutes)

### 2.1 Navigate to App Runner

1. Log in to AWS Console: https://console.aws.amazon.com
2. Search for **"App Runner"** in the search bar
3. Click **"AWS App Runner"**
4. Click **"Create service"** button

### 2.2 Configure Source

**Repository type**: Source code repository

1. Click **"Add new"** next to "Source code repository"
2. Choose **"GitHub"**
3. Click **"Connect to GitHub"**
4. Authorize AWS Connector for GitHub (follow the prompts)
5. **Select repository**: Choose `sentiment-api` from dropdown
6. **Branch**: `main`
7. Click **"Next"**

### 2.3 Configure Build Settings

**Deployment trigger**: Automatic (recommended)

**Build settings**:

```yaml
Configuration source: Configure all settings here

Runtime: Python 3

Build command:
pip install -r requirements.txt && python -m textblob.download_corpora

Start command:
uvicorn main:app --host 0.0.0.0 --port 8080

Port: 8080
```

Click **"Next"**

### 2.4 Configure Service

**Service name**: `sentiment-api`

**Virtual CPU & memory**:
- CPU: **1 vCPU**
- Memory: **2 GB**

**Environment variables**: (Optional)
- Leave empty for now

**Auto scaling**:
- Min instances: **1**
- Max instances: **10**
- Max concurrency: **100**

### 2.5 Configure Health Check

**Health check protocol**: HTTP

**Health check path**: `/health`

**Health check interval**: 30 seconds

**Health check timeout**: 5 seconds

**Healthy threshold**: 1

**Unhealthy threshold**: 3

### 2.6 Configure Security (Optional)

**Instance role**: (Leave default)

**Encryption**: (Leave default)

### 2.7 Review and Create

1. **Review all settings** - make sure everything is correct
2. Click **"Create & deploy"**
3. **Wait 5-7 minutes** ⏱️ (grab a coffee!)

You'll see deployment status:
- Building source code
- Deploying to AWS
- Health checks starting
- Service is running ✅

---

## 🎉 Step 3: Test Your Live API (2 minutes)

### 3.1 Get Your URL

After deployment completes, you'll see:

```
Default domain: https://abc123xyz.us-east-1.awsapprunner.com
```

**Copy this URL!**

### 3.2 Test in Browser

Open your browser and go to:

```
https://YOUR-URL.awsapprunner.com/docs
```

You'll see the interactive API documentation (Swagger UI)!

### 3.3 Test with curl

```bash
# Health check
curl https://YOUR-URL.awsapprunner.com/health

# Analyze positive sentiment
curl -X POST "https://YOUR-URL.awsapprunner.com/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this API! It works perfectly!"}'

# Analyze negative sentiment
curl -X POST "https://YOUR-URL.awsapprunner.com/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is terrible and I hate it."}'
```

### 3.4 Test in Python

```python
import requests

url = "https://YOUR-URL.awsapprunner.com/analyze"

response = requests.post(url, json={
    "text": "This deployment was so easy!"
})

print(response.json())
```

---

## 📊 Step 4: Monitor Your API

### 4.1 View Metrics

1. In App Runner console, click your service name
2. Go to **"Metrics"** tab
3. View:
   - Request count
   - Response time
   - Error rate
   - Active instances

### 4.2 View Logs

1. Click **"Logs"** tab
2. Click **"View in CloudWatch"**
3. See all application logs in real-time

### 4.3 Set Up Alarms (Optional)

1. Go to **CloudWatch** → **Alarms**
2. Create alarms for:
   - High error rate
   - Slow response time
   - High CPU usage

---

## 🔄 Step 5: Enable Auto-Deploy

**Already enabled!** Every time you push to GitHub:

```bash
git add .
git commit -m "Updated API"
git push
```

App Runner will automatically:
1. Detect the change
2. Build new version
3. Deploy with zero downtime
4. Run health checks
5. Switch traffic to new version

---

## 🎨 Customize Your API

### Add Custom Domain

1. In App Runner console → Your service
2. Click **"Custom domains"** tab
3. Click **"Link domain"**
4. Enter your domain (e.g., `api.yourdomain.com`)
5. Follow DNS configuration instructions

### Adjust Scaling

1. Go to **"Configuration"** tab
2. Click **"Edit"** on Auto scaling
3. Adjust:
   - Min/Max instances
   - Max concurrency per instance

### Add Environment Variables

1. Go to **"Configuration"** tab
2. Click **"Edit"** on Environment variables
3. Add variables like:
   - `LOG_LEVEL=debug`
   - `ENVIRONMENT=production`

---

## 💰 Cost Management

### Monitor Costs

1. AWS Console → **Billing Dashboard**
2. View **App Runner** charges
3. Set up **Budget alerts**

### Optimize Costs

- **Reduce instances**: Lower max instances if traffic is low
- **Right-size**: Use 0.5 vCPU if performance is acceptable
- **Pause service**: Stop service if not in use (no charges when paused)

**Typical costs (us-east-1)**:
- 1 instance, 24/7: ~$25-35/month
- Auto-scaling (avg 2 instances): ~$50-70/month

---

## 🐛 Troubleshooting

### Deployment Failed

**Check build logs**:
1. App Runner console → Your service
2. Click **"Logs"** tab
3. Look for errors in build phase

**Common issues**:
- Missing dependencies in requirements.txt
- Incorrect build/start commands
- Port mismatch

### Health Checks Failing

**Verify locally**:
```bash
curl http://localhost:8080/health
```

**Check in AWS**:
- Correct health check path: `/health`
- App is listening on port 8080
- Application is not crashing

### High Response Time

**Solutions**:
- Increase CPU/Memory
- Add more instances
- Optimize code
- Add caching

### Service Not Responding

**Steps**:
1. Check service status in console
2. Review CloudWatch logs
3. Verify GitHub repository is accessible
4. Check auto-deploy settings

---

## 🚀 What's Next?

### Immediate Next Steps
- [ ] Test all API endpoints
- [ ] Monitor for 24 hours
- [ ] Set up CloudWatch alarms
- [ ] Share API URL with team

### Future Enhancements
- [ ] Add authentication (API keys)
- [ ] Implement rate limiting
- [ ] Connect to database
- [ ] Add batch processing
- [ ] Set up custom domain
- [ ] Create staging environment
- [ ] Add CI/CD with GitHub Actions
- [ ] Implement caching layer

---

## 📚 Additional Resources

### AWS Documentation
- App Runner: https://docs.aws.amazon.com/apprunner/
- CloudWatch: https://docs.aws.amazon.com/cloudwatch/
- Pricing: https://aws.amazon.com/apprunner/pricing/

### FastAPI Documentation
- Official Docs: https://fastapi.tiangolo.com/
- Deployment Guide: https://fastapi.tiangolo.com/deployment/

### Support
- AWS Support: https://console.aws.amazon.com/support/
- GitHub Issues: Create issue in your repository
- Stack Overflow: Tag questions with `aws-app-runner` and `fastapi`

---

## ✅ Deployment Checklist

Use this checklist to ensure successful deployment:

**Pre-Deployment**:
- [ ] All files committed to git
- [ ] Code pushed to GitHub
- [ ] Repository is accessible
- [ ] requirements.txt is correct

**During Deployment**:
- [ ] Repository connected to App Runner
- [ ] Build command is correct
- [ ] Start command is correct
- [ ] Port 8080 is specified
- [ ] Health check path is `/health`

**Post-Deployment**:
- [ ] Service is running
- [ ] Health checks passing
- [ ] API responds to requests
- [ ] /docs page loads
- [ ] Logs are accessible
- [ ] Auto-deploy is working

---

## 🎉 Congratulations!

You've successfully deployed a production-ready sentiment analysis API to AWS App Runner!

**Your API is now**:
- ✅ Live and accessible worldwide
- ✅ Automatically scaling
- ✅ Continuously deploying from GitHub
- ✅ Monitored and logged
- ✅ Production-ready

**Share your API**:
```
https://YOUR-URL.awsapprunner.com/docs
```

---

**Need help?** Check the README.md or create an issue on GitHub!

**Last Updated**: February 2026  
**Version**: 1.0
