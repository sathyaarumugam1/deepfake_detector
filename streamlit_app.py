import streamlit as st
import cv2
import numpy as np
import tempfile
from detector import detect_video, detect_image

st.set_page_config(page_title="Deepfake Detector", layout="centered")

st.title("🔍 Deepfake Detection System")

# Sidebar menu
option = st.sidebar.selectbox(
    "Choose Option",
    ["Image", "Video", "Camera", "Audio"]
)

# ---------------- IMAGE ----------------
if option == "Image":
    st.header("🖼️ Image Detection")

    file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if file:
        file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)

        st.image(img, channels="BGR")

        label, confidence = detect_image(img)

        if label == "FAKE":
            st.error(f"🚨 Deepfake Image ({confidence:.2f}%)")
        else:
            st.success(f"✅ Real Image ({confidence:.2f}%)")


# ---------------- VIDEO ----------------
elif option == "Video":
    st.header("🎥 Video Detection")

    file = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])

    if file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(file.read())

        st.video(file)

        with st.spinner("Processing Video..."):
            label, confidence = detect_video(tfile.name)

        if label == "FAKE":
            st.error(f"🚨 Deepfake Video ({confidence:.2f}%)")
        else:
            st.success(f"✅ Real Video ({confidence:.2f}%)")


# ---------------- CAMERA ----------------
elif option == "Camera":
    st.header("📷 Camera Detection")

    camera = st.camera_input("Capture Image")

    if camera:
        file_bytes = np.asarray(bytearray(camera.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)

        st.image(img, channels="BGR")

        label, confidence = detect_image(img)

        if label == "FAKE":
            st.error(f"🚨 Deepfake ({confidence:.2f}%)")
        else:
            st.success(f"✅ Real ({confidence:.2f}%)")


# ---------------- AUDIO ----------------
elif option == "Audio":
    st.header("🎧 Audio Detection")

    file = st.file_uploader("Upload Audio", type=["wav", "mp3"])

    if file:
        st.audio(file)

        st.warning("⚠️ Audio detection model not implemented yet")