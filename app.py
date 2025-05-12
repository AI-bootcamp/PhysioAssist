import os
import streamlit as st
import groq
from dotenv import load_dotenv
import base64



# 1) تحميل متغيرات البيئة
load_dotenv()
client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

# 2) إعداد الصفحة
st.set_page_config(
    page_title="أخصائي العلاج الطبيعي الذكي",
    page_icon="🩺",
    initial_sidebar_state="collapsed",
    layout="wide"
)
st.title("🩺 أخصائي العلاج الطبيعي الذكي بالعربي")

# ─── inject CSS to right-align user bubbles ─────────────────────
st.markdown(
    """
    <style>
      /* chat bubbles */
      .msg { display: flex; align-items: flex-start; margin-bottom: 0.75rem; clear: both; }
      .assistant { justify-content: flex-start; }
      .user      { justify-content: flex-end; }

      .bubble {
        max-width: 60%;
        padding: 0.75rem 1rem;
        border-radius: 1rem;
        line-height: 1.4;
        word-wrap: break-word;
      }

      /* Assistant bubble */
      .assistant .bubble {
        background: #E5E5EA !important;
        color: #000 !important;
      }

      /* <-- Updated User bubble color here --> */
      .user .bubble {
        background: #BBD6EB !important;
        color: #000 !important;
      }

      .avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        margin: 0 0.5rem;
      }

      /* input bar styling (unchanged) */
      div[data-testid="stChatInput"] { margin-top: 1rem !important; }
      textarea[role="textbox"] {
        width: 100% !important;
        padding: 12px !important;
        border: none !important;
        border-radius: 18px !important;
        background: #262626 !important;
        color: #fff !important;
        font-size: 16px !important;
        outline: none !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.2) !important;
      }
      textarea[role="textbox"]::placeholder { color: #999 !important; }
      button[kind="primary"] {
        padding: 10px 20px !important;
        margin-left: 0.5rem !important;
        background: #4CAF50 !important;
        color: #fff !important;
        border: none !important;
        border-radius: 18px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2) !important;
      }
      button[kind="primary"]:hover { background: #45a049 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ─── Helper to force left/right layout ─────────────────────────
def render_message(role, text, avatar_uri):
    """
    role 'assistant' → left, role 'user' → right
    """
    if role == "assistant":
        html = f'''
          <div class="msg assistant">
            <img src="{avatar_uri}" class="avatar"/>
            <div class="bubble">{text}</div>
          </div>'''
    else:
        html = f'''
          <div class="msg user">
            <div class="bubble">{text}</div>
            <img src="{avatar_uri}" class="avatar"/>
          </div>'''
    st.markdown(html, unsafe_allow_html=True)



def img_to_datauri(path: str) -> str:
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f"data:image/png;base64,{b64}"

USER_ICON_URI      = img_to_datauri("assets/user_icon.png")
ASSISTANT_ICON_URI = img_to_datauri("assets/assistant_icon.png")





# ─── instead of st.sidebar.title, in code defaults ──────────────────
# Sidebar UI gone; we hard-code our defaults here:


# # 3) شريط جانبي: تخصيص مدرب العلاج الطبيعي
# st.sidebar.title("تخصيص مدرب العلاج الطبيعي")

# # اختيار النموذج
# model_options = {
#     "Llama 3 8B":   "llama3-8b-8192",
#     "Mixtral 8x7B": "mixtral-8x7b-32768",
#     "Gemma 7B":     "gemma-7b-it"
# }
# selected_model = st.sidebar.selectbox("اختر نموذج AI", list(model_options.keys()))
# model = model_options[selected_model]

# # ضبط العشوائية والطوكنز
# temperature = st.sidebar.slider("عشوائية الردّ", 0.0, 1.0, 0.7, 0.1)
# max_tokens = st.sidebar.slider("الحد الأقصى للطوكنز", 50, 4096, 1024, 50)

# # شخصية أخصائي العلاج الطبيعي فقط
# character_options = {
#     "أخصائي علاج طبيعي - إرشادات عامة": (
#         "أنت أخصائي علاج طبيعي محترف، تقدّم للمستخدم تعليمات واضحة لتصحيح الوضعيات وتحسين الأداء. "
#         "تتحدّث بلغة بسيطة وداعمة، مع أمثلة عملية لكل تمرين."
#     ),
#     "أخصائي إعادة تأهيل بعد جراحة": (
#         "أنت أخصائي علاج طبيعي مختص في إعادة التأهيل بعد الجراحة. "
#         "تتأكد من تقديم نصائح آمنة ومناسبة لمرحلة التعافي، وتعمل على تقليل الألم وتعزيز الحركة."
#     )
# }
# selected_character = st.sidebar.selectbox("اختر أسلوب الأخصائي", list(character_options.keys()))
# character_prompt = character_options[selected_character]

# # نبرة الصوت للعلاج الطبيعي
# mood_options = {
#     "محايد": "",
#     "مشجّع": "تحدث بأسلوب يحفّز المريض ويشجعه على الاستمرار.",
#     "صبور": "استخدم لغة هادئة وصبورة، وأضف تفسيرات مبسطة عند الحاجة."
# }
# selected_mood = st.sidebar.selectbox("اختر نبرة الصوت", list(mood_options.keys()))
# mood_prompt = mood_options[selected_mood]

# # دمج نص النظام
# system_prompt = character_prompt
# if mood_prompt:
#     system_prompt += " " + mood_prompt

# # خيار نص نظام مخصص
# if st.sidebar.checkbox("نظام مخصص"):
#     system_prompt = st.sidebar.text_area("نص نظام مخصص:", value=system_prompt, height=100)

# # إعدادات الإيموجي
# emoji_use = st.sidebar.select_slider(
#     "استخدام الإيموجي", ["لا شيء", "قليل", "متوسط", "كثير"], value="قليل"
# )
# if emoji_use == "لا شيء":
#     system_prompt += " لا تستخدم أي رموز تعبيرية."
# elif emoji_use == "كثير":
#     system_prompt += " استخدم الكثير من الرموز التعبيرية المناسبة للتشجيع."

# # رابط لدليل التخصيص (اختياري)
# st.sidebar.markdown("---")
# st.sidebar.markdown("[📋 دليل تخصيص العلاج الطبيعي](Cheat_Sheets/README.md)")


# ─── instead of st.sidebar.title, in code defaults ──────────────────
# Sidebar UI gone; we hard-code our defaults here:
DEFAULT_MODEL_KEY      = "ALLAM-2-7b"
DEFAULT_TEMPERATURE    = 0.7
DEFAULT_MAX_TOKENS     = 1024
DEFAULT_CHARACTER_KEY  = "أخصائي علاج طبيعي - إرشادات عامة"
DEFAULT_MOOD_KEY       = "محايد"   # choices: "محايد", "مشجّع", "صبور"
DEFAULT_EMOJI_USE      = "قليل"   # choices: "لا شيء", "قليل", "متوسط", "كثير"
USE_CUSTOM_SYSTEM_TEXT = False
CUSTOM_SYSTEM_TEXT     = ""       # fill if USE_CUSTOM_SYSTEM_TEXT=True

# ─── same option dicts as before ────────────────────────────────────
model_options = {
    "Llama 3 8B":   "llama3-8b-8192",
    "Mixtral 8x7B": "mixtral-8x7b-32768",
    "Gemma 7B":     "gemma-7b-it",
    "ALLAM-2-7b": "allam-2-7b"
}
character_options = {
    "أخصائي علاج طبيعي - إرشادات عامة": (
        "أنت أخصائي علاج طبيعي محترف، تقدّم للمستخدم تعليمات واضحة لتصحيح الوضعيات وتحسين الأداء. "
        "تتحدّث بلغة بسيطة وداعمة، مع أمثلة عملية لكل تمرين."
    ),
    "أخصائي إعادة تأهيل بعد جراحة": (
        "أنت أخصائي علاج طبيعي مختص في إعادة التأهيل بعد الجراحة. "
        "تتأكد من تقديم نصائح آمنة ومناسبة لمرحلة التعافي، وتعمل على تقليل الألم وتعزيز الحركة."
    )
}
mood_options = {
    "محايد": "",
    "مشجّع": "تحدث بأسلوب يحفّز المريض ويشجعه على الاستمرار.",
    "صبور": "استخدم لغة هادئة وصبورة، وأضف تفسيرات مبسطة عند الحاجة."
}

# ─── now derive your runtime settings ────────────────────────────────
selected_model   = DEFAULT_MODEL_KEY
model            = model_options[selected_model]
temperature      = DEFAULT_TEMPERATURE
max_tokens       = DEFAULT_MAX_TOKENS

selected_character = DEFAULT_CHARACTER_KEY
character_prompt   = character_options[selected_character]

selected_mood  = DEFAULT_MOOD_KEY
mood_prompt    = mood_options[selected_mood]

emoji_use      = DEFAULT_EMOJI_USE

# build the system prompt
if USE_CUSTOM_SYSTEM_TEXT and CUSTOM_SYSTEM_TEXT:
    system_prompt = CUSTOM_SYSTEM_TEXT
else:
    system_prompt = character_prompt
    if mood_prompt:
        system_prompt += " " + mood_prompt

    if emoji_use == "لا شيء":
        system_prompt += " لا تستخدم أي رموز تعبيرية."
    elif emoji_use == "كثير":
        system_prompt += " استخدم الكثير من الرموز التعبيرية المناسبة للتشجيع."


# 4) تهيئة سجل المحادثة
# بعد إعداد system prompt وتعديل session_state.messages:
if "messages" not in st.session_state:
    # نبدأ بقائمة تحتوي على system prompt
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    # نضيف رسالة ترحيبية من النموذج نفسه
    welcome = (
        f"مرحبًا! أنا أخصائي العلاج الطبيعي الذكي. "
        "أنا هنا لأساعدك في تصحيح الوضعيات وتحسين أدائك. كيف يمكنني مساعدتك اليوم؟"
    )
    st.session_state.messages.append({"role": "assistant", "content": welcome})
else:
    # لو أردت تحديث system_prompt في rerun
    st.session_state.messages[0]["content"] = system_prompt



# 5) عرض المحادثات السابقة
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue

    # pick the right data‐URI
    uri = USER_ICON_URI if msg["role"] == "user" else ASSISTANT_ICON_URI

    if msg["role"] == "assistant":
        html = f'''
          <div class="msg assistant">
            <img src="{uri}" class="avatar"/>
            <div class="bubble">{msg["content"]}</div>
          </div>
        '''
    else:
        html = f'''
          <div class="msg user">
            <div class="bubble">{msg["content"]}</div>
            <img src="{uri}" class="avatar"/>
          </div>
        '''

    st.markdown(html, unsafe_allow_html=True)


# 6) إدخال المستخدم واستدعاء الـ API
user_input = st.chat_input("اسأل عن تمرينك أو حالتك العلاجية…")
if user_input:
    # record user
    st.session_state.messages.append({"role": "user", "content": user_input})
    # render user
    render_message("user", user_input, USER_ICON_URI)

    # call API
    try:
        resp = client.chat.completions.create(
            messages=st.session_state.messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        reply = resp.choices[0].message.content
    except Exception as e:
        reply = f"خطأ في الـ API: {e}"

    # record + render assistant
    st.session_state.messages.append({"role": "assistant", "content": reply})
    render_message("assistant", reply, ASSISTANT_ICON_URI)

# 7) زر إعادة الضبط
if st.sidebar.button("إعادة ضبط"):
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.rerun()

# 8) معلومات الـ API في الأسفل
st.sidebar.divider()
st.sidebar.caption(f"النموذج الحالي: {model}")
if not os.getenv("GROQ_API_KEY"):
    st.sidebar.warning("⚠️ مفتاح Groq API غير موجود. تأكد من ملف .env")
