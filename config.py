import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY", "")

COLOR_BG = "#121212"
COLOR_PANEL = "#1E1E1E"
COLOR_ACCENT = "#D32F2F"
COLOR_ACCENT_HOVER = "#B71C1C"
COLOR_TEXT = "#E0E0E0"
COLOR_USER_MSG = "#4FC3F7"
COLOR_AI_MSG = "#81C784"
COLOR_ERROR = "#EF5350"

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
