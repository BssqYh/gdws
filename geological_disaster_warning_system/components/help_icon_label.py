# HelpIconLabel.py

from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QCursor
from PySide6.QtCore import Qt, QSize

from components.help_info_dialog import HelpInfoDialog
from utils.utils import MyUtils


class HelpIconLabel(QLabel):
    def __init__(self, tooltip_text: str, help_name: str,parent=None):
        super().__init__(parent)

        self.help_name = help_name

        # 加载并缩放图片
        pixmap = QPixmap(":/resources/help.png")
        scaled_pixmap = pixmap.scaled(
            QSize(32, 32),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.setPixmap(scaled_pixmap)

        # 设置提示信息
        self.setToolTip(tooltip_text)

        # 设置鼠标样式为手型
        self.setCursor(QCursor(Qt.PointingHandCursor))

        # 允许 QLabel 响应鼠标事件
        self.setAttribute(Qt.WA_Hover, True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._show_help_window(self.help_name)

    def _show_help_window(self, name):
        # 这里可以替换为你自己的逻辑
        print(f"帮助窗口已调用: {name}")
        help_dialog = HelpInfoDialog()
        help_dialog.set_data_source("dbtable",name)
        help_dialog.show()