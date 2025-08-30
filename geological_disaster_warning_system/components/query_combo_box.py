from PySide6.QtWidgets import QWidget, QFormLayout, QLabel, QComboBox
from PySide6.QtCore import Qt

class QueryComboBox(QWidget):
    def __init__(self, label_text, data, display_key, value_key=None, parent=None):
        """"""
        """
        :param label_text: 标签文字，如 "线路选择"
        :param data: 数据列表，如 [{'线别名称': '兰青线', '线别ID': 2}, ...]
        :param display_key: 显示字段名，如 '线别名称' 或 '里程K'
        :param value_key: 值字段名，如 '线别ID'，若不传则使用 display_key 的值作为 value
        :param parent: 父控件
        """
        super().__init__(parent)

        self.text = label_text
        self.display_key = display_key
        self.value_key = value_key if value_key is not None else display_key
        self.data = data

        self.combo_box = QComboBox()
        # 添加选项
        for item in self.data:
            display_text = item[display_key]
            value = item[value_key] if value_key in item else display_text
            self.combo_box.addItem(display_text, userData=value)
        self.combo_box.setCurrentIndex(-1)

        # 创建布局
        form_layout = QFormLayout(self)
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.addRow(QLabel(label_text), self.combo_box)

        # 暴露 comboBox 的 currentIndexChanged 信号
        self.combo_box.currentIndexChanged.connect(self._on_index_changed)

    def _on_index_changed(self, index):
        # 可以在这里做一些统一处理，也可以不实现
        pass

    def get_text(self):
        return self.text
    def current_display_name(self):
        return self.display_key

    def current_id(self):
        """获取当前选中的线别ID"""
        return self.combo_box.currentData()

    def current_value(self):
        """获取当前选中的线别名称"""
        return self.combo_box.currentText()

    @property
    def currentIndexChanged(self):
        """"""
        """外部监听使用"""
        return self.combo_box.currentIndexChanged