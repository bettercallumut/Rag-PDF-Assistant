import PyInstaller.__main__
import os
import shutil

if os.path.exists("build"):
    shutil.rmtree("build")
if os.path.exists("dist"):
    shutil.rmtree("dist")

params = [
    'main.py',
    '--name=R_A_G_PDF_Asistani',
    '--onefile',
    '--windowed',
    '--icon=NONE',
    '--clean',
    '--exclude-module=tkinter',
    '--exclude-module=matplotlib',
    '--exclude-module=notebook',
    '--exclude-module=ipython',
    '--exclude-module=torch',
    '--exclude-module=transformers',
    '--exclude-module=sentence_transformers',
    '--add-data=version.json:.',
    '--add-data=.env:.',
    '--add-data=fix_voice.ps1:.',
    '--hidden-import=chromadb',
    '--hidden-import=chromadb.api.rust',
    '--hidden-import=chromadb.api.segment',
    '--hidden-import=chromadb.telemetry.product.posthog',
    '--hidden-import=tiktoken_ext.openai_public',
    '--hidden-import=tiktoken_ext',
    '--hidden-import=pyttsx3.drivers',
    '--hidden-import=pyttsx3.drivers.sapi5',
    '--hidden-import=win32com.gen_py',
]

print("Building...")

if not os.path.exists("version.json"):
    with open("version.json", "w") as f:
        f.write('{"version": "1.0.0"}')

PyInstaller.__main__.run(params)
