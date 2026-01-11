# Kivy Versiyonu Kurulum Kılavuzu

## 📱 Kivy (Mobil/Desktop) Sürümü

### 🖥️ Desktop'ta Çalıştırma

#### 1. Gerekli Kütüphaneleri Yükleyin

```bash
pip install -r requirements-kivy.txt
```

#### 2. Uygulamayı Başlatın

```bash
python main_kivy.py
```

---

### 📱 Android APK Oluşturma

#### Gereksinimler
- Linux veya macOS (WSL2 ile Windows)
- Python 3.8+
- Buildozer
- Android SDK & NDK (otomatik yüklenir)

#### 1. Buildozer Kurulumu

```bash
pip install buildozer
pip install cython==0.29.33
```

#### 2. Android Bağımlılıklarını Yükleyin

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-11-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

**macOS:**
```bash
brew install autoconf automake libtool pkg-config
brew install openssl
```

#### 3. APK Oluşturma

**Debug APK (Test için):**
```bash
buildozer android debug
```

**Release APK (Yayın için):**
```bash
buildozer android release
```

#### 4. APK'yı Cihaza Yükleme

```bash
buildozer android deploy run
```

---

### 📋 Önemli Notlar

#### Buildozer İlk Çalıştırma
İlk derleme **çok uzun sürebilir** (30-60 dakika):
- Android SDK indirilir
- Android NDK indirilir
- Python-for-Android derlenir
- Tüm bağımlılıklar build edilir

Sonraki derlemeler çok daha hızlıdır (2-5 dakika).

#### WSL2 Kullanıcıları (Windows)
```bash
# WSL2 kurulumu
wsl --install

# Ubuntu başlatın ve içinde:
cd /mnt/c/Users/umut-/github/Rag-PDF-Assistant
pip install buildozer
buildozer android debug
```

#### Buildozer Yapılandırması

`buildozer.spec` dosyasını düzenleyerek:
- **Uygulama adı:** `title = PDF Asistanı`
- **Paket adı:** `package.name = pdfassistant`
- **Sürüm:** `version = 2.0`
- **İzinler:** `android.permissions = INTERNET,READ_EXTERNAL_STORAGE`
- **API Seviyesi:** `android.api = 31`

#### Sorun Giderme

**Hata: Command failed: git...**
```bash
buildozer android clean
buildozer android debug
```

**Hata: SDK License hatası**
```bash
buildozer.spec dosyasında:
android.accept_sdk_license = True
```

**Hata: NDK bulunamadı**
```bash
buildozer android clean
rm -rf ~/.buildozer
buildozer android debug
```

---

### 🎯 Hızlı Test

**Local test (Desktop):**
```bash
python main_kivy.py
```

**Android Emulator test:**
```bash
buildozer android debug deploy run logcat
```

---

### 📦 Çıktı Dosyaları

Derleme sonrası APK dosyaları:
```
bin/pdfassistant-2.0-debug.apk         # Debug sürüm
bin/pdfassistant-2.0-release.apk      # Release sürüm (imzalı)
```

---

### 🔐 Release APK İmzalama

#### 1. Keystore Oluşturma
```bash
keytool -genkey -v -keystore my-release-key.keystore -alias pdfassistant -keyalg RSA -keysize 2048 -validity 10000
```

#### 2. Buildozer ile İmzalama
`buildozer.spec` dosyasına ekleyin:
```ini
[app]
android.release_artifact = apk

# Keystore ayarları
p4a.release_artifact = apk
android.keystore = my-release-key.keystore
android.keyalias = pdfassistant
android.keystore_passwd = yourpassword
android.keyalias_passwd = yourpassword
```

#### 3. Release Build
```bash
buildozer android release
```

---

### 📊 requirements-kivy.txt İçeriği

```
Kivy>=2.2.0                    # UI Framework
openai>=1.0.0                  # OpenAI API
langchain>=0.1.0               # RAG Framework
langchain-community>=0.0.10    # Community tools
langchain-openai>=0.0.2        # OpenAI integration
langchain-text-splitters       # Text chunking
PyPDF2>=3.0.0                  # PDF parsing
requests>=2.31.0               # HTTP requests
python-dotenv>=1.0.0           # .env support
tiktoken>=0.5.0                # Token counting
pyjnius>=1.4.2                 # Android Java bridge
plyer>=2.1.0                   # Platform abstraction
gtts>=2.3.0                    # Google TTS
```

---

### 📊 requirements-android.txt İçeriği

```
python3
kivy==2.2.0
openai
langchain
langchain-community
langchain-openai
langchain-text-splitters
PyPDF2
requests
python-dotenv
tiktoken
pyjnius
plyer
gtts
android
```

Bu dosya Buildozer için optimize edilmiştir (version pinning yok).

---

## 🎓 Faydalı Komutlar

```bash
# Buildozer cache temizleme
buildozer android clean

# Tüm build dosyalarını silme
rm -rf .buildozer

# Logları izleme (cihaz bağlıyken)
buildozer android adb -- logcat

# Sadece logcat
adb logcat | grep python

# APK boyutunu görme
du -sh bin/*.apk

# Buildozer sürüm kontrolü
buildozer --version
```

---

## 🚀 Yayına Hazırlık

1. ✅ `buildozer.spec` kontrol edin
2. ✅ İkonlar ekleyin (`icon.png`, `presplash.png`)
3. ✅ Sürüm numarasını artırın
4. ✅ Release keystore oluşturun
5. ✅ `buildozer android release`
6. ✅ APK'yı test edin
7. ✅ Google Play'e yükleyin

---

**Hazırlayan:** Samet YILDIZ  
**Proje:** R.A.G PDF Asistanı  
**Tarih:** 2026-01-02
