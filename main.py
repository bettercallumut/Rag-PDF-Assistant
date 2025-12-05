import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
                             QLabel, QProgressBar, QFileDialog, QFrame, QCheckBox,
                             QDialog, QDialogButtonBox)
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

import config
from rag_system import RAGSystem
from workers import LoadPDFWorker, QueryWorker, TTSWorker
from visualizer import ThinkingVisualizer
from audio_visualizer import SpeakingVisualizer
from dialogs import StyledMessageBox

class ApiKeyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Neural Core - API Girişi")
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
        self.setWindowTitle("Neural Core AI")
        self.resize(1000, 800)
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

        # Global Stylesheet
        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {config.COLOR_BG}; }}
            QWidget {{ font-family: 'Segoe UI', sans-serif; font-size: 14px; color: {config.COLOR_TEXT}; }}

            /* Scrollbar Styling */
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

        # --- Top Header ---
        top_panel = QFrame()
        top_panel.setStyleSheet(f"background-color: {config.COLOR_PANEL}; border-bottom: 1px solid {config.COLOR_BORDER};")
        top_panel.setFixedHeight(60)
        top_layout = QHBoxLayout(top_panel)
        top_layout.setContentsMargins(20, 0, 20, 0)

        app_title = QLabel("Neural Core")
        app_title.setStyleSheet(f"font-weight: bold; font-size: 16px; color: {config.COLOR_TEXT};")
        top_layout.addWidget(app_title)

        self.lbl_status = QLabel("Başlatılıyor...")
        self.lbl_status.setStyleSheet(f"color: {config.COLOR_TEXT_DIM}; margin-left: 10px;")
        top_layout.addWidget(self.lbl_status)

        top_layout.addStretch()

        self.tts_checkbox = QCheckBox("Sesli Yanıt")
        self.tts_checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        self.tts_checkbox.setChecked(True)
        self.tts_checkbox.stateChanged.connect(lambda s: setattr(self, 'tts_enabled', s == 2))
        top_layout.addWidget(self.tts_checkbox)

        self.btn_load = QPushButton("+ PDF Yükle")
        self.btn_load.setCursor(Qt.CursorShape.PointingHandCursor)
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

        # --- Progress Bar ---
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        main_layout.addWidget(self.progress)

        # --- Content Area ---
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

        # --- Bottom Input Area ---
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
        self.btn_stop.setStyleSheet(f"background-color: {config.COLOR_ERROR}; border: none;")
        self.btn_stop.clicked.connect(self.stop_speaking)
        self.btn_stop.setVisible(False)
        bottom_layout.addWidget(self.btn_stop)

        self.btn_send = QPushButton("GÖNDER")
        self.btn_send.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_send.setFixedWidth(100)
        self.btn_send.clicked.connect(self.send_query)
        bottom_layout.addWidget(self.btn_send)

        main_layout.addWidget(bottom_panel)

    def init_system(self):
        self.lbl_status.setText("Yükleniyor...")
        QApplication.processEvents()
        try:
            self.rag_system = RAGSystem()
            self.lbl_status.setText("Hazır")
            self.btn_load.setEnabled(True)
            self.add_log("SİSTEM", "Neural Core aktif. Sohbet etmek için bir PDF belgesi yükleyin.")
        except Exception as e:
            self.lbl_status.setText("Başlatma Hatası")
            self.add_log("HATA", f"Sistem başlatılamadı: {str(e)}")

    def add_log(self, sender, message):
        color = config.COLOR_TEXT_DIM
        bg_color = "transparent"
        align = "left"
        padding = "0px"
        border_radius = "0px"

        if sender == "SEN":
            color = config.COLOR_USER_MSG
            align = "right"
            # User messages could be styled differently if desired
        elif sender == "ASİSTAN":
            color = config.COLOR_AI_MSG
        elif sender == "HATA":
            color = config.COLOR_ERROR

        # Simple timestamp could be added here

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

            # Show processing message
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

    def start_thinking_mode(self, question, mode="rag"):
        self.input_field.setEnabled(False)
        self.btn_send.setEnabled(False)
        self.btn_send.setText("...")
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
                "PDF içinde bu konuyla ilgili net bir bilgi bulamadım.\n\nGenel bilgi tabanını kullanarak cevap vermemi ister misiniz?"
            )
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.start_thinking_mode(original_question, mode="general")
                return
            else:
                self.add_log("SİSTEM", "İşlem iptal edildi.")
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
        self.tts_worker = TTSWorker(text)
        self.tts_worker.finished.connect(self.play_audio)
        self.tts_worker.error.connect(self.on_tts_error)
        self.tts_worker.start()

    def play_audio(self, file_path):
        self.current_audio_file = file_path
        self.lbl_status.setText("Yanıtlanıyor...")
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
            self.lbl_status.setText("Hazır")
            self.reset_ui()
            if self.current_audio_file and os.path.exists(self.current_audio_file):
                try:
                    os.remove(self.current_audio_file)
                except:
                    pass
                self.current_audio_file = None

    def on_tts_error(self, error):
        self.add_log("HATA", f"Ses motoru hatası: {error}")
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
