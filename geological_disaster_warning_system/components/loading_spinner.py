# loading_spinner.py
import logging

from PySide6.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QMovie
import sys

from utils.utils import MyUtils

"""
加载动画，模拟类
使用方法：
 spinner = LoadingSpinner.instance()
 spinner.start_animate("正在保存数据，请稍候...")  可以不提供参数，默认正在保存数据
 
如果有需要：设置父窗口
 spinner.set_parent_and_center(self)

 
 保存完数据过后，使用
spinner = LoadingSpinner.instance()
spinner.stop_animate()
"""
class LoadingSpinner(QDialog):
    _instance = None  # 强引用，不会被回收

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()  # 创建一次，永久持有
            cls._instance.setModal(True)
            cls._instance.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
            cls._instance.setAttribute(Qt.WA_TranslucentBackground)
        return cls._instance

    def __init__(self):
        # 注意：这里 super 必须只调用一次
        if LoadingSpinner._instance is not None:
            raise RuntimeError("Use LoadingSpinner.instance() instead of direct instantiation!")
        super().__init__()

        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet("""
            background-color: rgba(255, 255, 255, 220);
            border-radius: 10px;
            border: 1px solid #ddd;
        """)

        layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMinimumSize(80, 80)

        self.text_label = QLabel("正在保存...")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet("font-size: 14px; color: #333;")

        layout.addWidget(self.label)
        layout.addWidget(self.text_label)
        self.setLayout(layout)
        self.resize(160, 160)

        self.movie = QMovie(":/resources/loading.gif")  # 替换为你的路径
        if not self.movie.isValid():
            logging.error("❌ 动画文件无效，请检查路径")
            # 可以用纯色圆圈代替
            self.label.setStyleSheet("background: lightgray; border-radius: 40px;")
        else:
            self.movie.frameChanged.connect(self._on_frame_changed)
            self.label.setMovie(self.movie)

    def _on_frame_changed(self, frame):
        """当 GIF 帧变化时，自动缩放并设置到 label"""
        pixmap = self.movie.currentPixmap()
        scaled_pixmap = pixmap.scaled(
            self.label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.label.setPixmap(scaled_pixmap)

    def set_parent_and_center(self, parent):
        """
        手动设置父窗口，并居中显示
        :param parent: QWidget，通常是你当前的主窗口或页面
        """
        self.move(
            parent.x() + (parent.width() - self.width()) // 2,
            parent.y() + (parent.height() - self.height()) // 2
        )

    def start_animate(self, message="正在保存..."):
        self.text_label.setText(message)
        self.movie.start()
        self.show()

    def stop_animate(self):
        self.movie.stop()
        self.hide()