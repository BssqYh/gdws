import json
import logging
import math
import sys

from PIL.Image import alpha_composite
from PIL.ImageQt import qt_version
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QStyledItemDelegate, \
    QLabel, QLineEdit, QFrame, QFormLayout, QHBoxLayout, QSizePolicy, QSpinBox, QMessageBox
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QColor, QPainter, QRegularExpressionValidator

from components.dynamic_form_widget import DynamicFormWidget
from components.form_row import create_form_row
from components.help_icon_label import HelpIconLabel
from components.pearson_III_module import PearsonIIIModule
from utils.utils import MyUtils

logging.basicConfig(format='%(levelname)s:[%(filename)s:%(lineno)d]:%(funcName)s:%(message)s', level=logging.DEBUG)

"""
铁路水文勘探规范
"""
class BorderColorDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter: QPainter, option, index):
        # 获取背景色
        bg_color = index.data(Qt.BackgroundRole)

        # 设置背景颜色
        if bg_color:
            painter.fillRect(option.rect, bg_color)

        # 绘制文本
        text = index.data(Qt.DisplayRole)
        if text is not None:
            painter.drawText(option.rect, Qt.AlignCenter, text)

        # 绘制边框
        pen = painter.pen()
        pen.setColor(Qt.GlobalColor.gray)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRect(option.rect)

class CalcHydrologicalSurveySpecificationsView(QWidget):
    def __init__(self, model=None,data=None, parent=None):
        super().__init__(parent)
        self.name = "铁路水文勘探规范"
        self.setStyleSheet("font-size: 20px;")
        self.data = data or []
        self.column_labels = []  # 列头（时间维度）
        self.row_names = []      # 行名（非“降雨参数”的 name 字段）
        self.background_colors = [  # 每一行的背景色
            QColor("#f9f9f9"),
            QColor("#eef6ff"),
            QColor("#f9f9f9"),
            QColor("#eef6ff"),
            QColor("#f9f9f9")
        ]
        self.model = model
        logging.info(f"{data}")
        self.need_checked_data = {}
        self.frame = QFrame()
        # layout = QFormLayout()
        # layout.setSpacing(5)  # 控件之间的间距
        # layout.setContentsMargins(20, 20, 20, 20)  # 边距
        self.form_layout = QFormLayout(self.frame)
        self.form_layout.setSpacing(15)
        self.value_widget = {}
        self.init_ui()

    def _on_numer_input_changed(self,name,widget):
        wtype = type(widget).__name__
        if wtype == "QComboBox":
            value = widget.currentText()
        elif wtype == "QLineEdit":
            value = widget.text()
        elif wtype == "QTextEdit":
            value = widget.toPlainText()
        elif wtype == "QSpinBox":
            value = widget.text()
        else:
            value = None
        pass
    def _calc_chan_liu_yin_zi_k1(self,dynamic_form_name):
        tmp_widget = self.value_widget[dynamic_form_name]
        tmp_value = tmp_widget.get_values()
        hui_shui_f = float(tmp_value['汇水面积'])
        sp_50_value = float(tmp_value['五十年一遇Sp(mm/h)'])
        sp_100_value = float(tmp_value['百年一遇sp(mm/h)'])
        η_value = float(tmp_value['η值'])
        val_float = float(η_value)
        k1_50 = 0.278 * val_float * sp_50_value * hui_shui_f
        k1_100 = 0.278 * val_float * sp_100_value * hui_shui_f
        k1_50 = round(k1_50, 4)
        k1_100 = round(k1_100, 4)
        tmp_widget.set_value_by_name("五十年一遇产流因子K1", k1_50)
        tmp_widget.set_value_by_name("百年一遇产流因子K1", k1_100)

    def _calc_sun_shi_yin_zi_k2(self,dynamic_form_name):
        tmp_widget1 = self.value_widget["产流因子k1"]
        """只有产流因子k1才有五十年一遇sp"""
        can_liu_data = tmp_widget1.get_values()
        sp_50_value = float(can_liu_data['五十年一遇Sp(mm/h)'])
        sp_100_value = float(can_liu_data['百年一遇sp(mm/h)'])
        η_value = float(can_liu_data['η值'])

        tmp_widget = self.value_widget[dynamic_form_name]
        tmp_value = tmp_widget.get_values()
        string_sun_shi_zhi_shu_R = tmp_value['损失指数R']
        string_sun_shi_zhi_shu_r1 = tmp_value['损失指数r1']
        if string_sun_shi_zhi_shu_R =="" or string_sun_shi_zhi_shu_R == '' or string_sun_shi_zhi_shu_R ==None or string_sun_shi_zhi_shu_r1 =="" or string_sun_shi_zhi_shu_r1 == '' or string_sun_shi_zhi_shu_r1 == None:
            return
        """这里为什么不能使用安全的方法获取呢？因为安全的获取会有一个默认值，无论这个默认值是多少，其实都不应该继续。
        因此这里没有使用安全方法"""
        sun_shi_zhi_shu_R = float(string_sun_shi_zhi_shu_R)
        sun_shi_zhi_shu_r1 = float(string_sun_shi_zhi_shu_r1)

        k2_50 = sun_shi_zhi_shu_R*((η_value*sp_50_value)**(sun_shi_zhi_shu_r1-1))
        k2_100 = sun_shi_zhi_shu_R*((η_value*sp_100_value)**(sun_shi_zhi_shu_r1-1))
        k2_50 = round(k2_50, 4)
        k2_100 = round(k2_100, 4)
        tmp_widget.set_value_by_name("五十年一遇损失因子k2", k2_50)
        tmp_widget.set_value_by_name("百年年一遇损失因子k2", k2_100)
    def _dynamic_form_value_change(self, dynamic_form_name,dynamic_component_name, val):
        #TODO
        """"""
        """注意：这里是根据具体的表来使用不同的计算方法。这里不能通用。而且如果某一天某个结构改了名字
        那么这边也要对应更新"""
        logging.info(f"{dynamic_form_name}, {dynamic_component_name}, {val}")
        if dynamic_form_name=="产流因子k1" and dynamic_component_name=="η值":
            self._calc_chan_liu_yin_zi_k1(dynamic_form_name)
        if dynamic_form_name == "损失因子k2":
            self._calc_sun_shi_yin_zi_k2(dynamic_form_name)
    def init_ui(self):
        row_index = 0
        for item in self.data:
            logging.info(f"{item}")
            name = item["name"]
            label = QLabel(name)
            widget = None
            tmp_type = item["type"]
            if tmp_type == "有子表":
                if self.model is None:
                    logging.error("没有数据模型，无法处理有子表的选项。")
                    continue
                table_value = json.loads(item["value"])
                for key, value in table_value.items():
                    # value 是子表的ID
                    data,table_name = self.model.get_sub_menu_content(value)
                    logging.info(f"<UNK>{table_name} data: {data}")
                    widget = DynamicFormWidget(data, table_name)
                    self.value_widget[table_name] = widget
                    widget.value_changed.connect(lambda dynamic_form_name,dynamic_component_name, val: self._dynamic_form_value_change(dynamic_form_name,dynamic_component_name, val))
                    self.form_layout.addRow(widget)
                continue
            elif tmp_type == "Number":
                h_widget = QWidget()
                h_layout = QHBoxLayout(h_widget)
                h_layout.setContentsMargins(0, 0, 0, 0)
                h_layout.setSpacing(5)

                edit = QLineEdit()
                h_layout.addWidget(edit)
                value_range =item["value"]
                need_help = item["need_help"]
                unit = item["unit"]
                if value_range:
                    regx_text = MyUtils.generate_input_regex(json.loads(value_range))
                    regx = QRegularExpression(regx_text)
                    validator = QRegularExpressionValidator(regx)
                    edit.setValidator(validator)
                if unit != "NULL":
                    unit_label = QLabel(unit)
                    h_layout.addWidget(unit_label)
                if need_help == 1:
                    help_text = f"点击获取{name}详细信息"
                    help_label = HelpIconLabel(help_text, name, parent=self)
                    h_layout.addWidget(help_label)
                self.value_widget[name] = edit
                edit.editingFinished.connect(lambda e=edit, n=name: self._on_numer_input_changed(n, e))
                validator_rule =r'^\d+$'
                widget = create_form_row(label, h_widget,row_index,validator_rule =validator_rule)
            elif tmp_type == "QLabel":
                display_label = QLabel()
                self.value_widget[name] = display_label
                widget = create_form_row(label, display_label,row_index)
                tmp_value = item["value"]
                if tmp_value :
                    tmp_value1 = MyUtils._generate_need_checked_data(tmp_value)
                    if tmp_value1 :
                        for key, value in tmp_value1.items():
                            for k, v in value.items():
                                if k not in self.need_checked_data:
                                    self.need_checked_data[k] = []
                                self.need_checked_data[k].append(v)
            row_index += 1
            if widget:
                self.form_layout.addRow(widget)
        # self.frame.setLayout(self.form_layout)
        self.setLayout(self.form_layout)

    def get_all_values(self):
        result = {}
        for key, widget in self.value_widget.items():
            class_name = widget.__class__.__name__
            if class_name == "DynamicFormWidget":
                data = widget.get_values()
                for key, value in data.items():
                    result[key] = value
            else:
                wtype = type(widget).__name__
                if wtype == "QComboBox":
                    value = widget.currentText()
                elif wtype == "QLineEdit":
                    value = widget.text()
                elif wtype == "QTextEdit":
                    value = widget.toPlainText()
                elif wtype == "QSpinBox":
                    value = widget.text()
                elif wtype == "QLabel":
                    value = widget.text()
                else:
                    value = None
                result[key] = value
        return result

    def set_values(self, values_dict):
        """
        根据已有组件的名称设置值
        :param values_dict: 包含组件名称和对应值的字典
        """
        if not values_dict:
            return

        for key, widget in self.value_widget.items():
            class_name = widget.__class__.__name__
            if class_name == "DynamicFormWidget":
                widget.set_values(values_dict)
            else:
                if key in values_dict:
                    widget_type = type(widget).__name__
                    value = values_dict[key]
                    if value is None:
                        continue
                    if widget_type == "QLineEdit":
                        widget.setText(str(value))
                    elif widget_type == "QComboBox":
                        # 查找匹配的索引
                        index = widget.findText(str(value))
                        if index >= 0:
                            widget.setCurrentIndex(index)
                    elif widget_type == "QSpinBox":
                        widget.setValue(int(value))
                    elif widget_type == "QTextEdit":
                        widget.setPlainText(str(value))
                    elif widget_type == "QLabel":
                        widget.setText(str(value))
                    else:
                        logging.warning(f"不支持的组件类型: {widget_type} for component: {key}")

    def get_need_checked_data(self):
        result = {}
        for key, widget in self.value_widget.items():
            class_name = widget.__class__.__name__
            if class_name == "DynamicFormWidget":
                tmp_need_checked_data = widget.get_need_checked_data()
                for key, value in tmp_need_checked_data.items():
                    if key in result:
                        if isinstance(result[key], list):
                            for tmp_check_data in value:
                                if tmp_check_data in result[key]:
                                    continue
                                else:
                                    result[key].append(tmp_check_data)
                    else:
                        result[key] = value

        for key, value in self.need_checked_data.items():
            result[key] = value
        return result

    def get_name(self):
        return self.name