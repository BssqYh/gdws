from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QFrame, QSizePolicy
from PySide6.QtCore import Qt, Signal


class ButtonArea(QFrame):

    button_clicked = Signal(dict)  # 按钮点击信号

    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("background-color: #f5f5f5; border: 1px solid #e0e0e0;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setFixedHeight(70)  # 固定高度

        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(20)

        # 默认按钮
        self.add_button("确定", "#4caf50")
        self.add_button("取消", "#f44336")
        self.add_button("帮助", "#2196f3")

    def add_button(self, text, color=None):
        """添加按钮"""
        btn = QPushButton(text)
        btn.setFixedSize(100, 40)

        style = f"""
            QPushButton {{
                background-color: {color or '#9e9e9e'};
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {'#66bb6a' if color == '#4caf50' else
        '#ef5350' if color == '#f44336' else
        '#42a5f5' if color == '#2196f3' else '#bdbdbd'};
            }}
        """
        btn.setStyleSheet(style)
        btn.clicked.connect(self.on_button_clicked)
        self.layout.addWidget(btn)
        return btn

    def on_button_clicked(self):
        btn = self.sender()
        text = btn.text()
        """按钮点击处理"""
        # 取消其他按钮的选中状态
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, QPushButton) and widget.text() != text:
                widget.setChecked(False)

        item={}
        item["按钮名称"] = text
        item["menuItem"] = btn.property("menuItem")
        print(f"<UNK>{item}<UNK>")
        self.button_clicked.emit(item)

    def set_content(self, widgets):
        """设置按钮区域内容"""
        # 清除现有内容
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 添加新内容
        for widget in widgets:
            if isinstance(widget, QWidget):
                self.layout.addWidget(widget)
            elif isinstance(widget, tuple) and len(widget) >= 1:
                text = widget[0]
                color = widget[1] if len(widget) > 1 else None
                self.add_button(text, color)