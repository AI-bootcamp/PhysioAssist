import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
from PIL import Image

def main():
    st.title("🤚 Wrist Flexibility Tracker")
    if st.button("🔙 Return to Home"):
        st.query_params["page"] = "home"
        st.rerun()
    # UI placeholders
    frame_slot = st.empty()
    rep_counter = st.empty()
    angle_display = st.empty()

    # MediaPipe setup
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
    mp_draw = mp.solutions.drawing_utils

    def calculate_angle(a, b, c):
        try:
            a, b, c = np.array(a), np.array(b), np.array(c)
            radians = np.arccos(np.dot(a - b, c - b) / (np.linalg.norm(a - b) * np.linalg.norm(c - b)))
            return np.degrees(radians)
        except:
            return 0

    counter = 0
    direction = 0

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("❌ Could not access webcam.")
        return

    # Run camera loop (automatically starts)
    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("⚠️ Could not read from webcam.")
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
                h, w, _ = frame.shape
                lm = handLms.landmark

                wrist = [lm[0].x * w, lm[0].y * h]
                palm = [lm[9].x * w, lm[9].y * h]
                tip = [lm[12].x * w, lm[12].y * h]

                angle = calculate_angle(wrist, palm, tip)
                angle_display.metric("Wrist Angle", f"{int(angle)}°")

                if angle > 160 and direction == 0:
                    counter += 1
                    direction = 1
                    rep_counter.metric("Reps", counter)
                elif angle < 90:
                    direction = 0

        img = Image.fromarray(rgb)
        frame_slot.image(img)

    cap.release()
