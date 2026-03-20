import numpy as np
import cv2
from mtcnn import MTCNN
from tensorflow.keras.models import load_model

model = load_model("deepfake_model.h5")
detector = MTCNN()

def predict_frame(frame):
    try:
        faces = detector.detect_faces(frame)

        if not faces:
            return None

        x, y, w, h = faces[0]['box']
        x, y = max(0, x), max(0, y)

        face = frame[y:y+h, x:x+w]

        if face is None or face.size == 0:
            return None

        face = cv2.resize(face, (224, 224))
        face = face / 255.0
        face = np.expand_dims(face, axis=0)

        pred = model.predict(face, verbose=0)[0][0]
        return float(pred)

    except:
        return None