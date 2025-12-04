import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY", "")

# Modern Dark Theme Palette
COLOR_BG = "#18181B"          # Zinc-900 (Daha koyu, sofistike arka plan)
COLOR_PANEL = "#27272A"       # Zinc-800 (Panel rengi)
COLOR_BORDER = "#3F3F46"      # Zinc-700 (Kenarlıklar için)

COLOR_ACCENT = "#6366F1"      # Indigo-500 (Modern, profesyonel mavi-mor)
COLOR_ACCENT_HOVER = "#4F46E5"# Indigo-600

COLOR_TEXT = "#F4F4F5"        # Zinc-100 (Ana metin)
COLOR_TEXT_DIM = "#A1A1AA"    # Zinc-400 (İkincil metin)

COLOR_USER_MSG = "#38BDF8"    # Sky-400 (Kullanıcı mesajı)
COLOR_AI_MSG = "#4ADE80"      # Green-400 (Asistan mesajı)
COLOR_ERROR = "#F87171"       # Red-400 (Hata mesajı)

COLOR_INPUT_BG = "#1E1E20"    # Girdi alanı arka planı

def save_api_key(key):
    with open(".env", "w") as f:
        f.write(f"OPENAI_API_KEY={key}\n")
    global API_KEY
    API_KEY = key

def test_api_key(key):
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        client.models.list()
        return True
    except:
        return False
