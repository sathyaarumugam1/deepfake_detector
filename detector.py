import os
import cv2
import gdown
import numpy as np
import tempfile
from tensorflow.keras.models import load_model

# -----------------------------
# Model setup
# -----------------------------
MODEL_PATH = "deepfake_model.h5"
MODEL_FILE_ID = "1o64GzF0J6s4cTKI0vnrkkjgEdZxa6CZp"  # Replace with your Google Drive file ID
MODEL_URL = f"https://drive.google.com/uc?id=1o64GzF0J6s4cTKI0vnrkkjgEdZxa6CZp"

if not os.path.exists(MODEL_PATH):
    print("Downloading deepfake model from Google Drive...")
    gdown.download(MODEL_URL, MODEL_PATH, quiet=False)

# Load model
model = load_model(MODEL_PATH)

# -----------------------------
# Detection functions
# -----------------------------
def detect_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))  # Resize to model input
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)
    pred = model.predict(img)[0][0]
    return "Fake" if pred > 0.5 else "Real"

def detect_video(video_path):
    cap = cv2.VideoCapture(video_path)
    results = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        img = cv2.resize(frame, (224, 224))
        img = img.astype("float32") / 255.0
        img = np.expand_dims(img, axis=0)
        pred = model.predict(img)[0][0]
        results.append("Fake" if pred > 0.5 else "Real")

    cap.release()
    return results