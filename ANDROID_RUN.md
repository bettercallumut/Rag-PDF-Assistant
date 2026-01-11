# Android Cihazda Çalıştırma Kılavuzu

## ⚡ Hızlı Başlangıç

### 📱 Android'de Kullanım

Android cihazlarda uygulama **`main_kivy.py`** dosyasını kullanır, `main.py` değil!

---

## 🔨 APK Oluşturma (3 Adım)

### 1️⃣ Linux/macOS/WSL2'de Buildozer Kurun

```bash
pip install buildozer cython==0.29.33
```

### 2️⃣ APK'yı Derleyin

```bash
cd /path/to/Rag-PDF-Assistant

buildozer android debug
```

**İlk derleme 30-60 dakika sürebilir!** ☕

### 3️⃣ APK'yı Cihaza Yükleyin

APK dosyası `bin/` klasöründe:
```
bin/pdfassistant-2.0-debug.apk
```

**Yükleme seçenekleri:**

**A) USB ile:**
```bash
buildozer android deploy
```

**B) Elle transfer:**
- APK'yı telefona kopyalayın
- Dosya yöneticisinden açın
- "Bilinmeyen kaynaklar"a izin verin
- Yükle'ye tıklayın

---

## 📋 buildozer.spec Yapılandırması

Uygulama otomatik olarak `main_kivy.py` kullanacak:

```ini
[app]
title = PDF Asistanı
package.name = pdfassistant
source.main = main_kivy.py          # ← Ana dosya
requirements = python3,kivy,openai,langchain,...

android.permissions = INTERNET,READ_EXTERNAL_STORAGE
android.api = 31
```

---

## 🎯 Neden main_kivy.py?

| Dosya | Platform | Arayüz |
|-------|----------|---------|
| `main.py` | Windows/Linux/macOS | PyQt6 (Desktop GUI) |
| `main_kivy.py` | Android/iOS/Desktop | Kivy (Mobil uyumlu) |

**Android'de:**
- ✅ `main_kivy.py` → Kivy framework (dokunmatik ekran uyumlu)
- ❌ `main.py` → PyQt6 (Android'de çalışmaz)

---

## 🚀 Test Etme

### Desktop'ta Test (Derleme öncesi)

```bash
pip install -r requirements-kivy.txt
python main_kivy.py
```

Eğer desktop'ta çalışıyorsa, APK'da da çalışır!

### Android Emulator'da Test

```bash
buildozer android debug deploy run logcat
```

---

## ⚠️ Önemli Notlar

### Windows Kullanıcıları

Android APK oluşturmak için **Linux gerekir**. Seçenekler:

**1) WSL2 (Önerilen):**
```bash
# PowerShell'de:
wsl --install

# WSL Ubuntu'da:
cd /mnt/c/Users/umut-/github/Rag-PDF-Assistant
pip install buildozer
buildozer android debug
```

**2) Virtual Machine:**
- VirtualBox + Ubuntu
- VMware + Ubuntu

**3) Cloud Build:**
- GitHub Actions
- GitLab CI

### İlk Derleme

İlk `buildozer android debug`:
- ⏱️ **30-60 dakika** sürer
- 💾 **~3 GB** indirir (SDK, NDK, dependencies)
- ✅ Sonraki derlemeler **2-5 dakika**

### Gerekli İzinler

Uygulama şu izinlere ihtiyaç duyar:
- 🌐 **INTERNET** - OpenAI API
- 📁 **READ_EXTERNAL_STORAGE** - PDF okuma
- 💾 **WRITE_EXTERNAL_STORAGE** - Geçici dosyalar

---

## 🔧 Sorun Giderme

### Hata: "No such file: main.py"

**Çözüm:** `buildozer.spec` kontrol edin:
```ini
source.main = main_kivy.py  # Bu satır olmalı!
```

### Hata: "Permission denied"

```bash
chmod +x buildozer
buildozer android clean
buildozer android debug
```

### Hata: SDK License

`buildozer.spec` dosyasına ekleyin:
```ini
android.accept_sdk_license = True
```

### APK açılmıyor

```bash
# Logları kontrol edin
adb logcat | grep python
```

---

## 📦 Build Çıktısı

Başarılı derleme sonrası:

```
✅ bin/pdfassistant-2.0-debug.apk     (İmzasız, test için)
✅ bin/pdfassistant-2.0-release.apk  (İmzalı, yayın için)
```

**APK Boyutu:** ~50-80 MB (dependencies dahil)

---

## 🎓 Özet Komutlar

```bash
# İlk kurulum
pip install buildozer

# Debug APK (test)
buildozer android debug

# APK'yı cihaza yükle
buildozer android deploy

# Çalıştır ve log izle
buildozer android deploy run logcat

# Cache temizle
buildozer android clean

# Release APK (yayın)
buildozer android release
```

---

## ✅ Doğru Akış

```
1. main_kivy.py yaz ✅ (zaten mevcut)
2. buildozer.spec ayarla ✅ (source.main = main_kivy.py)
3. buildozer android debug ✅
4. APK'yı telefona at ✅
5. Yükle ve çalıştır ✅
```

---

**Hazırlayan:** Samet YILDIZ  
**Tarih:** 2026-01-02  
**Proje:** R.A.G PDF Asistanı
