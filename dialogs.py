from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QMessageBox
from PyQt6.QtCore import Qt
import config

class StyledMessageBox(QDialog):
    class StandardButton:
        Yes = 1
        No = 2
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.setMinimumWidth(400)
        self.result_button = None
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
        
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(25)
        self.layout.setContentsMargins(30, 30, 30, 30)
        
        self.title_lbl = QLabel()
        self.title_lbl.setStyleSheet(f"color: {config.COLOR_TEXT}; font-weight: bold; font-size: 16px; border: none;")
        self.title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.msg_label = QLabel()
        self.msg_label.setWordWrap(True)
        self.msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msg_label.setStyleSheet(f"color: {config.COLOR_TEXT_DIM}; font-size: 14px; border: none;")
        
        self.info_label = QLabel()
        self.info_label.setWordWrap(True)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet(f"color: {config.COLOR_TEXT_DIM}; font-size: 12px; border: none;")
        
        self.btn_layout = QHBoxLayout()
        self.btn_layout.setSpacing(15)
        
        self.no_btn = QPushButton("Hayır")
        self.no_btn.setObjectName("noBtn")
        self.no_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.no_btn.clicked.connect(lambda: self.button_clicked(self.StandardButton.No))
        
        self.yes_btn = QPushButton("Evet")
        self.yes_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.yes_btn.clicked.connect(lambda: self.button_clicked(self.StandardButton.Yes))
        
    def setText(self, text):
        self.msg_label.setText(text)
        
    def setInformativeText(self, text):
        self.info_label.setText(text)
        
    def setStandardButtons(self, buttons):
        pass
        
    def setDefaultButton(self, button):
        pass
        
    def button_clicked(self, button):
        self.result_button = button
        if button == self.StandardButton.Yes:
            self.accept()
        else:
            self.reject()
    
    def exec(self):
        self.layout.addWidget(self.title_lbl)
        self.layout.addWidget(self.msg_label)
        if self.info_label.text():
            self.layout.addWidget(self.info_label)
        
        self.btn_layout.addStretch()
        self.btn_layout.addWidget(self.no_btn)
        self.btn_layout.addWidget(self.yes_btn)
        self.btn_layout.addStretch()
        
        self.layout.addLayout(self.btn_layout)
        
        super().exec()
        return self.result_button

