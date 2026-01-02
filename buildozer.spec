[app]

# Uygulama bilgileri
title = PDF Asistanı
package.name = pdfassistant
package.domain = org.ragassistant

# Kaynak kodu
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

# Sürüm
version = 2.0
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/version.json

# Gereksinimler
requirements = python3,kivy,openai,langchain,langchain-community,langchain-openai,requests,PyPDF2,python-dotenv,gtts

# İzinler
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# Android API
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Orientation
orientation = portrait

# Icon ve Splash (opsiyonel)
#icon.filename = %(source.dir)s/icon.png
#presplash.filename = %(source.dir)s/presplash.png

# Fullscreen
fullscreen = 0

# Android meta-data
android.meta_data = com.google.android.gms.version=@integer/google_play_services_version

# Android services  
# android.services = TTS:tts_service.py

# Loglar
log_level = 2
warn_on_root = 1

[buildozer]
log_level = 2
warn_on_root = 1
