import cv2
from model import predict_frame

# 🎥 VIDEO DETECTION
def detect_video(video_path):
    cap = cv2.VideoCapture(video_path)
    preds = []

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # 🔥 speed optimization (skip frames)
        if frame_count % 30 != 0:
            continue

        p = predict_frame(frame)
        if p is not None:
            preds.append(p)

    cap.release()

    if len(preds) == 0:
        return {"result": "No face detected", "confidence": 0}

    avg = sum(preds) / len(preds)

    print("AI Score:", avg)

    if avg > 0.6:
        return {"result": "Deepfake", "confidence": int(avg * 100)}
    else:
        return {"result": "Real", "confidence": int((1 - avg) * 100)}


# 🖼️ IMAGE DETECTION
def detect_image(image_path):
    try:
        print("Reading image...")

        import cv2
        img = cv2.imread(image_path)

        if img is None:
            return {"result": "Error", "confidence": 0}

        img = cv2.resize(img, (224, 224))

        print("Running prediction...")

        p = predict_frame(img)

        print("Prediction:", p)

        if p > 0.6:
            return {"result": "Deepfake", "confidence": int(p * 100)}
        else:
            return {"result": "Real", "confidence": int((1 - p) * 100)}

    except Exception as e:
        print("ERROR:", e)
        return {"result": "Error", "confidence": 0}