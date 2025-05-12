import streamlit as st
import cv2
import mediapipe as mp
import math
from PIL import Image
import time
import base64

def main():
    st.markdown("<h1 style='color: black;'>🖐 Thumb-to-Finger Touch</h1>", unsafe_allow_html=True)

    # Return to home
    if st.button("🔙 Return to Home"):
        st.session_state.page = "home"
        if "cap" in st.session_state:
            st.session_state.cap.release()
            del st.session_state.cap
        st.stop()

    # CSS لتعديل اللون وتوسيط الفيديو
    st.markdown("""
       <style>
       body {
           color: black !important;
       }
       .stAlert {
           color: black !important;
       }
       video {
           max-width: 400px;
           height: auto;
           display: block;
           margin: 0 auto;
       }
       </style>
     """, unsafe_allow_html=True)

    # عرض فيديو توضيحي للتمرين
    video_file = open("videos\ThumbOppsition.mp4", "rb")
    video_bytes = video_file.read()
    st.video(video_bytes)

    # Initialize MediaPipe
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

    # Finger Data
    finger_ids = [8, 12, 16, 20]
    finger_names = ['Index', 'Middle', 'Ring', 'Pinky']
    current_finger = 0
    score = 0

    if "cap" not in st.session_state:
        st.session_state.cap = cv2.VideoCapture(0)

    cap = st.session_state.cap
    frame_slot = st.empty()
    score_display = st.empty()
    instruction_display = st.empty()
    prev_touch_time = 0

    def distance(a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    run_time = 60
    start_time = time.time()
   
    while time.time() - start_time < run_time:
        ret, image = cap.read()
        if not ret:
            st.error("❌ Could not access webcam.")
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

                cv2.circle(image, (int(thumb_tip[0]), int(thumb_tip[1])), 12, (255, 255, 0), -1)
                cv2.putText(image, "Thumb", (int(thumb_tip[0]), int(thumb_tip[1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

                cv2.circle(image, (int(target_tip[0]), int(target_tip[1])), 12, (255, 50, 50), -1)
                cv2.putText(image, "Target", (int(target_tip[0]), int(target_tip[1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 50, 50), 1)

                if distance(thumb_tip, target_tip) < 30:
                    if time.time() - prev_touch_time > 1:
                        score += 1
                        current_finger = (current_finger + 1) % 4
                        prev_touch_time = time.time()

        instruction_display.markdown(f"<p style='color: black;'>🟢 Touch your <strong>{finger_names[current_finger]}</strong> finger with your thumb.</p>", unsafe_allow_html=True)
        score_display.markdown(f"<h4 style='color: black;'>Score: {score}</h4>", unsafe_allow_html=True)

        # توسيط الكاميرا
        _, buffer = cv2.imencode('.jpg', image)
        img_b64 = base64.b64encode(buffer).decode()
        frame_slot.markdown(f"""
            <div style='display: flex; justify-content: center;'>
                <img src="data:image/jpeg;base64,{img_b64}" style="max-width: 100%; height: auto; border-radius: 10px;" />
            </div>
        """, unsafe_allow_html=True)

    cap.release()
    del st.session_state.cap
    st.success("🎉 Game finished!")