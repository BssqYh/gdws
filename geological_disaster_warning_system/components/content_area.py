from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QTextEdit, QSizePolicy, QScrollArea
from PySide6.QtCore import Qt


class ContentArea(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("background-color: #fffde7; border: 1px solid #fff9c4;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 主布局
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        # 创建一个滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # 内容部件可自动调整大小
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # 创建一个用于放置内容的容器部件
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setAlignment(Qt.AlignTop)

        # 默认内容
        title = QLabel("内容区域")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #5d4037;")
        title.setAlignment(Qt.AlignCenter)

        self.content_layout.addWidget(title)
        self.content_layout.addWidget(QLabel("在此添加您的内容组件"))

        # 将内容容器放入滚动区域
        self.scroll_area.setWidget(self.content_container)

        # 将滚动区域加入主布局
        self.layout.addWidget(self.scroll_area)

    def set_content(self, widgets):
        """设置内容区域内容"""
        # 清除现有内容
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # 内容部件可自动调整大小
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # 创建一个用于放置内容的容器部件
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setAlignment(Qt.AlignTop)

        # 添加新内容
        for widget in widgets:
            if isinstance(widget, QWidget):
                self.content_layout.addWidget(widget)

        self.scroll_area.setWidget(self.content_container)
        # 将滚动区域加入主布局
        self.layout.addWidget(self.scroll_area)