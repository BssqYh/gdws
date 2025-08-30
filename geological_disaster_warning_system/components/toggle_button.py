import logging

from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, Signal

logging.basicConfig(format='%(levelname)s:[%(filename)s:%(lineno)d]:%(funcName)s:%(message)s', level=logging.DEBUG)
class ToggleButton(QPushButton):
    state_changed = Signal(str,bool)  # 更通用的状态变化信号,2个参数，1：当前组件名称 2.是是否选择
    def __init__(self, name =None,parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedSize(60, 30)
        self.toggled.connect(self.animate_thumb)
        self._thumb_position = 3
        self.animation = QPropertyAnimation(self, b"thumb_position")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.OutBounce)
        self.animation.finished.connect(self.on_animation_finished)
        # 初始样式
        self.setStyleSheet("""
            QPushButton {
                background-color: #bbbbbb;
                border-radius: 15px;
                border: none;
            }
        """)
        if name:
            self.name = name

    def animate_thumb(self):
        # 停止当前动画（如果有的话）
        if hasattr(self, 'animation'):
            self.animation.stop()

        if self.isChecked():
            start = 3
            end = 33
        else:
            start = 33
            end = 3

        logging.info(f"<UNK>{self._thumb_position}<UNK>{start}<UNK>{end}<UNK>")
        self.animation.setStartValue(start)
        self.animation.setEndValue(end)
        self.animation.start()

        # 此时 isChecked() 已经是最新的状态
        color = "#4ade80" if self.isChecked() else "#bbbbbb"
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 15px;
                border: none;
            }}
        """)
    def paintEvent(self, event):
        super().paintEvent(event)
        # 绘制圆形滑块
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor("#ffffff"))
        painter.drawEllipse(self._thumb_position, 3, 24, 24)

    def thumb_position(self):
        return self._thumb_position

    def set_thumb_position(self, pos):
        self._thumb_position = pos
        self.update()

    def on_animation_finished(self):
        self.state_changed.emit(self.name,self.isChecked())
    thumb_position = Property(int, thumb_position, set_thumb_position)