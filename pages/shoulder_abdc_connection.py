import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import time
import threading
import pyttsx3
import math
def main():
    # Store the page state (whether the training page should be shown)
    if 'training_started' not in st.session_state:
        st.session_state.training_started = False

    # Define a function to run the respective script with utf-8 encoding
    def run_training_script(script_name):
        try:
            with open(script_name, 'r', encoding='utf-8') as file:
                script = file.read()
            exec(script)
        except Exception as e:
            st.error(f"Error loading the script: {e}")

    # Display the initial page or the training page based on the state
    if not st.session_state.training_started:
        # Create columns for centering
        col1, col2, col3 = st.columns([1, 0.5, 1])  # Adjust the middle column for centering

        # Display the logo in the center column
        with col2:
            logo_path = "physio_page2.png"  # Path to your logo image
            st.image(logo_path, width=100)  # Set the width to 100 pixels (adjust as needed)

        # Display a training video (Replace with the correct path)
        video_path = "IMG_7907.MP4"  # Example path to your video
        st.video(video_path)

        # Provide an option to choose left or right shoulder
        shoulder_choice = st.radio("Select Shoulder", ("Left", "Right"))

        # Store the choice in session state to remember the user's selection
        if 'shoulder_choice' not in st.session_state:
            st.session_state.shoulder_choice = shoulder_choice

        # Next button to navigate to the chosen training
        if st.button('Next'):
            # Mark the training as started
            st.session_state.training_started = True
            # Optionally, store the choice of the shoulder in session state for the training page
            st.session_state.shoulder_choice = shoulder_choice

    else:
        # Once training starts, show the training page content
        if st.session_state.shoulder_choice == "Left":
            # Show left shoulder training content
            st.write("Now starting the left shoulder training...")
            run_training_script("left_abduction_streamlit.py")  # Execute the left shoulder training script

        elif st.session_state.shoulder_choice == "Right":
            # Show right shoulder training content
            st.write("Now starting the right shoulder training...")
            # run_training_script("./right_abduction_streamlit.py")  # Execute the right shoulder training script
            run_training_script("pages/right_abduction_streamlit.py")



# main()
# Optional: allow running it directly
if __name__ == "__main__":
    main()