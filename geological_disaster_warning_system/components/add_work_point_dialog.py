import logging

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea, QWidget
from PySide6.QtCore import Qt, Signal

from components.dynamic_form_widget import DynamicFormWidget


class WorkPointInfoDialog(QDialog):

    submitted = Signal(dict)
    canceled = Signal()
    add_work_info_value_changed = Signal(str,str, str)

    def __init__(self, menu_data,parent=None, title="增加工点信息"):
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
        self.form_widget.value_changed.connect(
            lambda dynamic_form_name, dynamic_component_name, val: self._dynamic_form_value_change(dynamic_form_name,
                                                                                                   dynamic_component_name,
                                                                                                   val))
        self.form_layout.addWidget(self.form_widget)

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        self.error_label = QLabel("")
        self.error_label.setWordWrap(True)  # 允许自动换行
        self.error_label.setStyleSheet("color: red; font-size: 13px; padding: 8px;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setVisible(False)
        main_layout.addWidget(self.error_label)  # 独立添加到主布局

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

    def _dynamic_form_value_change(self, dynamic_form_name,dynamic_component_name, val):
        #TODO
        """"""
        """注意：这里是根据具体的表来使用不同的计算方法。这里不能通用。而且如果某一天某个结构改了名字
        那么这边也要对应更新"""
        logging.info(f"{dynamic_form_name}, {dynamic_component_name}, {val}")
        self.add_work_info_value_changed.emit(dynamic_form_name, dynamic_component_name, val)

    def on_save_clicked(self):
        self.form_data = self.form_widget.get_values()
        data = self.get_form_data()
        error_fields = []
        for key, value in data.items():
            """因为工点ID是自动生成，不可编辑"""
            if key !="工点ID":
                if not value and value != 0:  # 更严谨判断空值（排除 0）
                    error_fields.append(key)

        if error_fields:
            error_text = "、".join(error_fields) + " 不能为空"
            self.error_label.setText(error_text)
            self.error_label.setVisible(True)
            return
        self.error_label.setVisible(False)
        self.submitted.emit(self.form_data)
        self.accept()

    def on_cancel_clicked(self):
        self.canceled.emit()
        self.reject()

    def get_form_data(self):
        return self.form_data

    def set_form_data_and_readonly(self, data):
        self.form_widget.set_values_and_readonly(data)

    def set_form_data_by_name(self, name,data):
        self.form_widget.set_combox_values_by_name(name,data)

    def set_form_data(self, data):
        self.form_widget.set_values(data)

    def show_dialog(self):
        result = self.exec_()
        if result == QDialog.Accepted:
            return self.get_form_data()
        return None