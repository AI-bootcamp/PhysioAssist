import cv2
import mediapipe as mp
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

left_count = 0
center_count = 0
right_count = 0
cycle_count = 0
stage = "center"

countdown_time = 5
countdown_start_time = None
countdown_direction = None  # "left" or "right"

# Flags to ensure one count per side before resetting
left_ready = True
right_ready = True

def reset_countdown(message=None):
    global countdown_start_time, countdown_direction
    if countdown_start_time is not None and countdown_direction is not None and message:
        print(message)
    countdown_start_time = None
    countdown_direction = None

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark
            NOSE = [landmarks[mp_pose.PoseLandmark.NOSE.value].x,
                    landmarks[mp_pose.PoseLandmark.NOSE.value].y]
            LEFT_SHOULDER = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            RIGHT_SHOULDER = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

            shoulder_mid_x = (LEFT_SHOULDER[0] + RIGHT_SHOULDER[0]) / 2
            threshold = 0.15
            buffer = 0.03  # Tolerance for slight movement
            current_time = time.time()

            in_left_zone = NOSE[0] < (shoulder_mid_x - threshold)
            in_right_zone = NOSE[0] > (shoulder_mid_x + threshold)
            in_center_zone = not in_left_zone and not in_right_zone

            # LEFT
            if in_left_zone and left_ready:
                if countdown_direction != "left":
                    countdown_start_time = current_time
                    countdown_direction = "left"
                    print("Started countdown for LEFT hold...")
                else:
                    elapsed = current_time - countdown_start_time
                    if elapsed >= countdown_time and stage != "left":
                        stage = "left"
                        left_count += 1
                        print("✅ LEFT hold completed!")
                        reset_countdown()
                        left_ready = False

            # RIGHT
            elif in_right_zone and right_ready:
                if countdown_direction != "right":
                    countdown_start_time = current_time
                    countdown_direction = "right"
                    print("Started countdown for RIGHT hold...")
                else:
                    elapsed = current_time - countdown_start_time
                    if elapsed >= countdown_time and stage != "right":
                        stage = "right"
                        right_count += 1
                        print("✅ RIGHT hold completed!")
                        reset_countdown()
                        right_ready = False

            # CENTER
            elif in_center_zone:
                if stage in ["left", "right"]:
                    center_count += 1
                    stage = "center"
                    left_ready = True
                    right_ready = True
                    print("Returned to CENTER")
                reset_countdown(f"❌ {countdown_direction.upper()} hold interrupted — exited the zone early.")

            # Buffer-based reset
            if countdown_direction == "left":
                if NOSE[0] > (shoulder_mid_x - threshold + buffer):
                    reset_countdown("❌ LEFT hold interrupted — exited the zone early.")

            elif countdown_direction == "right":
                if NOSE[0] < (shoulder_mid_x + threshold - buffer):
                    reset_countdown("❌ RIGHT hold interrupted — exited the zone early.")

            # Count a cycle
            if left_count > 0 and right_count > 0 and center_count > 1:
                cycle_count += 1
                left_count = 0
                right_count = 0
                center_count = 0
                print("🔁 Full cycle completed!")

        except:
            pass

        # Display data
        cv2.rectangle(image, (0, 0), (250, 200), (245, 117, 16), -1)
        cv2.putText(image, f'Left: {left_count}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.putText(image, f'Center: {center_count}', (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.putText(image, f'Right: {right_count}', (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.putText(image, f'Cycles: {cycle_count}', (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

        if countdown_start_time is not None and countdown_direction is not None:
            remaining = countdown_time - int(current_time - countdown_start_time)
            if remaining > 0:
                cv2.putText(image, f'{countdown_direction.capitalize()} Hold: 00:{remaining:02}',
                            (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
            else:
                cv2.putText(image, f'{countdown_direction.capitalize()} Hold: Done',
                            (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()