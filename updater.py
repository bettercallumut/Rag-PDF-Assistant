import os
import json
import requests
import shutil
import tempfile
import zipfile
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QProgressBar, QTextEdit)
from PyQt6.QtCore import QThread, pyqtSignal, Qt

GITHUB_REPO = "bettercallumut/Rag-PDF-Assistant"
CURRENT_VERSION = "1.0.0"
VERSION_FILE = "version.json"

class UpdateChecker(QThread):
    update_available = pyqtSignal(str, str)
    no_update = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, repo):
        super().__init__()
        self.repo = repo
    
    def run(self):
        try:
            url = f"https://api.github.com/repos/{self.repo}/releases/latest"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                latest_version = data.get("tag_name", "").lstrip("v")
                download_url = data.get("zipball_url", "")
                if latest_version and self.is_newer(latest_version, CURRENT_VERSION):
                    self.update_available.emit(latest_version, download_url)
                else:
                    self.no_update.emit()
            elif response.status_code == 404:
                url = f"https://api.github.com/repos/{self.repo}/commits/main"
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    latest_sha = data.get("sha", "")[:7]
                    download_url = f"https://github.com/{self.repo}/archive/refs/heads/main.zip"
                    local_version = self.get_local_version()
                    if latest_sha != local_version:
                        self.update_available.emit(latest_sha, download_url)
                    else:
                        self.no_update.emit()
                else:
                    self.error.emit("Repo bulunamadı")
            else:
                self.error.emit(f"GitHub API hatası: {response.status_code}")
        except Exception as e:
            self.error.emit(str(e))
    
    def is_newer(self, latest, current):
        try:
            latest_parts = [int(x) for x in latest.split(".")]
            current_parts = [int(x) for x in current.split(".")]
            return latest_parts > current_parts
        except:
            return latest != current
    
    def get_local_version(self):
        try:
            if os.path.exists(VERSION_FILE):
                with open(VERSION_FILE, "r") as f:
                    data = json.load(f)
                    return data.get("commit", "")
        except:
            pass
        return ""

class UpdateDownloader(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, url, version):
        super().__init__()
        self.url = url
        self.version = version
    
    def run(self):
        try:
            response = requests.get(self.url, stream=True, timeout=60)
            total_size = int(response.headers.get('content-length', 0))
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    temp_file.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        self.progress.emit(int(downloaded / total_size * 100))
            temp_file.close()
            self.finished.emit(temp_file.name)
        except Exception as e:
            self.error.emit(str(e))

class UpdateDialog(QDialog):
    def __init__(self, parent, current_version, new_version, download_url):
        super().__init__(parent)
        self.setWindowTitle("Güncelleme Mevcut")
        self.setModal(True)
        self.setMinimumWidth(450)
        self.download_url = download_url
        self.new_version = new_version
        self.setStyleSheet("""
            QDialog { background-color: #1E1E1E; }
            QLabel { color: #E0E0E0; font-size: 13px; }
            QTextEdit { 
                background-color: #2A2A2A; 
                color: #E0E0E0; 
                border: 1px solid #444; 
                border-radius: 4px;
                font-size: 12px;
            }
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
            QPushButton#cancelBtn { background-color: #444; color: #E0E0E0; }
            QPushButton#cancelBtn:hover { background-color: #555; }
            QProgressBar {
                border: none;
                background-color: #333;
                height: 8px;
                border-radius: 4px;
            }
            QProgressBar::chunk { background-color: #00CED1; border-radius: 4px; }
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)
        title = QLabel(f"Yeni sürüm mevcut!")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #00CED1;")
        layout.addWidget(title)
        version_info = QLabel(f"Mevcut: {current_version}\nYeni: {new_version}")
        layout.addWidget(version_info)
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMaximumHeight(100)
        self.log_area.setVisible(False)
        layout.addWidget(self.log_area)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        self.status_label = QLabel("")
        self.status_label.setVisible(False)
        layout.addWidget(self.status_label)
        btn_layout = QHBoxLayout()
        self.update_btn = QPushButton("Güncelle")
        self.update_btn.clicked.connect(self.start_update)
        self.cancel_btn = QPushButton("Sonra")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
    
    def log(self, message):
        self.log_area.append(message)
    
    def start_update(self):
        self.update_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.status_label.setVisible(True)
        self.log_area.setVisible(True)
        self.status_label.setText("İndiriliyor...")
        self.log("Güncelleme indiriliyor...")
        self.downloader = UpdateDownloader(self.download_url, self.new_version)
        self.downloader.progress.connect(self.progress_bar.setValue)
        self.downloader.finished.connect(self.on_download_complete)
        self.downloader.error.connect(self.on_error)
        self.downloader.start()
    
    def on_download_complete(self, zip_path):
        self.log("İndirme tamamlandı. Dosyalar çıkarılıyor...")
        self.status_label.setText("Güncelleniyor...")
        try:
            app_dir = os.path.dirname(os.path.abspath(__file__))
            backup_dir = os.path.join(app_dir, "_backup")
            if os.path.exists(backup_dir):
                shutil.rmtree(backup_dir)
            os.makedirs(backup_dir)
            files_to_update = [
                "main.py", "config.py", "rag_system.py", "workers.py",
                "visualizer.py", "audio_visualizer.py", "dialogs.py",
                "text_processor.py", "updater.py", "requirements.txt"
            ]
            for f in files_to_update:
                src = os.path.join(app_dir, f)
                if os.path.exists(src):
                    shutil.copy2(src, os.path.join(backup_dir, f))
            self.log("Yedekleme tamamlandı.")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                temp_extract = tempfile.mkdtemp()
                zip_ref.extractall(temp_extract)
                extracted_dirs = os.listdir(temp_extract)
                if extracted_dirs:
                    source_dir = os.path.join(temp_extract, extracted_dirs[0])
                    for f in files_to_update:
                        src_file = os.path.join(source_dir, f)
                        if os.path.exists(src_file):
                            dst_file = os.path.join(app_dir, f)
                            shutil.copy2(src_file, dst_file)
                            self.log(f"Güncellendi: {f}")
                    shutil.rmtree(temp_extract)
            os.remove(zip_path)
            version_data = {"version": self.new_version, "commit": self.new_version}
            with open(os.path.join(app_dir, VERSION_FILE), "w") as f:
                json.dump(version_data, f)
            self.log("Güncelleme tamamlandı!")
            self.status_label.setText("Güncelleme tamamlandı! Uygulamayı yeniden başlatın.")
            self.status_label.setStyleSheet("color: #00E676;")
            self.cancel_btn.setText("Kapat")
            self.cancel_btn.setEnabled(True)
        except Exception as e:
            self.on_error(f"Güncelleme hatası: {e}")
    
    def on_error(self, error):
        self.log(f"Hata: {error}")
        self.status_label.setText(f"Hata: {error}")
        self.status_label.setStyleSheet("color: #FF5252;")
        self.cancel_btn.setEnabled(True)
        self.cancel_btn.setText("Kapat")

def check_for_updates(parent, repo, silent=False):
    checker = UpdateChecker(repo)
    
    def on_update_available(new_version, download_url):
        dialog = UpdateDialog(parent, CURRENT_VERSION, new_version, download_url)
        dialog.exec()
    
    def on_no_update():
        if not silent:
            from dialogs import StyledMessageBox
            msg = QDialog(parent)
            msg.setWindowTitle("Güncelleme")
            msg.setStyleSheet("QDialog { background-color: #1E1E1E; } QLabel { color: #E0E0E0; }")
            layout = QVBoxLayout(msg)
            layout.addWidget(QLabel("Uygulama güncel."))
            btn = QPushButton("Tamam")
            btn.clicked.connect(msg.accept)
            layout.addWidget(btn)
            msg.exec()
    
    def on_error(error):
        if not silent:
            print(f"Güncelleme kontrolü hatası: {error}")
    
    checker.update_available.connect(on_update_available)
    checker.no_update.connect(on_no_update)
    checker.error.connect(on_error)
    checker.start()
    return checker
