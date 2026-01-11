# 📱 Pydroid3 Kurulum Rehberi

## ⚡ Hızlı Kurulum (Android)

### Adım 1: Projeyi İndirin

Projeyi GitHub'dan indirin veya ZIP olarak telefonunuza aktarın:
- `/storage/emulated/0/Download/Rag-PDF-Assistant/`

### Adım 2: Pydroid3'ü Açın

**Pydroid3** uygulamasını Play Store'dan indirin ve açın.

---

## 🚀 YÖNTEM 1: Otomatik Kurulum (ÖNERİLEN)

### Tek Komutla Kurulum

```bash
# Proje klasörüne git
cd /storage/emulated/0/Download/Rag-PDF-Assistant/

# Otomatik kurulum scriptini çalıştır
python setup_android.py

# Uygulama başlayacak ve eksik paketleri otomatik kuracak!
python main_kivy_android.py
```

**Ne Olur?**
1. ✅ Eksik paketler otomatik tespit edilir
2. ✅ `openai==0.28.1`, `PyPDF2`, `python-dotenv` otomatik kurulur
3. ✅ Uygulama hemen başlar!

---

## 📦 YÖNTEM 2: Manuel Kurulum

Pydroid3 terminalinde şu komutları çalıştırın:

```bash
# Proje klasörüne gidin
cd /storage/emulated/0/Download/Rag-PDF-Assistant/

# VEYA projenin bulunduğu yere göre:
cd /storage/emulated/0/Download/

# Temel bağımlılıkları kur (Rust GEREKMEYENLERİ)
pip install langchain-core
pip install langchain-text-splitters
pip install langchain-community

# OpenAI (eski versiyon - Rust gerektirmeyen)
pip install "openai<1.0"

# LangChain OpenAI adapter
pip install langchain-openai
```

---

## ⚠️ Python 3.13 Uyumluluk Notu

**`tiktoken` ve yeni `openai` paketleri Rust derleyicisi gerektirir**, Android'de yok.

**Çözüm:**
- ✅ `openai<1.0` kullanıyoruz (eski, stabil versiyon)
- ✅ `tiktoken` yerine kendi token hesaplamamızı kullanıyoruz

---

## 🔑 API Key Ayarlayın

### Yöntem 1: .env Dosyası (Önerilen)

```bash
# Proje klasöründe .env dosyası oluşturun
cd /storage/emulated/0/Download/Rag-PDF-Assistant/
nano .env
```

İçine ekleyin:

```
OPENAI_API_KEY=sk-your-api-key-here
```

Kaydet: `Ctrl+O`, `Enter`, `Ctrl+X`

### Yöntem 2: config.py'yi Düzenleyin

```python
# config.py dosyasını açın
nano config.py
```

API keyinizi direkt yazın:

```python
API_KEY = "sk-your-api-key-here"
```

---

## ▶️ Uygulamayı Çalıştırın

```bash
# Proje klasöründe
python main_kivy.py
```

---

## ✅ Başarılı Çalışma Kontrolü

Uygulama açıldığında:

1. ✅ **PDF Asistanı** başlığı görünür
2. ✅ **📁 PDF Yükle** butonu aktif
3. ✅ PDF seçip yükleyebilirsiniz
4. ✅ Soru sorabilirsiniz

---

## 🐛 Sorun Giderme

### Hata: `ModuleNotFoundError: No module named 'langchain_core'`

**Çözüm:**
```bash
pip install langchain-core
```

### Hata: `No module named 'openai'`

**Çözüm:**
```bash
pip install "openai<1.0"
```

### Hata: `API key not found`

**Çözüm:**
- `.env` dosyasını kontrol edin
- VEYA `config.py`'de API_KEY'i ayarlayın

### Hata: `jiter` veya `tiktoken` build error

**Normal!** Bu paketler Rust gerektiriyor, gereksiz.

**Çözüm:**
- `openai<1.0` kullanın (yukarıda zaten var)
- requirements'dan `tiktoken`'ı kaldırdık ✓

---

## 📋 Tam Kurulum Komutları (Toplu)

```bash
cd /storage/emulated/0/Download/Rag-PDF-Assistant/
pip install "openai<1.0" langchain-core langchain-openai langchain-community langchain-text-splitters
python main_kivy.py
```

---

## 🎯 İzinler

İlk çalıştırmada Android şu izinleri isteyecek:

- ✅ **Depolama** - PDF dosyalarını okumak için
- ✅ **İnternet** - OpenAI API'ye bağlanmak için

**Kabul edin!**

---

## 📚 Ek Bilgi

- **Minimum Android:** 5.0 (API 21)
- **Önerilen:** Android 8.0+
- **Python:** 3.8+ (Pydroid3 3.13 kullanıyor)
- **İnternet:** API çağrıları için gerekli

---

**Geliştirici:** Samet YILDIZ  
**Tarih:** 2026-01-03  
**Proje:** R.A.G PDF Asistanı v2.0
