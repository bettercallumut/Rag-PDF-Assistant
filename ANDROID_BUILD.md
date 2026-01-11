# 📱 Android APK Oluşturma Rehberi (Kapsamlı)

> **R.A.G PDF Asistanı** için Android APK derleme kılavuzu  
> **Platform:** Windows (WSL2), Linux, macOS  
> **Süre:** İlk build 30-60 dakika, sonraki buildler 3-5 dakika

---

## 📋 Gereksinimler

### Sistem Gereksinimleri
- **İşletim Sistemi:** Linux / macOS / Windows (WSL2 ile)
- **Disk Alanı:** En az **10-15 GB** boş alan
- **RAM:** En az **4 GB** (8 GB önerilir)
- **İnternet:** Hızlı ve stabil bağlantı (ilk build için ~3 GB indirilecek)

### Yazılım Gereksinimleri
- ✅ Python 3.8+
- ✅ Git
- ✅ Java JDK 17
- ✅ Buildozer
- ✅ Android SDK & NDK (otomatik indirilir)

---

## 🪟 Yöntem 1: Windows (WSL2) ile APK Oluşturma

### Adım 1: WSL2 Kurulumu

#### 1.1 PowerShell'i Administrator Olarak Açın

```powershell
# WSL2'yi yükleyin (Windows 11 veya Windows 10 version 2004+)
wsl --install

# Alternatif: Ubuntu'yu manuel yükleyin
wsl --install -d Ubuntu-22.04
```

**💡 Not:** Kurulum bitince bilgisayarınızı yeniden başlatın.

#### 1.2 WSL'i İlk Kez Başlatın

```bash
# WSL Ubuntu terminalini açın
wsl

# Kullanıcı adı ve şifre belirleyin (ilk açılışta)
```

### Adım 2: WSL'de Sistem Güncellemesi

```bash
# Paket listesini güncelle
sudo apt update && sudo apt upgrade -y

# Gerekli sistem araçlarını kur
sudo apt install -y \
    git \
    zip \
    unzip \
    openjdk-17-jdk \
    python3 \
    python3-pip \
    python3-venv \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    build-essential \
    ccache \
    git \
    libssl-dev \
    libffi-dev
```

### Adım 3: Java Versiyonunu Kontrol Edin

```bash
# Java versiyonunu kontrol et
java -version

# Eğer Java 17 değilse, manuel seçin:
sudo update-alternatives --config java
# Listeden OpenJDK 17'yi seçin
```

### Adım 4: Buildozer ve Cython Kurulumu

```bash
# pip'i güncelle
pip3 install --upgrade pip

# Buildozer ve Cython'u kur (--user flag ile!)
pip3 install --user buildozer
pip3 install --user cython==0.29.36

# PATH'e ekle (Python 3.12+ için ZORUNLU)
export PATH=$PATH:~/.local/bin

# Kalıcı yap
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc

# Kurulumu doğrula
buildozer --version
```

**💡 Not:** Eğer `externally-managed-environment` hatası alırsanız, `--user` flag'ini kullanın (yukarıda zaten var).

### Adım 5: Proje Klasörüne Gidin

```bash
# Windows diskine eriş (C:\ → /mnt/c/)
cd /mnt/c/Users/umut-/github/Rag-PDF-Assistant

# Proje dosyalarını kontrol et
ls -la

# buildozer.spec dosyasının varlığını kontrol et
cat buildozer.spec
```

### Adım 6: İlk APK Derlemesi (Debug)

```bash
# Eski build dosyalarını temizle (isteğe bağlı)
buildozer android clean

# Debug APK oluştur (İLK SEFERDE 30-60 DAKİKA SÜRER!)
buildozer android debug

# Verbose modu (hata ayıklama için)
buildozer -v android debug
```

#### 📊 Build Süreci Aşamaları

Build sırasında şunlar gerçekleşir:

1. ⏳ **SDK/NDK İndirme** (ilk seferde, ~2-3 GB)
2. ⏳ **Python-for-Android (p4a) kurulumu**
3. ⏳ **Bağımlılıkların derlenmesi** (Kivy, OpenAI, Langchain, vb.)
4. ⏳ **APK paketleme**
5. ✅ **Başarılı: `bin/pdfassistant-2.0-arm64-v8a-debug.apk`**

### Adım 7: APK Dosyasını Bulun

```bash
# APK konumu
ls -lh bin/*.apk

# Örnek çıktı:
# bin/pdfassistant-2.0-arm64-v8a-debug.apk (yaklaşık 50-80 MB)
```

### Adım 8: APK'yı Windows'a Kopyalayın

```bash
# APK'yı Desktop'a kopyala
cp bin/pdfassistant-*.apk /mnt/c/Users/umut-/Desktop/

# Başarılı mesajı
echo "✅ APK Desktop'a kopyalandı!"
```

---

## 🐧 Yöntem 2: Native Linux ile APK Oluşturma

### Ubuntu/Debian Sistemlerde:

```bash
# Sistem güncelleme
sudo apt update && sudo apt upgrade -y

# Gerekli paketler
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
    libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Buildozer kurulumu
pip3 install buildozer cython==0.29.36

# Proje klasörüne git
cd ~/Rag-PDF-Assistant

# APK oluştur
buildozer android debug
```

---

## 🍎 Yöntem 3: macOS ile APK Oluşturma

```bash
# Homebrew kur (yoksa)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Gerekli araçlar
brew install python3 git openjdk@17

# Java PATH ayarı
export PATH="/usr/local/opt/openjdk@17/bin:$PATH"

# Buildozer kur
pip3 install buildozer cython==0.29.36

# Proje klasörüne git
cd ~/Rag-PDF-Assistant

# APK oluştur
buildozer android debug
```

---

## 📲 APK'yı Android Cihaza Kurma

### Yöntem A: USB ile Kurulum (ADB)

#### 1. Android Telefonunuzda Geliştirici Modunu Açın

1. **Ayarlar** → **Telefon Hakkında**
2. **Yapı Numarası**'na **7 kez** tıklayın
3. **Geliştirici Seçenekleri** açıldı!

#### 2. USB Debugging'i Etkinleştirin

1. **Ayarlar** → **Geliştirici Seçenekleri**
2. **USB Debugging**'i **Açık** yapın

#### 3. Telefonu USB ile Bağlayın

```bash
# ADB kurulu mu kontrol et
adb version

# Yoksa kur (Ubuntu/WSL):
sudo apt install adb

# Cihazları listele
adb devices

# Çıktı örneği:
# List of devices attached
# ABC123XYZ    device
```

#### 4. APK'yı Yükle

```bash
# WSL'de:
adb install bin/pdfassistant-2.0-arm64-v8a-debug.apk

# Başarılı çıktı:
# Success
```

### Yöntem B: Manuel Dosya Transferi

#### 1. APK'yı Telefonunuza Kopyalayın

- **USB Kablo** ile transfer
- **Google Drive / OneDrive** ile paylaş
- **Email** ile gönder
- **Bluetooth** ile aktar

#### 2. Telefonunuzda APK'yı Açın

1. **Dosya Yöneticisi** uygulamasını açın
2. APK dosyasını bulun (`pdfassistant-2.0-arm64-v8a-debug.apk`)
3. Dosyaya tıklayın

#### 3. Bilinmeyen Kaynaklara İzin Verin

- **"Bu kaynaktan kuruluma izin ver"** işaretleyin
- **Kur** butonuna tıklayın

#### 4. Uygulamayı Açın

- **PDF Asistanı** uygulaması menüde görünecek
- İlk açılışta izinleri kabul edin (İnternet, Depolama)

---

## 🔐 Release APK (İmzalı - Google Play İçin)

### Keystore Oluşturma

```bash
# Keystore dosyası oluştur (bir kez yapılır)
keytool -genkey -v \
    -keystore my-release-key.keystore \
    -alias pdfassistant \
    -keyalg RSA \
    -keysize 2048 \
    -validity 10000

# Şifre ve bilgilerinizi girin ve KAYDEDIN!
```

### buildozer.spec Dosyasını Düzenleyin

```bash
nano buildozer.spec
```

Son satırlara ekleyin:

```ini
# Keystore ayarları
android.keystore = my-release-key.keystore
android.keystore_alias = pdfassistant
```

### Release APK Oluştur

```bash
# Release APK derle (şifre soracak)
buildozer android release

# APK konumu:
# bin/pdfassistant-2.0-arm64-v8a-release-unsigned.apk
```

---

## ⚙️ buildozer.spec Ayarları (Kritik)

Güncel `buildozer.spec` dosyanız şu ayarlara sahip olmalı:

```ini
[app]

# Uygulama adı
title = PDF Asistanı
package.name = pdfassistant
package.domain = org.ragassistant

# Kaynak
source.dir = .
source.main = main_kivy.py

# Versiyon
version = 2.0

# ÖNEMLİ: Tüm bağımlılıklar
requirements = python3,kivy,openai,langchain,langchain-core,langchain-community,langchain-openai,langchain-text-splitters,requests,PyPDF2,python-dotenv,tiktoken,gtts

# İzinler
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# Android API
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Mimari (tüm cihazlar için)
android.archs = arm64-v8a,armeabi-v7a

# Orientation
orientation = portrait
fullscreen = 0
```

---

## 🐛 Sorun Giderme

### ❌ Hata 1: `ModuleNotFoundError: No module named 'langchain_core'`

**Çözüm:**
```bash
# buildozer.spec'i aç
nano buildozer.spec

# requirements satırına ekle:
requirements = ...,langchain,langchain-core,...

# Cache temizle
buildozer android clean
buildozer android debug
```

### ❌ Hata 2: `externally-managed-environment` (Python 3.12+)

**Hata Mesajı:**
```
error: externally-managed-environment
× This environment is externally managed
```

**Çözüm 1 (Önerilen):**
```bash
# --user flag'i ile kur
pip3 install --user buildozer cython==0.29.36

# PATH'e ekle
export PATH=$PATH:~/.local/bin
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc
```

**Çözüm 2 (Virtual Environment):**
```bash
# Python venv kur
sudo apt install python3-venv python3-full -y

# Virtual env oluştur
python3 -m venv ~/buildozer-env
source ~/buildozer-env/bin/activate

# Buildozer kur (venv içinde)
pip install buildozer cython==0.29.36
```

### ❌ Hata 3: `Command 'buildozer' not found`

**Çözüm:**
```bash
# PATH'e ekle
export PATH=$PATH:~/.local/bin

# Kalıcı yap (.bashrc'ye ekle)
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc

# Buildozer'ı yeniden kur
pip3 install --user buildozer
```

### ❌ Hata 4: `Java version mismatch`

**Çözüm:**
```bash
# Java 17'yi seç
sudo update-alternatives --config java

# JAVA_HOME ayarla
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# .bashrc'ye ekle
echo 'export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64' >> ~/.bashrc
```

### ❌ Hata 5: `NDK build failed`

**Çözüm:**
```bash
# buildozer.spec'te NDK versiyonunu belirt
android.ndk = 25b

# .buildozer klasörünü tamamen sil
rm -rf .buildozer

# Yeniden dene
buildozer android debug
```

### ❌ Hata 6: `Permission denied`

**Çözüm:**
```bash
# Gradlew için yetki ver
chmod +x .buildozer/android/platform/build-*/gradlew

# Buildozer'ı tekrar çalıştır
buildozer android debug
```

### ❌ Hata 7: APK kurulmuyor / Açılmıyor

**Çözüm:**
```bash
# Telefonunuzu USB'ye bağlayın ve logları kontrol edin
adb logcat | grep python

# Veya
adb logcat | grep "PDF Asistanı"
```

---

## 🚀 Hızlı Komut Referansı

```bash
# Yeni APK oluştur (debug)
buildozer android debug

# Eski dosyaları temizle
buildozer android clean

# APK'yı cihaza yükle
buildozer android deploy

# APK'yı yükle ve çalıştır
buildozer android deploy run

# Cihazda çalıştır ve logları göster
buildozer android deploy run logcat

# Verbose mod (detaylı log)
buildozer -v android debug

# Release APK
buildozer android release

# Tüm cache'i sil
rm -rf .buildozer
```

---

## 📊 Build Süresi ve Boyutlar

| Aşama | Süre (İlk) | Süre (Sonraki) |
|-------|-----------|----------------|
| SDK/NDK İndirme | 10-15 dk | - (cache'den) |
| Python-for-Android | 5-10 dk | 1-2 dk |
| Bağımlılık Derleme | 15-30 dk | 2-3 dk |
| APK Paketleme | 2-5 dk | 1-2 dk |
| **TOPLAM** | **30-60 dk** | **3-5 dk** |

**APK Boyutu:** ~50-80 MB (tüm bağımlılıklar dahil)

---

## ✅ Checklist (Kontrol Listesi)

Derleme öncesi kontrol edin:

- [ ] WSL2 veya Linux kurulu
- [ ] Java 17 yüklü (`java -version`)
- [ ] Buildozer kurulu (`buildozer --version`)
- [ ] `buildozer.spec` dosyası mevcut
- [ ] `requirements-android.txt` güncel
- [ ] `main_kivy.py` dosyası mevcut
- [ ] En az 10 GB boş disk alanı
- [ ] İnternet bağlantısı stabil

---

## � İlk Build Sonrası

APK başarıyla oluşturulduktan sonra:

1. ✅ APK'yı Android cihaza kurun
2. ✅ Uygulamayı açın ve test edin
3. ✅ PDF yükleyin
4. ✅ Soru-cevap özelliğini deneyin
5. ✅ Hata loglarını kontrol edin (`adb logcat`)

---

## 📚 Ek Kaynaklar

- [Buildozer Resmi Dokümantasyon](https://buildozer.readthedocs.io/)
- [Kivy Android Deployment](https://kivy.org/doc/stable/guide/packaging-android.html)
- [Python-for-Android GitHub](https://github.com/kivy/python-for-android)

---

**Hazırlayan:** Samet YILDIZ  
**Geliştirici:** Samet YILDIZ  
**Tarih:** 2026-01-03  
**Proje:** R.A.G PDF Asistanı v2.0
