import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
                             QLabel, QProgressBar, QFileDialog, QFrame, QCheckBox,
                             QDialog, QDialogButtonBox)
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QFont
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

import config
from rag_system import RAGSystem
from workers import LoadPDFWorker, QueryWorker, TTSWorker
from visualizer import ThinkingVisualizer
from audio_visualizer import SpeakingVisualizer
from dialogs import StyledMessageBox
from updater import check_for_updates, GITHUB_REPO

class ApiKeyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("API Anahtarı Gerekli")
        self.setModal(True)
        self.setMinimumWidth(450)
        self.setStyleSheet("""
            QDialog { background-color: #1E1E1E; }
            QLabel { color: #E0E0E0; font-size: 14px; }
            QLineEdit { 
                background-color: #2A2A2A; 
                border: 2px solid #444; 
                padding: 10px; 
                border-radius: 6px; 
                color: white; 
                font-size: 13px;
            }
            QLineEdit:focus { border: 2px solid #00CED1; }
            QPushButton {
                background-color: #00CED1;
                color: #121212;
                border: none;
                padding: 10px 25px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #20B2AA; }
            QPushButton:disabled { background-color: #333; color: #666; }
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)
        lbl = QLabel("Lütfen OpenAI API anahtarınızı girin:")
        layout.addWidget(lbl)
        self.input = QLineEdit()
        self.input.setPlaceholderText("sk-...")
        self.input.setEchoMode(QLineEdit.EchoMode.Password)
        self.input.textChanged.connect(self.validate)
        layout.addWidget(self.input)
        self.status_lbl = QLabel("")
        self.status_lbl.setStyleSheet("color: #888;")
        layout.addWidget(self.status_lbl)
        self.btn_save = QPushButton("Kaydet ve Başlat")
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
        self.status_lbl.setText("Test ediliyor...")
        self.status_lbl.setStyleSheet("color: #FFA500;")
        QApplication.processEvents()
        if config.test_api_key(key):
            config.save_api_key(key)
            self.status_lbl.setText("Başarılı!")
            self.status_lbl.setStyleSheet("color: #00E676;")
            QTimer.singleShot(500, self.accept)
        else:
            self.status_lbl.setText("Geçersiz API anahtarı!")
            self.status_lbl.setStyleSheet("color: #FF5252;")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Asistan - Neural Core")
        self.resize(600, 850)
        self.rag_system = None
        self.tts_enabled = True
        self.current_audio_file = None
        self.setup_ui()
        self.setup_audio()
        QTimer.singleShot(100, self.init_system)

    def setup_audio(self):
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(1.0)
        self.media_player.playbackStateChanged.connect(self.on_playback_state_changed)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {config.COLOR_BG}; }}
            QWidget {{ font-family: 'Segoe UI'; font-size: 14px; color: {config.COLOR_TEXT}; }}
            QTextEdit {{ background-color: {config.COLOR_PANEL}; border: none; padding: 10px; }}
            QLineEdit {{ 
                background-color: #2A2A2A; 
                border: 2px solid #444; 
                padding: 10px; 
                border-radius: 6px; 
                color: white; 
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 2px solid #00CED1;
            }}
            QPushButton {{ 
                background-color: {config.COLOR_ACCENT}; 
                color: white; 
                border: 2px solid {config.COLOR_ACCENT}; 
                padding: 10px 20px; 
                border-radius: 6px; 
                font-weight: bold; 
            }}
            QPushButton:hover {{ 
                background-color: {config.COLOR_ACCENT_HOVER}; 
                border: 2px solid {config.COLOR_ACCENT_HOVER};
            }}
            QPushButton:disabled {{ 
                background-color: #333; 
                color: #666; 
                border: 2px solid #444;
            }}
            QProgressBar {{ 
                border: none; 
                background-color: {config.COLOR_PANEL}; 
                height: 4px; 
            }}
            QProgressBar::chunk {{ background-color: #00CED1; }}
            QCheckBox {{
                color: {config.COLOR_TEXT};
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #FF1744;
                background-color: #FF1744;
            }}
            QCheckBox::indicator:checked {{
                border: 2px solid #00E676;
                background-color: #00E676;
            }}
        """)

        top_panel = QFrame()
        top_panel.setStyleSheet(f"background-color: {config.COLOR_PANEL}; border-bottom: 1px solid #333;")
        top_layout = QHBoxLayout(top_panel)
        self.lbl_status = QLabel("Başlatılıyor...")
        top_layout.addWidget(self.lbl_status)
        top_layout.addStretch()
        self.btn_update = QPushButton("⟳")
        self.btn_update.setFixedWidth(35)
        self.btn_update.setToolTip("Güncelleme Kontrolü")
        self.btn_update.setStyleSheet("background-color: #333; border: 1px solid #555; font-size: 16px;")
        self.btn_update.clicked.connect(self.check_updates)
        top_layout.addWidget(self.btn_update)
        self.tts_checkbox = QCheckBox("Sesli Yanıt")
        self.tts_checkbox.setChecked(True)
        self.tts_checkbox.stateChanged.connect(lambda s: setattr(self, 'tts_enabled', s == 2))
        top_layout.addWidget(self.tts_checkbox)
        self.btn_load = QPushButton("PDF YÜKLE")
        self.btn_load.setFixedWidth(110)
        self.btn_load.setStyleSheet(f"background-color: {config.COLOR_ACCENT}; border: 2px solid {config.COLOR_ACCENT}; border-radius: 6px;")
        self.btn_load.clicked.connect(self.select_pdf)
        self.btn_load.setEnabled(False)
        top_layout.addWidget(self.btn_load)
        main_layout.addWidget(top_panel)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        main_layout.addWidget(self.progress)

        self.thinking_viz = ThinkingVisualizer()
        self.thinking_viz.setVisible(False)
        main_layout.addWidget(self.thinking_viz)

        self.audio_viz = SpeakingVisualizer()
        self.audio_viz.setVisible(False)
        main_layout.addWidget(self.audio_viz)

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        main_layout.addWidget(self.chat_area)

        bottom_panel = QFrame()
        bottom_layout = QHBoxLayout(bottom_panel)
        bottom_panel.setStyleSheet(f"background-color: {config.COLOR_PANEL}; padding: 12px;")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Sorunuzu yazın...")
        self.input_field.returnPressed.connect(self.send_query)
        bottom_layout.addWidget(self.input_field)
        self.btn_stop = QPushButton("DURDUR")
        self.btn_stop.setFixedWidth(100)
        self.btn_stop.setStyleSheet("background-color: #FF5722; border: 2px solid #FF5722;")
        self.btn_stop.clicked.connect(self.stop_speaking)
        self.btn_stop.setVisible(False)
        bottom_layout.addWidget(self.btn_stop)
        self.btn_send = QPushButton("GÖNDER")
        self.btn_send.setFixedWidth(100)
        self.btn_send.clicked.connect(self.send_query)
        bottom_layout.addWidget(self.btn_send)
        main_layout.addWidget(bottom_panel)

    def init_system(self):
        self.lbl_status.setText("AI Yükleniyor...")
        QApplication.processEvents()
        try:
            self.rag_system = RAGSystem()
            self.lbl_status.setText("Hazır")
            self.btn_load.setEnabled(True)
            self.add_log("SİSTEM", "RAG aktif. PDF yükleyin.")
        except Exception as e:
            self.lbl_status.setText("Hata")
            self.add_log("HATA", str(e))

    def add_log(self, sender, message):
        color = "#888888"
        if sender == "SEN":
            color = config.COLOR_USER_MSG
        elif sender == "ASİSTAN":
            color = config.COLOR_AI_MSG
        elif sender == "HATA":
            color = config.COLOR_ERROR
        html = f"<div style='margin-bottom: 12px;'><b style='color: {color};'>{sender}:</b><br><span style='color: #E0E0E0;'>{message}</span></div>"
        self.chat_area.append(html)
        sb = self.chat_area.verticalScrollBar()
        sb.setValue(sb.maximum())

    def select_pdf(self):
        fname, _ = QFileDialog.getOpenFileName(self, "PDF Seç", "", "PDF Files (*.pdf)")
        if fname:
            self.lbl_status.setText(f"İşleniyor: {os.path.basename(fname)}")
            self.btn_load.setEnabled(False)
            self.btn_send.setEnabled(False)
            self.loader_thread = LoadPDFWorker(self.rag_system, fname)
            self.loader_thread.progress.connect(self.progress.setValue)
            self.loader_thread.finished.connect(self.on_pdf_loaded)
            self.loader_thread.error.connect(lambda e: self.add_log("HATA", e))
            self.loader_thread.start()

    def on_pdf_loaded(self, chunk_count):
        self.progress.setValue(100)
        self.lbl_status.setText("PDF Hazır")
        self.btn_load.setEnabled(True)
        self.btn_send.setEnabled(True)
        self.add_log("SİSTEM", f"PDF yüklendi. {chunk_count} parça.")
        QTimer.singleShot(2000, lambda: self.progress.setValue(0))

    def send_query(self):
        text = self.input_field.text().strip()
        if not text:
            return
        self.input_field.clear()
        self.add_log("SEN", text)
        self.start_thinking_mode(text)

    def start_thinking_mode(self, question, mode="rag"):
        self.input_field.setEnabled(False)
        self.btn_send.setEnabled(False)
        self.btn_send.setText("DÜŞÜNÜYOR...")
        self.audio_viz.setVisible(False)
        self.thinking_viz.setVisible(True)
        self.thinking_viz.start_animation()
        self.worker = QueryWorker(self.rag_system, question, mode)
        self.worker.result.connect(lambda r: self.on_query_result(r, question))
        self.worker.start()

    def on_query_result(self, result, original_question):
        if result == "###ASK_FALLBACK###":
            self.thinking_viz.stop_animation()
            dialog = StyledMessageBox(
                self, 
                "Bilgi Bulunamadı",
                "PDF içinde bu bilgi bulunamadı.\n\nGenel bilgi havuzundan araştırılsın mı?"
            )
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.start_thinking_mode(original_question, mode="general")
                return
            else:
                self.add_log("SİSTEM", "Arama iptal edildi.")
                self.reset_ui()
        else:
            self.add_log("ASİSTAN", result)
            self.thinking_viz.stop_animation()
            self.thinking_viz.setVisible(False)
            if self.tts_enabled and not result.startswith("Hata"):
                self.start_tts(result)
            else:
                self.reset_ui()

    def start_tts(self, text):
        self.lbl_status.setText("Ses oluşturuluyor...")
        self.btn_send.setText("SES...")
        self.tts_worker = TTSWorker(text)
        self.tts_worker.finished.connect(self.play_audio)
        self.tts_worker.error.connect(self.on_tts_error)
        self.tts_worker.start()

    def play_audio(self, file_path):
        self.current_audio_file = file_path
        self.lbl_status.setText("Konuşuyor...")
        self.thinking_viz.setVisible(False)
        self.audio_viz.set_audio_data(file_path)
        self.audio_viz.setVisible(True)
        self.audio_viz.start()
        self.btn_send.setVisible(False)
        self.btn_stop.setVisible(True)
        self.media_player.setSource(QUrl.fromLocalFile(file_path))
        self.media_player.play()

    def stop_speaking(self):
        self.media_player.stop()

    def on_playback_state_changed(self, state):
        if state == QMediaPlayer.PlaybackState.StoppedState:
            self.audio_viz.stop()
            self.audio_viz.setVisible(False)
            self.btn_stop.setVisible(False)
            self.btn_send.setVisible(True)
            self.lbl_status.setText("PDF Hazır")
            self.reset_ui()
            if self.current_audio_file and os.path.exists(self.current_audio_file):
                try:
                    os.remove(self.current_audio_file)
                except:
                    pass
                self.current_audio_file = None

    def on_tts_error(self, error):
        self.add_log("HATA", f"TTS: {error}")
        self.thinking_viz.stop_animation()
        self.thinking_viz.setVisible(False)
        self.audio_viz.stop()
        self.reset_ui()

    def reset_ui(self):
        self.input_field.setEnabled(True)
        self.btn_send.setEnabled(True)
        self.btn_send.setVisible(True)
        self.btn_stop.setVisible(False)
        self.btn_send.setText("GÖNDER")
        self.input_field.setFocus()

    def check_updates(self):
        self.update_checker = check_for_updates(self, GITHUB_REPO, silent=False)

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
