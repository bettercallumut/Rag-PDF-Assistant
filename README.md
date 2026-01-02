<div align="center">

# 🤖 R.A.G PDF Asistanı

### *Retrieval-Augmented Generation ile Akıllı PDF Analizi*

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![OpenAI](https://img.shields.io/badge/AI-GPT--4-orange.svg)](https://openai.com/)

---

### [🇹🇷 **Türkçe**](#turkish) | [🇬🇧 **English**](#english)

---

</div>

<a id="turkish"></a>

## 🇹🇷 Türkçe

### 📖 Genel Bakış

**R.A.G PDF Asistanı**, **Retrieval-Augmented Generation (RAG)** teknolojisi ile PDF'lerle etkileşim biçiminizi dönüştüren yenilikçi bir uygulamadır. OpenAI'nin GPT-4'ü ile çalışan bu araç, teknik belgeleri olağanüstü hassasiyetle analiz eder ve zarif bir PyQt6 arayüzü üzerinden akıllı, bağlam-duyarlı yanıtlar sunar.

### ✨ Temel Özellikler

#### 🧠 **Gelişmiş Yapay Zeka**
- **📄 Akıllı PDF Analizi** - Derin semantik anlama ve akıllı parçalama
- **🔍 RAG Mimarisi** - Halüsinasyon olmadan doğru yanıtlar için bağlam çıkarımı
- **💬 Akışkan Yanıtlar** - Gerçek zamanlı kelime-kelime cevap üretimi
- **📝 Otomatik Özetleme** - Uzun yanıtları kısa sesli özetlere dönüştürme

#### 🎙️ **Ses Özellikleri**
- **🔊 Metinden-Sese** - Yerel ve yüksek kaliteli ses sentezi (pyttsx3)
- **🇹🇷 Türkçe Dil Desteği** - Türkçe ses paketlerini otomatik algılama ve yükleme
- **⏯️ Çalma Kontrolleri** - Sesli yanıtları duraklat, devam ettir ve durdur
- **🎨 Ses Görselleştirme** - Konuşma sırasında Siri tarzı dalga formu animasyonları

#### 🎨 **Modern Arayüz**
- **🌙 Koyu Tema** - Göz dostu karanlık mod ve canlı vurgu renkleri
- **⚡ Akıcı Animasyonlar** - 3D düşünme küresi ve gerçek zamanlı ses görselleştirme
- **📊 İlerleme Takibi** - PDF işleme ve ses üretimi için görsel geri bildirim
- **🖱️ Sezgisel Kontroller** - Hover efektleriyle temiz, profesyonel arayüz

#### 🛠️ **Teknik Mükemmellik**
- **🚀 Asenkron İşlem** - Engellenmeyen PDF yükleme ve API çağrıları
- **🔐 Güvenli API Saklama** - Şifreli OpenAI API anahtarı yönetimi
- **⚙️ Platform Uyumlu** - Windows, Linux ve Android desteği
- **📦 Bağımsız Çalıştırılabilir** - PyInstaller derleme desteği

---

### 📦 Kurulum

#### Gereksinimler
- **Python 3.8+**
- **OpenAI API Anahtarı** ([Buradan alın](https://platform.openai.com/api-keys))

#### Hızlı Başlangıç

```bash
git clone https://github.com/yourusername/Rag-PDF-Assistant.git
cd Rag-PDF-Assistant

pip install -r requirements.txt

python main.py
```

<details>
<summary><b>📋 Linux/Mac Bağımlılıkları</b></summary>

```bash
sudo apt-get install python3-pyqt6 espeak ffmpeg

brew install espeak ffmpeg
```
</details>

---

### 🚀 Kullanım Kılavuzu

#### 1️⃣ **İlk Kurulum**
- Uygulamayı başlatın
- İstendiğinde OpenAI API Anahtarınızı girin
- Anahtar güvenle `.env` dosyasına kaydedilir

#### 2️⃣ **PDF Yükleme**
- **"+ PDF Yükle"** butonuna tıklayın
- PDF belgenizi seçin
- İşleme tamamlanmasını bekleyin (ilerleme çubuğu durumu gösterir)

#### 3️⃣ **Soru Sorma**
- Sorunuzu giriş alanına yazın
- **Enter**'a basın veya **"GÖNDER"**e tıklayın
- İşlem sırasında 3D düşünme animasyonunu izleyin

#### 4️⃣ **Ses Seçenekleri**
- ✅ **Sesli Yanıt** - Sesli yanıtları etkinleştir/devre dışı bırak
- ✅ **Özetle** - Uzun cevapları kısa özetlere dönüştür

#### 5️⃣ **Kontroller**
- **DURDUR** - Sesli oynatmayı anında durdur
- **GÖNDER** - Yeni bir sorgu gönder

---

### 🏗️ Mimari

```mermaid
graph LR
    A[PDF Belgesi] --> B[PyPDF2 Çıkarma]
    B --> C[Metin Parçalama]
    C --> D[Token Optimizasyonu]
    D --> E[Bağlam Seçimi]
    E --> F[OpenAI GPT-4]
    F --> G[Akışkan Yanıt]
    G --> H[TTS Üretimi]
    H --> I[Ses Çalma]
    I --> J[Görselleştirme]
```

#### Ana Bileşenler
- **`main.py`** - Ana uygulama penceresi ve olay yönetimi
- **`rag_system.py`** - RAG hattı ve bağlam yönetimi
- **`workers.py`** - Asenkron işlemler için arka plan thread'leri
- **`visualizer.py`** - 3D düşünme küresi animasyonu
- **`audio_visualizer.py`** - Siri tarzı ses dalga formu
- **`config.py`** - Yapılandırma ve tema ayarları

---

### ⚙️ Yapılandırma

`config.py` dosyasını düzenleyerek özelleştirin:

```python
TTS_ENABLED = True
TTS_LOCAL_RATE = 150
MAX_CONTEXT_TOKENS = 25000

COLOR_ACCENT = "#6366F1"
COLOR_BG = "#18181B"
```

---

### 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen şu adımları izleyin:

1. Depoyu fork'layın
2. Özellik dalı oluşturun (`git checkout -b feature/HarikaBirOzellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'HarikaBirOzellik eklendi'`)
4. Dalı push edin (`git push origin feature/HarikaBirOzellik`)
5. Pull Request açın

---

### 📄 Lisans

Bu proje **MIT Lisansı** altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

### 👨‍💻 Yapımcı & Katkıda Bulunanlar

**Proje Yapımcısı:** Samet YILDIZ  
**Üniversite Proje Ödevi**

**Katkıda Bulunanlar:**
- Samet YILDIZ - Ana Geliştirici & Yapay Zeka Entegrasyonu
- BetterCallUmut - Arayüz Tasarımı & Ses Özellikleri

---

### 🙏 Teşekkürler

- **OpenAI** - GPT-4 API için
- **PyQt6** - Modern GUI framework için
- **LangChain** - RAG altyapısı için
- **pyttsx3** - Çevrimdışı TTS yetenekleri için

---

### 📊 Teknoloji Yığını

| Kategori | Teknoloji |
|----------|-----------|
| **Frontend** | PyQt6, QPainter (Özel Widget'lar) |
| **AI/ML** | OpenAI GPT-4, LangChain |
| **Ses** | pyttsx3, PyAudio, NumPy (FFT) |
| **PDF** | PyPDF2, pdfplumber |
| **Derleme** | PyInstaller, Buildozer (Android) |

---

<div align="center">

### ⭐ Projeyi faydalı bulduysanız yıldız verin!

**Yapımcı: Samet YILDIZ**  
*Üniversite Proje Ödevi - 2026*

**Katkıda Bulunanlar:** Samet YILDIZ, BetterCallUmut

</div>

---

<div align="center">

### 📬 İletişim & Destek

**Creator:** Samet YILDIZ  
**Contributors:** Samet YILDIZ, BetterCallUmut

</div>

---

<br>

<a id="english"></a>

## 🇬🇧 English

### 📖 Overview

**R.A.G PDF Assistant** is a cutting-edge application that transforms how you interact with PDFs using **Retrieval-Augmented Generation (RAG)**. Powered by OpenAI's GPT-4, this tool analyzes technical documents with precision and delivers intelligent, context-aware responses through an elegant PyQt6 interface.

### ✨ Key Features

#### 🧠 **Advanced AI Capabilities**
- **📄 Smart PDF Analysis** - Deep semantic understanding with intelligent chunking
- **🔍 RAG Architecture** - Retrieves relevant context for accurate, hallucination-free responses
- **💬 Streaming Responses** - Real-time token-by-token answer generation
- **📝 Auto-Summarization** - Condense long responses into concise voice summaries

#### 🎙️ **Voice Features**
- **🔊 Text-to-Speech** - Local & high-quality voice synthesis (pyttsx3)
- **🇹🇷 Turkish Language Support** - Auto-detects and installs Turkish voice packs
- **⏯️ Playback Controls** - Pause, resume, and stop voice responses
- **🎨 Audio Visualization** - Siri-style waveform animations during speech

#### 🎨 **Modern UI/UX**
- **🌙 Dark Theme** - Eye-friendly dark mode with vibrant accent colors
- **⚡ Smooth Animations** - 3D thinking sphere & real-time audio visualization
- **📊 Progress Tracking** - Visual feedback for PDF processing and voice generation
- **🖱️ Intuitive Controls** - Clean, professional interface with hover effects

#### 🛠️ **Technical Excellence**
- **🚀 Asynchronous Processing** - Non-blocking PDF loading and API calls
- **🔐 Secure API Storage** - Encrypted OpenAI API key management
- **⚙️ Platform Adaptive** - Windows, Linux, and Android support
- **📦 Standalone Executable** - PyInstaller build support

---

### 📦 Installation

#### Prerequisites
- **Python 3.8+**
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))

#### Quick Start

```bash
git clone https://github.com/yourusername/Rag-PDF-Assistant.git
cd Rag-PDF-Assistant

pip install -r requirements.txt

python main.py
```

<details>
<summary><b>📋 Linux/Mac Dependencies</b></summary>

```bash
sudo apt-get install python3-pyqt6 espeak ffmpeg

brew install espeak ffmpeg
```
</details>

---

### 🚀 Usage Guide

#### 1️⃣ **Initial Setup**
- Launch the application
- Enter your OpenAI API Key when prompted
- The key is securely saved to `.env` file

#### 2️⃣ **Load a PDF**
- Click **"+ PDF Yükle"** button
- Select your PDF document
- Wait for processing (progress bar shows status)

#### 3️⃣ **Ask Questions**
- Type your question in the input field
- Press **Enter** or click **"GÖNDER"**
- Watch the 3D thinking animation during processing

#### 4️⃣ **Voice Options**
- ✅ **Sesli Yanıt** - Enable/disable voice responses
- ✅ **Özetle** - Condense long answers into brief summaries

#### 5️⃣ **Controls**
- **DURDUR** - Stop voice playback immediately
- **GÖNDER** - Submit a new query

---

### 🏗️ Architecture

```mermaid
graph LR
    A[PDF Document] --> B[PyPDF2 Extraction]
    B --> C[Text Chunking]
    C --> D[Token Optimization]
    D --> E[Context Selection]
    E --> F[OpenAI GPT-4]
    F --> G[Streaming Response]
    G --> H[TTS Generation]
    H --> I[Audio Playback]
    I --> J[Visualization]
```

#### Core Components
- **`main.py`** - Main application window and event handling
- **`rag_system.py`** - RAG pipeline and context management
- **`workers.py`** - Background threads for async operations
- **`visualizer.py`** - 3D thinking sphere animation
- **`audio_visualizer.py`** - Siri-style audio waveform
- **`config.py`** - Configuration and theme settings

---

### ⚙️ Configuration

Edit `config.py` to customize:

```python
TTS_ENABLED = True
TTS_LOCAL_RATE = 150
MAX_CONTEXT_TOKENS = 25000

COLOR_ACCENT = "#6366F1"
COLOR_BG = "#18181B"
```

---

### 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

### 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) file for details.

---

### 👨‍💻 Author & Contributors

**Project Creator:** Samet YILDIZ  
**University Project Assignment**

**Contributors:**
- Samet YILDIZ - Lead Developer & AI Integration
- BetterCallUmut - UI/UX Design & Audio Features

---

### 🙏 Acknowledgments

- **OpenAI** for GPT-4 API
- **PyQt6** for the modern GUI framework
- **LangChain** for RAG infrastructure
- **pyttsx3** for offline TTS capabilities

---

### 📊 Tech Stack

| Category | Technology |
|----------|-----------|
| **Frontend** | PyQt6, QPainter (Custom Widgets) |
| **AI/ML** | OpenAI GPT-4, LangChain |
| **Audio** | pyttsx3, PyAudio, NumPy (FFT) |
| **PDF** | PyPDF2, pdfplumber |
| **Build** | PyInstaller, Buildozer (Android) |

---

<div align="center">

### ⭐ Star this project if you find it useful!

**Created by Samet YILDIZ**  
*University Project - 2026*

</div>
