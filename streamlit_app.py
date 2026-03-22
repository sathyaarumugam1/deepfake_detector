# streamlit_app.py
import streamlit as st
import os
import tempfile
import cv2
import numpy as np
from detector import detect_image, detect_video  # Make sure these functions exist in detector.py

# ---------------------------
# Page Setup
# ---------------------------
st.set_page_config(page_title="Deepfake Detector", layout="wide")
st.title("🎈 Deepfake Detector App")
st.write("Upload an image or video and detect deepfake content using AI!")

# ---------------------------
# File Upload
# ---------------------------
st.sidebar.header("Upload Options")
upload_type = st.sidebar.radio("Choose input type:", ["Image", "Video"])

uploaded_file = None
if upload_type == "Image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
elif upload_type == "Video":
    uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])

# ---------------------------
# Process Upload
# ---------------------------
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    if upload_type == "Image":
        st.image(tmp_file_path, caption="Uploaded Image", use_column_width=True)
        st.write("Processing image...")
        result_img = detect_image(tmp_file_path)  # Returns processed image (numpy array)
        st.image(result_img, caption="Detection Result", use_column_width=True)

    elif upload_type == "Video":
        st.video(tmp_file_path)
        st.write("Processing video...")
        result_video_path = detect_video(tmp_file_path)  # Returns path to processed video
        st.video(result_video_path, format="video/mp4")

# ---------------------------
# Footer
# ---------------------------
st.markdown(
    """
    ---
    **Author:** Sathya  
    **Note:** Deepfake detection is AI-based. Accuracy may vary.
    """
)