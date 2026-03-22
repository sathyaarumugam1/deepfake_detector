import streamlit as st
import os
import tempfile
import cv2
import numpy as np
from detector import detect_image, detect_video

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
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Uploaded Image")
            st.image(tmp_file_path, use_column_width=True)
        
        st.write("Processing image...")
        result_img, prediction = detect_image(tmp_file_path)
        
        if result_img is not None:
            with col2:
                st.subheader("Detection Result")
                st.image(result_img, use_column_width=True)
                
                if prediction == "Fake":
                    st.error(f"⚠️ **Prediction: {prediction}**", icon="🚨")
                else:
                    st.success(f"✅ **Prediction: {prediction}**", icon="✔️")
        else:
            st.error(f"Error: {prediction}")

    elif upload_type == "Video":
        st.write("Processing video... This may take a while.")
        output_path, overall_prediction, fake_count, real_count = detect_video(tmp_file_path)
        
        if output_path is not None:
            st.subheader("Detection Result")
            st.video(output_path, format="video/mp4")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Overall", overall_prediction)
            with col2:
                st.metric("Fake Frames", fake_count)
            with col3:
                st.metric("Real Frames", real_count)
        else:
            st.error(f"Error: {overall_prediction}")

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
