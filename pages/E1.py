import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import time

def main():
    # ====== REMOVE TITLE & STYLING ======
    st.markdown("""
        <style>
            .appview-container .main .block-container {
                padding-top: 0rem;
            }
            h1 {
                display: none !important;
            }
            .status-box {
                font-size: 20px;
                font-weight: bold;
                padding: 10px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 10px;
            }
            .good {
                background-color: #c4f0c5;
                color: #2e7d32;
            }
            .bad {
                background-color: #ffe6e6;
                color: #c62828;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title(" ")

    # ====== Instructions ======
    st.markdown("## 🖐️ Wrist Angle Exercise Game")
    st.markdown("""
    Try to **bend and straighten your wrist** repeatedly for 30 seconds.  
    - Straighten: Angle above **160°**  
    - Bend: Angle below **90°**  
    - Every cycle (bend → straighten) counts as **1 rep**.
    """)

    if st.button("Return to Home"):
        st.session_state.page = "home"
        st.rerun()

    # ==== Game Timer ====
    run_time = 30  # seconds
    start_time = time.time()

    # ==== MediaPipe Setup ====
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
    mp_draw = mp.solutions.drawing_utils

    # ==== Angle Calculation Function ====
    def calculate_angle(a, b, c):
        try:
            a, b, c = np.array(a), np.array(b), np.array(c)
            radians = np.arccos(np.dot(a - b, c - b) / (np.linalg.norm(a - b) * np.linalg.norm(c - b)))
            return np.degrees(radians)
        except:
            return 0

    # ==== Game Counters ====
    counter = 0
    points = 0
    direction = 0
    cap = cv2.VideoCapture(0)

    # ==== Layout Placeholders ====
    col1, col2 = st.columns([2, 1])  # Wider for bar, narrower for status
    progress_bar = col1.progress(0)
    status_box = col2.empty()

    frame_placeholder = st.empty()
    rep_counter = st.empty()
    angle_display = st.empty()
    point_display = st.empty()

    # ==== Game Loop ====
    while True:
        current_time = time.time()
        elapsed = current_time - start_time
        progress = min(1.0, elapsed / run_time)
        progress_bar.progress(progress)

        if elapsed >= run_time:
            break

        ret, frame = cap.read()
        if not ret:
            st.warning("⚠️ Could not read from webcam.")
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        status = "Keep Going..."
        status_style = "status-box"

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
                h, w, _ = frame.shape
                lm = handLms.landmark

                wrist = [lm[0].x * w, lm[0].y * h]
                palm = [lm[9].x * w, lm[9].y * h]
                tip = [lm[12].x * w, lm[12].y * h]

                angle = calculate_angle(wrist, palm, tip)

                # Rep logic fix
                if angle < 90 and direction == 0:
                    direction = 1  # Bent
                    status = "↘️ Bend Your Wrist"
                    status_style += " bad"
                elif angle > 160 and direction == 1:
                    counter += 1
                    points += 1
                    direction = 0  # Reset
                    status = "✅ Wrist Straightened!"
                    status_style += " good"

                # Display black-colored angle
                angle_display.markdown(f"""
                    <div style='
                        font-size: 24px;
                        font-weight: bold;
                        color: black;
                        background-color: white;
                        padding: 10px;
                        border-radius: 10px;
                        text-align: center;
                        border: 1px solid #ccc;
                        margin-bottom: 10px;
                    '>
                        🔁 Wrist Angle: {int(angle)}°
                    </div>
                """, unsafe_allow_html=True)

        # Display webcam and other UI
        frame_placeholder.image(rgb, channels="RGB")

        # Display black-colored rep counter
        rep_counter.markdown(f"""
            <div style='
                font-size: 24px;
                font-weight: bold;
                color: black;
                background-color: white;
                padding: 10px;
                border-radius: 10px;
                text-align: center;
                border: 1px solid #ccc;
                margin-bottom: 10px;
            '>
                💪 Reps: {counter}
            </div>
        """, unsafe_allow_html=True)

        point_display.metric("🏆 Points", points)
        status_box.markdown(f'<div class="{status_style}">{status}</div>', unsafe_allow_html=True)

    # ==== End of Game ====
    cap.release()
    st.success("✅ Time's up! Great job!")
    st.markdown(f"### 🏁 Final Score: **{points}** points / **{counter}** reps in {run_time} seconds")

if __name__ == "__main__":
    main()
