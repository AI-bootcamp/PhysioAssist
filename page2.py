import streamlit as st
import os
import importlib
import base64

# --- Paths ---
script_dir = os.path.dirname(os.path.abspath(__file__))
background_image_path = os.path.join(script_dir, "images", "backgound.jpg")
character_image_path = os.path.join(script_dir, "images", "physio_page2.png")

# --- Utilities ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        return base64.b64encode(f.read()).decode()

def set_custom_style(jpg_file):
    bin_str = get_base64_of_bin_file(jpg_file)
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&family=Quicksand:wght@600&display=swap');

    .stApp {{
        background-image: url("data:image/jpeg;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
    }}

    section[data-testid="stSidebar"] {{
        background-color: #7096d1 !important;
        padding: 1rem;
        font-family: 'Roboto', sans-serif;
        height: 60vh;
        overflow-y: auto;
    }}

    .block-container {{
        color: #334eac;
        font-family: 'Roboto', sans-serif;
        padding-left: 0 !important;
        padding-right: 0 !important;
        max-width: none !important;
    }}

    h1 {{
        font-family: 'Quicksand', sans-serif;
        font-weight: 600;
        font-size: 3rem;
        color: #334eac;
        text-align: center;
        margin-top: 0;
    }}

    .question-text {{
        color: #334eac;
        font-family: 'Poppins', sans-serif;
        font-size: 1rem;
        margin-bottom: 0.5rem;
        margin-top: 1.5rem;
    }}

    #MainMenu, header, footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

# --- App Setup ---
st.set_page_config(page_title="Physio", layout="wide")
set_custom_style(background_image_path)

if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Sidebar Navigation ---
sidebar_selection = st.sidebar.radio("📂 Navigation", ["Home", "Team", "Profile"])
if sidebar_selection == "Team":
    st.title("👥 Our Team")
    st.markdown("""
    - **عبدالمحسن الدغيم**: Developed the AI wrist tracking system with MediaPipe
    - **Sara Almutairi**: Front-end Developer
    - **Reem Alotaibi**: Project Manager
    - **Faisal Alzahrani**: DevOps Specialist
    """)
    st.stop()

elif sidebar_selection == "Profile":
    st.title("👤 Your Profile")
    st.write("This is your profile page. You can display stats, preferences, etc.")
    st.stop()

# --- Page Routing ---
if st.session_state.page != "home":
    try:
        module = importlib.import_module(f"pages.{st.session_state.page}")
        module.main()
    except Exception as e:
        st.error(f"❌ Failed to load `{st.session_state.page}`: {e}")
    st.stop()

# --- Header Logo and Title ---
st.markdown(f"""
<div class="logo-container" style="margin-bottom: 0.01rem; display: flex; justify-content: center;">
    <img src="data:image/png;base64,{get_base64_of_bin_file(character_image_path)}" width="90">
</div>
<h1 style="margin-top: -20px;">&nbsp;&nbsp;&nbsp;Physio</h1>
<div style="font-family: 'Poppins', sans-serif; font-size: 1rem; color: #334eac; text-align: center; margin-bottom: 4rem;">
    Hello! I'm Physio, your AI Doctor Assistant.
</div>
""", unsafe_allow_html=True)

# --- Exercise Cards ---
exercises = [
    {"title": "Wrist Flexibility", "image": "./images/wrist_flex.jpg", "module": "E1"},
    {"title": "Thumb Opposition", "image": "./images/Thumb Opposition Exercise.png", "module": "E14"},
    {"title": "Neck Tilt", "image": "./images/Neck Tilt.png", "module": "E15"},
]

cols = st.columns(3)
for i, ex in enumerate(exercises):
    with cols[i % 3]:
        st.image(ex["image"], use_column_width=True)
        st.markdown(f"### {ex['title']}")
        if st.button(f"Start {ex['title']}", key=ex["module"]):
            st.session_state.page = ex["module"]
            st.rerun()

# --- Form Section ---
st.markdown("""<div style="padding-left: 3rem; max-width: 600px;">""", unsafe_allow_html=True)

st.markdown('<p class="question-text">&nbsp;&nbsp;How many reps would you like to do?</p>', unsafe_allow_html=True)
reps = st.number_input("", min_value=1, max_value=50, value=10, step=1, format="%d", label_visibility="collapsed", key="reps_input")

st.markdown('<p class="question-text">&nbsp;&nbsp;Which part would you like to focus on?</p>', unsafe_allow_html=True)
body_part = st.selectbox("", ["Left", "Right"], label_visibility="collapsed")

st.markdown("</div>", unsafe_allow_html=True)

# --- Next Button ---
st.markdown("""
<style>
.next-btn {
    background-color: #334EAC;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    border-radius: 10px;
    font-family: sans-serif;
    cursor: pointer;
    transition: all 0.3s ease;
}
.next-btn:hover {
    background-color: #7096d1;
}
</style>
<div style="position: fixed; bottom: 30px; right: 30px; z-index: 9999;">
    <form action="">
        <button type="submit" class="next-btn">
            Next
        </button>
    </form>
</div>
""", unsafe_allow_html=True)
