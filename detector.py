# detector.py

import os
import gdown
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from mtcnn import MTCNN

# ----------------------------
# Model download from Google Drive
# ----------------------------
MODEL_PATH = "deepfake_model.h5"
MODEL_FILE_ID = "YOUR_FILE_ID_HERE"  # replace with your Google Drive file ID
MODEL_URL = f"https://drive.google.com/uc?id={MODEL_FILE_ID}"

if not os.path.exists(MODEL_PATH):
    print("Downloading deepfake model from Google Drive...")
    gdown.download(MODEL_URL, MODEL_PATH, quiet=False)

# ----------------------------
# Load model
# ----------------------------
model = load_model(MODEL_PATH)
detector = MTCNN()

# ----------------------------
# Image detection function
# ----------------------------
def detect_image(image_path):
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(img_rgb)

    results = []
    for face in faces:
        x, y, w, h = face['box']
        face_img = img_rgb[y:y+h, x:x+w]
        face_img_resized = cv2.resize(face_img, (224, 224)) / 255.0
        face_input = np.expand_dims(face_img_resized, axis=0)
        pred = model.predict(face_input)
        label = "Deepfake" if pred[0][0] > 0.5 else "Real"
        results.append({
            "box": (x, y, w, h),
            "label": label,
            "confidence": float(pred[0][0])
        })
    return results

# ----------------------------
# Video detection function
# ----------------------------
def detect_video(video_path, output_path="output.mp4"):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = detector.detect_faces(img_rgb)
        for face in faces:
            x, y, w, h = face['box']
            face_img = img_rgb[y:y+h, x:x+w]
            face_img_resized = cv2.resize(face_img, (224, 224)) / 255.0
            face_input = np.expand_dims(face_img_resized, axis=0)
            pred = model.predict(face_input)
            label = "Deepfake" if pred[0][0] > 0.5 else "Real"
            color = (0, 0, 255) if label == "Deepfake" else (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, f"{label} {pred[0][0]:.2f}", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        out.write(frame)

    cap.release()
    out.release()
    return output_path