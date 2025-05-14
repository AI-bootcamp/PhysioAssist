import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import pyttsx3
import time
import threading

# Initialize mediapipe and TTS
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
engine = pyttsx3.init()

# Speak function using threading
def speak(text):
    def _speak():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=_speak).start()

# Angle calculation
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
              np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# Main Streamlit app
def main():
    # Streamlit setup
    st.set_page_config(layout="wide")
    st.markdown("<h1 style='text-align: center;'>🦵 Knee Extension Exercise Tracker</h1>", unsafe_allow_html=True)
    
    target_reps = st.slider("🎯 Select number of repetitions", 1, 20, 10)
    
    frame_placeholder = st.empty()
    counter_display = st.empty()
    success_message = st.empty()

    # Variables
    counter = 0
    stage = None
    rep_completed = False
    started = False
    success_shown = False
    first_rep_skipped = False
    run_time = 60  # seconds
    start_time = time.time()

    # Open camera
    cap = cv2.VideoCapture(0)

    with mp_pose.Pose(min_detection_confidence=0.5,
                      min_tracking_confidence=0.5) as pose:
        while cap.isOpened() and (time.time() - start_time < run_time):
            ret, frame = cap.read()
            if not ret:
                st.warning("⚠️ Could not access webcam.")
                break

            frame = cv2.flip(frame, 1)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark

                hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                angle = calculate_angle(hip, knee, ankle)

                # Draw angle
                cv2.putText(image, str(int(angle)),
                            tuple(np.multiply(knee, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

                # Rep logic
                if angle > 150:
                    if not started:
                        started = True
                    else:
                        stage = "up"
                        rep_completed = True

                if angle < 120 and stage == "up":
                    if rep_completed:
                        if not first_rep_skipped:
                            first_rep_skipped = True
                            rep_completed = False
                        else:
                            counter += 1
                            rep_completed = False
                            print(f"Rep: {counter}")
                            if counter >= target_reps and not success_shown:
                                speak("Excellent! Knee extension complete.")
                                success_message.success("✅ Excellent! Knee extension complete.")
                                success_shown = True

                counter_display.markdown(f"### 🔁 Repetitions: **{counter} / {target_reps}**")

                # Draw landmarks
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

            except Exception as e:
                pass

            frame_placeholder.image(image, channels="BGR")

        cap.release()

if __name__ == "__main__":
    main()
