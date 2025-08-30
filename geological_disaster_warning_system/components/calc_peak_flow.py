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
计算洪峰流量Qp
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

class CalcPeakFlowView(QWidget):
    def __init__(self, model=None,data=None, parent=None):
        super().__init__(parent)
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
        self.name = "计算洪峰流量Qp"
        self.model = model
        logging.info(f"{data}")
        self.frame = QFrame()
        # layout = QFormLayout()
        # layout.setSpacing(5)  # 控件之间的间距
        # layout.setContentsMargins(20, 20, 20, 20)  # 边距
        self.form_layout = QFormLayout(self.frame)
        self.form_layout.setSpacing(15)
        self.value_widget = {}
        """当未来计算方法发生改变的时候，
        第一步:检查init_ui 中有子表的地方，名称是否发生改变。
        因为t1，t2的具体值也是直接从数据库中获取的。
        只需要更改
        _calc_t1
        _calc_t2
        _calc_overland_flow
        为什么这里要更改：
        因为_calc_t1、_calc_t2等中，获取具体字段无法从数据库里面获取。
        总之，这样至少改动会少很多。
        """
        self.t1={ }
        self.t2={ }
        self.overland_flow_data ={ }
        self.init_ui()

    def _calc_t1(self):
        m1_str = self.t1.get('地表粗度系数m1', '').strip()
        Ls_str = self.t1.get('坡面流的长度Ls', '').strip()
        is_str = self.t1.get('坡面流的坡度is', '').strip()
        # 判断是否都存在且非空
        if not all([m1_str, Ls_str, is_str]):
            logging.warning("参数不完整，无法计算 t1")
            return

        try:
            m1 = float(m1_str)
            Ls = float(Ls_str)
            is_slope = float(is_str)

            if is_slope <= 0:
                QMessageBox.warning(
                    self,  # 父窗口
                    "输入错误",  # 标题
                    "坡度必须大于0，请检查输入值！",  # 提示内容
                    QMessageBox.Ok  # 按钮
                )
                return

            # 执行公式计算
            numerator = m1 * Ls
            denominator = math.sqrt(is_slope)
            t1_value = 1.445 * (numerator / denominator) ** 0.467
            rain_t1 = round(t1_value, 2)
            self.t1['坡面汇流历时T1'] = rain_t1
            logging.info(f"t1 计算结果: {self.t1}")

            tmp_widget = self.value_widget['坡面汇流历时T1']
            tmp_widget.set_value_by_name("坡面汇流历时T1",rain_t1)
            tmp_widget = self.value_widget['降雨历时']
            self.overland_flow_data['降雨历时'] = rain_t1
            tmp_widget.setText(str(rain_t1))

        except ValueError as e:
            logging.error(f"数值转换失败: {e}")

    def _calc_t2(self):
        logging.info(self.t2)
        long_str = self.t2.get('第i段水沟长度(m)', '').strip()
        speed_str = self.t2.get('第i段沟平均流速(m/s)', '').strip()
        if not all([long_str, speed_str]):
            logging.warning("参数不完整，无法计算 t2")
            return
        try:
            i_long = float(long_str)
            i_speed = float(speed_str)

            re_speed = 20*i_speed**0.6

            if re_speed <= 0:
                QMessageBox.warning(
                    self,  # 父窗口
                    "输入错误",  # 标题
                    "速度必须大于0，请检查输入值！",  # 提示内容
                    QMessageBox.Ok)  # 按钮
                return

            # 执行公式计算
            numerator = i_long / re_speed /60
            rain_t2 = round(numerator, 2)
            self.t2['沟内汇流历时T2'] = rain_t2
            logging.info(f"t1 计算结果: {self.t2}")
            tmp_widget = self.value_widget['沟内汇流历时T2']
            tmp_widget.set_value_by_name("沟内汇流历时T2",rain_t2)
        except ValueError as e:
            logging.error(f"数值转换失败: {e}")
        pass
    def _calc_overland_flow(self):
        logging.info(self.overland_flow_data)
        Cp_value = self.overland_flow_data.get('重现期转换系数Cp', '').strip()
        Ct_value = self.overland_flow_data.get('降雨历时转换系数Ct', '').strip()
        I5_10_value = self.overland_flow_data.get('I₅,₁₀', '').strip()
        rain_value = self.overland_flow_data.get('降雨历时', '')
        if rain_value == '':
            QMessageBox.warning(
                self,
                "错误",
                "请首先输入降雨历时参数，计算降雨时间！",
                QMessageBox.Ok)
        if not all([Cp_value, Ct_value, I5_10_value]):
            logging.warning("参数不完整，无法计算平均降雨强度")
            return
        try:
            Cp_float = float(Cp_value)
            Ct_float = float(Ct_value)
            I5_10_float = float(I5_10_value)
            rain_float = float(rain_value)
            Ct_re = -1*Ct_float * math.log(rain_float) + 1.7515
            logging.info(f"<UNK>: {Cp_float}*{Ct_re}*{I5_10_float}")
            p_float = Cp_float * Ct_re * I5_10_float
            p_float = round(p_float, 2)
            self.overland_flow_data['平均降雨强度'] = p_float
            tmp_widget = self.value_widget['平均降雨强度']
            tmp_widget.setText(str(p_float))
        except ValueError as e:
            QMessageBox.warning(
                self,
                "输入错误",
                "平均降雨强度计算错误，请检查输入重现期转换系数Cp、降雨历时转换系数Ct、I₅,₁₀！",
                QMessageBox.Ok)
        pinyin_chong_xian_qi_value = self.overland_flow_data.get('重现期', '').strip()
        pinyin_jin_liu_xi_shu_value = self.overland_flow_data.get('地表径流系数', '').strip()
        area_value = self.overland_flow_data.get('汇水面积', '').strip()
        if not all([pinyin_chong_xian_qi_value, pinyin_jin_liu_xi_shu_value, area_value, rain_value]):
            logging.warning("参数不完整，无法计算 t2")
            return
        rain_value = self.overland_flow_data.get('平均降雨强度', '')
        if rain_value == '':
            QMessageBox.warning(
                self,
                "错误",
                "请先输入入重现期转换系数Cp、降雨历时转换系数Ct、I₅,₁₀，计算平均降雨强度！",
                QMessageBox.Ok)
            return
        try:
            pinyin_jin_liu_xi_shu_float = float(pinyin_jin_liu_xi_shu_value)
            area_float = float(area_value)
            rain_float = float(rain_value)
            re_jing_liu_liu_liang  =  i=16.67 * pinyin_jin_liu_xi_shu_float * area_float * rain_float * 1.1
            re_jing_liu_liu_liang = round(re_jing_liu_liu_liang, 4)
            self.overland_flow_data['设计径流量'] = re_jing_liu_liu_liang
            tmp_widget = self.value_widget['设计径流量']
            tmp_widget.setText(str(re_jing_liu_liu_liang))
        except ValueError as e:
            QMessageBox.warning(
                self,
                "输入错误",
                "平均降雨强度计算错误，请检查输入重现期转换系数Cp、降雨历时转换系数Ct、I₅,₁₀！",
                QMessageBox.Ok)
        pass
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
        self.overland_flow_data[name] = value
        self._calc_overland_flow()
        pass
    def _dynamic_form_value_change(self, dynamic_form_name,dynamic_component_name, val):
        if dynamic_form_name =="坡面汇流历时T1":
            self.t1[dynamic_component_name] = val
            self._calc_t1()
        elif dynamic_form_name == "沟内汇流历时T2":
            self.t2[dynamic_component_name] = val
            self._calc_t2()
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
                    if table_name == "坡面汇流历时T1":
                        self.t1 = {item['name']: '' for item in self.data}
                    elif table_name == "沟内汇流历时T2":
                        self.t2 = {item['name']: '' for item in self.data}
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
                self.overland_flow_data[name]=''
                validator_rule =r'^\d+$'
                widget = create_form_row(label, h_widget,row_index,validator_rule =validator_rule)
            elif tmp_type == "QLabel":
                display_label = QLabel()
                self.value_widget[name] = display_label
                self.overland_flow_data[name] = ''
                widget = create_form_row(label, display_label,row_index)
            row_index += 1
            if widget:
                self.form_layout.addRow(widget)
        # self.frame.setLayout(self.form_layout)
        self.setLayout(self.form_layout)

    def get_all_values(self):
        result = {}
        for key,widget in self.value_widget.items():
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
                elif wtype == "Qlable":
                    value = widget.text()
                else:
                    value = None
                result[key] = value
        return result



    def get_name(self):
        return self.name