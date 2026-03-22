import os
import cv2
import gdown
import numpy as np
import tempfile
from tensorflow.keras.models import load_model

# Model setup
MODEL_PATH = "deepfake_model.h5"
MODEL_FILE_ID = "1o64GzF0J6s4cTKI0vnrkkjgEdZxa6CZp"
MODEL_URL = f"https://drive.google.com/uc?id={MODEL_FILE_ID}"

if not os.path.exists(MODEL_PATH):
    print("Downloading deepfake model from Google Drive...")
    try:
        gdown.download(MODEL_URL, MODEL_PATH, quiet=False)
    except Exception as e:
        print(f"Error downloading model: {e}")

try:
    model = load_model(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def detect_image(image_path):
    if model is None:
        return None, "Model not loaded"
    
    try:
        img = cv2.imread(image_path)
        if img is None:
            return None, "Failed to read image"
            
        img = cv2.resize(img, (224, 224))
        img = img.astype("float32") / 255.0
        img_normalized = np.expand_dims(img, axis=0)
        pred = model.predict(img_normalized)[0][0]
        prediction = "Fake" if pred > 0.5 else "Real"
        
        result_img = (img * 255).astype(np.uint8)
        result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
        
        return result_img, prediction
    except Exception as e:
        print(f"Error in detect_image: {e}")
        return None, f"Error: {str(e)}"

def detect_video(video_path):
    if model is None:
        return None, "Model not loaded", 0, 0
    
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return None, "Failed to read video", 0, 0
            
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        output_path = tempfile.mktemp(suffix=".mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_results = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            img = cv2.resize(frame, (224, 224))
            img = img.astype("float32") / 255.0
            img_normalized = np.expand_dims(img, axis=0)
            pred = model.predict(img_normalized)[0][0]
            prediction = "Fake" if pred > 0.5 else "Real"
            
            color = (0, 0, 255) if prediction == "Fake" else (0, 255, 0)
            cv2.putText(frame, prediction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 2)
            
            out.write(frame)
            frame_results.append(prediction)
        
        cap.release()
        out.release()
        
        fake_count = frame_results.count("Fake")
        real_count = frame_results.count("Real")
        overall_prediction = "Likely Fake" if fake_count > real_count else "Likely Real"
        
        return output_path, overall_prediction, fake_count, real_count
    except Exception as e:
        print(f"Error in detect_video: {e}")
        return None, f"Error: {str(e)}", 0, 0
