from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt
import config

class StyledMessageBox(QDialog):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {config.COLOR_BG};
                border: 1px solid {config.COLOR_BORDER};
            }}
            QLabel {{
                color: {config.COLOR_TEXT};
                font-size: 14px;
                padding: 10px;
            }}
            QPushButton {{
                background-color: {config.COLOR_ACCENT};
                color: white;
                border: none;
                padding: 10px 25px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {config.COLOR_ACCENT_HOVER};
            }}
            QPushButton#noBtn {{
                background-color: {config.COLOR_PANEL};
                color: {config.COLOR_TEXT_DIM};
                border: 1px solid {config.COLOR_BORDER};
            }}
            QPushButton#noBtn:hover {{
                background-color: {config.COLOR_BORDER};
                color: {config.COLOR_TEXT};
            }}
        """)

        # Kaldır: setWindowFlags(Qt.WindowType.FramelessWindowHint) - Pencereler için standart başlık çubuğu kalsın

        layout = QVBoxLayout(self)
        layout.setSpacing(25)
        layout.setContentsMargins(30, 30, 30, 30)

        # Başlık
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"color: {config.COLOR_TEXT}; font-weight: bold; font-size: 16px; border: none;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_lbl)

        # Mesaj
        msg_label = QLabel(message)
        msg_label.setWordWrap(True)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_label.setStyleSheet(f"color: {config.COLOR_TEXT_DIM}; font-size: 14px; border: none;")
        layout.addWidget(msg_label)

        # Butonlar
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        self.no_btn = QPushButton("Hayır")
        self.no_btn.setObjectName("noBtn")
        self.no_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.yes_btn = QPushButton("Evet")
        self.yes_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.yes_btn.clicked.connect(self.accept)
        self.no_btn.clicked.connect(self.reject)

        btn_layout.addStretch()
        btn_layout.addWidget(self.no_btn)
        btn_layout.addWidget(self.yes_btn)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)
