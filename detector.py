import cv2
import numpy as np
from model import predict_frame

# ---------------- IMAGE ----------------
def detect_image(image):
    try:
        label, confidence = predict_frame(image)
        return label, confidence
    except Exception as e:
        print("Image Error:", e)
        return "ERROR", 0.0


# ---------------- VIDEO ----------------
def detect_video(video_path):
    cap = cv2.VideoCapture(video_path)

    confidences = []

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Optional resize for speed
            frame = cv2.resize(frame, (224, 224))

            label, confidence = predict_frame(frame)

            # 🔥 ONLY store numbers (fix for numpy error)
            confidences.append(float(confidence))

        cap.release()

        # ❌ No frames case
        if len(confidences) == 0:
            return "ERROR", 0.0

        # ✅ Average confidence
        avg_conf = np.mean(confidences)

        # ✅ Final decision
        if avg_conf > 50:
            return "FAKE", round(avg_conf, 2)
        else:
            return "REAL", round(100 - avg_conf, 2)

    except Exception as e:
        print("Video Error:", e)
        return "ERROR", 0.0