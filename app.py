import os
import logging
import joblib
import numpy as np
from flask import Flask, request, jsonify
from utils.text_preprocessing import preprocess_text

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model components
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'training_script/models')
MODEL_PATH = os.path.join(MODEL_DIR, 'best_model.joblib')
VECTORIZER_PATH = os.path.join(MODEL_DIR, 'vectorizer.joblib')
ENCODER_PATH = os.path.join(MODEL_DIR, 'label_encoder.joblib')

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)
label_encoder = joblib.load(ENCODER_PATH)

# Root route (for basic testing in browser)
@app.route('/')
def home():
    return jsonify({"message": "Sentiment prediction API is running."}), 200

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'Missing "text" field in request.'}), 400

    text = data['text']

    if not isinstance(text, str) or not text.strip():
        return jsonify({'error': 'Text must be a non-empty string.'}), 400

    logger.info(f"Received input text: {text}")

    try:
        # Preprocess and vectorize
        cleaned_text = preprocess_text(text)
        vector = vectorizer.transform([cleaned_text])

        # Predict and decode label
        prediction_encoded = model.predict(vector)[0]
        prediction_label = label_encoder.inverse_transform([prediction_encoded])[0]

        # Get confidence score
        probabilities = model.predict_proba(vector)[0]
        confidence = float(np.max(probabilities))

        logger.info(f"Prediction: {prediction_label}, Confidence: {confidence:.4f}")

        response = {
            'predicted_sentiment': prediction_label,
            'confidence_score': round(confidence, 4)
        }

        return jsonify(response), 200

    except Exception as e:
        logger.exception("Prediction error")
        return jsonify({'error': 'Internal server error.'}), 500

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8501)
