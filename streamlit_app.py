import streamlit as st
import requests
import json

# Page Config
st.set_page_config(
    page_title="معلمك الخاص",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stTextInput > div > div > input {
        text-align: right;
        direction: rtl;
    }
    .stChatInput > div > div > textarea {
        text-align: right;
        direction: rtl;
    }
    .stMarkdown {
        text-align: right;
        direction: rtl;
    }
    div[data-testid="stChatMessageContent"] {
        text-align: right;
        direction: rtl;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    h1 {
        text-align: center; 
        color: #2e86c1;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
    st.title("إعدادات المعلم")
    
    if "api_url" not in st.session_state:
        st.session_state.api_url = ""
        
    api_url_input = st.text_input(
        "رابط السيرفر (Ngrok URL)", 
        value=st.session_state.api_url,
        placeholder="https://xxxx.ngrok-free.app",
        help="انسخ الرابط من كود كاجل والصقه هنا"
    )
    
    if api_url_input:
        st.session_state.api_url = api_url_input.rstrip("/")

    st.markdown("---")
    
    subject = st.selectbox(
        "اختر المادة الدراسية",
        ["رياضيات", "كيمياء", "لغة عربية", "فيزياء", "تاريخ", "جغرافيا", "إنجليزي"],
        index=0
    )
    
    st.markdown("---")
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 معلمك الخاص المصري")
st.markdown("<h4 style='text-align: center; color: gray;'>اسألني في أي مادة وهشرحلك بالمصري البسيط</h4>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اكتب سؤالك هنا..."):
    if not st.session_state.api_url:
        st.error("⚠️ من فضلك أدخل رابط السيرفر في القائمة الجانبية أولاً!")
    else:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        history_pairs = []
        temp_user = None
        for msg in st.session_state.messages[:-1]:
            if msg["role"] == "user":
                temp_user = msg["content"]
            elif msg["role"] == "assistant" and temp_user:
                history_pairs.append([temp_user, msg["content"]])
                temp_user = None

        with st.chat_message("assistant"):
            with st.spinner("بيفكر..."):
                try:
                    payload = {
                        "message": prompt,
                        "subject": subject,
                        "history": history_pairs
                    }
                    
                    full_url = f"{st.session_state.api_url}/chat"
                    response = requests.post(full_url, json=payload, timeout=60)
                    
                    if response.status_code == 200:
                        bot_reply = response.json().get("response", "مفيش رد وصل من السيرفر.")
                        st.markdown(bot_reply)
                        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                    else:
                        st.error(f"خطأ من السيرفر: {response.status_code}")
                except Exception as e:
                    st.error(f"فشل الاتصال: {e}")
                    st.info("تأكد أن رابط Ngrok صحيح وأن السيرفر شغال.")