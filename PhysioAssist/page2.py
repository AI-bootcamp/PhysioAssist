import streamlit as st
import os
import base64

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Correct filename for background and character image
background_image_path = os.path.join(script_dir, "images", "backgound.jpg")
character_image_path = os.path.join(script_dir, "images", "physio_page2.png")  # Update with your image path

# Convert image to base64 string
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Inject CSS to style background, sidebar, and layout
def set_custom_style(jpg_file):
    bin_str = get_base64_of_bin_file(jpg_file)
    page_bg_img = f"""
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

    .stSelectbox, .stSlider, .stNumberInput {{
        margin-top: -0.5rem !important;
        margin-bottom: 0.5rem !important;
    }}

    div[data-testid="stNumberInput"] {{
        margin-top: 0.5rem !important;
        padding-top: 0 !important;
    }}

    div[data-testid="stNumberInput"] > div {{
        margin-top: 0 !important;
        padding-top: 0 !important;
    }}

    div[data-baseweb="select"], div[data-testid="stNumberInput"] {{
        width: 300px !important;
    }}

    div[data-baseweb="select"] {{
        margin-top: -1rem !important;
    }}

    /* Styles for input bars */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="select"] > div,
    div[data-baseweb="base-input"] > div {{
        background-color: #e9ecee !important;
        border-color: #334eac !important;
        border-radius: 8px !important;
    }}

    /* Style for number input buttons */
    button[data-baseweb="button"] > div > svg {{
        color: #334eac !important;
    }}

    /* Style for dropdown menu */
    div[role="listbox"] {{
        background-color: #e9ecee !important;
    }}

    /* Style for selected option in dropdown */
    li[role="option"]:hover {{
        background-color: #7096d1 !important;
        color: white !important;
    }}

    /* Style for the focused state */
    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within {{
        box-shadow: 0 0 0 2px #7096d1 !important;
    }}

    .logo-container {{
        display: flex;
        justify-content: center;
        margin-bottom: 0.5rem;
    }}

    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    header {{ visibility: hidden; }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Apply custom styles
set_custom_style(background_image_path)

# Center the logo image above the title using a container
st.markdown("""
<div class="logo-container" style="margin-bottom: 0.01rem;">
    <img src="data:image/png;base64,{}" width="90">
</div>
""".format(get_base64_of_bin_file(character_image_path)), unsafe_allow_html=True)

# Centered title using Quicksand SemiBold
st.markdown('<h1 style="margin-top: -20px;">&nbsp;&nbsp;&nbsp;Physio</h1>', unsafe_allow_html=True)

# Centered intro text
st.markdown(
    """
    <div style="font-family: 'Poppins', sans-serif; font-size: 1rem; color: #334eac; text-align: center; margin-bottom: 4rem;">
        Hello! I'm Physio, your AI Doctor Assistant.
    </div>
    """,
    unsafe_allow_html=True
)

# Left-aligned but padded content container
st.markdown("""<div style="padding-left: 3rem; max-width: 600px;">""", unsafe_allow_html=True)

# Left-aligned therapy motivation
st.markdown(
    """
    <div style="font-family: 'Poppins', sans-serif; font-size: 1rem; color: #334eac; text-align: left; margin-bottom: 1rem; font-weight: 600;">
       &nbsp;&nbsp; Let's work through today's therapy session and take one step closer to your recovery:
    </div>
    """,
    unsafe_allow_html=True
)

# Form elements
st.markdown("<p style='color: #334eac; font-family: Poppins, sans-serif; font-size: 1rem; text-align: left; margin-bottom: 1rem;'>&nbsp;&nbsp;Choose an exercise:</p>", unsafe_allow_html=True)
exercise = st.selectbox("", ["Push-ups", "Squats", "Lunges", "Plank", "Stretching"])

st.markdown("""
<div style='color: #334eac; font-family: Poppins, sans-serif; text-align: left; margin-bottom: 0.25rem;'>
    &nbsp;&nbsp;How many reps would you like to do?
</div>
""", unsafe_allow_html=True)
reps = st.number_input("", min_value=1, max_value=50, value=10, step=1, format="%d", 
                      label_visibility="collapsed")

st.markdown("<p style='color: #334eac; font-family: Poppins, sans-serif; text-align: left; margin-bottom: 1rem;'>&nbsp;&nbsp;Which part would you like to focus on?</p>", unsafe_allow_html=True)
body_part = st.selectbox("", ["Left", "Right"])

# Close the padded div
st.markdown("</div>", unsafe_allow_html=True)

# "Next" button in bottom-right corner
st.markdown(
    """
    <style>
    .next-btn {
        background-color: #e9ecee;
        color: #081f5c;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        border-radius: 10px;
        font-family: sans-serif;
        cursor: pointer;
        box-shadow: 0;
        transition: all 0.3s ease;
    }

    .next-btn:hover {
        background-color: #d0d7de;
        color: #334eac;
    }
    </style>

    <div style="position: fixed; bottom: 30px; right: 30px; z-index: 9999;">
        <form action="">
            <button type="submit" class="next-btn">
                Next
            </button>
        </form>
    </div>
    """,
    unsafe_allow_html=True
)