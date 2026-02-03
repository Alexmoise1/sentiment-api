# 🚀 Quick Start Guide - Sentiment Analysis API

Get your sentiment analysis API running in under 10 minutes!

## 📦 1. Local Setup (2 minutes)

```bash
# Clone or download the project
cd sentiment-api

# Install dependencies
pip install -r requirements.txt

# Download TextBlob data (first time only)
python -m textblob.download_corpora

# Run the app
python main.py
```

**✅ Your API is now running at http://localhost:8080**

## 🧪 2. Test It (1 minute)

### Test in your browser:
Open http://localhost:8080/docs - Interactive API documentation!

### Test with curl:

```bash
# Positive sentiment
curl -X POST "http://localhost:8080/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this! It is amazing and wonderful!"}'

# Negative sentiment
curl -X POST "http://localhost:8080/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is terrible and I hate it."}'

# Health check
curl http://localhost:8080/health
```

### Run tests:

```bash
pytest test_app.py -v
```

## ☁️ 3. Deploy to AWS App Runner (5 minutes)

### Prerequisites:
- AWS account
- GitHub account (for easiest deployment)

### Steps:

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR-USERNAME/sentiment-api.git
   git push -u origin main
   ```

2. **Go to AWS App Runner Console:**
   https://console.aws.amazon.com/apprunner

3. **Click "Create service"**

4. **Configure Source:**
   - Choose: "Source code repository"
   - Click: "Add new" to connect GitHub
   - Select your repository: `sentiment-api`
   - Branch: `main`

5. **Configure Build:**
   - Runtime: **Python 3**
   - Build command: 
     ```bash
     pip install -r requirements.txt && python -m textblob.download_corpora
     ```
   - Start command:
     ```bash
     uvicorn main:app --host 0.0.0.0 --port 8080
     ```
   - Port: **8080**

6. **Configure Service:**
   - Service name: `sentiment-api`
   - CPU: **1 vCPU**
   - Memory: **2 GB**

7. **Configure Health Check:**
   - Path: `/health`
   - Interval: 30 seconds
   - Timeout: 5 seconds

8. **Review and Create!**

### ⏱️ Wait 5-7 minutes for deployment...

### 🎉 Your API is now live!

You'll get a URL like:
```
https://abc123xyz.us-east-1.awsapprunner.com
```

## 🎯 Test Your Live API

```bash
# Replace YOUR-URL with your actual App Runner URL
curl -X POST "https://YOUR-URL.awsapprunner.com/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "This API deployment was so easy!"}'
```

## 📊 Monitor Your API

### CloudWatch Logs:
AWS Console → CloudWatch → Log Groups → `/aws/apprunner/sentiment-api`

### App Runner Metrics:
AWS Console → App Runner → Your Service → Metrics

## 🔧 Common Issues

### "Port already in use" locally?
```bash
# Use different port
uvicorn main:app --port 8000
```

### "TextBlob corpora not found"?
```bash
python -m textblob.download_corpora
```

### Deployment failing?
- Check CloudWatch logs in AWS Console
- Verify build command is correct
- Make sure port 8080 is specified

## 💡 Tips

- **Auto-deploy**: Enable in App Runner to deploy on every git push
- **Custom domain**: Add in App Runner settings
- **Scale up**: Adjust vCPU/Memory in Instance Configuration
- **Monitor**: Set up CloudWatch alarms for errors/latency

## 📚 What's Next?

- [ ] Add authentication
- [ ] Implement rate limiting
- [ ] Connect to database
- [ ] Add batch processing
- [ ] Set up CI/CD pipeline
- [ ] Add monitoring alerts

## 🆘 Need Help?

1. Check `/docs` endpoint for interactive API documentation
2. Review CloudWatch logs
3. Test locally first
4. Check the full README.md for detailed info

---

**Congratulations! 🎉 You've deployed a production-ready sentiment analysis API!**
