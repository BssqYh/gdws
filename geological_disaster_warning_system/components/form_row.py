# form_row.py
import logging
import math

from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QMessageBox, \
    QSizePolicy
from PySide6.QtCore import Qt, QTimer

from components.chinese_message_box import ChineseMessageBox

"""
使用方法：
from form_row import create_form_row
layout = QFormLayout()
label = QLabel(key)
line_edit = QLineEdit(str(value))
line_edit.setReadOnly(True)
wrapped = create_form_row(label, line_edit, row_index)
layout.addRow(wrapped)
"""

import re


def do_adjust(label1):
    # 设置自动换行
    label1.setWordWrap(True)
    label1.setFixedWidth(190)  # 固定宽度

    # 强制重新布局
    label1.adjustSize()

    # 如果需要额外的空间，可以添加一些 padding
    current_height = label1.height()
    label1.setFixedHeight(current_height + 10)
def do_adjust1(label1):
    font_metrics = label1.fontMetrics()
    text_value = label1.text()
    text_width = font_metrics.horizontalAdvance(text_value)
    text_height = font_metrics.height()
    available_width = 190
    height_index = math.ceil(text_width / available_width)
    lines = height_index + 1
    logging.info(f"text_value={text_value}--text_width={text_width}--height_index = {height_index} ---{lines}<UNK>")
    label1.setFixedHeight(lines * text_height)

def create_form_row(label: QLabel, widget, row_index: int, validator_rule=None):
    """"""
    """
    创建一个带样式的表单行，包含 label + 控件，并应用隔行背景色和边框
    :param label: QLabel 标签
    :param widget: 控件（QLineEdit/QSpinBox/QDoubleSpinBox 等）
    :param row_index: 行号，用于隔行变色
    :param validator_rule: 可选的校验规则，可以是：
                           - 正则表达式字符串（如 r'^\\d+$'）
                           - 校验函数（接受值并返回 True/False）
    :return: QWidget 容器
    """

    # 设置标签固定宽度（如果未设置）
    if label.minimumWidth() == 0:
        label.setFixedWidth(100)


    label.setStyleSheet("""
        font-weight: bold;
        font-size: 14px;
        padding: 4px 0;
        background: transparent;
    """)

    # 创建主容器
    row_container = QWidget()
    row_layout = QHBoxLayout()
    row_layout.setContentsMargins(8, 4, 8, 4)
    row_layout.setSpacing(10)

    # 关键设置：开启自动换行并设置最大宽度
    label.setWordWrap(True)  # 启用自动换行
    label.setMaximumWidth(200)  # 控制自动换行点

    if widget is not None:
        # 根据文本长度调整尺寸策略
        QTimer.singleShot(0, lambda: do_adjust(label))
    else:
        label.setFixedWidth(500)

    # 添加 label 和 控件
    # row_layout.addWidget(label, alignment=Qt.AlignLeft | Qt.AlignVCenter)
    row_layout.addWidget(label, 3,alignment=Qt.AlignVCenter)
    if widget is not None:
        row_layout.addWidget(widget, 7)

    row_container.setLayout(row_layout)

    # 设置样式（隔行变色 + 边框）
    if row_index % 2 == 0:
        bg_color = "#f9f9f9"
    else:
        bg_color = "#eef6ff"

    row_container.setStyleSheet(f"""
        background-color: {bg_color};
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 4px;
    """)
    if widget is None:
        return row_container
    # 保存原始值
    original_value = None

    if isinstance(widget, (QLineEdit, QSpinBox, QDoubleSpinBox)):
        if validator_rule is not None:
            if isinstance(validator_rule, str):
                pattern = re.compile(validator_rule)

                def validate_regex(val):
                    return bool(pattern.match(str(val)))

                def on_edit():
                    if not validate_regex(get_current_value()):
                        show_error_and_reset()

                def get_current_value():
                    if isinstance(widget, QLineEdit):
                        return widget.text()
                    elif isinstance(widget, QSpinBox):
                        return str(widget.value())
                    elif isinstance(widget, QDoubleSpinBox):
                        return str(widget.value())

                def show_error_and_reset():
                    ChineseMessageBox.show_message("输入错误", "输入不符合格式要求!", button0="知道了")
                    original_value = widget.property("original_value") or ""
                    if isinstance(widget, QLineEdit):
                        widget.setText(original_value)
                    elif isinstance(widget, QSpinBox):
                        widget.setValue(original_value)
                    elif isinstance(widget, QDoubleSpinBox):
                        widget.setValue(original_value)

            else:
                # 假设是函数
                def on_edit():
                    current_val = None
                    if isinstance(widget, QLineEdit):
                        current_val = widget.text()
                    elif isinstance(widget, QSpinBox):
                        current_val = widget.value()
                    elif isinstance(widget, QDoubleSpinBox):
                        current_val = widget.value()

                    if not validator_rule(current_val):
                        QMessageBox.warning(row_container, "输入错误", "输入不符合要求，请重新输入！")
                        if isinstance(widget, QLineEdit):
                            widget.setText(original_value)
                        elif isinstance(widget, QSpinBox):
                            widget.setValue(original_value)
                        elif isinstance(widget, QDoubleSpinBox):
                            widget.setValue(original_value)

            # 绑定信号
            if isinstance(widget, QLineEdit):
                widget.editingFinished.connect(on_edit)
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                widget.editingFinished.connect(on_edit)

    return row_container