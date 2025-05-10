import streamlit as st
import cv2
import mediapipe as mp
import math
import numpy as np

# Title
st.title("🖐️ Finger Touch Game")
st.markdown("Touch your thumb to each finger in order: Index ➝ Middle ➝ Ring ➝ Pinky")

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Initialize session state
if "run" not in st.session_state:
    st.session_state.run = False
if "score" not in st.session_state:
    st.session_state.score = 0
if "current_finger" not in st.session_state:
    st.session_state.current_finger = 0

finger_ids = [8, 12, 16, 20]
finger_names = ["Index", "Middle", "Ring", "Pinky"]

def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

# Start/Stop button
if st.button("▶️ Start" if not st.session_state.run else "⏹ Stop"):
    st.session_state.run = not st.session_state.run

# Placeholder for video
frame_window = st.image([])

# Run loop
camera = cv2.VideoCapture(0)

while st.session_state.run:
    success, frame = camera.read()
    if not success:
        st.error("❌ Failed to access the camera.")
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lm = handLms.landmark
            thumb_tip = (lm[4].x * w, lm[4].y * h)
            target_tip = (lm[finger_ids[st.session_state.current_finger]].x * w,
                          lm[finger_ids[st.session_state.current_finger]].y * h)

            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            cv2.circle(frame, tuple(map(int, thumb_tip)), 10, (255, 0, 0), -1)
            cv2.circle(frame, tuple(map(int, target_tip)), 10, (0, 255, 0), -1)

            if distance(thumb_tip, target_tip) < 30:
                st.session_state.score += 1
                st.session_state.current_finger = (st.session_state.current_finger + 1) % 4

    # Show instructions
    cv2.putText(frame, f"Touch: {finger_names[st.session_state.current_finger]}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 100, 0), 2)
    cv2.putText(frame, f"Score: {st.session_state.score}", (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 150, 0), 2)

    # Display
    frame_window.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

camera.release()
