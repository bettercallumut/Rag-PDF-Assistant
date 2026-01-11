# 📱 Android Kivy - Hızlı Başlangıç

## 🚀 En Basit Yöntem (3 Adım)

### 1️⃣ Proje dosyalarını Android'e kopyalayın

Şu dosyaları `/storage/emulated/0/Download/` klasörüne atın:
- `main_kivy_android.py`
- `rag_system_android.py`
- `setup_android.py`
- `config.py` (veya `.env`)

### 2️⃣ Pydroid3'te çalıştırın

```bash
cd /storage/emulated/0/Download/

# Otomatik kurulum + çalıştırma
python main_kivy_android.py
```

**İşte bu kadar!** Uygulama başlayacak ve eksik paketleri otomatik kuracak.

---

## 📋 İlk Çalıştırmada Ne Olur?

```
==================================================
PDF ASISTANI - ANDROID
==================================================

[>>] Bagimliliklari kontrol ediliyor...

[OK] openai yuklendi
[OK] PyPDF2 yuklendi
[OK] dotenv yuklendi
[OK] Tum paketler mevcut

[>>] Uygulama baslatiliyor...

[OK] Android RAG sistemi yuklendi
```

Eğer paket eksikse:

```
[!] openai eksik, kurulacak...

[>>] 1 paket kuruluyor...
[OK] openai==0.28.1 kuruldu
[OK] Tum paketler kuruldu!
```

---

## ⚙️ API Key Ayarlama

### Yöntem 1: config.py

```python
# config.py
API_KEY = "sk-your-api-key-here"
```

### Yöntem 2: .env dosyası

```bash
# .env
OPENAI_API_KEY=sk-your-api-key-here
```

---

## ✅ Özellikler

- ✅ **Otomatik Paket Kurulumu** - İlk çalıştırmada eksik paketleri kurar
- ✅ **Emoji Yok** - Android font uyumluluğu için düz metin
- ✅ **Minimal Bağımlılık** - Sadece `openai==0.28.1`, `PyPDF2`, `python-dotenv`
- ✅ **Rust Yok** - LangChain kullanmıyor, direkt OpenAI API
- ✅ **Hızlı** - Kivy ile doğal Android arayüzü

---

## 🐛 Sorun Giderme

### "ModuleNotFoundError: No module named 'openai'"

**Otomatik çözülür!** Uygulama ilk çalıştırmada kuracak.

Manuel kurulum isterseniz:
```bash
pip install openai==0.28.1
```

### "API key not found"

`config.py` veya `.env` dosyasında API keyinizi ayarlayın.

### "Rust not found" hatası

**Doğru dosyayı kullanın:**
- ✅ `main_kivy_android.py` (Android için)
- ❌ `main_kivy.py` (LangChain gerektirir)

---

## 📦 Dosyalar

| Dosya | Açıklama |
|-------|----------|
| `main_kivy_android.py` | Android Kivy uygulaması (otomatik kurulum dahil) |
| `rag_system_android.py` | OpenAI API kullanan RAG sistemi (LangChain yok) |
| `setup_android.py` | Manuel kurulum scripti |
| `config.py` | API key konfigürasyonu |

---

## 🎯 Kullanım

1. Uygulamayı başlat
2. **PDF YUKLE** butonuna bas
3. PDF dosyası seç
4. Soru sor!

---

**Geliştirici:** Samet YILDIZ  
**Tarih:** 2026-01-03
