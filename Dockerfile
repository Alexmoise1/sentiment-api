FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m textblob.download_corpora

# Copy application files
COPY main.py .
COPY index.html .

# Expose port
EXPOSE 8080

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

5. Scroll down and click **"Commit changes"**

---

## **Step 2: Create .dockerignore File**

1. Click **"Add file"** → **"Create new file"**
2. Name it: `.dockerignore`
3. **Paste this:**
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.so
.env
.venv
env/
venv/
.git
.gitignore
README.md
*.md
test_app.py
requirements-dev.txt
