import streamlit as st
import os
import tempfile
import config
from rag_system import RAGSystem

# Sayfa Yapılandırması (Mobil Dostu)
st.set_page_config(
    page_title="Neural Core Mobil",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Optimizasyonu (Mobil için)
st.markdown("""
<style>
    /* Font ve Renk Ayarları */
    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }
    .stTextInput > div > div > input {
        background-color: #2A2A2A;
        color: white;
        border: 1px solid #444;
        border-radius: 10px;
    }
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        background-color: #D32F2F;
        color: white;
        border: none;
    }
    .stButton > button:hover {
        background-color: #B71C1C;
    }

    /* Mobil Sohbet Baloncukları */
    .user-msg {
        background-color: #1E88E5;
        color: white;
        padding: 10px;
        border-radius: 15px 15px 0 15px;
        margin: 5px 0;
        text-align: right;
        float: right;
        clear: both;
        max-width: 80%;
    }
    .ai-msg {
        background-color: #43A047;
        color: white;
        padding: 10px;
        border-radius: 15px 15px 15px 0;
        margin: 5px 0;
        text-align: left;
        float: left;
        clear: both;
        max-width: 80%;
    }
    .clearfix::after {
        content: "";
        clear: both;
        display: table;
    }
</style>
""", unsafe_allow_html=True)

# Oturum Durumu Başlatma
if "rag" not in st.session_state:
    st.session_state.rag = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key" not in st.session_state:
    st.session_state.api_key = config.API_KEY

def init_rag():
    if st.session_state.rag is None:
        try:
            with st.spinner("AI Sistemi Yükleniyor..."):
                st.session_state.rag = RAGSystem()
            st.toast("Sistem Hazır!", icon="✅")
        except Exception as e:
            st.error(f"Başlatma Hatası: {e}")

def process_pdf(uploaded_file):
    if uploaded_file and st.session_state.rag:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        try:
            with st.spinner("PDF Analiz Ediliyor..."):
                chunk_count = st.session_state.rag.process_pdf(tmp_path)
            st.toast(f"PDF Yüklendi! ({chunk_count} parça)", icon="📄")
            os.remove(tmp_path)
        except Exception as e:
            st.error(f"PDF Hatası: {e}")

# --- Arayüz ---
st.title("Neural Core 🤖")

# API Key Kontrolü
if not st.session_state.api_key:
    api_input = st.text_input("OpenAI API Anahtarı", type="password")
    if st.button("Kaydet"):
        if config.test_api_key(api_input):
            config.save_api_key(api_input)
            st.session_state.api_key = api_input
            st.rerun()
        else:
            st.error("Geçersiz API Anahtarı")
    st.stop()

# Sistemi Başlat
init_rag()

# Sidebar (Menü)
with st.sidebar:
    st.header("Ayarlar")
    uploaded_file = st.file_uploader("PDF Yükle", type=["pdf"])
    if uploaded_file:
        if st.button("PDF'i İşle"):
            process_pdf(uploaded_file)

    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

# Sohbet Geçmişi
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            st.markdown(f"<div class='user-msg'>{content}</div><div class='clearfix'></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='ai-msg'>{content}</div><div class='clearfix'></div>", unsafe_allow_html=True)

# Girdi Alanı (Alt Kısım)
prompt = st.chat_input("Bir soru sorun...")

if prompt:
    if not st.session_state.rag:
        st.error("Sistem hazır değil.")
    else:
        # Kullanıcı mesajını ekle
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            st.markdown(f"<div class='user-msg'>{prompt}</div><div class='clearfix'></div>", unsafe_allow_html=True)

        # Yanıt üret
        with st.spinner("Düşünüyor..."):
            response = st.session_state.rag.query(prompt, st.session_state.api_key)

            # Fallback kontrolü
            if response == "###ASK_FALLBACK###":
                response = st.session_state.rag.query_general(prompt, st.session_state.api_key)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
