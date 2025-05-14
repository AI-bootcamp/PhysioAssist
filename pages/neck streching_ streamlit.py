import cv2
import mediapipe as mp
import numpy as np
import time
import pygame
from collections import deque
from enum import Enum, auto
import streamlit as st
from PIL import Image



def main():
    
    # =================== USER SETTINGS ===================
    DISPLAY_WIDTH = 960
    DISPLAY_HEIGHT = 720
    # =====================================================

    # Initialize pygame mixer
    pygame.mixer.init()

    # Sound files 
    SOUND_FILES = {
        "countdown": "sounds\second-hand-149907.mp3",
        "complete": "sounds\correct-6033.mp3",
        "wrong": "sounds\wrong-47985.mp3",
        "success": "sounds\scorrect-6033.mp3"
    }

    # Load arrow images
    ARROW_LEFT = cv2.imread("physio_page2.png", cv2.IMREAD_UNCHANGED)
    ARROW_RIGHT = cv2.imread("physio_page2.png", cv2.IMREAD_UNCHANGED)

    # Constants
    GRACE_PERIOD = 1.0
    SMOOTHING_WINDOW = 15
    MIN_LANDMARK_CONFIDENCE = 0.5
    THRESHOLD_RATIO = 0.3
    BUFFER_RATIO = 0.08

    class Stage(Enum):
        CENTER = auto()
        LEFT = auto()
        RIGHT = auto()

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    def overlay_image_alpha(img, img_overlay, pos, alpha_mask):
        x, y = pos
        h, w = img_overlay.shape[:2]

        if y + h > img.shape[0] or x + w > img.shape[1]:
            return

        for c in range(3):
            img[y:y+h, x:x+w, c] = img[y:y+h, x:x+w, c] * (1 - alpha_mask) + img_overlay[:, :, c] * alpha_mask

    class HeadMovementTracker:
        def __init__(self, target_cycles=10, countdown_time=5, status_placeholder=None):
            self.target_cycles = target_cycles
            self.countdown_time = countdown_time
            self.left_count = 0
            self.center_count = 0
            self.right_count = 0
            self.cycle_count = 0
            self.stage = Stage.CENTER
            self.countdown_start_time = None
            self.countdown_direction = None
            self.zone_exit_time = None
            self.left_ready = True
            self.right_ready = True
            self.nose_x_history = deque(maxlen=SMOOTHING_WINDOW)
            self.pose = mp_pose.Pose(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5,
                model_complexity=1
            )
            self.status_placeholder = status_placeholder
            self.last_interruption_time = 0
            self.interruption_cooldown = 3

        def play_sound(self, sound_type):
            if sound_type in SOUND_FILES:
                try:
                    pygame.mixer.music.load(SOUND_FILES[sound_type])
                    pygame.mixer.music.play()
                except pygame.error:
                    print(f"⚠️ Could not play sound: {sound_type}")

        def reset_countdown(self, message=None):
            if message:
                now = time.time()
                if now - self.last_interruption_time > self.interruption_cooldown:
                    if self.status_placeholder:
                        self.status_placeholder.warning(message)
                    self.last_interruption_time = now
            self.countdown_start_time = None
            self.countdown_direction = None
            self.zone_exit_time = None

        def calculate_zones(self, landmarks):
            nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
            if nose.visibility < MIN_LANDMARK_CONFIDENCE:
                return None, None, None, None, None
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            shoulder_width = abs(left_shoulder.x - right_shoulder.x)
            shoulder_mid_x = (left_shoulder.x + right_shoulder.x) / 2
            dynamic_threshold = shoulder_width * THRESHOLD_RATIO
            dynamic_buffer = shoulder_width * BUFFER_RATIO
            self.nose_x_history.append(nose.x)
            smoothed_nose_x = np.mean(self.nose_x_history)
            left_boundary = shoulder_mid_x - dynamic_threshold + dynamic_buffer
            right_boundary = shoulder_mid_x + dynamic_threshold - dynamic_buffer
            in_left = smoothed_nose_x < left_boundary
            in_right = smoothed_nose_x > right_boundary
            in_center = not in_left and not in_right
            return in_left, in_center, in_right, shoulder_mid_x, smoothed_nose_x

        def update_state(self, in_left, in_center, in_right, current_time):
            if in_left and self.left_ready:
                if self.countdown_direction != "left":
                    self.start_countdown("left", current_time)
                elif current_time - self.countdown_start_time >= self.countdown_time and self.stage != Stage.LEFT:
                    self.complete_movement("left", current_time)
            elif in_right and self.right_ready:
                if self.countdown_direction != "right":
                    self.start_countdown("right", current_time)
                elif current_time - self.countdown_start_time >= self.countdown_time and self.stage != Stage.RIGHT:
                    self.complete_movement("right", current_time)
            elif in_center:
                self.handle_center_zone(current_time)
            self.check_grace_period(in_left, in_right, current_time)

        def start_countdown(self, direction, current_time):
            self.countdown_start_time = current_time
            self.countdown_direction = direction
            print(f"Started countdown for {direction.upper()} hold...")
            self.play_sound("countdown")

        def complete_movement(self, direction, current_time):
            if direction == "left":
                self.stage = Stage.LEFT
                self.left_count += 1
            else:
                self.stage = Stage.RIGHT
                self.right_count += 1
            print(f"✅ {direction.upper()} hold completed!")
            self.reset_countdown()
            setattr(self, f"{direction}_ready", False)
            self.play_sound("complete")

        def handle_center_zone(self, current_time):
            if self.stage in [Stage.LEFT, Stage.RIGHT]:
                self.center_count += 1
                self.stage = Stage.CENTER
                self.left_ready = True
                self.right_ready = True
                print("Returned to CENTER")
                if self.left_count > 0 and self.right_count > 0 and self.center_count > 1:
                    self.cycle_count += 1
                    self.left_count = 0
                    self.right_count = 0
                    self.center_count = 0
                    print(f"🔁 Full cycle completed! ({self.cycle_count}/{self.target_cycles})")
                    self.play_sound("complete")
                    if self.cycle_count >= self.target_cycles:
                        self.play_sound("success")
                        if self.status_placeholder:
                            self.status_placeholder.success("🎉 Great job! You smashed your goal!")
            if self.countdown_direction is not None:
                self.reset_countdown(f"❌ {self.countdown_direction.upper()} hold interrupted. Stay still")
                self.play_sound("wrong")
            else:
                self.reset_countdown()

        def check_grace_period(self, in_left, in_right, current_time):
            if self.countdown_direction == "left" and not in_left:
                self.handle_zone_exit(current_time)
            elif self.countdown_direction == "right" and not in_right:
                self.handle_zone_exit(current_time)
            else:
                self.zone_exit_time = None

        def handle_zone_exit(self, current_time):
            if self.zone_exit_time is None:
                self.zone_exit_time = current_time
            elif current_time - self.zone_exit_time > GRACE_PERIOD:
                if self.countdown_direction is not None:
                    self.reset_countdown(f"❌ {self.countdown_direction.upper()} hold interrupted. Stay still")
                    self.play_sound("wrong")

        def draw_ui(self, image):
            # Show arrows only when in center
            if self.stage == Stage.CENTER:
                arrow_size = 100
                if ARROW_LEFT is not None and ARROW_LEFT.shape[2] == 4:
                    left = cv2.resize(ARROW_LEFT, (arrow_size, arrow_size))
                    left_alpha = left[:, :, 3] / 255.0
                    overlay_image_alpha(image, left[:, :, :3], (50, 300), left_alpha)
                if ARROW_RIGHT is not None and ARROW_RIGHT.shape[2] == 4:
                    right = cv2.resize(ARROW_RIGHT, (arrow_size, arrow_size))
                    right_alpha = right[:, :, 3] / 255.0
                    overlay_image_alpha(image, right[:, :, :3], (image.shape[1] - arrow_size - 50, 300), right_alpha)

            return image

    # ============================== STREAMLIT APP ==============================

    st.title("Head Movement Tracker")

    target_cycles = st.slider("Select Number of Repetitions", 1, 20, value=2)
    countdown_seconds = st.slider("How many seconds?", 1, 20, value=3)

    frame_placeholder = st.empty()
    cycle_placeholder = st.empty()
    status_placeholder = st.empty()

    tracker = HeadMovementTracker(
        target_cycles=target_cycles,
        countdown_time=countdown_seconds,
        status_placeholder=status_placeholder
    )

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (960, 720))
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = tracker.pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        current_time = time.time()

        if results.pose_landmarks:
            if tracker.cycle_count < tracker.target_cycles:
                zones = tracker.calculate_zones(results.pose_landmarks.landmark)
                if zones[0] is not None:
                    tracker.update_state(*zones[:3], current_time)

            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(245, 117, 66)),
                mp_drawing.DrawingSpec(color=(245, 66, 230))
            )

        image = tracker.draw_ui(image)

        cycle_placeholder.text(f"Cycles: {tracker.cycle_count}/{tracker.target_cycles}")
        display_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        display_image = Image.fromarray(display_image).resize((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        frame_placeholder.image(display_image)

    cap.release()

# Run main
if __name__ == "__main__":
    main()
