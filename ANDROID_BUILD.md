# Android APK Derleme Rehberi

## 📋 Gereksinimler

- **Linux** veya **WSL** (Windows Subsystem for Linux)
- En az **10 GB** disk alanı
- İnternet bağlantısı

---

## 1️⃣ WSL Kurulumu (Windows İçin)

### Windows Terminal (Administrator) açın:

```powershell
wsl --install
```

**Bilgisayarı yeniden başlatın.**

### WSL'i başlatın:

```bash
wsl
```

---

## 2️⃣ Gerekli Paketleri Kurun

### Sistem güncellemesi:

```bash
sudo apt update && sudo apt upgrade -y
```

### Android build araçları:

```bash
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev python3-venv
```

### Buildozer ve Cython:

```bash
pip3 install --upgrade pip
pip3 install buildozer cython
```

---

## 3️⃣ Projeyi WSL'e Kopyalayın

```bash
# Windows klasörüne erişim
cd /mnt/c/Users/umut-/github/Rag-PDF-Assistant

# VEYA projeyi klonlayın
git clone https://github.com/yourusername/Rag-PDF-Assistant.git
cd Rag-PDF-Assistant
```

---

## 4️⃣ Buildozer Konfigürasyonunu Kontrol Edin

`buildozer.spec` dosyasının olduğundan emin olun. Düzenlemek için:

```bash
nano buildozer.spec
```

**Önemli ayarlar**:
- `title = PDF Asistanı`
- `package.name = pdfassistant`
- `requirements = python3,kivy,openai,langchain,...` (requirements.txt'teki paketler)

---

## 5️⃣ APK Oluşturun

### İlk derleme (20-30 dakika sürer):

```bash
buildozer android debug
```

**Not**: İlk seferde Android SDK, NDK vb. indirilecek. İnternet bağlantınız iyi olmalı.

### Hata alırsanız cache temizleyin:

```bash
buildozer android clean
buildozer android debug
```

---

## 6️⃣ APK Konumu

APK dosyası şurada oluşur:

```
bin/pdfassistant-2.0-arm64-v8a-debug.apk
```

---

## 7️⃣ Android Telefonunuza Kurun

### Yöntem 1: USB ile (ADB)

1. Telefonunuzda **USB Debugging** açın:
   - Ayarlar → Telefon Hakkında → Yapı Numarası'na 7 kez tıklayın
   - Geliştirici Seçenekleri → USB Debugging açın

2. USB kabloyla bağlayın:

```bash
adb devices  # Telefonun tanındığını kontrol edin
adb install bin/pdfassistant-2.0-arm64-v8a-debug.apk
```

### Yöntem 2: Dosya Transferi

1. APK'yı Windows'a kopyalayın:

```bash
cp bin/pdfassistant-2.0-arm64-v8a-debug.apk /mnt/c/Users/umut-/Desktop/
```

2. Desktop'tan telefonunuza kopyalayın (USB, Google Drive, vb.)

3. Telefonunuzda:
   - **Dosya Yöneticisi** açın
   - APK'yı bulun ve tıklayın
   - **Bilinmeyen Kaynaklardan Kuruluma İzin Ver**
   - **Kur** deyin

---

## 8️⃣ Release APK (İmzalı)

Production için imzalı APK:

```bash
buildozer android release
```

**Keystore oluşturma**:

```bash
keytool -genkey -v -keystore my-release-key.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000
```

---

## ⚠️ Sık Karşılaşılan Hatalar

### "Command failed: ..."
```bash
buildozer android clean
rm -rf .buildozer
buildozer android debug
```

### "Java hatası"
```bash
sudo update-alternatives --config java
# OpenJDK 17 seçin
```

### "NDK build failed"
```bash
# buildozer.spec'te:
android.ndk = 25b
```

---

## ✅ Test

APK kurduktan sonra:

1. **PDF Asistanı** uygulamasını açın
2. API Key girin (.env dosyasından veya manuel)
3. PDF yükleyin
4. Soru sorun

---

## 📝 Notlar

- İlk build çok uzun sürer (NDK, SDK indirir)
- Her build 5-10 dakika sürer
- APK boyutu ~50-80 MB olacak
- Android 5.0+ (API 21+) desteklenir

---

## 🆘 Yardım

Hata alırsanız:

```bash
buildozer -v android debug  # Verbose log
```

Logları inceleyin ve gerekirse paylaşın.
