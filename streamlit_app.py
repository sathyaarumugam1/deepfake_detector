import streamlit as st
from detector import detect_video, detect_image
import os
import cv2

st.set_page_config(page_title="AI Deepfake Detector", layout="centered")

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- LOGIN ----------------
def login_page():
    st.title("🔐 Sign In")

    username = st.text_input("Username")
    st.markdown("Already have an account? Login")

    if st.button("Login"):
        if username:
            st.session_state.user = username
            st.session_state.page = "home"
            st.rerun()
        else:
            st.error("Enter username")

# ---------------- HOME ----------------
def home_page():
    st.title(f"🤖 Welcome {st.session_state.user}")

    col1, col2 = st.columns(2)

    if col1.button("🎥 Video"):
        st.session_state.page = "video"

    if col2.button("🖼 Image"):
        st.session_state.page = "image"

    if col1.button("🎤 Audio"):
        st.session_state.page = "audio"

    if col2.button("📸 Camera"):
        st.session_state.page = "camera"

    st.markdown("---")

    if st.button("📜 History"):
        st.session_state.page = "history"

    if st.button("🚪 Logout"):
        st.session_state.page = "login"
        st.session_state.history = []
        st.rerun()

# ---------------- VIDEO ----------------
def video_page():
    st.title("🎥 Video Detection")

    file = st.file_uploader("Upload Video", type=["mp4"])

    if file:
        st.video(file)

        path = "temp.mp4"
        with open(path, "wb") as f:
            f.write(file.read())

        if st.button("🔍 Analyze"):
            with st.spinner("Processing Video..."):
                res = detect_video(path)

                st.success("Detected Successfully")

                if res["result"] == "Deepfake":
                    st.error("🚨 Deepfake")
                else:
                    st.success("✅ Real")

                st.progress(res["confidence"] / 100)
                st.write(f"Confidence: {res['confidence']}%")

                st.session_state.history.append(
                    f"Video → {res['result']} ({res['confidence']}%)"
                )

    if st.button("⬅ Back"):
        st.session_state.page = "home"

# ---------------- IMAGE ----------------
def image_page():
    st.title("🖼 Image Detection")

    file = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])

    if file:
        st.image(file)

        path = "temp.jpg"
        with open(path, "wb") as f:
            f.write(file.read())

        if st.button("🔍 Analyze"):
            with st.spinner("Processing Image..."):
                res = detect_image(path)

                st.success("Detected Successfully")

                if res["result"] == "Deepfake":
                    st.error("🚨 Deepfake")
                else:
                    st.success("✅ Real")

                st.progress(res["confidence"] / 100)
                st.write(f"Confidence: {res['confidence']}%")

                st.session_state.history.append(
                    f"Image → {res['result']} ({res['confidence']}%)"
                )

    if st.button("⬅ Back"):
        st.session_state.page = "home"

# ---------------- AUDIO ----------------
def audio_page():
    st.title("🎤 Audio Detection")

    file = st.file_uploader("Upload Audio", type=["mp3","wav"])

    if file:
        st.audio(file)

        if st.button("🔍 Analyze"):
            st.success("Detected Successfully")
            st.warning("Demo Mode")

            result = "Real"
            confidence = 80

            st.success("✅ Real Voice")
            st.progress(confidence / 100)
            st.write(f"Confidence: {confidence}%")

            st.session_state.history.append(
                f"Audio → {result} ({confidence}%)"
            )

    if st.button("⬅ Back"):
        st.session_state.page = "home"

# ---------------- CAMERA ----------------
def camera_page():
    st.title("📸 Camera Detection")

    if st.button("Capture"):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if ret:
            st.image(frame, channels="BGR")

            path = "cam.jpg"
            cv2.imwrite(path, frame)

            res = detect_image(path)

            st.success("Detected Successfully")

            if res["result"] == "Deepfake":
                st.error("🚨 Deepfake")
            else:
                st.success("✅ Real")

            st.progress(res["confidence"] / 100)
            st.write(f"Confidence: {res['confidence']}%")

            st.session_state.history.append(
                f"Camera → {res['result']} ({res['confidence']}%)"
            )

    if st.button("⬅ Back"):
        st.session_state.page = "home"

# ---------------- HISTORY ----------------
def history_page():
    st.title("📜 History")

    if len(st.session_state.history) == 0:
        st.info("No history yet")
    else:
        for item in reversed(st.session_state.history):
            st.write(item)

    if st.button("⬅ Back"):
        st.session_state.page = "home"

# ---------------- ROUTER ----------------
if st.session_state.page == "login":
    login_page()

elif st.session_state.page == "home":
    home_page()

elif st.session_state.page == "video":
    video_page()

elif st.session_state.page == "image":
    image_page()

elif st.session_state.page == "audio":
    audio_page()

elif st.session_state.page == "camera":
    camera_page()

elif st.session_state.page == "history":
    history_page()