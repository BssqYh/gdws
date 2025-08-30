from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea, QWidget
from PySide6.QtCore import Qt, Signal

from components.dynamic_form_widget import DynamicFormWidget


class DisasterPointInfoDialog(QDialog):
    submitted = Signal(dict)
    canceled = Signal()

    def __init__(self, menu_data,parent=None, title="增加风险点信息"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowModality(Qt.ApplicationModal)
        self.setMinimumSize(500, 400)
        self.form_data = None
        self.menu_data = menu_data
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 标题
        title_label = QLabel(self.windowTitle())
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 表单区域（使用滚动区域）
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.form_layout = QVBoxLayout(scroll_content)
        self.form_widget = DynamicFormWidget(self.menu_data)
        self.form_layout.addWidget(self.form_widget)

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        # 按钮区域（固定在底部）
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("保存")
        cancel_btn = QPushButton("取消")

        save_btn.clicked.connect(self.on_save_clicked)
        cancel_btn.clicked.connect(self.on_cancel_clicked)

        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        main_layout.addLayout(btn_layout)
    def on_save_clicked(self):
        self.form_data = self.form_widget.get_values()
        self.submitted.emit(self.form_data)
        self.accept()

    def on_cancel_clicked(self):
        self.canceled.emit()
        self.reject()

    def get_form_data(self):
        return self.form_data
    def set_form_data(self, data):
        self.form_widget.set_values_and_readonly(data)

    def show_dialog(self):
        result = self.exec_()
        if result == QDialog.Accepted:
            return self.get_form_data()
        return None