import streamlit as st
import cv2
import mediapipe as mp
from PIL import Image

# Streamlit UI
st.title("↻ Pronation vs Supination Tracker")
run = st.checkbox("Start Tracking")

frame_slot = st.empty()
cycle_display = st.empty()
pose_display = st.empty()

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# State
direction = 0  # 0 = waiting for pronation, 1 = waiting for supination
counter = 0

# Webcam setup
cap = cv2.VideoCapture(0)

while run:
    ret, image = cap.read()
    if not ret:
        st.warning("❌ Cannot access webcam.")
        break

    image = cv2.flip(image, 1)
    h, w, _ = image.shape
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    pose = "Not detected"  # Default state

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lm = handLms.landmark

            # Get base points for index and pinky
            x_index = lm[5].x * w
            x_pinky = lm[17].x * w

            # Determine hand pose based on relative position
            pose = "Supination" if x_index < x_pinky else "Pronation"

            # Cycle counting logic
            if pose == "Pronation" and direction == 0:
                direction = 1
            elif pose == "Supination" and direction == 1:
                counter += 1
                direction = 0

            # Draw landmarks
            mp_draw.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS)

    # Streamlit display
    pose_display.info(f"🧭 Current Pose: **{pose}**")
    cycle_display.metric("Cycles", counter)
    frame_slot.image(Image.fromarray(rgb))

cap.release()
