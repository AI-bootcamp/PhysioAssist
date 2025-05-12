import streamlit as st
import cv2
import mediapipe as mp
from PIL import Image

def main():
    st.title("↻ Pronation vs Supination Tracker")

    # Return to Home button
    if st.button("🔙 Return to Home"):
        st.session_state.page = "home"
        st.rerun()

    # Streamlit placeholders
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
    if not cap.isOpened():
        st.error("❌ Cannot access webcam.")
        return

    for _ in range(150):  # Loop for limited frames to keep Streamlit responsive
        ret, image = cap.read()
        if not ret:
            st.warning("⚠️ Could not read from webcam.")
            break

        image = cv2.flip(image, 1)
        h, w, _ = image.shape
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        pose = "Not detected"

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                lm = handLms.landmark

                x_index = lm[5].x * w
                x_pinky = lm[17].x * w

                pose = "Supination" if x_index < x_pinky else "Pronation"

                if pose == "Pronation" and direction == 0:
                    direction = 1
                elif pose == "Supination" and direction == 1:
                    counter += 1
                    direction = 0

                mp_draw.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS)

        pose_display.info(f"🧭 Current Pose: **{pose}**")
        cycle_display.metric("Cycles", counter)
        frame_slot.image(Image.fromarray(rgb))

    cap.release()
