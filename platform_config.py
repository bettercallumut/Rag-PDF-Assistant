import platform
import os
from typing import Literal

PlatformType = Literal["windows", "android", "linux"]

def detect_platform() -> PlatformType:
    system = platform.system().lower()
    
    if 'ANDROID_ROOT' in os.environ or 'ANDROID_DATA' in os.environ:
        return "android"
    
    try:
        import jnius
        return "android"
    except ImportError:
        pass
    
    if 'win' in system:
        return "windows"
    elif 'linux' in system:
        return "linux"
    else:
        return "windows"

class PlatformConfig:
    def __init__(self, platform: PlatformType, tts_engine: str, ui_framework: str,
                 supports_local_tts: bool, requires_internet: bool, temp_dir: str,
                 max_context_tokens: int = 25000):
        self.platform = platform
        self.tts_engine = tts_engine
        self.ui_framework = ui_framework
        self.supports_local_tts = supports_local_tts
        self.requires_internet = requires_internet
        self.temp_dir = temp_dir
        self.max_context_tokens = max_context_tokens
    
    @classmethod
    def create_for_platform(cls, platform_type: PlatformType = None):
        if platform_type is None:
            platform_type = detect_platform()
        
        if platform_type == "windows":
            return cls(
                platform="windows",
                tts_engine="pyttsx3",
                ui_framework="pyqt6",
                supports_local_tts=True,
                requires_internet=False,
                temp_dir=os.environ.get('TEMP', '/tmp'),
                max_context_tokens=25000
            )
        elif platform_type == "android":
            return cls(
                platform="android",
                tts_engine="gtts",
                ui_framework="kivy",
                supports_local_tts=False,
                requires_internet=True,
                temp_dir="/data/local/tmp",
                max_context_tokens=20000
            )
        else:
            return cls(
                platform="linux",
                tts_engine="gtts",
                ui_framework="pyqt6",
                supports_local_tts=False,
                requires_internet=True,
                temp_dir="/tmp",
                max_context_tokens=25000
            )

CURRENT_PLATFORM = detect_platform()
_config = PlatformConfig.create_for_platform(CURRENT_PLATFORM)

TTS_ENGINE = _config.tts_engine
UI_FRAMEWORK = _config.ui_framework
MAX_CONTEXT_TOKENS = _config.max_context_tokens
IS_WINDOWS = CURRENT_PLATFORM == "windows"
IS_ANDROID = CURRENT_PLATFORM == "android"
TTS_LANGUAGE = "tr"
