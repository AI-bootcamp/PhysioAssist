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
    }}

    .block-container {{
        color: #EDF1F6;
        font-family: 'Roboto', sans-serif;
        padding-left: 0 !important;
        padding-right: 0 !important;
        max-width: none !important;
    }}

    .exercise-box {{
        border: 3px solid transparent;
        border-radius: 15px;
        margin-bottom: 1rem;
        transition: 0.3s ease;
        text-align: center;
        background-color: white;
        cursor: pointer;
        width: 300px;
        height: 300px;
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}

    .exercise-box:hover {{
        border-color: #334eac;
        background-color: #f0f4ff;
    }}

    .exercise-box.selected {{
        border-color: #334eac;
        background-color: #dce6ff;
    }}

    .exercise-button {{
        background-color: #334EAC;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 8px;
        font-family: 'Poppins', sans-serif;
        font-size: 0.9rem;
        cursor: pointer;
        margin-top: 5px;
        width: 100%;
    }}

    .exercise-button:hover {{
        background-color: #7096d1;
    }}

    .question-text {{
        font-size: 1rem;
        font-family: 'Poppins', sans-serif;
        color: #334EAC;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }}

    #MainMenu, header, footer, [data-testid="stSidebarNav"] {{
        display: none !important;
        visibility: hidden !important;
    }}

    .stButton>button {{
        background-color: #7096d1 !important;
        color: white !important;
        padding: 0.5rem 1rem !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 0.9rem !important;
        cursor: pointer !important;
        width: 100% !important;
        margin-bottom: 0.5rem !important;
        transition: background-color 0.3s ease !important;
    }}

    .stButton>button:hover {{
        background-color: #4a7cc7 !important;
    }}

    .sidebar-radio label {{
        display: block;
        padding: 10px 0;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- App Setup ---
st.set_page_config(page_title="Physio", layout="wide")
set_custom_style(background_image_path)

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_exercise" not in st.session_state:
    st.session_state.selected_exercise = None

# --- Handle query param selection ---
if "ex_select" in st.query_params:
    st.session_state.selected_exercise = st.query_params["ex_select"]
    st.session_state.page = st.query_params["page"]
    st.query_params.clear()
    st.rerun()

# --- Sidebar Navigation ---
with st.sidebar:
    if st.button("Home"):
        st.session_state.page = "profile"  # Was 'Profile'
        st.rerun()

    if st.button("Physio"):
        st.session_state.page = "home"  # Was 'Home'
        st.rerun()

    if st.button("Chat"):
        st.session_state.page = "chat"
        st.rerun()

    if st.button("About us"):
        st.session_state.page = "team"  # Was 'Team'
        st.rerun()

# Handle different pages
if "page" in st.query_params:
    page = st.query_params["page"]
    st.session_state.page = page

if st.session_state.page == "team":#========================================================================//
    
# If user navigates to a special sidebar section

    

    # Set background image
    def set_background(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded}");
                background-size: cover;
                background-position: bottom;
                background-repeat: no-repeat;
                font-family: 'Segoe UI', sans-serif;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    background_image_path = os.path.join(script_dir, "images", "backgound.jpg")

    # Add logo to the About Us page
    logo_image_path = os.path.join(script_dir, "images", "about_us logo.png")
    st.markdown(f"""
    <div style="display: flex; justify-content: center; margin-top: 10px; margin-bottom: 20px;">
        <img src="data:image/png;base64,{get_base64_of_bin_file(logo_image_path)}" width="230">
    </div>
    """, unsafe_allow_html=True)

    

    # Enhanced card CSS: Wider + Tall + Responsive
    st.markdown("""
        <style>
        .team-card {
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 25px;
            margin: 20px auto;
            width: 90%;
            text-align: center;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            transition: transform 0.2s ease-in-out;
            height: 400px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            word-wrap: break-word;
        }
        .team-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 28px rgba(0,0,0,0.3);
        }
        .team-name {
            font-size: 22px;
            font-weight: bold;
            color: #003366;
            margin-bottom: 12px;
        }
        .team-link {
            display: inline-block;
            margin-bottom: 12px;
            color: #0077b5;
            font-weight: 600;
            text-decoration: none;
        }
        .team-link:hover {
            text-decoration: underline;
        }
        .team-bio {
            font-size: 15px;
            color: #444;
            line-height: 1.6;
            overflow-wrap: break-word;
            word-break: break-word;
        }
        </style>
    """, unsafe_allow_html=True)

    # Team members
    team = [
        {
            "name": "Wasan Alotaibi",
            "linkedin": "https://www.linkedin.com/in/wasano?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app",
            "bio": "We developed an intelligent system where a camera serves as a virtual assistant for physical therapy. It uses MediaPipe for tracking and analyzing joint angles to monitor the user's movements, ensuring correct execution of exercises. I contributed to the computer vision backend, focusing on joint analysis for accurate therapy guidance, and worked on developing a customized AI chat feature."
        },
        {
            "name": "Renad Alajmi ",
            "linkedin": "https://www.linkedin.com/in/re30",
            "bio": "We developed an intelligent system where a camera serves as a virtual assistant for physical therapy. It uses MediaPipe for tracking and analyzing joint angles to monitor the user's movements, ensuring correct execution of exercises. I contributed to both the computer vision backend, focusing on joint analysis for accurate therapy guidance, and the frontend, using Streamlit to create a user-friendly, interactive interface."
        },
        {
            "name": "Abdulmohsen Aldughayem",
            "linkedin": "https://www.linkedin.com/in/abdulmohsen-adel-aldughayem",
            "bio": "We developed an intelligent system where a camera serves as a virtual assistant for physical therapy. It uses MediaPipe for tracking and analyzing joint angles to monitor the user's movements, ensuring correct execution of exercises. I contributed to both the computer vision backend, focusing on joint analysis for accurate therapy guidance, and the frontend, using Streamlit to create a user-friendly, interactive interface."
        },
        {
            "name": "Alhanouf Alswayed",
            "linkedin": "https://www.linkedin.com/in/alhanof-a-0997162a0?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app",
            "bio": "We developed an intelligent system where a camera serves as a virtual assistant for physical therapy. It uses MediaPipe for tracking and analyzing joint angles to monitor the user's movements, ensuring correct execution of exercises. I contributed to both the computer vision backend, focusing on joint analysis for accurate therapy guidance, and the frontend, using Streamlit to create a user-friendly, interactive interface."
        },
        {
            "name": "Abdulaziz Alkharjy",
            "linkedin": "https://www.linkedin.com/in/abdulaziz--saad?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app",
            "bio": "We developed an intelligent system where a camera serves as a virtual assistant for physical therapy. It uses MediaPipe for tracking and analyzing joint angles to monitor the user's movements, ensuring correct execution of exercises, and I worked on developing a customized AI chat feature."
        }

        
    ]


    # Use 3 columns per row for wider layout
    rows = [team[i:i+3] for i in range(0, len(team), 3)]
    for row in rows:
        cols = st.columns(len(row))
        for idx, member in enumerate(row):
            with cols[idx]:
                st.markdown(f"""
                    <div class="team-card">
                        <div class="team-name">{member['name']}</div>
                        <a class="team-link" href="{member['linkedin']}" target="_blank">LinkedIn Profile</a>
                        <div class="team-bio">{member['bio']}</div>
                    </div>
                """, unsafe_allow_html=True)
    st.stop()

elif st.session_state.page == "profile":
    logo_image_path = os.path.join(script_dir, "images", "Physio_1.png")

    def set_custom_style(jpg_file):
        bin_str = get_base64_of_bin_file(jpg_file)
        st.markdown(f"""
        <style>
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
        """, unsafe_allow_html=True)

    set_custom_style(background_image_path)

    st.markdown(f"""
    <div class="logo-container" style="margin-bottom: 0.01rem;">
        <img src="data:image/png;base64,{get_base64_of_bin_file(logo_image_path)}" width="90">
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<h1 style="margin-top: -20px;">&nbsp;&nbsp;PhysioAssist</h1>', unsafe_allow_html=True)

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
    st.stop()

# --- Page Routing ---
if st.session_state.page != "home":
    try:
        module = importlib.import_module(f"pages.{st.session_state.page}")
        module.main()
    except Exception as e:
        st.error(f"❌ Failed to load `{st.session_state.page}`: {e}")
    st.stop()

# --- Header Logo, Title, and Subtitle ---
st.markdown(f"""
<div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 4rem;">
    <img src="data:image/png;base64,{get_base64_of_bin_file(character_image_path)}" width="90">
    <h1 style="margin-top: -10px; font-family: 'Poppins', sans-serif; color: #334eac; margin-left: 30px;">Physio</h1>
    <div style="font-family: 'Poppins', sans-serif; font-size: 1rem; color: #334eac; text-align: center;">
        Hello! I'm Physio, your AI Doctor Assistant.
    </div>
</div>
""", unsafe_allow_html=True)

# --- Exercise List ---
exercises = [
    {"title": "Wrist Flexibility", "image": "./images/wrist_flex_white.jpg", "module": "E1"},
    {"title": "Thumb Opposition", "image": "./images/Thumb Opposition Exercise_white.jpg", "module": "E14"},
    {"title": "Finger Resistance", "image": "./images/Finger Resistance_white.png", "module": "E15"},
    {"title": "Pronation vs Supination", "image": "./images/Pronation vs Supination_white.jpg", "module": "E16"},
    {"title": "Pose Tracker", "image": "./images/Shoulder Abduction.jpeg", "module": "pose_tracker"},
    {"title": "Neck Tilt", "image": "./images/Neck Tilt_white.jpg", "module": "pose_tracker"}, 
    {"title": "Knee Extension", "image": "./images/Knee Extension.png", "module": "pose_tracker"},
]

st.markdown('<div style="color: #334EAC; font-size: 1.1rem; font-family: Poppins, sans-serif; margin-bottom: 1.5rem;">Let\'s work through today\'s therapy session and take one step closer to your recovery:</div>', unsafe_allow_html=True)

cols = st.columns(3)
for i, ex in enumerate(exercises):
    with cols[i % 3]:
        selected = st.session_state.selected_exercise == ex["title"]
        box_class = "exercise-box selected" if selected else "exercise-box"
        image_base64 = get_base64_of_bin_file(ex["image"])
        st.markdown(f"""
        <div class="{box_class}">
            <img src="data:image/png;base64,{image_base64}" style="width:100%; height:85%; object-fit: cover; border-radius:10px 10px 0 0;" />
            <div>
                <a href="?page={ex['module']}&ex_select={ex['title']}">
                    <button class="exercise-button">{ex['title']}</button>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
