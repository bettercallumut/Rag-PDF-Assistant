import os
import sys
import json
import requests
import shutil
import tempfile
import zipfile
import subprocess
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QProgressBar, QTextEdit)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
import config

GITHUB_REPO = "bettercallumut/Rag-PDF-Assistant"
CURRENT_VERSION = "1.0.0"
VERSION_FILE = "version.json"

class UpdateChecker(QThread):
    update_available = pyqtSignal(str, str, bool) # version, url, is_exe
    no_update = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, repo):
        super().__init__()
        self.repo = repo
    
    def run(self):
        try:
            # Sadece Releases kontrol edelim, çünkü EXE dağıtımı hedefliyoruz.
            url = f"https://api.github.com/repos/{self.repo}/releases/latest"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                latest_version = data.get("tag_name", "").lstrip("v")
                assets = data.get("assets", [])

                # EXE var mı kontrol et
                exe_url = None
                for asset in assets:
                    if asset.get("name", "").endswith(".exe") or asset.get("name", "").endswith(".zip"):
                         exe_url = asset.get("browser_download_url")
                         break

                # Yedek olarak kaynak kod zip'i
                if not exe_url:
                    exe_url = data.get("zipball_url", "")

                if latest_version and self.is_newer(latest_version, CURRENT_VERSION):
                    self.update_available.emit(latest_version, exe_url, True)
                else:
                    self.no_update.emit()
            elif response.status_code == 404:
                # Geliştirme ortamı için commit kontrolü (opsiyonel, release yoksa)
                url = f"https://api.github.com/repos/{self.repo}/commits/main"
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    latest_sha = data.get("sha", "")[:7]
                    download_url = f"https://github.com/{self.repo}/archive/refs/heads/main.zip"
                    local_version = self.get_local_version()

                    if latest_sha != local_version:
                        self.update_available.emit(latest_sha, download_url, False) # False = exe değil, kaynak kod
                    else:
                        self.no_update.emit()
                else:
                    self.error.emit("Repo bulunamadı veya erişilemiyor.")
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
    
    def __init__(self, url):
        super().__init__()
        self.url = url
    
    def run(self):
        try:
            response = requests.get(self.url, stream=True, timeout=120)
            total_size = int(response.headers.get('content-length', 0))

            # Uzantıyı belirle
            ext = ".zip"
            if self.url.lower().endswith(".exe"):
                ext = ".exe"

            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
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
    def __init__(self, parent, current_version, new_version, download_url, is_exe_update):
        super().__init__(parent)
        self.setWindowTitle("Güncelleme Mevcut")
        self.setModal(True)
        self.setMinimumWidth(450)
        self.download_url = download_url
        self.new_version = new_version
        self.is_exe_update = is_exe_update
        self.setStyleSheet(f"""
            QDialog {{ background-color: {config.COLOR_BG}; border: 1px solid {config.COLOR_BORDER}; }}
            QLabel {{ color: {config.COLOR_TEXT}; font-size: 13px; }}
            QTextEdit {{
                background-color: {config.COLOR_INPUT_BG};
                color: {config.COLOR_TEXT};
                border: 1px solid {config.COLOR_BORDER};
                border-radius: 4px;
                font-size: 12px;
            }}
            QPushButton {{
                background-color: {config.COLOR_ACCENT};
                color: white;
                border: none;
                padding: 10px 25px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {config.COLOR_ACCENT_HOVER}; }}
            QPushButton:disabled {{ background-color: {config.COLOR_PANEL}; color: {config.COLOR_TEXT_DIM}; }}
            QPushButton#cancelBtn {{ background-color: {config.COLOR_PANEL}; color: {config.COLOR_TEXT_DIM}; border: 1px solid {config.COLOR_BORDER}; }}
            QPushButton#cancelBtn:hover {{ background-color: {config.COLOR_BORDER}; color: {config.COLOR_TEXT}; }}
            QProgressBar {{
                border: none;
                background-color: {config.COLOR_PANEL};
                height: 6px;
                border-radius: 3px;
            }}
            QProgressBar::chunk {{ background-color: {config.COLOR_ACCENT}; border-radius: 3px; }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)

        title = QLabel(f"Yeni Sürüm Mevcut!")
        title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {config.COLOR_ACCENT};")
        layout.addWidget(title)

        version_info = QLabel(f"Mevcut Sürüm: {current_version}\nYeni Sürüm: {new_version}")
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
        self.update_btn = QPushButton("Şimdi Güncelle")
        self.update_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_btn.clicked.connect(self.start_update)

        self.cancel_btn = QPushButton("Daha Sonra")
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.clicked.connect(self.reject)

        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.update_btn)
        layout.addLayout(btn_layout)
    
    def log(self, message):
        self.log_area.append(message)
    
    def start_update(self):
        self.update_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.status_label.setVisible(True)
        self.log_area.setVisible(True)

        self.status_label.setText("İndirme başlatılıyor...")
        self.log("Güncelleme paketi indiriliyor...")

        self.downloader = UpdateDownloader(self.download_url)
        self.downloader.progress.connect(self.progress_bar.setValue)
        self.downloader.finished.connect(self.on_download_complete)
        self.downloader.error.connect(self.on_error)
        self.downloader.start()
    
    def on_download_complete(self, file_path):
        self.log("İndirme tamamlandı.")
        self.status_label.setText("Kuruluma hazırlanıyor...")

        try:
            if getattr(sys, 'frozen', False) and self.is_exe_update:
                # EXE Modu
                self.handle_exe_update(file_path)
            else:
                # Kaynak Kod Modu (Geliştirme)
                self.handle_source_update(file_path)

        except Exception as e:
            self.on_error(f"Güncelleme uygulama hatası: {e}")

    def handle_exe_update(self, downloaded_file):
        """EXE güncellemesi için bat dosyası oluşturur ve çalıştırır."""
        self.log("Çalıştırılabilir dosya güncelleniyor...")

        # Eğer indirilen dosya zip ise, içindeki exe'yi çıkar
        target_exe = downloaded_file
        if downloaded_file.endswith(".zip"):
             with zipfile.ZipFile(downloaded_file, 'r') as zip_ref:
                temp_dir = tempfile.mkdtemp()
                zip_ref.extractall(temp_dir)
                # Zip içinde exe ara
                found_exe = False
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith(".exe"):
                            target_exe = os.path.join(root, file)
                            found_exe = True
                            break
                    if found_exe: break

                if not found_exe:
                    self.on_error("İndirilen pakette .exe dosyası bulunamadı.")
                    return

        current_exe = sys.executable
        exe_dir = os.path.dirname(current_exe)
        exe_name = os.path.basename(current_exe)
        new_exe_path = os.path.join(exe_dir, f"{exe_name}.new")

        # Yeni exe'yi geçici isimle taşı
        shutil.move(target_exe, new_exe_path)

        # Bat dosyası oluştur
        bat_path = os.path.join(exe_dir, "_update.bat")
        with open(bat_path, "w") as bat:
            bat.write(f"""
@echo off
timeout /t 2 /nobreak > NUL
del "{exe_name}"
rename "{os.path.basename(new_exe_path)}" "{exe_name}"
start "" "{exe_name}"
del "%~f0"
            """)

        self.log("Uygulama yeniden başlatılıyor...")
        self.status_label.setText("Yeniden başlatılıyor...")

        # Bat dosyasını çalıştır ve çık
        subprocess.Popen([bat_path], shell=True)
        sys.exit(0)

    def handle_source_update(self, zip_path):
        """Geliştirme ortamı için kaynak kod güncellemesi."""
        self.log("Kaynak kodları güncelleniyor...")
        app_dir = os.path.dirname(os.path.abspath(__file__))

        # Yedekle
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

        # Version güncelle
        version_data = {"version": self.new_version, "commit": self.new_version}
        with open(os.path.join(app_dir, VERSION_FILE), "w") as f:
            json.dump(version_data, f)

        self.log("Güncelleme tamamlandı!")
        self.status_label.setText("Tamamlandı! Uygulamayı yeniden başlatın.")
        self.status_label.setStyleSheet(f"color: {config.COLOR_AI_MSG};")
        self.cancel_btn.setText("Kapat")
        self.cancel_btn.setEnabled(True)
    
    def on_error(self, error):
        self.log(f"Hata: {error}")
        self.status_label.setText(f"Hata oluştu!")
        self.status_label.setStyleSheet(f"color: {config.COLOR_ERROR};")
        self.cancel_btn.setEnabled(True)
        self.cancel_btn.setText("Kapat")

def check_for_updates(parent, repo, silent=False):
    checker = UpdateChecker(repo)
    
    def on_update_available(new_version, download_url, is_exe):
        dialog = UpdateDialog(parent, CURRENT_VERSION, new_version, download_url, is_exe)
        dialog.exec()
    
    def on_no_update():
        if not silent:
            msg = QDialog(parent)
            msg.setWindowTitle("Güncelleme")
            msg.setMinimumWidth(300)
            msg.setStyleSheet(f"""
                QDialog {{ background-color: {config.COLOR_BG}; border: 1px solid {config.COLOR_BORDER}; }}
                QLabel {{ color: {config.COLOR_TEXT}; margin: 10px; }}
                QPushButton {{
                    background-color: {config.COLOR_ACCENT};
                    color: white;
                    border: none;
                    padding: 8px 20px;
                    border-radius: 6px;
                }}
            """)
            layout = QVBoxLayout(msg)
            layout.addWidget(QLabel("Uygulamanız güncel."))
            btn = QPushButton("Tamam")
            btn.clicked.connect(msg.accept)
            layout.addWidget(btn)
            msg.exec()
    
    def on_error(error):
        if not silent:
            # Hataları loglayabiliriz ama kullanıcıyı her seferinde rahatsız etmeyelim
            print(f"Update Check Error: {error}")
    
    checker.update_available.connect(on_update_available)
    checker.no_update.connect(on_no_update)
    checker.error.connect(on_error)
    checker.start()
    return checker
