import streamlit as st
import cv2
import mediapipe as mp
import math
import time
from PIL import Image

def main():
    st.title("✋ Finger Resistance Exercise Tracker")

    # 🔙 Return to home button
    if st.button("🔙 Return to Home"):
        st.query_params["page"] = "home"
        st.rerun()

    # UI containers
    frame_slot = st.empty()
    count_display = st.empty()
    hold_display = st.empty()

    # MediaPipe setup
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils

    # Helper function
    def dist(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    # Game state
    open_count = 0
    is_open = False
    hold_start = None

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("❌ Could not access webcam.")
        return

    # Camera loop
    while True:
        ret, image = cap.read()
        if not ret:
            st.warning("⚠️ Could not read from webcam.")
            break

        image = cv2.flip(image, 1)
        h, w, _ = image.shape
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                lm = handLms.landmark
                points = [(lm[i].x * w, lm[i].y * h) for i in [4, 8, 12, 16, 20]]
                distances = [dist(points[0], p) for p in points[1:]]
                avg_dist = sum(distances) / len(distances)

                if avg_dist > 100:
                    if not is_open:
                        open_count += 1
                        is_open = True
                        hold_start = time.time()
                else:
                    is_open = False
                    hold_start = None

                mp_draw.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS)

        count_display.metric("Open Count", open_count)

        if is_open and hold_start:
            hold_time = round(time.time() - hold_start, 1)
            hold_display.info(f"✊ Holding open for {hold_time} seconds")
        else:
            hold_display.empty()

        img = Image.fromarray(image_rgb)
        frame_slot.image(img)

    cap.release()
