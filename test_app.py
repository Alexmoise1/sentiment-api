"""
Unit tests for Sentiment Analysis API
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Sentiment Analysis API" in response.json()["message"]

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_analyze_positive_sentiment():
    """Test positive sentiment analysis"""
    response = client.post(
        "/analyze",
        json={"text": "I love this product! It's amazing and wonderful!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment_score"] >= 7
    assert data["sentiment_label"] == "Positive"

def test_analyze_negative_sentiment():
    """Test negative sentiment analysis"""
    response = client.post(
        "/analyze",
        json={"text": "This is terrible and awful. I hate it!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment_score"] < 4
    assert data["sentiment_label"] == "Negative"

def test_analyze_neutral_sentiment():
    """Test neutral sentiment analysis"""
    response = client.post(
        "/analyze",
        json={"text": "The sky is blue."}
    )
    assert response.status_code == 200
    data = response.json()
    assert 4 <= data["sentiment_score"] < 7
    assert data["sentiment_label"] == "Neutral"

def test_analyze_empty_text():
    """Test empty text input"""
    response = client.post(
        "/analyze",
        json={"text": ""}
    )
    assert response.status_code == 400

def test_analyze_missing_text():
    """Test missing text field"""
    response = client.post("/analyze", json={})
    assert response.status_code == 422

def test_sentiment_score_range():
    """Test that sentiment score is within valid range"""
    test_texts = [
        "Absolutely fantastic!",
        "This is okay.",
        "Completely horrible!"
    ]
    
    for text in test_texts:
        response = client.post("/analyze", json={"text": text})
        assert response.status_code == 200
        score = response.json()["sentiment_score"]
        assert 1 <= score <= 10, f"Score {score} out of range for text: {text}"

def test_response_structure():
    """Test response contains all required fields"""
    response = client.post(
        "/analyze",
        json={"text": "This is a test"}
    )
    assert response.status_code == 200
    data = response.json()
    
    # Check all required fields exist
    assert "text" in data
    assert "sentiment_score" in data
    assert "sentiment_label" in data
    assert "polarity" in data
    assert "subjectivity" in data
    
    # Check data types
    assert isinstance(data["text"], str)
    assert isinstance(data["sentiment_score"], (int, float))
    assert isinstance(data["sentiment_label"], str)
    assert isinstance(data["polarity"], (int, float))
    assert isinstance(data["subjectivity"], (int, float))
