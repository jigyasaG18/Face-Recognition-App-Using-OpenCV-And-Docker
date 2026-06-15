import streamlit as st
import cv2
import numpy as np
import time
import tempfile
import os
import pandas as pd
import base64
from ultralytics import YOLO

st.markdown("""
<style>

/* =========================
   GLOBAL APP
========================= */

.stApp {
    background-color: #f8fafc;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* =========================
   PAGE TITLE FIX (IMPORTANT)
========================= */

/* Streamlit main titles like st.title() */
h1 {
    font-size:34px !important;
    font-weight:800 !important;
    color:#111827 !important;
}

h2 {
    font-size:28px !important;
    font-weight:700 !important;
}

h3 {
    font-size:22px !important;
    font-weight:700 !important;
}

/* =========================
   SECTION TEXT (FIX YOUR ISSUE)
========================= */

/* "Select Mode" + similar labels */
label, .stRadio label, .stFileUploader label {
    font-size:18px !important;
    font-weight:600 !important;
    color:#111827 !important;
}

/* Radio options (Single Image / Batch Images) */
div[role="radiogroup"] label {
    font-size:18px !important;
    font-weight:600 !important;
    color:#111827 !important;
}

/* Force radio container spacing */
div[role="radiogroup"] {
    gap:10px;
}

/* =========================
   FILE UPLOADER FIX
========================= */

/* "Upload an Image" text */
section[data-testid="stFileUploader"] label {
    font-size:18px !important;
    font-weight:600 !important;
}

/* File uploader box text */
section[data-testid="stFileUploader"] div {
    font-size:16px !important;
}

/* =========================
   HOME PAGE TEXT (KEEP BALANCED)
========================= */

.big-title{
    font-size:44px;
    font-weight:800;
    color:#2563eb;
    text-align:center;
    margin-bottom:10px;
}

.sub-title{
    font-size:18px;
    font-weight:500;
    text-align:center;
    color:#475569;
    max-width:900px;
    margin:auto;
    line-height:1.7;
}

/* =========================
   SIDEBAR FIX
========================= */

section[data-testid="stSidebar"] {
    background-color: #ffffff;
}

.sidebar-title {
    font-size:26px !important;
    font-weight:800 !important;
    color:#2563eb;
}

/* Sidebar radio text */
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    font-size:20px !important;
    font-weight:700 !important;
}

/* =========================
   BUTTONS
========================= */

.stButton>button,
.stDownloadButton>button {
    font-size:16px !important;
    font-weight:600 !important;
    border-radius:8px !important;
    padding:10px 18px !important;
}

/* =========================
   GENERAL TEXT
========================= */

p, span, li {
    font-size:16.5px !important;
    line-height:1.6;
}

/* Image spacing */
[data-testid="stImage"] {
    margin-top:10px;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# Sidebar menu with custom font sizes
st.sidebar.markdown('<div class="sidebar-title">🚀 Navigation</div>', unsafe_allow_html=True)
option = st.sidebar.radio(
    "",
    ["Home 🏠", "Image Processing", "Video Processing"],
    label_visibility="collapsed"
)

# Load Haar cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize session state for face detection count
if 'faces_detected' not in st.session_state:
    st.session_state.faces_detected = 0

# ----------------------
# Home Page with explanation
if option == "Home 🏠":
    st.markdown(
        """
        <div class='big-title'>🛡️ Face Redaction & Privacy Protection System</div>
        <div class='sub-title'>
            Welcome to the AI-powered Face Redaction system!<br><br>
            This application helps you anonymize faces in images and videos to protect privacy.<br><br>
            <b>Features include:</b><br>
            - Single & batch image face redaction<br>
            - Video face blurring<br>
            - Easy download of processed images and videos<br><br>
            <b>How to use:</b><br>
            1. Select the mode (single or batch image) or video processing from the sidebar.<br>
            2. Upload your images or videos.<br>
            3. The system detects faces and applies redaction.<br>
            4. Download the redacted images/videos directly.<br><br>
            Enjoy privacy protection with ease!
        </div>
        """, unsafe_allow_html=True)
    st.write("\n")
    st.write("Navigate using the options on the sidebar to get started.")

# -----------------------------------
# Image Processing Section
elif option == "Image Processing":
    st.title("🖼️ Single & Batch Image Processing")
    mode = st.radio("Select Mode", ["Single Image", "Batch Images"])

    if mode == "Single Image":
        uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            start_time = time.time()
            file_bytes = uploaded_file.read()
            np_array = np.frombuffer(file_bytes, np.uint8)
            image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

            # Show original
            st.image(image, channels="BGR", caption="Original Image")

            # Detect and redact
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            st.session_state.faces_detected += len(faces)

            for (x, y, w, h) in faces:
                face = image[y:y+h, x:x+w]
                image[y:y+h, x:x+w] = cv2.GaussianBlur(face, (99, 99), 30)

            elapsed_time = time.time() - start_time

            # Show redacted image
            st.image(image, channels="BGR", caption="Redacted Image")
            # Download button
            _, buffer = cv2.imencode(".jpg", image)
            st.download_button(
                label="⬇️ Download Redacted Image",
                data=buffer.tobytes(),
                file_name="redacted_image.jpg",
                mime="image/jpeg"
            )

    else:
        uploaded_files = st.file_uploader("Upload Multiple Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
        if uploaded_files:
            for file in uploaded_files:
                start_time = time.time()
                bytes_data = file.read()
                np_array = np.frombuffer(bytes_data, np.uint8)
                img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

                # Detect faces
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                st.session_state.faces_detected += len(faces)

                # Redact faces
                for (x, y, w, h) in faces:
                    face = img[y:y+h, x:x+w]
                    img[y:y+h, x:x+w] = cv2.GaussianBlur(face, (99, 99), 30)

                # Show each image
                st.subheader(f"{file.name}")
                st.image(img, channels="BGR")

                # Download processed image
                _, buffer = cv2.imencode(".jpg", img)
                st.download_button(
                    label=f"⬇️ Download {file.name}",
                    data=buffer.tobytes(),
                    file_name=f"redacted_{file.name}",
                    mime="image/jpeg"
                )

# -----------------------------------
# Video Processing Section
elif option == "Video Processing":
    st.title("🎥 Video Face Redaction")
    video_file = st.file_uploader("Upload MP4 Video", type=["mp4"])
    if video_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_in:
            temp_in.write(video_file.read())
            input_path = temp_in.name

        # Initialize YOLOv8 model
        model = YOLO("yolov8n.pt")
        st.write("Processing video, please wait...")

        cap = cv2.VideoCapture(input_path)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        output_path = input_path.replace('.mp4', '_blurred.mp4')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        processed_frames = 0

        start_time = time.time()

        # Process frames
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            results = model(frame)
            # For each face detected, apply blur
            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    face = frame[y1:y2, x1:x2]
                    frame[y1:y2, x1:x2] = cv2.GaussianBlur(face, (99, 99), 30)
            out.write(frame)

        cap.release()
        out.release()
        elapsed_time = time.time() - start_time

        st.success(f"Processed video in {elapsed_time:.2f} seconds.")

        # Display video preview
        with open(output_path, "rb") as f:
            video_bytes = f.read()
        st.video(video_bytes)

        # Download processed video
        with open(output_path, "rb") as f:
            st.download_button("Download Blurred Video", f, file_name=os.path.basename(output_path))
