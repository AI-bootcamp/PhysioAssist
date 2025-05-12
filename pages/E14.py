import streamlit as st
import cv2
import mediapipe as mp
import math
from PIL import Image

def main():
    st.title("🖐️ Thumb-to-Finger Touch Game")

    if st.button("🔙 Return to Home"):
        st.session_state.page = "home"
        st.rerun()

    frame_slot = st.empty()
    score_display = st.empty()
    instruction_display = st.empty()

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils

    finger_ids = [8, 12, 16, 20]
    finger_names = ['Index', 'Middle', 'Ring', 'Pinky']
    current_finger = 0
    score = 0

    def distance(a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("❌ Could not access webcam.")
        return

    for _ in range(150):
        ret, image = cap.read()
        if not ret:
            break

        image = cv2.flip(image, 1)
        h, w, _ = image.shape
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                lm = hand_landmarks.landmark
                thumb_tip = (lm[4].x * w, lm[4].y * h)
                target_tip = (lm[finger_ids[current_finger]].x * w, lm[finger_ids[current_finger]].y * h)

                mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                cv2.circle(image, (int(thumb_tip[0]), int(thumb_tip[1])), 12, (255, 0, 0), -1)
                cv2.putText(image, "Thumb", (int(thumb_tip[0]), int(thumb_tip[1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

                cv2.circle(image, (int(target_tip[0]), int(target_tip[1])), 12, (0, 0, 255), -1)
                cv2.putText(image, "Target", (int(target_tip[0]), int(target_tip[1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                if distance(thumb_tip, target_tip) < 30:
                    score += 1
                    current_finger = (current_finger + 1) % 4

        instruction_display.info(f"🟢 Touch your **{finger_names[current_finger]}** finger with your thumb.")
        score_display.metric("Score", score)
        img = Image.fromarray(image_rgb)
        frame_slot.image(img)

    cap.release()
