# R.A.G PDF Assistant

RAG Pdf Assistant is a sophisticated Retrieval-Augmented Generation (RAG) tool designed to analyze technical documentation and provide precise, context-aware answers. It features a modern PyQt6 interface, real-time voice synthesis, and advanced visualization capabilities.

![Interface](https://via.placeholder.com/800x450.png?text=RAG+Pdf+Assistant)

## Key Features

- **Advanced Document Analysis**: Uses BERT-based embeddings for deep semantic understanding of PDF content.
- **RAG Architecture**: Retrieves relevant context from documents to answer questions accurately without hallucination.
- **Intelligent Voice Response**:
  - **Auto-Summarization**: Optional "Summarize" mode condenses complex technical explanations into 1-2 sentence voice summaries while displaying full details.
  - **Local TTS Engine**: Low-latency, fast neural-like speech synthesis with automatic Turkish language support.
  - **Real-time Visualization**: Dynamic audio visualizer that reacts to voice amplitude and frequency.
- **Robust Error Handling**:
  - **Smart Post-Processing**: Automatically corrects missing technical symbols or button names in AI responses.
  - **Automatic Setup**: Auto-installs missing language packs and voice components on first run.

## Technical Stack

- **Frontend**: Python PyQt6 (Modern UI/UX)
- **AI/ML**: LangChain, OpenAI GPT-4o-mini / GPT-4, ChromaDB (Vector Store)
- **Embeddings**: HuggingFace (`bert-base-turkish-cased`)
- **Audio**: PyAudio, NumPy (FFT Visualization), pyttsx3

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. Launch the application.
2. Enter your OpenAI API Key when prompted (stored securely).
3. Click **"+ PDF Load"** to analyze a document.
4. Ask questions in the chat interface.
5. Toggle **"Voice Response"** or **"Summarize"** options as needed.

## License

MIT License.
