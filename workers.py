import tempfile
from PyQt6.QtCore import QThread, pyqtSignal
from openai import OpenAI
import config
from text_processor import process_text_for_tts

class LoadPDFWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(int)
    error = pyqtSignal(str)

    def __init__(self, rag_system, path):
        super().__init__()
        self.rag = rag_system
        self.path = path

    def run(self):
        try:
            count = self.rag.process_pdf(self.path, lambda x: self.progress.emit(x))
            self.finished.emit(count)
        except Exception as e:
            self.error.emit(str(e))

class QueryWorker(QThread):
    result = pyqtSignal(str)
    
    def __init__(self, rag_system, question, mode="rag"):
        super().__init__()
        self.rag = rag_system
        self.question = question
        self.mode = mode

    def run(self):
        if self.mode == "rag":
            res = self.rag.query(self.question, config.API_KEY)
        else:
            res = self.rag.query_general(self.question, config.API_KEY)
        self.result.emit(res)

class TTSWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, text):
        super().__init__()
        self.text = text
    
    def run(self):
        try:
            processed_text = process_text_for_tts(self.text)
            if len(processed_text) > 4000:
                processed_text = processed_text[:4000]
            client = OpenAI(api_key=config.API_KEY)
            response = client.audio.speech.create(
                model="tts-1",
                voice="nova",
                input=processed_text,
                speed=1.1,
                response_format="mp3"
            )
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            for chunk in response.iter_bytes(chunk_size=4096):
                temp_file.write(chunk)
            temp_file.close()
            self.finished.emit(temp_file.name)
        except Exception as e:
            self.error.emit(str(e))
