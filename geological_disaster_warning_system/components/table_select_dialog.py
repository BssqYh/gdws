from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QScrollArea, QWidget, QApplication
from PySide6.QtCore import Signal, Qt

class TableSelectDialog(QDialog):
    table_selected = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("请选择操作")
        self.resize(400, 300)  # 初始窗口大小设为较大值


        main_layout = QVBoxLayout(self)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # 内容自动适应滚动区域大小

        self.container = QWidget()
        self.button_layout = QVBoxLayout(self.container)
        self.button_layout.setAlignment(Qt.AlignTop)  # 按钮靠上对齐

        scroll_area.setWidget(self.container)

        main_layout.addWidget(scroll_area)

        self.buttons = []

    def add_button(self, button_name: str, table_name: str):
        btn = QPushButton(button_name)
        btn.clicked.connect(lambda _, n=button_name, tn=table_name: self.on_button_clicked(n, tn))
        btn.setStyleSheet("""
            QPushButton {
                background-color: #26c6da;
                border: none;
                border-radius: 6px;
                padding: 12px 16px;
                margin: 8px 5px;
                text-align: left;
                font-weight: bold;
                color: white;
                font-size: 14px;
                transition: background-color 0.3s;
            }
            QPushButton:hover {
                background-color: #0097a7;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            QPushButton:checked {
                background-color: #006064;
                border-left: 4px solid #004d40;
            }
            QPushButton::icon {
                margin-right: 8px;
            }
        """)
        self.button_layout.addWidget(btn)
        self.buttons.append(btn)

    def on_button_clicked(self, name, table_name: str):
        item = {
            "name": name,
            "db_name": table_name
        }
        self.table_selected.emit(item)
        self.accept()  # 关闭对话框

    def popup(self):
        return self.exec_()