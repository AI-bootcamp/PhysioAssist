import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
from PIL import Image

# Mediapipe setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Angle calculation
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180.0 else angle

# Streamlit UI
st.title("🏋️‍♂️ Shoulder Abduction Tracker")
run = st.checkbox('Start Tracking')

frame_slot = st.empty()
rep_counter = st.empty()
warning_display = st.empty()

counter = 0
stage = "down"
rep_completed = False

cap = cv2.VideoCapture(0)

while run:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        landmarks = results.pose_landmarks.landmark

        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
               landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        angle = calculate_angle(hip, shoulder, elbow)
        elbow_angle = calculate_angle(shoulder, elbow, wrist)

        if elbow_angle < 160:
            warning_display.warning("⚠️ Elbow bent! Keep it straight.")
        else:
            warning_display.empty()

        if angle < 30:
            stage = "down"
            if rep_completed:
                counter += 1
                rep_counter.metric("Reps", counter)
                rep_completed = False
        elif angle > 170 and stage == "down":
            stage = "up"
            rep_completed = True

    img = Image.fromarray(rgb)
    frame_slot.image(img)

cap.release()
