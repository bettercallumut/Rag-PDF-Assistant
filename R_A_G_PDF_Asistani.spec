# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('version.json', '.'), ('.env', '.'), ('fix_voice.ps1', '.')],
    hiddenimports=['chromadb', 'chromadb.api.rust', 'chromadb.api.segment', 'chromadb.telemetry.product.posthog', 'tiktoken_ext.openai_public', 'tiktoken_ext', 'pyttsx3.drivers', 'pyttsx3.drivers.sapi5', 'win32com.gen_py'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'notebook', 'ipython', 'torch', 'transformers', 'sentence_transformers'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='R_A_G_PDF_Asistani',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='NONE',
)
