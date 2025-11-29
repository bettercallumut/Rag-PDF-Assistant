# 🤖 RAG-PDF Assistant - AI-Powered PDF Question Answering System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**An intelligent desktop application that answers questions from PDF documents using RAG (Retrieval-Augmented Generation) technology with Turkish Text-to-Speech support.**

[🇹🇷 Türkçe](#-türkçe) | [🇬🇧 English](#-english)

</div>

---

## 🇬🇧 English

### ✨ Features

- **📄 PDF Processing** - Load and analyze PDF documents with intelligent text chunking
- **🔍 Smart Search** - Vector-based semantic search using HuggingFace embeddings
- **🤖 AI Responses** - GPT-4o-mini powered answers based on document context
- **🔊 Text-to-Speech** - Turkish TTS with OpenAI's voice synthesis (Nova voice)
- **🎨 Modern UI** - Dark-themed PyQt6 interface with animated visualizers
- **💫 Thinking Visualizer** - 3D geodesic sphere animation during processing
- **🎵 Speaking Visualizer** - Frequency-synchronized audio visualization
- **🌐 Fallback Search** - Option to search general knowledge when PDF doesn't contain the answer
- **🔄 Auto-Update** - GitHub-based automatic update system
- **🔐 Secure API Key** - Environment-based API key management

### 📋 Requirements

- Python 3.10+
- OpenAI API Key
- Windows/macOS/Linux

### 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/bettercallumut/Rag-PDF-Assistant.git
cd Rag-PDF-Assistant

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### 📦 Dependencies

```
langchain, langchain-community, langchain-huggingface
chromadb, sentence-transformers
openai, tiktoken
PyQt6, numpy, pydub, mutagen
python-dotenv, requests, imageio-ffmpeg
```

### 🎯 Usage

1. **Start the app** - Enter your OpenAI API key on first launch
2. **Load PDF** - Click "PDF YÜKLE" to select a document
3. **Ask questions** - Type your question and press Enter or click "GÖNDER"
4. **Listen** - Enable "Sesli Yanıt" for voice responses
5. **Update** - Click ⟳ to check for updates

### 🏗️ Architecture

```
Rag-PDF-Assistant/
├── main.py              # Main application & UI
├── config.py            # Configuration & API key management
├── rag_system.py        # RAG logic & PDF processing
├── workers.py           # Background threads (PDF, Query, TTS)
├── visualizer.py        # Thinking animation (3D sphere)
├── audio_visualizer.py  # Speaking animation (frequency bars)
├── text_processor.py    # TTS text preprocessing
├── dialogs.py           # Custom styled dialogs
├── updater.py           # GitHub update system
├── requirements.txt     # Python dependencies
└── .env                 # API key storage (not in repo)
```

### 🔧 Configuration

Create a `.env` file or enter your API key on first launch:
```
OPENAI_API_KEY=sk-your-api-key-here
```

---

## 🇹🇷 Türkçe

### ✨ Özellikler

- **📄 PDF İşleme** - PDF belgelerini akıllı metin parçalama ile yükleyin ve analiz edin
- **🔍 Akıllı Arama** - HuggingFace embedding'leri ile vektör tabanlı semantik arama
- **🤖 AI Yanıtları** - Belge bağlamına dayalı GPT-4o-mini destekli cevaplar
- **🔊 Sesli Yanıt** - OpenAI ses sentezi ile Türkçe TTS (Nova sesi)
- **🎨 Modern Arayüz** - Animasyonlu görselleştiricilerle koyu temalı PyQt6 arayüzü
- **💫 Düşünme Görselleştiricisi** - İşlem sırasında 3D geodezik küre animasyonu
- **🎵 Konuşma Görselleştiricisi** - Frekans senkronizeli ses görselleştirmesi
- **🌐 Yedek Arama** - PDF'de cevap bulunamazsa genel bilgi havuzunda arama seçeneği
- **🔄 Otomatik Güncelleme** - GitHub tabanlı otomatik güncelleme sistemi
- **🔐 Güvenli API Anahtarı** - Ortam değişkeni tabanlı API anahtarı yönetimi

### 📋 Gereksinimler

- Python 3.10+
- OpenAI API Anahtarı
- Windows/macOS/Linux

### 🚀 Kurulum

```bash
# Depoyu klonlayın
git clone https://github.com/bettercallumut/Rag-PDF-Assistant.git
cd Rag-PDF-Assistant

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Uygulamayı çalıştırın
python main.py
```

### 🎯 Kullanım

1. **Uygulamayı başlatın** - İlk açılışta OpenAI API anahtarınızı girin
2. **PDF yükleyin** - "PDF YÜKLE" butonuna tıklayarak belge seçin
3. **Soru sorun** - Sorunuzu yazın ve Enter'a basın veya "GÖNDER"e tıklayın
4. **Dinleyin** - Sesli yanıtlar için "Sesli Yanıt" seçeneğini etkinleştirin
5. **Güncelleyin** - Güncellemeleri kontrol etmek için ⟳ butonuna tıklayın

### 🎨 Ekran Görüntüleri

| Ana Ekran | Düşünme Animasyonu | Konuşma Animasyonu |
|-----------|-------------------|-------------------|
| Modern koyu tema | 3D küre efekti | Frekans çubukları |

### 🔧 Yapılandırma

İlk açılışta API anahtarınızı girin veya `.env` dosyası oluşturun:
```
OPENAI_API_KEY=sk-api-anahtariniz
```

### 📝 Notlar

- Uygulama Türkçe dil desteği için optimize edilmiştir
- TTS özelliği özel karakterleri ve kısaltmaları otomatik olarak düzenler
- Güncelleme sistemi dosyaları güncellemeden önce yedekler

---

## 📄 License / Lisans

MIT License - see [LICENSE](LICENSE) for details.

## 🤝 Contributing / Katkıda Bulunma

Pull requests are welcome! / Pull request'ler kabul edilir!

## 👤 Author / Geliştirici

**Samet Yıldız**

---

<div align="center">
Made with ❤️ using Python & PyQt6
</div>
