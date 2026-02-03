"""
Sentiment Analysis FastAPI App built with GPT4 and AWS AppRunner
This is a simple FastAPI app that takes a string as input and returns a sentiment score 
from 1 (negative) to 10 (positive) using TextBlob for sentiment analysis.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from textblob import TextBlob
import uvicorn
import os

app = FastAPI(
    title="Sentiment Analysis API",
    description="Analyze text sentiment with scores from 1-10",
    version="1.0.0"
)

class TextInput(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    text: str
    sentiment_score: float
    sentiment_label: str
    polarity: float
    subjectivity: float

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the beautiful frontend interface"""
    try:
        # Try to read the HTML file
        html_path = os.path.join(os.path.dirname(__file__), "index.html")
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        # Fallback to API information if HTML not found
        return """
        <html>
            <body style="font-family: Arial; padding: 50px; text-align: center;">
                <h1>Sentiment Analysis API</h1>
                <p>Visit <a href="/docs">/docs</a> for interactive API documentation</p>
            </body>
        </html>
        """

@app.get("/health")
async def health_check():
    """Health check endpoint for AWS App Runner"""
    return {"status": "healthy", "service": "sentiment-api"}

@app.post("/analyze", response_model=SentimentResponse)
async def analyze_sentiment(input_data: TextInput):
    """
    Analyze sentiment of input text
    Returns sentiment score from 1 (negative) to 10 (positive)
    """
    try:
        text = input_data.text.strip()
        
        if not text:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Perform sentiment analysis using TextBlob
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # Range: -1 to 1
        subjectivity = blob.sentiment.subjectivity  # Range: 0 to 1
        
        # Convert polarity from [-1, 1] to [1, 10]
        sentiment_score = ((polarity + 1) / 2) * 9 + 1
        
        # Determine sentiment label
        if sentiment_score >= 7:
            sentiment_label = "Positive"
        elif sentiment_score >= 4:
            sentiment_label = "Neutral"
        else:
            sentiment_label = "Negative"
        
        return SentimentResponse(
            text=text,
            sentiment_score=round(sentiment_score, 2),
            sentiment_label=sentiment_label,
            polarity=round(polarity, 3),
            subjectivity=round(subjectivity, 3)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing sentiment: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
