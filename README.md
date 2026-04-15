# Bengali Hate Speech Classifier - Web App

A Flask web application that uses your Hugging Face model to classify Bengali text for hate speech detection.

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask app:
```bash
python app.py
```

3. Open your browser and go to:
```
http://localhost:5000
```

## How It Works

- The Flask backend downloads your model from Hugging Face (`nuri63/bengali-hate-classifier`)
- It loads the TF-IDF vectorizers and trained model
- The UI sends text to the `/predict` endpoint
- The backend processes the text and returns classification results
- Results are displayed with confidence scores for each class

## API Endpoint

**POST /predict**

Request body:
```json
{
  "text": "Your Bengali text here"
}
```

Response:
```json
{
  "prediction": "0",
  "all_scores": [
    {"label": "0", "score": 0.85},
    {"label": "1", "score": 0.10},
    {"label": "2", "score": 0.03},
    {"label": "3", "score": 0.02}
  ]
}
```

## Features

- Clean, modern UI with gradient design
- Real-time text classification
- Confidence scores visualization with progress bars
- Error handling
- Loading states
- Responsive design
