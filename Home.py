import streamlit as st
import os
import base64

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Correct filename for background and logo image
background_image_path = os.path.join(script_dir, "images", "backgound.jpg")
logo_image_path = os.path.join(script_dir, "images", "Physio_full body.png")

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

    .logo-container {{
        display: flex;
        justify-content: center;
        margin-bottom: 0.5rem;
    }}

    .intro-text {{
        font-family: 'Poppins', sans-serif;
        font-size: 1rem;
        color: #334eac;
        text-align: center;
        margin-bottom: 4rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }}

    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    header {{ visibility: hidden; }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Apply custom styles
set_custom_style(background_image_path)

# Sidebar content
st.sidebar.title("Navigation")
st.sidebar.write("Choose a section:")

# Center the logo image above the title using a container
st.markdown("""
<div class="logo-container" style="margin-bottom: 0.01rem;">
    <img src="data:image/png;base64,{}" width="90">
</div>
""".format(get_base64_of_bin_file(logo_image_path)), unsafe_allow_html=True)

# Centered title using Quicksand SemiBold
st.markdown('<h1 style="margin-top: -20px;">&nbsp;&nbsp;PhysioAssist</h1>', unsafe_allow_html=True)

# Centered intro text with project explanation
st.markdown(
    """
    <div class="intro-text">
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Don't have time for a second appointment?  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  PhysioAssist is here to help.
         Our platform combines AI-powered guidance with targeted exercises to support your recovery journey. 
         Whether you're rehabilitating from an injury or working to improve mobility, PhysioAssist offers personalized exercises 
         and performance tracking to help you achieve your physiotherapy goals.
    </div>
    """,
    unsafe_allow_html=True
)

# Get started button
st.markdown(
    """
    <style>
    .start-btn {
        background-color: #334EAC;
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        border-radius: 10px;
        font-family: sans-serif;
        cursor: pointer;
        transition: all 0.3s ease;
        display: block;
        margin: 0 auto;
    }

    .start-btn:hover {
        background-color: #7096d1;
    }
    </style>

    <div style="text-align: center; margin-top: 2rem;">
        <form action="">
            <button type="submit" class="start-btn">
                Get Started
            </button>
        </form>
    </div>
    """,
    unsafe_allow_html=True
)