# components/survey_card.py（新增卡片组件）
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPixmap


class SurveyCard(QWidget):
    clicked = Signal(str)  # 信号携带调查表名称

    def __init__(self, title, image_path):
        super().__init__()
        self.title = title
        self.image_path = image_path
        self._setup_ui()
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(200, 220)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # 缩略图
        self.image_label = QLabel()
        pixmap = QPixmap(self.image_path).scaled(180, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(pixmap)
        layout.addWidget(self.image_label)

        # 标题
        title_label = QLabel(self.title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 14px; margin-top: 8px;")
        layout.addWidget(title_label)

    def mousePressEvent(self, event):
        self.clicked.emit(self.title)
        super().mousePressEvent(event)