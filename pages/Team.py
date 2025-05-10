import streamlit as st
from PIL import Image
import base64

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

set_background("./Untitled design.png")

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
        "name": "",
        "linkedin": "https://www.linkedin.com/in/example1",
        "bio": "AI Researcher specializing in deep learning, neural networks, and predictive analytics for smart enterprise systems."
    },
    {
        "name": "Sara Almutairi",
        "linkedin": "https://www.linkedin.com/in/example2",
        "bio": "Creative front-end developer passionate about crafting elegant, responsive, and accessible user interfaces for modern web applications."
    },
    {
        "name": "عبدالمحسن الدغيم",
        "linkedin": "https://www.linkedin.com/in/abdulmohsen-adel-aldughayem",
        "bio": "في هذا المشروع، طورت نظامًا ذكيًا يتعرف على حركة اليد ويحسب عدد التكرارات تلقائيًا أثناء أداء التمرين، باستخدام الكاميرا فقط. استخدمت مكتبة MediaPipe لتتبع نقاط اليد بدقة، مع خوارزميات لحساب الزوايا بين المفاصل لتحديد الوضع الصحيح للحركة."
    },
    {
        "name": "Reem Alotaibi",
        "linkedin": "https://www.linkedin.com/in/example4",
        "bio": "Project Manager experienced in agile delivery, team leadership, stakeholder alignment, and launching AI-powered platforms."
    },
    {
        "name": "Faisal Alzahrani",
        "linkedin": "https://www.linkedin.com/in/example5",
        "bio": "DevOps and Cloud Specialist skilled in CI/CD pipelines, infrastructure as code (IaC), and cloud-native architecture on AWS and Azure."
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
