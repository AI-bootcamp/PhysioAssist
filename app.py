import os
import streamlit as st
import groq
from dotenv import load_dotenv

# 1) تحميل متغيرات البيئة
load_dotenv()
client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

# 2) إعداد الصفحة
st.set_page_config(
    page_title="أخصائي العلاج الطبيعي الذكي",
    page_icon="🩺",
    layout="wide"
)
st.title("🩺 أخصائي العلاج الطبيعي الذكي بالعربي")

# 3) شريط جانبي: تخصيص مدرب العلاج الطبيعي
st.sidebar.title("تخصيص مدرب العلاج الطبيعي")

# اختيار النموذج
model_options = {
    "Llama 3 8B":   "llama3-8b-8192",
    "Mixtral 8x7B": "mixtral-8x7b-32768",
    "Gemma 7B":     "gemma-7b-it"
}
selected_model = st.sidebar.selectbox("اختر نموذج AI", list(model_options.keys()))
model = model_options[selected_model]

# ضبط العشوائية والطوكنز
temperature = st.sidebar.slider("عشوائية الردّ", 0.0, 1.0, 0.7, 0.1)
max_tokens = st.sidebar.slider("الحد الأقصى للطوكنز", 50, 4096, 1024, 50)

# شخصية أخصائي العلاج الطبيعي فقط
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
selected_character = st.sidebar.selectbox("اختر أسلوب الأخصائي", list(character_options.keys()))
character_prompt = character_options[selected_character]

# نبرة الصوت للعلاج الطبيعي
mood_options = {
    "محايد": "",
    "مشجّع": "تحدث بأسلوب يحفّز المريض ويشجعه على الاستمرار.",
    "صبور": "استخدم لغة هادئة وصبورة، وأضف تفسيرات مبسطة عند الحاجة."
}
selected_mood = st.sidebar.selectbox("اختر نبرة الصوت", list(mood_options.keys()))
mood_prompt = mood_options[selected_mood]

# دمج نص النظام
system_prompt = character_prompt
if mood_prompt:
    system_prompt += " " + mood_prompt

# خيار نص نظام مخصص
if st.sidebar.checkbox("نظام مخصص"):
    system_prompt = st.sidebar.text_area("نص نظام مخصص:", value=system_prompt, height=100)

# إعدادات الإيموجي
emoji_use = st.sidebar.select_slider(
    "استخدام الإيموجي", ["لا شيء", "قليل", "متوسط", "كثير"], value="قليل"
)
if emoji_use == "لا شيء":
    system_prompt += " لا تستخدم أي رموز تعبيرية."
elif emoji_use == "كثير":
    system_prompt += " استخدم الكثير من الرموز التعبيرية المناسبة للتشجيع."

# رابط لدليل التخصيص (اختياري)
st.sidebar.markdown("---")
st.sidebar.markdown("[📋 دليل تخصيص العلاج الطبيعي](Cheat_Sheets/README.md)")

# 4) تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
else:
    st.session_state.messages[0]["content"] = system_prompt

# 5) عرض المحادثات السابقة
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 6) إدخال المستخدم واستدعاء الـ API
user_input = st.chat_input("اسأل عن تمرينك أو حالتك العلاجية…")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            resp = client.chat.completions.create(
                messages=st.session_state.messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            reply = resp.choices[0].message.content
            placeholder.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            placeholder.error(f"خطأ في الـ API: {e}")

# 7) زر إعادة الضبط
if st.sidebar.button("إعادة ضبط"):
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.rerun()

# 8) معلومات الـ API في الأسفل
st.sidebar.divider()
st.sidebar.caption(f"النموذج الحالي: {model}")
if not os.getenv("GROQ_API_KEY"):
    st.sidebar.warning("⚠️ مفتاح Groq API غير موجود. تأكد من ملف .env")
