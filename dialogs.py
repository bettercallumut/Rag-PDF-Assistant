from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class StyledMessageBox(QDialog):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setStyleSheet("""
            QDialog {
                background-color: #1E1E1E;
                border: 2px solid #00CED1;
                border-radius: 10px;
            }
            QLabel {
                color: #E0E0E0;
                font-size: 14px;
                padding: 10px;
            }
            QPushButton {
                background-color: #00CED1;
                color: #121212;
                border: none;
                padding: 12px 30px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #20B2AA;
            }
            QPushButton#noBtn {
                background-color: #444;
                color: #E0E0E0;
            }
            QPushButton#noBtn:hover {
                background-color: #555;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)
        msg_label = QLabel(message)
        msg_label.setWordWrap(True)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(msg_label)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        self.yes_btn = QPushButton("Evet, Ara")
        self.no_btn = QPushButton("Hayır")
        self.no_btn.setObjectName("noBtn")
        self.yes_btn.clicked.connect(self.accept)
        self.no_btn.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(self.yes_btn)
        btn_layout.addWidget(self.no_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
