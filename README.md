# Bengali Hate Speech Classifier

A web application that classifies Bengali text into four categories of hate speech: Geopolitical, Personal, Political, and Religious. The application uses a machine learning model trained on Bengali hate speech data and deployed as a Flask web service.

---

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Exploratory Data Analysis](#exploratory-data-analysis)
4. [Model Architecture](#model-architecture)
5. [Hugging Face](#hugging-face)
6. [Text Vectorization Process](#text-vectorization-process)
7. [How the Backend Works](#how-the-backend-works)
8. [System Architecture](#system-architecture)
9. [Summary](#summary)


---

## Overview

This application analyzes Bengali text and classifies it into one of four hate speech categories:

- **Geopolitical**: Hate speech related to countries, borders, and international relations
- **Personal**: Personal attacks and insults targeting individuals
- **Political**: Hate speech related to political parties and ideologies
- **Religious**: Hate speech based on religious beliefs and communities

The system uses a LightGBM classifier trained on TF-IDF features extracted from Bengali text.

---

## Project Structure

```
bengali-hate-speech-classifier/
├── app.py                     # Flask backend application
├── templates/
│   └── index.html             # Frontend UI
├── charts                     # All project charts
├── EDA_Summary.csv            # EDA results
├── Model_Results.csv          # Result comparison of all models
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── Procfile                   # Process configuration for deployment
├── nixpacks.toml              # Railway build configuration
├── README.md                  # This file
└── .gitignore                 # Git ignore rules
```
---

## Exploratory Data Analysis

### Dataset Overview

The model was trained on the Bengali Hate Speech v2.0 dataset. Before training, we performed comprehensive exploratory data analysis to understand the data characteristics and distribution.

#### Dataset Statistics

| Metric | Value |
|--------|-------|
| Total Samples | 5,698 |
| Duplicate Texts | 0 |
| Number of Classes | 4 |
| Mean Character Count | 90.9 |
| Mean Word Count | 15.9 |
| Mean Word Length | 4.76 characters |
| Character-Label Correlation (Pearson r) | 0.2518 |


### Analysis Performed

#### 1. Class Distribution Analysis

We analyzed the distribution of samples across the four categories using bar charts and pie charts to identify any class imbalance. This helped us understand if certain types of hate speech were more prevalent in the dataset.

**Finding**: The dataset showed some imbalance across classes, which we addressed during training using SMOTE (Synthetic Minority Over-sampling Technique) to ensure the model learns all categories equally well.

#### 2. Text Length Analysis

We examined both character count and word count distributions across all classes using histograms and box plots.

**Key Observations**:
- Texts are relatively short, averaging approximately 16 words per sample
- Average character count is around 91 characters per sample
- Text length varies across different hate speech categories
- Some categories tend to have longer expressions than others

#### 3. Average Word Length Analysis

We computed the mean word length per category to detect vocabulary-level differences between hate speech types.

**Finding**: Word length averages are similar across all classes (approximately 4.76 characters), indicating that morphological complexity is fairly uniform across different types of hate speech. This suggests that word length alone is not a distinguishing feature.

#### 4. Top Bengali Words per Class

We extracted the 20 most frequent Bengali words for each category using Unicode regex patterns. This analysis revealed category-specific vocabulary patterns.

**Finding**: Each category has distinct high-frequency Bengali vocabulary, which confirms that lexical features (word choice) will be highly informative for classification. For example:
- Political hate speech contains more party names and political terms
- Religious hate speech includes more religion-specific vocabulary
- Personal attacks use more direct insult words
- Geopolitical hate speech references countries and borders

#### 5. Text Length vs Label Correlation

We created scatter plots to visualize the relationship between character count and label categories, calculating the Pearson correlation coefficient.

**Finding**: The correlation between text length and label is weak (r = 0.2518), meaning text length alone is not a strong discriminator between hate speech categories. This indicates that the model needs to rely on content (words and patterns) rather than just length.

#### 6. Duplicate Detection

We checked for duplicate texts in the dataset to ensure data quality.

**Finding**: Zero duplicate entries were found, confirming the dataset is clean and no deduplication was needed.

### Impact on Model Design

Based on these EDA findings, we designed our model with:

- **TF-IDF Features**: To capture the distinct vocabulary patterns identified in each category
- **Dual Vectorization**: Both word-level and character-level features to capture semantic meaning and spelling patterns
- **SMOTE Balancing**: To address class imbalance and ensure fair representation
- **LightGBM Classifier**: To handle the high-dimensional sparse features efficiently

---

## Model Architecture

### Machine Learning Pipeline

The classification system uses the following components:

1. **Text Preprocessing**: Cleans Bengali text by removing URLs, mentions, and special characters
2. **Feature Extraction**: Converts text into numerical features using TF-IDF vectorization
3. **Classification**: Uses a LightGBM model to predict the hate speech category
4. **Output**: Returns the predicted class and confidence scores for all categories

### Model Details

- **Algorithm**: LightGBM (Light Gradient Boosting Machine)
- **Features**: 8,000 TF-IDF features (5,000 word-level + 3,000 character-level)
- **Classes**: 4 categories (Geopolitical, Personal, Political, Religious)
- **Training Data**: Bengali hate speech dataset with balanced classes using SMOTE

---

## Hugging Face

We uploaded four essential files to Hugging Face Hub under the repository `nuri63/bengali-hate-classifier`:

### 1. best_model.pkl (932 KB)
- **What it is**: The trained LightGBM classifier model
- **Purpose**: Contains the learned patterns for classifying hate speech
- **Format**: Python pickle file containing the serialized model object

### 2. tfidf_word_vectorizer.pkl (213 KB)
- **What it is**: Word-level TF-IDF vectorizer
- **Purpose**: Converts Bengali words into numerical features
- **Configuration**: 
  - Maximum features: 5,000
  - N-gram range: (1, 2) - captures single words and word pairs
  - Uses sublinear TF scaling

### 3. tfidf_char_vectorizer.pkl (118 KB)
- **What it is**: Character-level TF-IDF vectorizer
- **Purpose**: Converts character sequences into numerical features
- **Configuration**:
  - Maximum features: 3,000
  - N-gram range: (2, 5) - captures character sequences of length 2-5
  - Analyzes character patterns instead of words

### 4. label_encoder.pkl (293 bytes)
- **What it is**: Label encoder for class names
- **Purpose**: Maps between class names and numerical labels
- **Mapping**:
  - 0 → Geopolitical
  - 1 → Personal
  - 2 → Political
  - 3 → Religious

---

## Text Vectorization Process

### Two-Level Vectorization Approach

We used two types of vectorization to capture different aspects of the text:

#### 1. Word-Level TF-IDF Vectorization

**What it does**: Analyzes the importance of words in the text.

**Process**:
1. Splits text into words (tokens)
2. Creates word pairs (bigrams) to capture context
3. Calculates TF-IDF scores:
   - **TF (Term Frequency)**: How often a word appears in the text
   - **IDF (Inverse Document Frequency)**: How unique the word is across all texts
4. Produces 5,000 numerical features

**Example**:
```
Input: "তুমি একজন মূর্খ মানুষ"
Output: [0.0, 0.3, 0.0, 0.8, 0.0, 0.5, ...] (5,000 numbers)
```

#### 2. Character-Level TF-IDF Vectorization

**What it does**: Analyzes patterns in character sequences.

**Process**:
1. Splits text into character sequences (2-5 characters)
2. Captures spelling patterns and morphology
3. Useful for handling misspellings and variations
4. Produces 3,000 numerical features

**Example**:
```
Input: "তুমি"
Character n-grams: ["তু", "তুম", "তুমি", "ুম", "ুমি", "মি"]
Output: [0.0, 0.4, 0.0, 0.6, ...] (3,000 numbers)
```

#### 3. Feature Combination

The final feature vector combines both approaches:
- 5,000 word-level features
- 3,000 character-level features
- **Total: 8,000 features** fed into the model

This dual approach captures both semantic meaning (words) and structural patterns (characters).

---

## How the Backend Works

### Complete Data Flow

```
User Input (Bengali Text)
        ↓
    Frontend (HTML/JavaScript)
        ↓
    HTTP POST Request to /predict
        ↓
    Flask Backend (app.py)
        ↓
    Text Cleaning Function
        ↓
    Download Model Files from Hugging Face (if not cached)
        ↓
    Load Model Components into Memory
        ↓
    Word-Level Vectorization (5,000 features)
        ↓
    Character-Level Vectorization (3,000 features)
        ↓
    Combine Features (8,000 total)
        ↓
    LightGBM Model Prediction
        ↓
    Get Probabilities for All Classes
        ↓
    Format Response (JSON)
        ↓
    Send to Frontend
        ↓
    Display Results to User
```

### Detailed Backend Process

#### Step 1: Model Loading (Happens Once at Startup)

When the application starts, the `load_model()` function:

1. **Downloads files from Hugging Face**:
   ```python
   model_path = hf_hub_download(repo_id="nuri63/bengali-hate-classifier", 
                                 filename="best_model.pkl")
   ```
   - Uses the `huggingface_hub` library
   - Downloads to local cache directory
   - Subsequent runs use cached files (no re-download)

2. **Loads each component**:
   ```python
   with open(model_path, 'rb') as f:
       model = pickle.load(f)
   ```
   - Deserializes pickle files
   - Loads into memory as Python objects
   - Ready for immediate use

#### Step 2: Receiving User Input

When a user submits text:

1. **Frontend sends HTTP POST request**:
   ```javascript
   fetch('/predict', {
       method: 'POST',
       body: JSON.stringify({ text: "আওয়ামী লীগ দেশকে ধ্বংস করে দিয়েছে" })
   })
   ```

2. **Backend receives request**:
   ```python
   @app.route('/predict', methods=['POST'])
   def predict():
       data = request.get_json()
       text = data.get('text', '')
   ```

#### Step 3: Text Preprocessing

The `clean_text()` function processes the input:

```python
def clean_text(text):
    text = str(text)
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    # Remove mentions
    text = re.sub(r'@\w+', ' ', text)
    # Keep only Bengali characters, numbers, and basic punctuation
    text = re.sub(r'[^\u0980-\u09FF0-9\s.,!?;:()-]', ' ', text)
    # Normalize whitespace
    return re.sub(r'\s+', ' ', text).strip()
```

**Example**:
```
Input:  "আওয়ামী লীগ @user দেশকে https://example.com ধ্বংস করে!!!"
Output: "আওয়ামী লীগ দেশকে ধ্বংস করে"
```

#### Step 4: Feature Extraction

The `predict_text()` function vectorizes the text:

```python
# Word-level vectorization
w = tfidf_word.transform([cleaned])  # Shape: (1, 5000)

# Character-level vectorization
c = tfidf_char.transform([cleaned])  # Shape: (1, 3000)

# Combine features
X = hstack([w, c])  # Shape: (1, 8000)
```

#### Step 5: Model Prediction

The LightGBM model processes the features:

```python
# Get probability scores for all classes
probas = model.predict_proba(X_df)[0]  # [0.05, 0.85, 0.07, 0.03]

# Get the predicted class
pred_class = model.predict(X_df)[0]  # 1 (Personal)
```

#### Step 6: Response Formatting

The backend formats the results:

```python
# Map class number to name
pred_class_name = label_encoder.classes_[pred_class]  # "Personal"

# Create response with all scores
results = []
for cls, score in zip(label_encoder.classes_, probas):
    results.append({
        "label": cls,      # "Personal", "Religious", etc.
        "score": float(score)  # 0.85, 0.10, etc.
    })

# Sort by confidence (highest first)
results.sort(key=lambda x: x['score'], reverse=True)

return {
    "prediction": pred_class_name,
    "all_scores": results
}
```

#### Step 7: Sending Response to Frontend

The Flask backend sends JSON response:

```json
{
  "prediction": "Personal",
  "all_scores": [
    {"label": "Personal", "score": 0.8523},
    {"label": "Religious", "score": 0.1012},
    {"label": "Geopolitical", "score": 0.0312},
    {"label": "Political", "score": 0.0153}
  ]
}
```

#### Step 8: Frontend Display

JavaScript receives and displays the results:

```javascript
function displayResult(data) {
    // Show predicted class
    document.getElementById('prediction').textContent = data.prediction;
    
    // Show confidence scores with progress bars
    data.all_scores.forEach(item => {
        const percentage = (item.score * 100).toFixed(2);
        // Create visual bar showing confidence
    });
}
```

---

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         USER BROWSER                        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Frontend (HTML/CSS/JavaScript)            │ │
│  │  - Text input field                                    │ │
│  │  - Analyze button                                      │ │
│  │  - Results display                                     │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ↓ HTTP POST
                              ↓ /predict
┌─────────────────────────────────────────────────────────────┐
│                      FLASK BACKEND (app.py)                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Route: /predict                                       │ │
│  │  - Receives text input                                 │ │
│  │  - Calls predict_text()                                │ │
│  │  - Returns JSON response                               │ │
│  └────────────────────────────────────────────────────────┘ │
│                              ↓                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Function: clean_text()                                │ │
│  │  - Removes URLs, mentions                              │ │
│  │  - Keeps only Bengali characters                       │ │
│  │  - Normalizes whitespace                               │ │
│  └────────────────────────────────────────────────────────┘ │
│                              ↓                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Function: predict_text()                              │ │
│  │  - Vectorizes text (word + char level)                 │ │
│  │  - Calls model.predict_proba()                         │ │
│  │  - Formats results                                     │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ↓
                    Accesses Model Components
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    HUGGING FACE HUB                         │
│  Repository: nuri63/bengali-hate-classifier                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Files:                                                │ │
│  │  - best_model.pkl (LightGBM classifier)                │ │
│  │  - tfidf_word_vectorizer.pkl (Word features)           │ │
│  │  - tfidf_char_vectorizer.pkl (Char features)           │ │
│  │  - label_encoder.pkl (Class mappings)                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                              ↓                              │
│  Downloaded once and cached locally                         │
│  Subsequent requests use cached files                       │
└─────────────────────────────────────────────────────────────┘
```
---

## Summary

This Bengali Hate Speech Classifier represents a complete end-to-end machine learning solution for content moderation. Built on a foundation of 5,698 carefully analyzed Bengali text samples, the system employs a LightGBM classifier with 8,000 TF-IDF features to distinguish between four categories of hate speech: Geopolitical, Personal, Political, and Religious. Through comprehensive exploratory data analysis, we identified distinct vocabulary patterns across categories, leading to our dual vectorization approach that captures both word-level semantics and character-level spelling patterns. The model components are efficiently distributed via Hugging Face Hub, enabling seamless deployment and automatic caching. With a modern, minimalist web interface and Docker-based deployment on Railway, the application provides real-time hate speech classification accessible to users worldwide, serving as a practical tool for content moderation and social media safety.

---

