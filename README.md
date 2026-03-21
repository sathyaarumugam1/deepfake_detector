Deepfake Detector AI

Real-time Deepfake Image & Video Detection Web Application using AI.

Description

This project is a Deepfake Detection web application built with Streamlit and TensorFlow.
It can detect whether an uploaded image or video is real or fake and provides a confidence percentage.
The model is automatically downloaded if not present.

Features

- Detects real or deepfake images.
- Detects real or deepfake videos.
- Displays confidence (%) for predictions.
- Automatic download of deepfake_model.h5 from Google Drive.
- Simple Streamlit web app interface for easy upload and analysis.

Repository Files

- model.py         → Loads the model & predicts on frames.
- detector.py      → Handles image & video detection.
- streamlit_app.py → Streamlit app interface.
- requirements.txt → Required packages with stable versions.
- README.md        → Project overview.

Installation

1. Clone the repository:
   git clone https://github.com/sathyaarumugam1/repo.git
   cd repo

2. Install required packages:
   pip install -r requirements.txt

3. Run the app:
   streamlit run streamlit_app.py

Usage

1. Open the Streamlit app.
2. Choose "Image" or "Video".
3. Upload your file.
   - For images: prediction appears immediately.
   - For videos: click Analyze Video button.
4. Check prediction (Real / Fake) and confidence %.

Model

- The deepfake model (deepfake_model.h5) is automatically downloaded from Google Drive if not present.
- Google Drive link: https://drive.google.com/file/d/1o64GzF0J6s4cTKI0vnrkkjgEdZxa6CZp/view?usp=sharing

Note: Model file too large for GitHub → use above link.

Live App

- Deployed on Streamlit 

Requirements (Fixed Versions)

- streamlit==1.55.0
- tensorflow==2.13.0
- opencv-python-headless==4.8.1.78
- numpy==1.25.2
- pillow==10.1.0
- gdown==5.2.1

Author

- Sathya Arumugam
