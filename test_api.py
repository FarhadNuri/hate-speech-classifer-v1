import requests
import json

# Test the API endpoint
def test_prediction():
    url = "http://localhost:5000/predict"
    
    # Sample Bengali text
    test_texts = [
        "আমি তোমাকে ভালোবাসি",  # I love you
        "তুমি খুব ভালো মানুষ",    # You are a very good person
    ]
    
    print("Testing API endpoint...\n")
    
    for text in test_texts:
        print(f"Testing text: {text}")
        
        response = requests.post(
            url,
            json={"text": text},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Prediction: {result['prediction']}")
            print("Scores:")
            for score in result['all_scores']:
                print(f"  Class {score['label']}: {score['score']:.4f}")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
        
        print("-" * 50)

if __name__ == "__main__":
    print("Make sure the Flask app is running on http://localhost:5000")
    print("Run: python app.py\n")
    
    try:
        test_prediction()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server.")
        print("Please make sure the Flask app is running.")
