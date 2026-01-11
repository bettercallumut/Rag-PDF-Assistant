import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
                             QLabel, QProgressBar, QFileDialog, QFrame, QCheckBox,
                             QDialog, QDialogButtonBox, QProgressDialog)
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

import config
from rag_system import RAGSystem
from collections import deque
from workers import LoadPDFWorker, QueryWorker, PersistentTTSWorker, SummaryWorker
from visualizer import ThinkingVisualizer
from audio_visualizer import SpeakingVisualizer
from dialogs import StyledMessageBox

class ApiKeyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("API Girişi")
        self.setModal(True)
        self.setMinimumWidth(450)
        self.setStyleSheet(f"""
            QDialog {{ background-color: {config.COLOR_BG}; }}
            QLabel {{ color: {config.COLOR_TEXT}; font-size: 14px; }}
            QLineEdit {{
                background-color: {config.COLOR_INPUT_BG};
                border: 1px solid {config.COLOR_BORDER};
                padding: 12px;
                border-radius: 8px;
                color: {config.COLOR_TEXT};
                font-size: 13px;
            }}
            QLineEdit:focus {{ border: 1px solid {config.COLOR_ACCENT}; }}
            QPushButton {{
                background-color: {config.COLOR_ACCENT};
                color: white;
                border: none;
                padding: 10px 25px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:hover {{ background-color: {config.COLOR_ACCENT_HOVER}; }}
            QPushButton:disabled {{ background-color: {config.COLOR_PANEL}; color: {config.COLOR_TEXT_DIM}; }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        lbl = QLabel("OpenAI API Anahtarı")
        lbl.setStyleSheet(f"color: {config.COLOR_TEXT}; font-weight: bold; font-size: 16px;")
        layout.addWidget(lbl)

        lbl_desc = QLabel("Asistanın çalışması için geçerli bir OpenAI API anahtarı gereklidir.")
        lbl_desc.setStyleSheet(f"color: {config.COLOR_TEXT_DIM}; font-size: 12px;")
        lbl_desc.setWordWrap(True)
        layout.addWidget(lbl_desc)

        self.input = QLineEdit()
        self.input.setPlaceholderText("sk-...")
        self.input.setEchoMode(QLineEdit.EchoMode.Password)
        self.input.textChanged.connect(self.validate)
        layout.addWidget(self.input)

        self.status_lbl = QLabel("")
        self.status_lbl.setStyleSheet(f"color: {config.COLOR_TEXT_DIM}; font-size: 12px;")
        layout.addWidget(self.status_lbl)

        self.btn_save = QPushButton("Doğrula ve Başlat")
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save.setEnabled(False)
        self.btn_save.clicked.connect(self.save_key)
        layout.addWidget(self.btn_save)

    def validate(self):
        key = self.input.text().strip()
        if key.startswith("sk-") and len(key) > 20:
            self.btn_save.setEnabled(True)
            self.status_lbl.setText("")
        else:
            self.btn_save.setEnabled(False)

    def save_key(self):
        key = self.input.text().strip()
        self.status_lbl.setText("API anahtarı doğrulanıyor...")
        self.status_lbl.setStyleSheet(f"color: {config.COLOR_USER_MSG};")
        self.input.setEnabled(False)
        self.btn_save.setEnabled(False)
        QApplication.processEvents()

        if config.test_api_key(key):
            config.save_api_key(key)
            self.status_lbl.setText("Başarılı! Başlatılıyor...")
            self.status_lbl.setStyleSheet(f"color: {config.COLOR_AI_MSG};")
            QTimer.singleShot(800, self.accept)
        else:
            self.status_lbl.setText("Geçersiz API anahtarı! Lütfen kontrol edin.")
            self.status_lbl.setStyleSheet(f"color: {config.COLOR_ERROR};")
            self.input.setEnabled(True)
            self.btn_save.setEnabled(True)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("R.A.G PDF Asistanı")
        self.resize(1000, 800)
        self.rag_system = None
        self.tts_enabled = True
        self.current_audio_file = None
        self.audio_queue = deque()
        self.is_playing_audio = False
        self.setup_ui()
        self.setup_audio()
        
        self.tts_generation_queue = []
        self.is_generating_tts = False
        self.active_tts_worker = None
        
        QTimer.singleShot(100, self.init_system)

    def setup_audio(self):
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(1.0)
        
        self.media_player.playbackStateChanged.connect(self.on_playback_state_changed)
        self.media_player.errorOccurred.connect(self.on_media_error)
        self.media_player.mediaStatusChanged.connect(self.on_media_status_changed)
        
        self.persistent_tts = PersistentTTSWorker()
        self.persistent_tts.finished.connect(self.on_persistent_tts_finished)
        self.persistent_tts.error.connect(self.on_tts_error)
        self.persistent_tts.start()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {config.COLOR_BG}; }}
            QWidget {{ font-family: 'Segoe UI', sans-serif; font-size: 14px; color: {config.COLOR_TEXT}; }}

            QScrollBar:vertical {{
                border: none;
                background: {config.COLOR_BG};
                width: 8px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {config.COLOR_BORDER};
                min-height: 20px;
                border-radius: 4px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}

            QTextEdit {{
                background-color: {config.COLOR_BG};
                border: none;
                padding: 15px;
                selection-background-color: {config.COLOR_ACCENT};
            }}

            QLineEdit {{ 
                background-color: {config.COLOR_INPUT_BG};
                border: 1px solid {config.COLOR_BORDER};
                padding: 12px;
                border-radius: 8px;
                color: {config.COLOR_TEXT};
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 1px solid {config.COLOR_ACCENT};
            }}

            QPushButton {{ 
                background-color: {config.COLOR_ACCENT}; 
                color: white; 
                border: none;
                padding: 10px 20px; 
                border-radius: 8px;
                font-weight: 600;
            }}
            QPushButton:hover {{ 
                background-color: {config.COLOR_ACCENT_HOVER}; 
            }}
            QPushButton:disabled {{ 
                background-color: {config.COLOR_PANEL};
                color: {config.COLOR_TEXT_DIM};
            }}

            QProgressBar {{ 
                border: none; 
                background-color: {config.COLOR_PANEL}; 
                height: 4px; 
            }}
            QProgressBar::chunk {{ background-color: {config.COLOR_ACCENT}; }}

            QCheckBox {{
                color: {config.COLOR_TEXT_DIM};
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid {config.COLOR_BORDER};
                background-color: {config.COLOR_INPUT_BG};
            }}
            QCheckBox::indicator:checked {{
                border: 1px solid {config.COLOR_ACCENT};
                background-color: {config.COLOR_ACCENT};
            }}
        """)

        top_panel = QFrame()
        top_panel.setStyleSheet(f"background-color: {config.COLOR_PANEL}; border-bottom: 1px solid {config.COLOR_BORDER};")
        top_panel.setFixedHeight(60)
        top_layout = QHBoxLayout(top_panel)
        top_layout.setContentsMargins(20, 0, 20, 0)

        app_title = QLabel("R.A.G PDF Asistanı")
        app_title.setStyleSheet(f"font-weight: bold; font-size: 16px; color: {config.COLOR_TEXT};")
        top_layout.addWidget(app_title)

        self.lbl_status = QLabel("Başlatılıyor...")
        self.lbl_status.setStyleSheet(f"color: {config.COLOR_TEXT_DIM}; margin-left: 10px;")
        top_layout.addWidget(self.lbl_status)

        self.tts_progress_bar = QProgressBar()
        self.tts_progress_bar.setRange(0, 0)
        self.tts_progress_bar.setFixedWidth(150)
        self.tts_progress_bar.setFixedHeight(15)
        self.tts_progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {config.COLOR_BORDER};
                border-radius: 7px;
                background-color: {config.COLOR_INPUT_BG};
                margin-left: 10px;
            }}
            QProgressBar::chunk {{
                background-color: {config.COLOR_ACCENT};
                border-radius: 7px;
                width: 20px;
            }}
        """)
        self.tts_progress_bar.setVisible(False)
        top_layout.addWidget(self.tts_progress_bar)

        top_layout.addStretch()

        self.tts_checkbox = QCheckBox("Sesli Yanıt")
        self.tts_checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        self.tts_checkbox.setChecked(True)
        self.tts_checkbox.setToolTip("Yanıtları sesli olarak dinleyin")
        self.tts_checkbox.stateChanged.connect(self.on_tts_checkbox_changed)
        top_layout.addWidget(self.tts_checkbox)

        self.summary_checkbox = QCheckBox("Özetle")
        self.summary_checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        self.summary_checkbox.setChecked(False)
        self.summary_checkbox.setToolTip("İşaretliyse: Yazı uzun kalsa bile sesli yanıt sadece özet geçer.")
        top_layout.addWidget(self.summary_checkbox)
        
        self.btn_load = QPushButton("+ PDF Yükle")
        self.btn_load.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_load.setToolTip("Analiz için bir PDF belgesi yükleyin")
        self.btn_load.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.COLOR_PANEL};
                border: 1px solid {config.COLOR_ACCENT};
                color: {config.COLOR_ACCENT};
                font-weight: 600;
                padding: 6px 15px;
            }}
            QPushButton:hover {{
                background-color: {config.COLOR_ACCENT};
                color: white;
            }}
            QPushButton:disabled {{
                border: 1px solid {config.COLOR_BORDER};
                color: {config.COLOR_TEXT_DIM};
                background-color: transparent;
            }}
        """)
        self.btn_load.clicked.connect(self.select_pdf)
        self.btn_load.setEnabled(False)
        top_layout.addWidget(self.btn_load)

        main_layout.addWidget(top_panel)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        main_layout.addWidget(self.progress)

        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.thinking_viz = ThinkingVisualizer()
        self.thinking_viz.setVisible(False)
        content_layout.addWidget(self.thinking_viz)

        self.audio_viz = SpeakingVisualizer()
        self.audio_viz.setVisible(False)
        content_layout.addWidget(self.audio_viz)

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setFrameShape(QFrame.Shape.NoFrame)
        content_layout.addWidget(self.chat_area)

        main_layout.addWidget(content_area)

        bottom_panel = QFrame()
        bottom_layout = QHBoxLayout(bottom_panel)
        bottom_panel.setStyleSheet(f"background-color: {config.COLOR_PANEL}; padding: 15px; border-top: 1px solid {config.COLOR_BORDER};")

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Bir soru sorun...")
        self.input_field.returnPressed.connect(self.send_query)
        bottom_layout.addWidget(self.input_field)

        self.btn_stop = QPushButton("DURDUR")
        self.btn_stop.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_stop.setFixedWidth(100)
        self.btn_stop.setToolTip("Sesli yanıtı durdur")
        self.btn_stop.setStyleSheet(f"background-color: {config.COLOR_ERROR}; border: none;")
        self.btn_stop.clicked.connect(self.stop_speaking)
        self.btn_stop.setVisible(False)
        bottom_layout.addWidget(self.btn_stop)

        self.btn_send = QPushButton("GÖNDER")
        self.btn_send.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_send.setFixedWidth(100)
        self.btn_send.setToolTip("Sorunuzu gönderin")
        self.btn_send.clicked.connect(self.send_query)
        bottom_layout.addWidget(self.btn_send)

        main_layout.addWidget(bottom_panel)
    
    def on_tts_checkbox_changed(self, state):
        self.tts_enabled = (state == 2)
        if self.tts_enabled:
            self.lbl_status.setText("Sesli yanıt açık")
            QTimer.singleShot(100, self.check_and_fix_voices)
        else:
            self.lbl_status.setText("Sesli yanıt kapalı")
            self.stop_speaking()            

    def check_and_fix_voices(self):
        try:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            turkish_found = False
            for v in voices:
                if "TR" in v.id or "Turkish" in v.name or "Tolga" in v.name:
                    turkish_found = True
                    break
            
            if not turkish_found:
                self.add_log("SİSTEM", "⚠️ Türkçe ses paketi eksik. Yükleme aracı başlatılıyor...")
                import subprocess
                if hasattr(sys, '_MEIPASS'):
                    script_path = os.path.join(sys._MEIPASS, "fix_voice.ps1")
                else:
                    script_path = os.path.abspath("fix_voice.ps1")
                subprocess.Popen(["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path], shell=True)
        except Exception as e:
            pass

    def init_system(self):
        self.lbl_status.setText("Yükleniyor...")
        QApplication.processEvents()
        try:
            self.rag_system = RAGSystem()
            self.lbl_status.setText("Hazır")
            self.btn_load.setEnabled(True)
            self.add_log("SİSTEM", "Asistan aktif. Sohbet etmek için bir PDF belgesi yükleyin.")
        except Exception as e:
            self.lbl_status.setText("Başlatma Hatası")
            self.add_log("HATA", f"Sistem başlatılamadı: {str(e)}")

    def add_log(self, sender, message):
        color = config.COLOR_TEXT_DIM
        align = "left"

        if sender == "SEN":
            color = config.COLOR_USER_MSG
            align = "right"
        elif sender == "ASİSTAN":
            color = config.COLOR_AI_MSG
        elif sender == "HATA":
            color = config.COLOR_ERROR

        html = f"""
            <div style='margin-bottom: 20px; text-align: {align};'>
                <b style='color: {color}; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px;'>{sender}</b><br>
                <div style='color: {config.COLOR_TEXT}; margin-top: 5px; line-height: 1.5;'>{message}</div>
            </div>
        """
        self.chat_area.append(html)
        sb = self.chat_area.verticalScrollBar()
        sb.setValue(sb.maximum())

    def select_pdf(self):
        fname, _ = QFileDialog.getOpenFileName(self, "PDF Seç", "", "PDF Files (*.pdf)")
        if fname:
            self.lbl_status.setText(f"İşleniyor...")
            self.btn_load.setEnabled(False)
            self.btn_send.setEnabled(False)
            self.input_field.setEnabled(False)

            self.add_log("SİSTEM", f"'{os.path.basename(fname)}' analizi başlatıldı, lütfen bekleyin...")

            self.loader_thread = LoadPDFWorker(self.rag_system, fname)
            self.loader_thread.progress.connect(self.progress.setValue)
            self.loader_thread.finished.connect(self.on_pdf_loaded)
            self.loader_thread.error.connect(lambda e: self.add_log("HATA", e))
            self.loader_thread.start()

    def on_pdf_loaded(self, chunk_count):
        self.progress.setValue(100)
        self.lbl_status.setText("Hazır")
        self.btn_load.setEnabled(True)
        self.btn_send.setEnabled(True)
        self.input_field.setEnabled(True)
        self.input_field.setFocus()
        self.add_log("SİSTEM", f"Analiz tamamlandı. {chunk_count} veri parçası belleğe alındı.")
        QTimer.singleShot(1500, lambda: self.progress.setValue(0))

    def send_query(self):
        text = self.input_field.text().strip()
        if not text:
            return
        self.input_field.clear()
        self.add_log("SEN", text)
        self.start_thinking_mode(text)

    def start_thinking_mode(self, question):
        self.last_question = question
        self.input_field.setEnabled(False)
        self.btn_send.setEnabled(False)
        self.btn_send.setText("...")
        self.audio_viz.setVisible(False)
        self.thinking_viz.setVisible(True)
        self.thinking_viz.start_animation()
        
        self.worker = QueryWorker(self.rag_system, question)
        self.worker.finished.connect(self.on_query_result)
        self.worker.error.connect(lambda e: self.add_log("HATA", e))
        self.worker.token_received.connect(self.on_token_received)
        
        self.add_log("ASİSTAN", "")
        self.current_message_buffer = ""
        
        self.worker.start()

    def on_token_received(self, token):
        self.current_message_buffer += token
        cursor = self.chat_area.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.insertText(token)
        sb = self.chat_area.verticalScrollBar()
        sb.setValue(sb.maximum())

    def on_sentence_ready(self, sentence):
        try:
            if self.tts_enabled:
                self.tts_generation_queue.append(sentence)
                self.process_tts_queue()
        except Exception as e:
            pass

    def on_stream_finished(self):
        self.thinking_viz.stop_animation()
        self.thinking_viz.setVisible(False)
        self.btn_send.setText("GÖNDER")

    def process_tts_queue(self):
        try:
            if not self.tts_generation_queue:
                return

            if self.is_generating_tts:
                if self.active_tts_worker is None or not self.active_tts_worker.isRunning():
                     self.is_generating_tts = False
                else:
                     return

            self.is_generating_tts = True
            sentence = self.tts_generation_queue.pop(0)

            self.persistent_tts.speak(sentence)
            self.is_generating_tts = False
            self.process_tts_queue()
            return
            
        except Exception as e:
            self.is_generating_tts = False
            self.process_tts_queue()

    def on_persistent_tts_finished(self, file_path):
        if file_path and os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            self.queue_audio(file_path)
        else:
            self.add_log("HATA", "Ses dosyası oluşturulamadı veya boş")
            self.reset_ui()

    def on_tts_generated(self, file_path, sentence):
        self.is_generating_tts = False
        self.active_tts_worker = None
        if file_path and os.path.exists(file_path):
            self.queue_audio(file_path)
        self.process_tts_queue()

    def queue_audio(self, file_path):
        self.audio_queue.append(file_path)
        if not self.is_playing_audio:
            self.is_playing_audio = True
            self.play_next_in_queue()

    def play_next_in_queue(self):
        if not self.audio_queue:
            self.is_playing_audio = False
            self.reset_ui()
            return
        
        try:
            self.is_playing_audio = True
            file_path = self.audio_queue.popleft()
            
            if not file_path or not os.path.exists(file_path):
                self.add_log("HATA", f"Ses dosyası bulunamadı: {file_path}")
                self.play_next_in_queue()
                return
            
            self.play_audio(file_path)
        except Exception as e:
            self.add_log("HATA", f"Ses çalma hatası: {str(e)}")
            self.is_playing_audio = False
            self.reset_ui()

    def on_query_result(self, result):
        self.thinking_viz.stop_animation()
        self.thinking_viz.setVisible(False)
        self.btn_send.setText("GÖNDER")
        
        if result == "###ASK_FALLBACK###":
            self.reset_ui()
            
            msg = StyledMessageBox(self)
            msg.setWindowTitle("Bilgi Bulunamadı")
            msg.setText("PDF'de bu konuyla ilgili bilgi bulunamadı.")
            msg.setInformativeText("Genel bilgi için ChatGPT'ye sormak ister misiniz?")
            msg.setStandardButtons(StyledMessageBox.StandardButton.Yes | StyledMessageBox.StandardButton.No)
            msg.setDefaultButton(StyledMessageBox.StandardButton.Yes)
            
            response = msg.exec()
            
            if response == StyledMessageBox.StandardButton.Yes:
                self.add_log("SİSTEM", "Genel bilgi için ChatGPT'ye soruluyor...")
                self.query_with_chatgpt()
            else:
                self.add_log("SİSTEM", "Sorgu iptal edildi.")
            return
        
        if self.tts_enabled:
             self.start_tts(result)
        else:
             self.reset_ui()

    
    def query_with_chatgpt(self):
        if not hasattr(self, 'last_question'):
            self.add_log("HATA", "Soru bulunamadı.")
            self.reset_ui()
            return
        
        self.input_field.setEnabled(False)
        self.btn_send.setEnabled(False)
        self.thinking_viz.setVisible(True)
        self.thinking_viz.start_animation()
        
        self.worker = QueryWorker(self.rag_system, self.last_question, mode="general")
        self.worker.finished.connect(self.on_query_result)
        self.worker.error.connect(lambda e: self.add_log("HATA", e))
        self.worker.token_received.connect(self.on_token_received)
        
        self.add_log("ASİSTAN", "")
        self.current_message_buffer = ""
        
        self.worker.start()

    def start_tts(self, text):
        if self.summary_checkbox.isChecked():
            self.lbl_status.setText("Özetleniyor...")
            self.summary_worker = SummaryWorker(self.rag_system, text)
            self.summary_worker.finished.connect(lambda summary: self.on_summary_ready(summary))
            self.summary_worker.error.connect(self.on_summary_error)
            self.summary_worker.start()
        else:
            self.lbl_status.setText("Seslendiriliyor...")
            self.persistent_tts.speak(text)

    def on_summary_ready(self, summary_text):
        self.lbl_status.setText("Özet okunuyor...")
        self.persistent_tts.speak(summary_text)
    
    def on_summary_error(self, error):
        self.add_log("HATA", f"Özetleme hatası: {error}")
        self.reset_ui()

    def play_audio(self, file_path):
        self.tts_progress_bar.setVisible(False)
        self.current_audio_file = file_path
        self.lbl_status.setText("Yanıtlanıyor...")
        self.thinking_viz.setVisible(False)
        self.audio_viz.set_audio_data(file_path)
        self.audio_viz.setVisible(True)
        self.btn_send.setVisible(False)
        self.btn_stop.setVisible(True)
        self.media_player.setSource(QUrl.fromLocalFile(file_path))
        self.media_player.play()
        
    def stop_speaking(self):
        self.audio_queue.clear()
        self.is_playing_audio = False
        self.media_player.stop()
        self.tts_generation_queue = []
        self.is_generating_tts = False
        try:
            while not self.persistent_tts.queue.empty():
                try:
                    self.persistent_tts.queue.get_nowait()
                    self.persistent_tts.queue.task_done()
                except:
                    break
        except:
            pass
        self.audio_viz.stop()
        self.audio_viz.setVisible(False)
        self.thinking_viz.stop_animation()
        self.thinking_viz.setVisible(False)
        self.reset_ui()

    def on_playback_state_changed(self, state):
        if state == QMediaPlayer.PlaybackState.StoppedState:
            self.audio_viz.stop()
            self.audio_viz.setVisible(False)
            if self.current_audio_file and os.path.exists(self.current_audio_file):
                try:
                    os.remove(self.current_audio_file)
                except:
                    pass
                self.current_audio_file = None
            if self.is_playing_audio:
                self.play_next_in_queue()
            else:
                self.reset_ui()

    def on_media_error(self, error, error_string):
        self.add_log("HATA", f"Ses çalma hatası: {error_string}")
        self.stop_speaking()
    
    def on_media_status_changed(self, status):
        pass
        
    def update_visualizer_from_timer(self):
        pass

    def on_tts_error(self, error):
        self.tts_progress_bar.setVisible(False)
        self.add_log("HATA", f"Ses hatası: {error}")
        
        self.tts_generation_queue = []
        self.is_generating_tts = False
        self.active_tts_worker = None
        self.audio_queue.clear()
        self.is_playing_audio = False
        self.thinking_viz.stop_animation()
        self.thinking_viz.setVisible(False)
        self.audio_viz.stop()
        self.audio_viz.setVisible(False)
        self.reset_ui()

    def reset_ui(self):
        self.input_field.setEnabled(True)
        self.btn_send.setEnabled(True)
        self.btn_send.setVisible(True)
        self.btn_stop.setVisible(False)
        self.btn_send.setText("GÖNDER")
        self.input_field.setFocus()
        self.lbl_status.setText("Hazır")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    if not config.API_KEY:
        dialog = ApiKeyDialog()
        if dialog.exec() != QDialog.DialogCode.Accepted:
            sys.exit(0)
    else:
        if not config.test_api_key(config.API_KEY):
            dialog = ApiKeyDialog()
            if dialog.exec() != QDialog.DialogCode.Accepted:
                sys.exit(0)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
