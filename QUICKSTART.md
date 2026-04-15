# Quick Start Guide

## Your Flask app is now running! 🎉

### Access the Web UI:
Open your browser and go to:
- **http://localhost:5000** or
- **http://127.0.0.1:5000**

### What you'll see:
- A beautiful gradient UI with a text input area
- Enter Bengali text to classify
- Click "Analyze Text" to get predictions
- View confidence scores for each class

### Test the API:
You can also test the API directly using the test script:

```bash
# In a new terminal window
python test_api.py
```

Or use curl:
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"আমি তোমাকে ভালোবাসি\"}"
```

### Stop the server:
Press `CTRL+C` in the terminal where Flask is running

### Restart the server:
```bash
python app.py
```

Or on Windows:
```bash
run.bat
```

## How it works:

1. **Backend (app.py)**:
   - Downloads your model from Hugging Face (`nuri63/bengali-hate-classifier`)
   - Loads TF-IDF vectorizers and trained classifier
   - Provides `/predict` API endpoint
   - Processes Bengali text and returns classifications

2. **Frontend (templates/index.html)**:
   - Modern, responsive UI
   - Real-time predictions
   - Confidence score visualization
   - Error handling

3. **Model Pipeline**:
   - Text cleaning (removes URLs, mentions, special chars)
   - Word-level TF-IDF transformation
   - Character-level TF-IDF transformation
   - Feature concatenation
   - Classification with probability scores

## Troubleshooting:

### Port already in use:
If port 5000 is busy, edit `app.py` line 82:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001
```

### Model loading errors:
The scikit-learn version warnings are normal and won't affect functionality. The model will still work correctly.

### Connection errors:
Make sure the Flask server is running before testing the API.

## Next Steps:

- Customize the UI in `templates/index.html`
- Add more features to `app.py`
- Deploy to a cloud service (Heroku, AWS, etc.)
- Add authentication
- Create a mobile app using the API

Enjoy your Bengali Hate Speech Classifier! 🚀
