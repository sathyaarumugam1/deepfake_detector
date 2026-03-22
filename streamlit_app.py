import streamlit as st
import cv2
import numpy as np

# Updated detect_image function with error handling
def detect_image(image):
    try:
        # Your existing image detection logic here
        st.success('Image processed successfully!')
    except Exception as e:
        st.error(f'Error processing image: {e}') 

# Updated detect_video function with error handling
def detect_video(video):
    try:
        # Your existing video detection logic here
        st.success('Video processed successfully!')
    except Exception as e:
        st.error(f'Error processing video: {e}') 

# Streamlit UI
st.title('Deepfake Detector')

option = st.selectbox('Select Mode:', ['Image', 'Video'])

if option == 'Image':
    uploaded_file = st.file_uploader('Choose an image...', type=['jpg', 'jpeg', 'png'])
    if uploaded_file is not None:
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
        detect_image(image)

else:
    uploaded_file = st.file_uploader('Choose a video...', type=['mp4', 'mov', 'avi'])
    if uploaded_file is not None:
        video = cv2.VideoCapture(uploaded_file)
        detect_video(video)
        video.release()  
