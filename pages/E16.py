import streamlit as st
import cv2
import mediapipe as mp
from PIL import Image
import time

def main():
    st.title("↻ Pronation vs Supination Tracker")

    if st.button("🔙 Return to Home"):
        st.session_state.page = "home"
        st.rerun()

    # UI placeholders
    col1, col2 = st.columns([2, 1])
    guide_msg = col1.empty()
    cycle_display = col2.empty()
    frame_slot = st.empty()

    # === Guided Countdown ===
    for i in range(3, 0, -1):
        guide_msg.markdown(f"""
            <div style='
                font-size: 24px;
                font-weight: bold;
                background-color: #fffae6;
                padding: 12px;
                border-radius: 10px;
                color: #444;
                text-align: center;
                border: 1px solid #ffd500;
            '>🧭 Start with: <strong>Pronation</strong> in {i}...</div>
        """, unsafe_allow_html=True)
        time.sleep(1)

    for i in range(3, 0, -1):
        guide_msg.markdown(f"""
            <div style='
                font-size: 24px;
                font-weight: bold;
                background-color: #e6f7ff;
                padding: 12px;
                border-radius: 10px;
                color: #004080;
                text-align: center;
                border: 1px solid #91d5ff;
            '>🔁 Then: <strong>Supination</strong> in {i}...</div>
        """, unsafe_allow_html=True)
        time.sleep(1)

    guide_msg.success("✅ Start moving your hand!")

    # === MediaPipe Setup ===
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.5)
    mp_draw = mp.solutions.drawing_utils

    direction = 0  # 0 = waiting for pronation, 1 = waiting for supination
    counter = 0

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("❌ Cannot access webcam.")
        return

    while True:
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

        # Display pose message
        guide_msg.markdown(f"""
            <div style='
                font-size: 22px;
                font-weight: bold;
                background-color: #f0f0f0;
                padding: 12px;
                border-radius: 10px;
                color: black;
                text-align: center;
                border: 1px solid #ccc;
            '>🧭 Detected Pose: <strong>{pose}</strong></div>
        """, unsafe_allow_html=True)

        # Display cycles
        cycle_display.markdown(f"""
            <div style='
                font-size: 24px;
                font-weight: bold;
                color: black;
                background-color: white;
                padding: 12px;
                border-radius: 10px;
                text-align: center;
                border: 1px solid #ccc;
                margin-bottom: 10px;
            '>
                🔁 Cycles: {counter}
            </div>
        """, unsafe_allow_html=True)

        frame_slot.image(Image.fromarray(rgb))

    cap.release()

if __name__ == "__main__":
    main()
