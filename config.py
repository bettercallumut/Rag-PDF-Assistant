import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY", "")

TTS_ENGINE = "openai"
TTS_LOCAL_RATE = 150

try:
    from platform_config import (
        CURRENT_PLATFORM,
        TTS_ENGINE as PLATFORM_TTS_ENGINE,
        TTS_LANGUAGE,
        MAX_CONTEXT_TOKENS,
        IS_WINDOWS,
        IS_ANDROID
    )
except ImportError:
    CURRENT_PLATFORM = "windows"
    PLATFORM_TTS_ENGINE = "pyttsx3"
    TTS_LANGUAGE = "tr"
    MAX_CONTEXT_TOKENS = 25000
    IS_WINDOWS = True
    IS_ANDROID = False

COLOR_BG = "#18181B"
COLOR_PANEL = "#27272A"
COLOR_BORDER = "#3F3F46"
COLOR_ACCENT = "#6366F1"
COLOR_ACCENT_HOVER = "#4F46E5"
COLOR_TEXT = "#F4F4F5"
COLOR_TEXT_DIM = "#A1A1AA"
COLOR_USER_MSG = "#38BDF8"
COLOR_AI_MSG = "#4ADE80"
COLOR_ERROR = "#F87171"
COLOR_INPUT_BG = "#1E1E20"

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
