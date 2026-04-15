"""
Script to re-upload the correct vectorizers to HuggingFace

The issue: The best_model.pkl was trained with vectorizers that have:
- Word TF-IDF: max_features=5000
- Char TF-IDF: max_features=3000
- Total: 8000 features

But the uploaded vectorizers have:
- Word TF-IDF: max_features=10000
- Char TF-IDF: max_features=5000
- Total: 15000 features

This script will:
1. Load your dataset
2. Create the correct vectorizers (5000 + 3000)
3. Fit them on your training data
4. Upload them to HuggingFace
"""

import os
import pickle
import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from huggingface_hub import HfApi

# Configuration
DATASET_PATH = "/content/drive/MyDrive/BN_Fact_Check_Model/bengali_hate_v2.0.csv"  # Colab path
# Or if running locally, update to your local path:
# DATASET_PATH = "D:/path/to/bengali_hate_v2.0.csv"

HF_TOKEN = "YOUR_HF_TOKEN_HERE"  # Replace with your actual token
REPO_ID = "nuri63/bengali-hate-classifier"
RS = 42

print("=" * 80)
print("FIXING HUGGINGFACE MODEL - UPLOADING CORRECT VECTORIZERS")
print("=" * 80)

# Check if dataset exists
if not os.path.exists(DATASET_PATH):
    print(f"\n❌ ERROR: Dataset not found at {DATASET_PATH}")
    print("\nPlease update DATASET_PATH in this script to point to your CSV file.")
    print("The file should be: bengali_hate_v2.0.csv")
    exit(1)

# Load dataset
print("\n[1/5] Loading dataset...")
df = pd.read_csv(DATASET_PATH)
print(f"  Loaded {len(df)} samples")

# Clean text function (same as in notebook)
def clean(t):
    t = str(t)
    t = re.sub(r'https?://\S+', ' ', t)
    t = re.sub(r'@\w+', ' ', t)
    t = re.sub(r'[^ঀ-৿0-9\s.,!?;:()-]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

print("\n[2/5] Cleaning text...")
df['cleaned'] = df['text'].apply(clean)

# Encode labels
print("\n[3/5] Encoding labels...")
le = LabelEncoder()
y = le.fit_transform(df['label'].astype(str))
print(f"  Classes: {list(le.classes_)}")

# Split data (same as in notebook)
print("\n[4/5] Splitting data...")
X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    df['cleaned'].values, y, test_size=0.2, stratify=y, random_state=RS
)
print(f"  Train: {len(X_train_raw)}, Test: {len(X_test_raw)}")

# Create CORRECT vectorizers (matching the model training)
print("\n[5/5] Creating and fitting correct vectorizers...")
print("  Word TF-IDF: max_features=5000, ngram_range=(1,2)")
tw = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), sublinear_tf=True)
tw.fit(X_train_raw)
print(f"    ✓ Word vectorizer fitted with {len(tw.vocabulary_)} features")

print("  Char TF-IDF: max_features=3000, ngram_range=(2,5)")
tc = TfidfVectorizer(max_features=3000, ngram_range=(2, 5), analyzer='char', sublinear_tf=True)
tc.fit(X_train_raw)
print(f"    ✓ Char vectorizer fitted with {len(tc.vocabulary_)} features")

total_features = len(tw.vocabulary_) + len(tc.vocabulary_)
print(f"\n  Total features: {total_features} (should be ~8000)")

# Save locally
print("\n[6/6] Saving vectorizers locally...")
os.makedirs("fixed_vectorizers", exist_ok=True)

with open("fixed_vectorizers/tfidf_word_vectorizer.pkl", 'wb') as f:
    pickle.dump(tw, f)
print("  ✓ Saved: fixed_vectorizers/tfidf_word_vectorizer.pkl")

with open("fixed_vectorizers/tfidf_char_vectorizer.pkl", 'wb') as f:
    pickle.dump(tc, f)
print("  ✓ Saved: fixed_vectorizers/tfidf_char_vectorizer.pkl")

# Upload to HuggingFace
print("\n[7/7] Uploading to HuggingFace...")
api = HfApi(token=HF_TOKEN)

try:
    print("  Uploading word vectorizer...")
    api.upload_file(
        path_or_fileobj="fixed_vectorizers/tfidf_word_vectorizer.pkl",
        path_in_repo="tfidf_word_vectorizer.pkl",
        repo_id=REPO_ID
    )
    print("  ✓ Word vectorizer uploaded")
    
    print("  Uploading char vectorizer...")
    api.upload_file(
        path_or_fileobj="fixed_vectorizers/tfidf_char_vectorizer.pkl",
        path_in_repo="tfidf_char_vectorizer.pkl",
        repo_id=REPO_ID
    )
    print("  ✓ Char vectorizer uploaded")
    
    print("\n" + "=" * 80)
    print("✅ SUCCESS! Correct vectorizers uploaded to HuggingFace")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Restart your Flask app (it will download the new vectorizers)")
    print("2. Test the predictions - they should now work correctly!")
    print("3. The model should now classify different hate speech types properly")
    
except Exception as e:
    print(f"\n❌ ERROR uploading to HuggingFace: {e}")
    print("\nThe vectorizers are saved locally in 'fixed_vectorizers/' folder")
    print("You can manually upload them to HuggingFace if needed")

print("\n" + "=" * 80)
