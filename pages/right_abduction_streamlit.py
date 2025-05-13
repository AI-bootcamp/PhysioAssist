import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import time
import threading
import pyttsx3
import math

# Initialize mediapipe and TTS
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
engine = pyttsx3.init()

# TTS function using threading
def speak(text):
    def _speak():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=_speak).start()

# Angle calculation helper
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# Streamlit app
def main():
    # ====== FORCE REMOVE TITLE ====== 
    st.markdown(""" 
        <style>
            .appview-container .main .block-container {
                padding-top: 0rem;
            }
            h1 {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)
    st.title(" ")  # Empty title

    target_reps = st.slider("Select Number of Repetitions", min_value=1, max_value=20, value=10)

    # Exercise variables
    counter = 0
    stage = "down"
    rep_completed = False
    elbow_warning_issued = False
    success_message_displayed = False  # Flag to show success only once

    target_angles = np.linspace(-90, 90, 10)
    upper_arm_len = 90
    lower_arm_len = 90

    run_time = 60  # in seconds
    start_time = time.time()

    cap = cv2.VideoCapture(0)
    frame_placeholder = st.empty()
    rep_counter = st.empty()
    angle_display = st.empty()
    warning_placeholder = st.empty()
    success_placeholder = st.empty()

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened() and (time.time() - start_time < run_time):
            ret, frame = cap.read()
            if not ret:
                st.warning("⚠️ Could not read from webcam.")
                break

            frame = cv2.flip(frame, 1)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark

                # Right arm (mirrored camera)
                r_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                r_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
                r_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
                r_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]

                shoulder = [r_shoulder.x, r_shoulder.y]
                elbow = [r_elbow.x, r_elbow.y]
                wrist = [r_wrist.x, r_wrist.y]
                hip = [r_hip.x, r_hip.y]

                shoulder_px = np.multiply(shoulder, [640, 480]).astype(int)
                elbow_px = np.multiply([r_elbow.x, r_elbow.y], [640, 480]).astype(int)

                shoulder_angle = calculate_angle(hip, shoulder, elbow)
                elbow_angle = calculate_angle(shoulder, elbow, wrist)

                # Elbow check with TTS + warning box
                if elbow_angle < 160:
                    if not elbow_warning_issued:
                        speak("Straighten your elbow")
                        elbow_warning_issued = True
                    warning_placeholder.warning("⚠️ Elbow bent. Please straighten your elbow.")
                else:
                    elbow_warning_issued = False
                    warning_placeholder.empty()

                # Repetition logic
                if shoulder_angle < 30:
                    stage = "down"
                    if rep_completed:
                        counter += 1
                        rep_completed = False
                        print(f"Rep: {counter}")
                        if counter >= target_reps and not success_message_displayed:
                            speak("Great job! You smashed your goal")
                            success_placeholder.success("🎉 Great job! You smashed your goal!")
                            success_message_displayed = True
                        counter = min(counter, target_reps)
                elif shoulder_angle > 170 and stage == "down":
                    stage = "up"
                    rep_completed = True

                # Ghost arm drawing
                for angle in target_angles:
                    angle_rad = math.radians(angle)
                    ghost_elbow = [
                        shoulder_px[0] + upper_arm_len * math.cos(angle_rad),
                        shoulder_px[1] - upper_arm_len * math.sin(angle_rad)
                    ]
                    ghost_wrist = [
                        ghost_elbow[0] + lower_arm_len * math.cos(angle_rad),
                        ghost_elbow[1] - lower_arm_len * math.sin(angle_rad)
                    ]

                    color_intensity = min(abs(shoulder_angle - angle) / 180, 1)
                    ghost_color = (int(255 * (1 - color_intensity)), 0, int(255 * color_intensity))

                    cv2.arrowedLine(image, tuple(shoulder_px), tuple(np.int32(ghost_elbow)), ghost_color, 2, tipLength=0.05)
                    cv2.arrowedLine(image, tuple(np.int32(ghost_elbow)), tuple(np.int32(ghost_wrist)), ghost_color, 2, tipLength=0.05)
                    cv2.circle(image, tuple(shoulder_px), 4, ghost_color, -1)
                    cv2.circle(image, tuple(np.int32(ghost_elbow)), 4, ghost_color, -1)
                    cv2.circle(image, tuple(np.int32(ghost_wrist)), 4, ghost_color, -1)

                # Draw user's current arm (shoulder to elbow only)
                cv2.line(image, tuple(shoulder_px), tuple(elbow_px), (0, 255, 255), 2)
                cv2.circle(image, tuple(shoulder_px), 5, (0, 255, 255), -1)
                cv2.circle(image, tuple(elbow_px), 5, (0, 255, 255), -1)

            except Exception:
                pass

            # ✅ Display reps only in Streamlit, not on the camera frame
            rep_counter.text(f"Repetitions: {counter} / {target_reps}")

            frame_placeholder.image(image, channels="BGR")

        cap.release()

if __name__ == "__main__":
    main()
