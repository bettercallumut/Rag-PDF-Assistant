import PyInstaller.__main__
import os
import shutil
import platform

# Temizlik yap
if os.path.exists("build"):
    shutil.rmtree("build")
if os.path.exists("dist"):
    shutil.rmtree("dist")

# Platforma göre ayırıcı (Windows için ';', Linux/Mac için ':')
# Ancak kullanıcı Windows exe derlemek istediği için Windows'ta çalıştırıyorsa ';' olmalı.
# Kullanıcının hangi işletim sisteminde derlediği önemli.
# Eğer Linux'ta derleyip Windows'a exe üretiyorsa (cross-compile) işler karışır ama
# PyInstaller cross-compile desteklemez (wine hariç).
# Bu yüzden kullanıcının Windows makinesinde çalışacağını varsayıyoruz.
sep = ';' if os.name == 'nt' else ':'

# PyInstaller parametreleri
params = [
    'main.py',
    '--name=NeuralCore',
    '--onefile',
    '--windowed',  # Konsol penceresini gizle
    '--icon=NONE', # İkon yok (varsayılan)
    '--clean',

    # Gereksiz kütüphaneleri hariç tut (Boyut Optimizasyonu)
    '--exclude-module=tkinter',
    '--exclude-module=matplotlib',
    '--exclude-module=notebook',
    '--exclude-module=ipython',

    # Gerekli veri dosyaları
    f'--add-data=version.json{sep}.',
    f'--add-data=.env{sep}.',
    f'--add-data=web_app.py{sep}.', # Streamlit uygulamasını dahil et

    # Hidden imports (ChromaDB, Langchain ve Streamlit için kritik)
    '--hidden-import=chromadb',
    '--hidden-import=chromadb.telemetry.product.posthog',
    '--hidden-import=tiktoken_ext.openai_public',
    '--hidden-import=tiktoken_ext',
    '--hidden-import=sentence_transformers',
    '--hidden-import=langchain_community.embeddings.huggingface',
    '--hidden-import=streamlit',
    '--hidden-import=altair',
]

print("Derleme işlemi başlatılıyor... Bu işlem biraz sürebilir.")

# version.json kontrolü
if not os.path.exists("version.json"):
    print("UYARI: version.json bulunamadı! Varsayılan bir tane oluşturuluyor.")
    with open("version.json", "w") as f:
        f.write('{"version": "1.0.0", "commit": "initial"}')

PyInstaller.__main__.run(params)

print("\n------------------------------------------------")
print("Derleme Tamamlandı!")
print("EXE dosyası 'dist/NeuralCore.exe' konumunda.")
print("------------------------------------------------")
