# Features Overview

## ✨ What's Included

### 🎨 Beautiful UI
- Modern gradient design (purple theme)
- Responsive layout (works on mobile, tablet, desktop)
- Smooth animations and transitions
- Loading states and error handling
- Progress bars for confidence scores

### 🔧 Flask Backend
- RESTful API endpoint (`/predict`)
- Automatic model loading from Hugging Face
- Text preprocessing and cleaning
- Multi-class classification with probabilities
- Error handling and validation

### 🤖 Model Integration
- Downloads model artifacts from HF Hub
- Loads TF-IDF vectorizers (word + character level)
- Loads trained classifier
- Processes Bengali text
- Returns predictions with confidence scores

### 📊 Output Format
The API returns:
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

### 🔒 Text Cleaning
- Removes URLs
- Removes mentions (@username)
- Keeps only Bengali characters, numbers, and basic punctuation
- Normalizes whitespace

### 🚀 Easy Deployment
- Simple requirements.txt
- One-command setup (run.bat)
- Works on Windows, Mac, Linux
- Ready for cloud deployment

## 📱 UI Features

1. **Text Input Area**
   - Large textarea for Bengali text
   - Placeholder text in Bengali
   - Keyboard shortcut (Ctrl+Enter to submit)

2. **Analyze Button**
   - Full-width button
   - Hover effects
   - Disabled state during processing

3. **Loading Indicator**
   - Shows "Analyzing..." message
   - Appears during API call

4. **Results Display**
   - Predicted class highlighted
   - All confidence scores shown
   - Visual progress bars
   - Sorted by confidence (highest first)

5. **Error Handling**
   - Empty text validation
   - API error messages
   - Network error handling

## 🎯 Use Cases

- Content moderation
- Social media monitoring
- Comment filtering
- Research and analysis
- Educational purposes
- API integration with other apps

## 🔄 Workflow

1. User enters Bengali text
2. Clicks "Analyze Text"
3. Frontend sends POST request to `/predict`
4. Backend cleans and processes text
5. Model generates predictions
6. Results displayed with confidence scores
7. User can analyze more text

## 🛠️ Customization Options

- Change color scheme in CSS
- Modify text cleaning rules
- Add authentication
- Implement rate limiting
- Add logging
- Store predictions in database
- Add batch processing
- Create API documentation
- Add more languages
