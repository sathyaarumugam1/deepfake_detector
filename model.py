import os
import gdown
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Model file path
MODEL_PATH = "deepfake_model.h5"

# 🔥 Auto download model if not present
if not os.path.exists(MODEL_PATH):
    print("Downloading model...")
    url = "https://drive.google.com/uc?id=1o64GzF0J6s4cTKI0vnrkkjgEdZxa6CZp"
    gdown.download(url, MODEL_PATH, quiet=False)

# Load model
model = load_model(MODEL_PATH)

# ✅ Prediction function
def predict_frame(frame):
    try:
        # Resize frame to match model input
        frame = cv2.resize(frame, (224, 224))
        
        # Normalize
        frame = frame / 255.0
        
        # Reshape for model
        frame = np.reshape(frame, (1, 224, 224, 3))

        # Prediction
        prediction = model.predict(frame)[0][0]

        # Convert to percentage
        if prediction > 0.5:
            label = "FAKE"
            confidence = float(prediction * 100)
        else:
            label = "REAL"
            confidence = float((1 - prediction) * 100)

        return label, round(confidence, 2)

    except Exception as e:
        print("❌ Prediction Error:", e)
        return "ERROR", 0.0