# R.A.G PDF Asistanı

## 🌐 Dil Seçeneği / Language Option

[[Türkçe 🇹🇷](#türkçe)] | [[English 🇬🇧](#english)]

---

<p align="center">
  <img src="https://pngimg.com/uploads/ai/ai_PNG2.png" alt="Yapay Zeka Asistanı Görseli" width="300"/>
</p>

---

<a id="türkçe"></a>
## 🇹🇷 R.A.G PDF Asistanı (Retrieval-Augmented Generation)

RAG PDF Asistanı, teknik dokümantasyonları analiz etmek ve hassas, bağlama duyarlı yanıtlar sağlamak için tasarlanmış gelişmiş bir Geri Getirim-Genişletilmiş Üretim (RAG) aracıdır. Modern bir PyQt6 arayüzü, gerçek zamanlı ses sentezi ve ileri düzey görselleştirme yetenekleri sunar.

### ✨ Temel Özellikler

* **Gelişmiş Belge Analizi**: PDF içeriğinin derin anlamsal olarak anlaşılması için BERT tabanlı gömülmeleri (embeddings) kullanır.
* **RAG Mimarisi**: Halüsinasyon olmadan soruları doğru bir şekilde yanıtlamak için belgelerden ilgili bağlamı alır.
* **Akıllı Sesli Yanıt**:
    * **Otomatik Özetleme**: İsteğe bağlı "Özetle" modu, karmaşık teknik açıklamaları 1-2 cümlelik sesli özetlere dönüştürürken, tam detayları ekranda gösterir.
    * **Yerel TTS Motoru**: Otomatik Türkçe dil desteği ile düşük gecikmeli, hızlı sinirsel (neural-like) konuşma sentezi.
    * **Gerçek Zamanlı Görselleştirme**: Sesin genliğine ve frekansına tepki veren dinamik bir ses görselleştiricisi.
* **Sağlam Hata Yönetimi**:
    * **Akıllı Son İşleme**: Yapay zeka yanıtlarında eksik teknik sembolleri veya düğme adlarını otomatik olarak düzeltir.
    * **Otomatik Kurulum**: İlk çalıştırmada eksik dil paketlerini ve ses bileşenlerini otomatik olarak kurar.

### 💻 Teknik Yığın

* **Ön Yüz (Frontend)**: Python PyQt6 (Modern UI/UX)
* **YZ/ML**: LangChain, OpenAI GPT-4o-mini / GPT-4, ChromaDB (Vektör Deposu)
* **Gömülmeler (Embeddings)**: HuggingFace (`bert-base-turkish-cased`)
* **Ses**: PyAudio, NumPy (FFT Görselleştirme), pyttsx3

### 💾 Kurulum

1.  Depoyu klonlayın.
2.  Bağımlılıkları yükleyin:
    ```bash
    pip install -r requirements.txt
    ```
3.  Uygulamayı çalıştırın:
    ```bash
    python main.py
    ```

### 🚀 Kullanım

1.  Uygulamayı başlatın.
2.  İstendiğinde OpenAI API Anahtarınızı girin (güvenli bir şekilde saklanır).
3.  Bir belgeyi analiz etmek için **"+ PDF Yükle"** düğmesine tıklayın.
4.  Sohbet arayüzünde sorularınızı sorun.
5.  Gerektiğinde **"Sesli Yanıt"** veya **"Özetle"** seçeneklerini açıp kapatın.

### ⚖️ Lisans

MIT Lisansı.

---
---

<a id="english"></a>
## 🇬🇧 R.A.G PDF Assistant (Retrieval-Augmented Generation)

RAG Pdf Assistant is a sophisticated Retrieval-Augmented Generation (RAG) tool designed to analyze technical documentation and provide precise, context-aware answers. It features a modern PyQt6 interface, real-time voice synthesis, and advanced visualization capabilities.

### ✨ Key Features

* **Advanced Document Analysis**: Uses BERT-based embeddings for deep semantic understanding of PDF content.
* **RAG Architecture**: Retrieves relevant context from documents to answer questions accurately without hallucination.
* **Intelligent Voice Response**:
    * **Auto-Summarization**: Optional "Summarize" mode condenses complex technical explanations into 1-2 sentence voice summaries while displaying full details.
    * **Local TTS Engine**: Low-latency, fast neural-like speech synthesis with automatic Turkish language support.
    * **Real-time Visualization**: Dynamic audio visualizer that reacts to voice amplitude and frequency.
* **Robust Error Handling**:
    * **Smart Post-Processing**: Automatically corrects missing technical symbols or button names in AI responses.
    * **Automatic Setup**: Auto-installs missing language packs and voice components on first run.

### 💻 Technical Stack

* **Frontend**: Python PyQt6 (Modern UI/UX)
* **AI/ML**: LangChain, OpenAI GPT-4o-mini / GPT-4, ChromaDB (Vector Store)
* **Embeddings**: HuggingFace (`bert-base-turkish-cased`)
* **Audio**: PyAudio, NumPy (FFT Visualization), pyttsx3

### 💾 Installation

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the application:
    ```bash
    python main.py
    ```

### 🚀 Usage

1.  Launch the application.
2.  Enter your OpenAI API Key when prompted (stored securely).
3.  Click **"+ PDF Load"** to analyze a document.
4.  Ask questions in the chat interface.
5.  Toggle **"Voice Response"** or **"Summarize"** options as needed.

### ⚖️ License

MIT License.
