import PyInstaller.__main__
import os
import shutil

# Temizlik yap
if os.path.exists("build"):
    shutil.rmtree("build")
if os.path.exists("dist"):
    shutil.rmtree("dist")

# PyInstaller parametreleri
params = [
    'main.py',
    '--name=NeuralCore',
    '--onefile',
    '--windowed',  # Konsol penceresini gizle
    '--icon=NONE', # İkon yok (varsayılan)
    '--clean',

    # Gereksiz kütüphaneleri hariç tut (Boyut Optimizasyonu)
    # NOT: sentence-transformers ve chromadb için scipy ve numpy gereklidir.
    # Bu yüzden çok agresif exclude yapamıyoruz.
    '--exclude-module=tkinter',
    '--exclude-module=matplotlib',
    '--exclude-module=notebook',
    '--exclude-module=ipython',
    # '--exclude-module=scipy', # KALDIRILDI: sentence-transformers bağımlılığı
    # '--exclude-module=pandas', # KALDIRILDI: Olası veri işleme bağımlılığı

    # Gerekli veri dosyaları
    '--add-data=version.json:.',
    '--add-data=.env:.',

    # Hidden imports (ChromaDB ve Langchain için kritik)
    '--hidden-import=chromadb',
    '--hidden-import=chromadb.telemetry.product.posthog',
    '--hidden-import=tiktoken_ext.openai_public',
    '--hidden-import=tiktoken_ext',
    '--hidden-import=sentence_transformers',
    '--hidden-import=langchain_community.embeddings.huggingface',
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
