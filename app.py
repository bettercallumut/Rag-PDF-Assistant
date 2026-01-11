import sys
import os

from platform_config import CURRENT_PLATFORM, IS_ANDROID

print(f"Platform detected: {CURRENT_PLATFORM}")

if IS_ANDROID:
    print("Starting Kivy UI for Android...")
    from main_kivy import main as kivy_main
    kivy_main()
else:
    print("Starting PyQt6 UI for Desktop...")
    from main import app, window
    sys.exit(app.exec())
