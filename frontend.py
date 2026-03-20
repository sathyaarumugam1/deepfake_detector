import streamlit as st
import requests

st.set_page_config(page_title="Deepfake Detection")

# -------- SESSION --------
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "signup"

# -------- SIGNUP --------
def signup():
    st.title("Signup")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Create an account"):
        if user and pwd:
            st.session_state.users[user] = pwd
            st.session_state.page = "login"
            st.rerun()

    if st.button("Login"):
        st.session_state.page = "login"
        st.rerun()

# -------- LOGIN --------
def login():
    st.title("Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user in st.session_state.users and st.session_state.users[user] == pwd:
            st.session_state.logged_in = True
            st.session_state.username = user
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("Invalid credentials")

# -------- DASHBOARD --------
def dashboard():
    st.title("Deepfake Detection")

    st.write(f"Welcome {st.session_state.username}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Image"):
            st.session_state.page = "image"
            st.rerun()

        if st.button("Video"):
            st.session_state.page = "video"
            st.rerun()

    with col2:
        if st.button("Audio"):
            st.session_state.page = "audio"
            st.rerun()

        if st.button("Camera"):
            st.session_state.page = "camera"
            st.rerun()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

# -------- IMAGE --------
def image_page():
    st.title("Image Detection")

    file = st.file_uploader("Upload Image")

    if file:
        st.image(file)

        if st.button("Analyze"):
            res = requests.post(
                "http://127.0.0.1:5000/analyze_image",
                files={"file": (file.name, file, file.type)}
            )

            if res.status_code == 200:
                data = res.json()

                if data["result"] == "Real":
                    st.success(f"Real ✅ ({data['confidence']}%)")
                elif data["result"] == "Deepfake":
                    st.error(f"Deepfake ❌ ({data['confidence']}%)")
                else:
                    st.warning(f"Uncertain ⚠️ ({data['confidence']}%)")
            else:
                st.error("Error")

    if st.button("Back"):
        st.session_state.page = "dashboard"
        st.rerun()

# -------- VIDEO --------
def video_page():
    st.title("Video Detection")

    file = st.file_uploader("Upload Video")

    if file:
        st.video(file)

        if st.button("Analyze"):
            res = requests.post(
                "http://127.0.0.1:5000/analyze_video",
                files={"file": (file.name, file, file.type)}
            )

            if res.status_code == 200:
                data = res.json()

                if data["result"] == "Real":
                    st.success(f"Real ✅ ({data['confidence']}%)")
                elif data["result"] == "Deepfake":
                    st.error(f"Deepfake ❌ ({data['confidence']}%)")
                else:
                    st.warning(f"Uncertain ⚠️ ({data['confidence']}%)")
            else:
                st.error("Error")

    if st.button("Back"):
        st.session_state.page = "dashboard"
        st.rerun()

# -------- AUDIO --------
def audio_page():
    st.title("Voice Detection")

    audio = st.audio_input("Record your voice")

    if audio:
        st.audio(audio)

        if st.button("Analyze Voice"):
            res = requests.post(
                "http://127.0.0.1:5000/analyze_audio",
                files={"file": ("voice.wav", audio.getvalue(), "audio/wav")}
            )

            data = res.json()

            if data["result"] == "Real":
                st.success(f"Real ✅ ({data['confidence']}%)")
            elif data["result"] == "Deepfake":
                st.error(f"Deepfake ❌ ({data['confidence']}%)")
            else:
                st.warning(f"Uncertain ⚠️ ({data['confidence']}%)")
                    
# -------- CAMERA --------
def camera_page():
    st.title("Camera Detection")

    img = st.camera_input("Take Photo")

    if img:
        st.image(img)

        with st.spinner("Analyzing..."):
            predictions = []

            for i in range(3):
                res = requests.post(
                    "http://127.0.0.1:5000/analyze_image",
                    files={"file": ("cam.jpg", img.getvalue(), "image/jpeg")}
                )

                data = res.json()
                predictions.append(data["confidence"])

            avg_conf = sum(predictions) / len(predictions)

            if avg_conf > 75:
                st.success(f"Real ✅ ({round(avg_conf,2)}%)")
            elif avg_conf < 45:
                st.error(f"Deepfake ❌ ({round(avg_conf,2)}%)")
            else:
                st.warning(f"Uncertain ⚠️ ({round(avg_conf,2)}%)")

    if st.button("Back"):
        st.session_state.page = "dashboard"
        st.rerun()       
# -------- NAV --------
if not st.session_state.logged_in:
    if st.session_state.page == "signup":
        signup()
    else:
        login()
else:
    if st.session_state.page == "dashboard":
        dashboard()
    elif st.session_state.page == "image":
        image_page()
    elif st.session_state.page == "video":
        video_page()
    elif st.session_state.page == "audio":
        audio_page()
    elif st.session_state.page == "camera":
        camera_page()
