from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QSizePolicy, QScrollArea
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from components.flow_layou import FlowLayout


class ImageArea(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("background-color: #ffebee; border: 1px solid #ffcdd2;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        # 创建滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # 初始化一个容器用于放置图片和上传按钮
        self.content_container = QWidget()
        self.flow_layout = FlowLayout(self.content_container)
        self.flow_layout.setSpacing(10)

        self.scroll_area.setWidget(self.content_container)

        # 将滚动区域加入主布局
        self.layout.addWidget(self.scroll_area)

    def get_scroll_area(self):
        """供外部获取 scroll_area，方便操作"""
        return self.scroll_area

    def set_image(self, image_path):
        """设置图片"""
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaled(
                self.width(), self.height(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))

    def set_content(self, widget):
        """设置内容（接受单个组件）"""
        # 清除现有内容
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

            # 2. 重建内容容器和 flow layout
        self.content_container = QWidget()
        self.flow_layout = FlowLayout(self.content_container)
        self.flow_layout.setSpacing(10)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setWidget(self.content_container)

        # 如果传入的是一个单独的控件（如上传按钮），直接添加
        if isinstance(widget, QWidget):
            self.flow_layout.addWidget(widget)
        elif isinstance(widget, list):
            # 如果是列表，可能是多个 ImageItemWidget 和 uploader
            for w in widget:
                if isinstance(w, QWidget):
                    self.flow_layout.addWidget(w)

        self.layout.addWidget(self.scroll_area)