import streamlit as st
import os
import base64

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Correct filename
background_image_path = os.path.join(script_dir, "images", "backgound.jpg")

# Convert image to base64 string
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Inject CSS to style background, sidebar, and hide top bar
def set_custom_style(jpg_file):
    bin_str = get_base64_of_bin_file(jpg_file)
    page_bg_img = f"""
    <style>
    /* Background */
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Full sidebar container */
    section[data-testid="stSidebar"] {{
        background-color: #aecad7 !important;
        padding: 1rem;
        border-radius: 0 10px 10px 0;
    }}

    /* Hide top menu and footer */
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    header {{ visibility: hidden; }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Apply all custom styles
set_custom_style(background_image_path)

# Sidebar content
st.sidebar.title("Navigation")
st.sidebar.write("Choose a section:")

# Main content
st.title("PhysioAssist App")
st.write("Welcome to your physiotherapy assistant application.")
