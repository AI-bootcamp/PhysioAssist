import streamlit as st
import cv2
import mediapipe as mp
import math
import time
from PIL import Image

def main():
    st.title("✋ Finger Resistance Exercise Tracker")

    if st.button("🔙 Return to Home"):
        st.session_state.page = "home"
        st.rerun()

    # MediaPipe setup
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils

    def dist(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    open_count = 0
    is_open = False
    hold_start = None
    last_feedback_time = 0  # To control when "Good Job" is shown

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("❌ Could not access webcam.")
        return

    # Top layout
    top_col1, top_col2 = st.columns(2)
    count_display = top_col1.empty()
    hold_display = top_col2.empty()
    frame_slot = st.empty()
    feedback_box = st.empty()

    while True:
        ret, image = cap.read()
        if not ret:
            st.warning("⚠️ Could not read from webcam.")
            break

        image = cv2.flip(image, 1)
        h, w, _ = image.shape
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        feedback_message = ""
        show_feedback = False

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
                        last_feedback_time = 0  # reset feedback timer
                    else:
                        if hold_start:
                            held_for = time.time() - hold_start
                            if int(held_for) % 5 == 0 and int(held_for) != last_feedback_time:
                                feedback_message = "🎉 Good Job! Keep it up!"
                                show_feedback = True
                                last_feedback_time = int(held_for)
                else:
                    is_open = False
                    hold_start = None
                    feedback_box.empty()

                mp_draw.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS)

        # Show custom black text counter
        count_display.markdown(f"""
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
                💪 Open Count: {open_count}
            </div>
        """, unsafe_allow_html=True)

        if is_open and hold_start:
            hold_time = round(time.time() - hold_start, 1)
            hold_display.info(f"⏱️ Holding open: {hold_time} sec")
        else:
            hold_display.empty()
            feedback_box.empty()

        # Show feedback message every 5 seconds
        if show_feedback:
            feedback_box.success(feedback_message)

        # Display the frame
        img = Image.fromarray(image_rgb)
        frame_slot.image(img)

    cap.release()

if __name__ == "__main__":
    main()
