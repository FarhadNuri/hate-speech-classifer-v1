from flask import Flask, request, jsonify, render_template
from huggingface_hub import hf_hub_download
import pickle
import re
import numpy as np
import pandas as pd
from scipy.sparse import hstack
import os

app = Flask(__name__)

# Global variables for model artifacts
tfidf_word = None
tfidf_char = None
label_encoder = None
model = None

REPO_ID = "nuri63/bengali-hate-classifier"

def load_model():
    """Load model and artifacts from Hugging Face"""
    global tfidf_word, tfidf_char, label_encoder, model
    
    print("Loading model artifacts from Hugging Face...")
    
    # Download files from HF
    model_path = hf_hub_download(repo_id=REPO_ID, filename="best_model.pkl")
    word_vec_path = hf_hub_download(repo_id=REPO_ID, filename="tfidf_word_vectorizer.pkl")
    char_vec_path = hf_hub_download(repo_id=REPO_ID, filename="tfidf_char_vectorizer.pkl")
    label_enc_path = hf_hub_download(repo_id=REPO_ID, filename="label_encoder.pkl")
    
    # Load pickled objects
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(word_vec_path, 'rb') as f:
        tfidf_word = pickle.load(f)
    with open(char_vec_path, 'rb') as f:
        tfidf_char = pickle.load(f)
    with open(label_enc_path, 'rb') as f:
        label_encoder = pickle.load(f)
    
    print(f"Model loaded successfully!")
    print(f"Word vectorizer features: {len(tfidf_word.vocabulary_)}")
    print(f"Char vectorizer features: {len(tfidf_char.vocabulary_)}")



def clean_text(text):
    """Clean Bengali text"""
    text = str(text)
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    text = re.sub(r'@\w+', ' ', text)
    text = re.sub(r'[^\u0980-\u09FF0-9\s.,!?;:()\-\u200C\u200D]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

def predict_text(text):
    """Predict hate speech classification"""
    cleaned = clean_text(text)
    
    # Transform text
    w = tfidf_word.transform([cleaned])
    c = tfidf_char.transform([cleaned])
    
    # Get actual feature counts
    n_word = w.shape[1]
    n_char = c.shape[1]
    total_features = n_word + n_char
    
    print(f"Debug: Word features={n_word}, Char features={n_char}, Total={total_features}")
    
    # The model expects 8000 features (5000 word + 3000 char)
    # But uploaded vectorizers give 15000 (10000 word + 5000 char)
    # We need to truncate to match
    if total_features > 8000:
        # Truncate word features to 5000 and char features to 3000
        w_truncated = w[:, :5000]
        c_truncated = c[:, :3000]
        X = hstack([w_truncated, c_truncated])
    else:
        X = hstack([w, c])
    
    # Convert to DataFrame with feature names
    feature_names = [f'word_{i}' for i in range(min(5000, n_word))] + \
                    [f'char_{i}' for i in range(min(3000, n_char))]
    
    X_df = pd.DataFrame(X.toarray(), columns=feature_names)
    
    # Get predictions
    probas = model.predict_proba(X_df)[0]
    pred_class = model.predict(X_df)[0]
    
    # Map class numbers to names
    class_names = {
        'Geopolitical': 'Geopolitical',
        'Personal': 'Personal',
        'Political': 'Political',
        'Religious': 'Religious'
    }
    
    # Get the predicted class name
    pred_class_name = label_encoder.classes_[pred_class]
    
    # Format results
    results = []
    for cls, score in zip(label_encoder.classes_, probas):
        results.append({
            "label": cls,  # Use the actual class name
            "score": float(score)
        })
    
    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return {
        "prediction": pred_class_name,  # Return class name instead of number
        "all_scores": results
    }

@app.route('/')
def home():
    """Render the UI"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for predictions"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        result = predict_text(text)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    load_model()
    app.run(debug=True, host='0.0.0.0', port=5000)
