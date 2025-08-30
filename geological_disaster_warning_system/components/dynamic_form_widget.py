import json
import logging
import math

from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QWidget, QFormLayout, QCheckBox, QComboBox, QLineEdit, QGridLayout, QLabel, QSizePolicy, QHBoxLayout, QTextEdit
)
from PySide6.QtCore import Qt, QTimer, Signal
from components.China_area_selector import ChinaAreaSelector
from components.form_row import create_form_row
from components.help_icon_label import HelpIconLabel
from components.toggle_button import ToggleButton
from utils.utils import MyUtils

"""
动态生成表单的组件：
使用方法：
传入结构体：
config = [
    {'id': 1, 'disaster_id': 1, 'name': '坡形', 'type': 'QCheckBox', 'unit': 'NULL',
     'value': '{1:"凸地形",2:"凹地形",3:"折线形",4:"直线形"}', 'need_help': 0},
    {'id': 2, 'disaster_id': 1, 'name': '地面坡度', 'type': 'Number', 'unit': '°', 'value': '', 'need_help': 0},
    {'id': 3, 'disaster_id': 1, 'name': '地面相对高差', 'type': 'Number', 'unit': '米', 'value': '', 'need_help': 0},
    {'id': 4, 'disaster_id': 1, 'name': '植被覆盖度', 'type': 'QComboBox', 'unit': 'NULL',
     'value': '{1:"低，坡面裸露",2:"中等，坡面局部裸露",3:"高"}', 'need_help': 0}
]


layout = QVBoxLayout(main_window)

# 创建动态表单组件
form_widget = DynamicFormWidget(config)
layout.addWidget(form_widget)


"""
class DynamicFormWidget(QWidget):
    """
    """
    """
    第一个参数：整个表格的名称
    第二个参数：组件的名称
    第三个参数：传递的值
    第四个参数：计算方法
    """
    value_changed = Signal(str,str, object,dict)
    def __init__(self, config_list,title="",parent=None,validator_func=None):
        super().__init__(parent)

        self.config_list = config_list
        """
        这两个字段的作用：
        1.配件信号进行数据传递，当组件内原始组件值发生改变的时候，发送信号
        2.两个字典：快速找到组件，进而设置组件的值。
         widgets ：存储每个字段对应的控件 {id: widget}
         name_to_id_map： 名称-ID映射，{name: id}
        """
        self.widgets = {}
        self.calc_func ={}#存储计算方法。
        self.name_to_id_map = {}  # 新增映射：{name: id}

        #外部的验证函数。
        self.validator_func = validator_func
        self.validator_widgets ={}

        #trogbutton相关数据
        self.toggle_data={}

        self.form_layout = QFormLayout(self)
        self.form_layout.setSpacing(15)
        # 新增：如果提供了标题，则先添加标题行
        if title:
            self.title = title
            title_label = QLabel(title)
            title_label.setAlignment(Qt.AlignLeft)
            title_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 8px;")
            self.form_layout.addRow(title_label)  # 添加标题行
        else:
            self.title = ""
        self._build_form()

    def _build_form(self):
        row_index = 0
        for item in self.config_list:
            field_id = item['id']
            name = item['name']
            field_type = item['type']
            unit = item['unit']
            value = item['value']
            need_help = item['need_help']

            self.name_to_id_map[name] = field_id

            label = QLabel(name)

            label.setStyleSheet("font-weight: bold;")
            label.setAlignment(Qt.AlignLeft|Qt.AlignCenter)
            # 关键设置：开启自动换行并设置最大宽度
            label.setWordWrap(True)  # 启用自动换行

            widget = None
            if field_type == 'QCheckBox':
                # 复选框组容器 - 使用网格布局实现横向排列并自动换行
                group_widget = QWidget()
                grid_layout = QGridLayout(group_widget)
                grid_layout.setContentsMargins(0, 0, 0, 0)

                # 配置每行显示的复选框数量
                max_columns = 4  # 每行最多显示4个复选框
                row, column = 0, 0

                options = eval(value)
                # 为每个选项创建复选框
                for index, value in options.items():
                    checkbox = QCheckBox(value)
                    checkbox.setStyleSheet("QCheckBox { font-size: 14px; }")
                    checkbox.setCheckable(True)
                    checkbox.clicked.connect(lambda _, cb=checkbox, n=name: self._on_checkbox_group_changed(n))
                    # checkbox.clicked.connect(self._on_value_changed)
                    # 添加复选框到网格布局
                    grid_layout.addWidget(checkbox, row, column)
                    # 更新位置
                    column += 1
                    if column >= max_columns:
                        column = 0
                        row += 1
                widget = create_form_row(label, group_widget, row_index)
                self.widgets[name] = {"widget": group_widget, "type": "QCheckBoxGroup","name": name}

            elif field_type == 'QComboBox':
                combo = QComboBox()
                try:
                    options = eval(value) if value else {}
                except Exception:
                    options = {}
                # 添加选项
                for key, value in options.items():
                    combo.addItem(value, key)
                if not options or not value:
                    combo.setEnabled(False)
                combo.currentIndexChanged.connect(lambda _, c=combo, n=name: self._on_combo_or_line_changed(n, c))
                self.widgets[name] = {"widget": combo, "type": "QComboBox","name": name}
                widget = create_form_row(label, combo, row_index)
            elif field_type == 'QTextEdit':
                text = QTextEdit()
                default = f"请输入{name}"
                font_metrics = text.fontMetrics()
                line_height = font_metrics.lineSpacing()
                # 设置默认显示 3 行的高度
                text.setFixedHeight(line_height * 3)
                text.setStyleSheet("font-weight: bold;")
                text.setPlaceholderText(default)
                text.textChanged.connect(lambda _, t=text, n=name: self._on_combo_or_line_changed(n, t))
                self.widgets[name] = {"widget": text, "type": "QTextEdit","name": name}
                widget = create_form_row(label, text, row_index)
            elif field_type == 'Number':
                # 创建水平布局容器
                h_widget = QWidget()
                h_layout = QHBoxLayout(h_widget)
                h_layout.setContentsMargins(0, 0, 0, 0)
                h_layout.setSpacing(5)
                # 数字输入框 - 设置固定宽度变窄
                edit = QLineEdit()
                edit.setPlaceholderText("请输入数值")
                edit.setFixedWidth(200)  # 设置固定宽度为100像素
                edit.editingFinished.connect(lambda e=edit, n=name: self._on_combo_or_line_changed(n, e))
                h_layout.addWidget(edit)
                self.widgets[name] = {"widget": edit, "type": "Number","name": name}
                # 添加单位
                unit = item["unit"]
                help_mark = item["need_help"]
                if unit != "NULL":
                    unit_label = QLabel(unit)
                    h_layout.addWidget(unit_label)
                else:
                    if help_mark == 0:
                        unit_label = QLabel("")
                        h_layout.addWidget(unit_label)
                if help_mark == 1:
                    help_text = f"点击获取{name}详细信息"
                    help_label = HelpIconLabel(help_text,name)
                    h_layout.addWidget(help_label)
                widget = create_form_row(label, h_widget, row_index)
            elif field_type == "QLabel":
                calc_func = item.get("计算方法")
                if calc_func is not None and calc_func != "":
                    label1 = QLabel(f"{name}计算方法")
                    label1.setStyleSheet("font-weight: bold;")
                    label1.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
                    label2 = QLabel(calc_func)
                    widget_calc = create_form_row(label1, label2, row_index)
                    row_index = row_index + 1
                    self.form_layout.addRow(widget_calc)
                    self.calc_func[name] = calc_func
                display_label = QLabel()
                widget = create_form_row(label, display_label,row_index)
                self.widgets[name] = {"widget": display_label, "type": "QLabel","name": name}
            elif field_type == "ToggleButton":
                h_widget = QWidget()
                h_layout = QHBoxLayout(h_widget)
                h_layout.setContentsMargins(0, 0, 0, 0)
                h_layout.setSpacing(5)
                toggle_button = ToggleButton(name=name)
                h_layout.addWidget(toggle_button)
                widget = create_form_row(label, h_widget,row_index)
                self.widgets[name] = {"widget": toggle_button, "type": "ToggleButton", "name": name}
                self.toggle_data[name] = value
                toggle_button.state_changed.connect(lambda toggle_name,isChecked: self._update_toggle_data(toggle_name, isChecked))
            elif field_type == "QLineEdit":
                line_edit = QLineEdit()
                if name == "工点ID":
                    line_edit.setReadOnly(True)
                validator_rule = None
                if name == '里程':
                    validator_rule = r'^\s*([a-zA-Z][a-zA-Z0-9]*)\s*([+-])\s*(\d+(\.\d+)?)\s*(?:~\s*([+-])\s*(\d+(\.\d+)?))?\s*$'
                widget = create_form_row(label, line_edit, row_index,validator_rule =validator_rule)
                self.widgets[name] = {"widget": line_edit, "type": "QLineEdit", "name": name}
            elif field_type == "ChinaAreaSelector":
                area_selectors = ChinaAreaSelector()
                widget = create_form_row(label, area_selectors, row_index)
                self.widgets[name] = {"widget": area_selectors, "type": "ChinaAreaSelector", "name": name}
            row_index += 1
            if widget:
                pre_conds = item.get("前置条件", {})
                if pre_conds:
                    self.validator_widgets[name] = pre_conds
                self.form_layout.addRow(widget)

    def _on_combo_or_line_changed(self, name, widget):
        wtype = type(widget).__name__
        if wtype == "QComboBox":
            value = widget.currentText()
        elif wtype == "QLineEdit":
            value = widget.text()
        elif wtype == "QTextEdit":
            value = widget.toPlainText()
        else:
            value = None
        if value is not None:
            self.value_changed.emit(self.title,name, value,self.calc_func)

    def _on_checkbox_group_changed(self, name):
        group_widget = self.widgets[name]["widget"]
        checked_items = [cb.text() for cb in group_widget.findChildren(QCheckBox) if cb.isChecked()]
        self.value_changed.emit(self.title,name, checked_items,self.calc_func)

    def set_value_by_name(self, component_name, value):
        """"""
        """
        根据组件名称设置值
        :param component_name: 字段名（name）
        :param value: 要设置的值
        """
        if value is None:
            return
        info = self.widgets.get(component_name)
        if not info:
            return

        widget = info["widget"]
        wtype = info["type"]

        if wtype == "QComboBox":
            index = widget.findText(str(value))
            if index >= 0:
                widget.setCurrentIndex(index)
        elif wtype in ["QLineEdit", "Number"]:
            widget.setText(str(value))
            if isinstance(widget, QLineEdit):
                widget.setProperty("original_value", str(value))
        elif wtype == "QTextEdit":
            widget.setText(str(value))
        elif wtype == "QCheckBoxGroup":
            for cb in widget.findChildren(QCheckBox):
                cb.setChecked(cb.text() in value)
        elif wtype == "QLabel":
            widget.setText(str(value))

    def get_name(self):
        return self.title
    def get_values(self):
        """获取当前所有字段的值"""
        result = {}
        for field_id, info in self.widgets.items():
            widget = info["widget"]
            wtype = info["type"]
            name = info["name"]
            if wtype == "QComboBox":
                # current_text = widget.currentText()
                #result[name] = current_text
                """与设置一样的道理，current_data 返回的是key"""
                current_data = widget.currentData()
                result[name] = current_data
            elif wtype == "QTextEdit":
                result[name] =widget.toPlainText()
            elif wtype == "QLineEdit":
                text = widget.text()
                result[name] = float(text) if text.replace('.', '', 1).isdigit() else text
            elif wtype == "QLabel":
                text = widget.text()
                if text == "":
                    result[name] = ""
                result[name] = text
            elif wtype == 'Number':
                text = widget.text()
                result[name] = text
            elif wtype == "QCheckBoxGroup":
                checked = []
                for cb in widget.findChildren(QCheckBox):
                    if cb.isChecked():
                        key = cb.text()
                        checked.append(key)
                result[name] = checked
            elif wtype == "ToggleButton":
                pass
            elif wtype == "ChinaAreaSelector":
                result['省'] =widget.get_province_name()
                result['市'] = widget.get_city_name()
                result['县'] = widget.get_area_name()
                result['乡'] = widget.get_town_name()


        return result
    def get_need_checked_data(self):
        return self.need_checked_data
    def set_values(self, values:dict):
        """"""
        """
        设置各个字段的值
        values: dict {id: value}
        """
        logging.info(f"<UNK>{values}")
        for field_id, info in self.widgets.items():
            if str(field_id) == "地区选择":
                logging.info(f"<UNK>地区选择是一个特殊情况 ")
            elif str(field_id) not in values:
                logging.info(f"<UNK>field_id:{field_id} is not in values! ")
                continue
            if str(field_id) == "地区选择":
                sheng_value = values['省或直辖市']
                shi_value = values['市']
                xian_value = values['县或区']
                xiang_value = values['乡或镇']
            else:
                value = values[str(field_id)]
            widget = info["widget"]
            wtype = info["type"]
            name = info["name"]
            if wtype == "QComboBox":
                """为什么这要用findText，因为我们value的是具体显示值
                但是我们在创建的时候，实际上保存的是key"""
                index = widget.findText(str(value))
                if index >= 0:
                    widget.setCurrentIndex(index)
            elif wtype in ["QLineEdit","Number","QTextEdit","QLabel"]:
                widget.setText(str(value))
                if isinstance(widget, QLineEdit):
                    widget.setProperty("original_value", str(value))
                self.value_changed.emit(self.title, name, value, self.calc_func)
            elif wtype == "QCheckBoxGroup":
                for cb in widget.findChildren(QCheckBox):
                    if cb.text() == str(value):
                        cb.setChecked(True)
                    else:
                        cb.setChecked(False)
            elif wtype == "ChinaAreaSelector":
                widget.set_default_values(sheng_value, shi_value, xian_value, xiang_value)

    def set_values_and_readonly(self, values):
        """
        设置各个字段的值
        values: dict {id: value}
        """
        for field_id, info in self.widgets.items():
            if str(field_id) not in values:
                logging.info(f"<UNK>field_id:{field_id} is not in values! ")
                continue
            value = values[str(field_id)]
            widget = info["widget"]
            wtype = info["type"]
            if wtype == "QComboBox":
                """为什么这要用findText，因为我们value的是具体显示值
                但是我们在创建的时候，实际上保存的是key"""
                index = widget.findText(value)
                if index >= 0:
                    widget.setCurrentIndex(index)
                    widget.setEnabled(False)
            elif wtype in ["QLineEdit","Number","QTextEdit","QLabel"]:
                widget.setText(str(value))
                widget.setReadOnly(True)
            elif wtype == "ChinaAreaSelector":
                for selector in widget.findChildren(QComboBox):
                    selector.setEnabled(False)

    def set_combox_values_by_name(self, name, values):
        """
        动态更新指定名称的 QComboBox 的下拉选项
        :param name: 组件的字段名称（name）
        :param values: 新的选项字典，格式如: {key: "显示文本"}，例如 {1: "凸地形", 2: "凹地形"}
                       也可以是元组列表: [("1", "选项1"), ("2", "选项2")]
        :param default_value: 可选，默认选中的 key（不是文本！），如果 None 则不设置
        """
        info = self.widgets.get(name)
        if not info:
            logging.warning(f"未找到名称为 '{name}' 的组件")
            return False
        if values is None:
            return
        widget = info["widget"]
        wtype = info["type"]

        if wtype != "QComboBox":
            logging.warning(f"组件 '{name}' 不是 QComboBox 类型，无法设置下拉选项")
            return False

        # 保存当前状态，避免误触发信号
        was_enabled = widget.isEnabled()
        widget.setEnabled(False)
        widget.clear()

        # 处理输入数据格式
        if isinstance(values, dict):
            options = values.items()
        elif isinstance(values, (list, tuple)) and all(isinstance(i, (list, tuple)) for i in values):
            options = values
        else:
            logging.error(f"不支持的 values 格式：{type(values)}")
            widget.setEnabled(was_enabled)
            return False

        # 添加选项，key 作为 userData，text 作为显示文本
        for key, text in options:
            widget.addItem(str(text), key)

        # 恢复启用状态
        widget.setEnabled(True)

        logging.info(f"成功更新 QComboBox '{name}' 的选项，共 {widget.count()} 项")
        return True

    def set_readonly_by_name(self, component_name, readonly=True):
        """
        通过字段名称设置组件为只读/不可选状态
        :param component_name: 字段名称（name）
        :param readonly: True 表示只读，False 表示可编辑
        """
        info = self.widgets.get(component_name)
        if not info:
            logging.warning(f"未找到名称为 {component_name} 的组件")
            return

        widget = info["widget"]
        wtype = info["type"]

        if wtype == "QComboBox":
            widget.setEnabled(not readonly)  # 禁用下拉框

        elif wtype in ["QLineEdit", "Number", "QTextEdit"]:
            widget.setReadOnly(readonly)  # 设置只读

        elif wtype == "QCheckBoxGroup":
            for cb in widget.findChildren(QCheckBox):
                cb.setEnabled(not readonly)  # 禁用复选框

        elif wtype == "ToggleButton":
            widget.setEnabled(not readonly)  # 禁用 ToggleButton

        elif wtype == "ChinaAreaSelector":
            for selector in widget.findChildren(QComboBox):
                selector.setEnabled(not readonly)  # 禁用地区选择器中的下拉框

        elif wtype == "QLabel":
            pass  # QLabel 本身不可编辑，无需处理

        else:
            logging.warning(f"组件类型 {wtype} 不支持设置只读状态")

    def get_value_by_name(self, component_name: str):
        info = self.widgets.get(component_name)
        if not info:
            logging.warning(f"未找到名称为 {component_name} 的组件")
            return ""

        widget = info["widget"]
        wtype = info["type"]

        try:
            if wtype == "QComboBox":
                current_data = widget.currentData()
                # 注意：currentData() 可能是 0，不能用 if current_data 判断
                return current_data if current_data is not None else ""

            elif wtype == "QLineEdit":
                text = widget.text().strip()
                return text if text != "" else ""

            elif wtype == "Number":
                text = widget.text().strip()
                if text == "":
                    return ""
                try:
                    # 尝试转 float，但允许 0.0
                    value = float(text)
                    return value
                except ValueError:
                    return ""  # 非法输入视为未填

            elif wtype == "QTextEdit":
                text = widget.toPlainText().strip()
                return text if text != "" else ""

            elif wtype == "QLabel":
                text = widget.text().strip()
                if text == "":
                    return ""
                try:
                    return float(text) if '.' in text else int(text)
                except ValueError:
                    return text  # 保持原始字符串

            elif wtype == "QCheckBoxGroup":
                checked_items = [cb.text() for cb in widget.findChildren(QCheckBox) if cb.isChecked()]
                return checked_items if checked_items else []  # 未选返回空列表

            elif wtype == "ToggleButton":
                # ToggleButton 返回布尔值，不会是 0，但可明确返回
                return widget.isChecked()

            elif wtype == "ChinaAreaSelector":
                province = widget.get_province_name()
                city = widget.get_city_name()
                area = widget.get_area_name()
                town = widget.get_town_name()
                # 只有当所有都为空时才视为未填？或按需返回 dict
                return {
                    "省": province or "",
                    "市": city or "",
                    "县": area or "",
                    "乡": town or ""
                }

            else:
                logging.warning(f"组件类型 {wtype} 尚未支持通过 get_value_by_name 获取值")
                return ""

        except Exception as e:
            logging.error(f"获取组件 {component_name} 的值时发生错误: {e}")
            return ""

    def validate(self) -> tuple[bool, str]:
        """执行验证，返回 (是否通过, 错误信息)"""
        if not self.validator_func:
            return True, ""
        return self.validator_func(self.validator_widgets)

    def _update_toggle_data(self, toggle_name, isChecked):
        """
        根据 ToggleButton 的状态，更新 validator_widgets 中的多个字段值
        支持一个开关控制多个字段
        """
        logging.info(f"ToggleButton 状态变化: {toggle_name} -> {isChecked}")
        logging.info(f"触发器之前原始的数据{self.validator_widgets}")

        # 1. 获取该开关对应的映射表 {目标字段名: {"0": 值, "1": 值}}
        field_mapping_str = self.toggle_data.get(toggle_name)
        if not field_mapping_str:
            logging.warning(f"未找到 {toggle_name} 的值映射表")
            return

        try:
            field_mapping = json.loads(field_mapping_str)
        except json.JSONDecodeError as e:
            logging.error(f"{toggle_name} 的值映射表不是合法 JSON: {e}")
            return
        """
        field_mapping:{'存在性-降雨历时': {'0': '45-坡面汇流历时T1', '1': '100-测试'}}
        """
        logging.info(f"<UNK> {field_mapping}")

        # 2. 遍历所有要更新的字段
        for target_key, value_map in field_mapping.items():
            try:
                group_name, field_name = target_key.split("-", 1)
            except ValueError:
                logging.error(f"无效的目标字段名格式: {target_key}，应为 '组名-字段名'")
                continue

            # 3. 根据开关状态选择值
            value_key = "1" if isChecked else "0"
            back_key = "0" if isChecked else "1"
            back_value =value_map.get(back_key)
            new_value = value_map.get(value_key)
            """new_value:{'45-坡面汇流历时T1'}"""
            if new_value is None:
                logging.warning(f"{target_key} 在状态 {value_key} 下无对应值")
                continue
            validator_menu_id,validator_column = new_value.split("-", 1)
            back_validator_menu_id, back_validator_column = back_value.split("-", 1)
            # 4. 获取该字段的当前完整配置（所有组）
            field_json_str = self.validator_widgets.get(field_name)
            if not field_json_str:
                logging.warning(f"未找到字段 {field_name} 的当前值")
                continue

            try:
                full_data = json.loads(field_json_str)  # 完整的 dict，如 {"存在性":{...}, "判断性":{...}}
            except json.JSONDecodeError:
                logging.error(f"{field_name} 的值不是合法 JSON")
                continue
            """{'存在性': {'45': '坡面汇流历时T1'}, '判断性': {'1': '5=6'}}"""
            logging.info(f"获取需要更新的字段： {full_data}")
            # 确保存在该组
            if group_name not in full_data:
                full_data[group_name] = {}

            group_data = full_data[group_name]
            if back_validator_menu_id in group_data:
                del group_data[back_validator_menu_id]
                logging.info(f"已移除旧反向项: {back_validator_menu_id} -> {back_validator_column}")

                # 更新为新值
            group_data[validator_menu_id] = validator_column
            logging.info(f"已设置新值: {validator_menu_id} -> {validator_column}")


            # 5. 回写整个字段的 JSON 字符串
            self.validator_widgets[field_name] = json.dumps(full_data, ensure_ascii=False)
            logging.info(f"已更新 {group_name} -> {field_name} = {new_value} (来自开关: {toggle_name})")

        logging.info(f"最终数据{self.validator_widgets}")
        self.validate()

    def shou_dong_diao_yong_ji_suan(self):
        """
        手动触发计算请求：
        - 自动识别所有带有 '计算方法' 的字段
        - 若该字段是 QLabel 且当前无值，则 emit value_changed 信号
        - 仅在表单中所有组件都是 QLabel 时触发（即：无用户输入项）
        """
        logging.info(f"[{self.title}] 手动触发计算请求（自动识别可计算字段）")

        # 1. 检查是否所有字段都是 QLabel（即：纯显示表单）
        # if not all(widget_info["type"] == "QLabel" for widget_info in self.widgets.values()):
        #     logging.info("表单中存在可编辑字段，不触发手动计算信号")
        #     return  # 有输入项，应由用户操作触发

        # 2. 遍历所有字段，查找带有 '计算方法' 的 QLabel
        triggered = False
        for name, info in self.widgets.items():
            if info["type"] != "QLabel":
                continue

            # 检查是否有计算方法（在 calc_func 中）
            if name not in self.calc_func:
                continue

            label_widget = info["widget"]
            current_text = label_widget.text().strip()

            # 如果已有值，跳过
            if current_text:
                logging.debug(f"字段 {name} 已有值，跳过触发")
                continue

            logging.info(f"触发计算请求: {name}")
            self.value_changed.emit(self.title, name, True, self.calc_func)
            triggered = True

        if not triggered:
            logging.info("未找到需要触发计算的字段（可能已有值或无计算方法）")
        else:
            logging.info(f"共触发 {triggered} 个计算请求")
