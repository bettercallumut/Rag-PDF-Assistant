import tempfile
import queue
import os
import time
import random
from PyQt6.QtCore import QThread, pyqtSignal
import config
from text_processor import process_text_for_tts

try:
    import pyttsx3
    import pythoncom
    HAS_PYTTSX3 = True
except ImportError:
    HAS_PYTTSX3 = False

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
    finished = pyqtSignal(str)
    token_received = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, rag_system, question, mode="rag"):
        super().__init__()
        self.rag = rag_system
        self.question = question
        self.mode = mode

    def run(self):
        try:
            if self.mode == "rag":
                res = self.rag.query(self.question, config.API_KEY)
            else:
                res = self.rag.query_general(self.question, config.API_KEY)

            if res == "###ASK_FALLBACK###":
                self.finished.emit(res)
                return

            words = res.split(" ")
            accumulated_text = ""
            
            for word in words:
                chunk = word + " "
                self.token_received.emit(chunk)
                accumulated_text += chunk
                time.sleep(random.uniform(0.02, 0.05))

            self.finished.emit(accumulated_text)
            
        except Exception as e:
            self.error.emit(str(e))

class PersistentTTSWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.queue = queue.Queue()
        self.running = True

    def speak(self, text):
        self.queue.put(text)

    def stop(self):
        self.running = False
        self.queue.put(None)
        self.wait()

    def run(self):
        if not HAS_PYTTSX3:
            self.error.emit("pyttsx3 modülü eksik.")
            return

        try:
            import pythoncom
            
            while self.running:
                text = self.queue.get()
                if text is None:
                    break
                
                try:
                    pythoncom.CoInitialize()
                    engine = pyttsx3.init()
                    
                    voices = engine.getProperty('voices')
                    turkish_voice = None
                    for voice in voices:
                        if "tr" in voice.id.lower() or "turkish" in voice.name.lower() or "tolga" in voice.name.lower():
                            turkish_voice = voice.id
                            break
                    
                    if turkish_voice:
                        engine.setProperty('voice', turkish_voice)
                    
                    engine.setProperty('rate', config.TTS_LOCAL_RATE)
                    
                    from text_processor import basic_text_cleanup
                    clean_text = basic_text_cleanup(text)
                    
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                    temp_file.close()
                    
                    engine.save_to_file(clean_text, temp_file.name)
                    engine.runAndWait()
                    
                    del engine
                    pythoncom.CoUninitialize()
                    
                    if os.path.exists(temp_file.name) and os.path.getsize(temp_file.name) > 0:
                        self.finished.emit(temp_file.name)
                    else:
                        self.error.emit("Ses dosyası oluşturulamadı.")
                        
                except Exception as e:
                    self.error.emit(str(e))
                    try:
                        pythoncom.CoUninitialize()
                    except:
                        pass
                finally:
                    self.queue.task_done()
                    
        except Exception as e:
            self.error.emit(f"TTS Başlatma Hatası: {e}")

class SummaryWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, rag_system, text):
        super().__init__()
        self.rag_system = rag_system
        self.text = text

    def run(self):
        try:
            summary = self.rag_system.generate_summary(self.text, config.API_KEY)
            self.finished.emit(summary)
        except Exception as e:
            self.error.emit(str(e))
