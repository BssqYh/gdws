import json
import logging
import math
import sys

from PIL.Image import alpha_composite
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QStyledItemDelegate, \
    QLabel, QLineEdit, QFrame, QFormLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter

from components.form_row import create_form_row
from components.pearson_III_module import PearsonIIIModule

"""
降雨数据
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
        pen.setWidth(4)
        painter.setPen(pen)
        painter.drawRect(option.rect)

class CalcHeavyRainView(QWidget):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self.name = "降雨数据"
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
        self.init_ui()
        self.pearson_iii_module = PearsonIIIModule()
        self.HeavyRainData ={
            "%1sp":0.0,
            "%2sp":0.0,
            "%1storm_decay_index":0.0,
            "%2storm_decay_index":0.0,
        }

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 提取列头（从“降雨参数”中提取 unit）
        self.extract_column_headers()

        # 提取行名（排除“降雨参数”）
        self.extract_row_names()

        # 创建表格
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(len(self.row_names))
        self.table_widget.setColumnCount(len(self.column_labels))
        self.table_widget.setHorizontalHeaderLabels(self.column_labels)
        self.delegate = BorderColorDelegate(self.table_widget)
        self.table_widget.setItemDelegate(self.delegate)

        # 隐藏左侧的行号
        self.table_widget.verticalHeader().setVisible(False)

        for row_index in range(self.table_widget.rowCount()):
            self.table_widget.setRowHeight(row_index, 50)
        for col_index in range(self.table_widget.columnCount()):
            self.table_widget.setColumnWidth(col_index, 200)

        # 填充表格
        self.populate_table()

        # 设置不可编辑单元格
        for row_index in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row_index, 0)
            item.setFlags(Qt.NoItemFlags)
            if self.row_names[row_index] in ['百年一遇sp', '五十年一遇sp']:
                for col_index in range(1, self.table_widget.columnCount()):
                    item = self.table_widget.item(row_index, col_index)
                    if item:
                        item.setFlags(Qt.NoItemFlags)


        # 单元格变化监听
        self.table_widget.cellChanged.connect(self.on_cell_changed)

        # 新增：为表格添加一个外层容器 widget + layout，用于控制内边距
        main_container = QWidget()
        main_layout = QHBoxLayout(main_container)
        main_layout.setContentsMargins(20, 20, 20, 20)  # 左右内边距
        main_layout.addWidget(self.table_widget)

        # 允许容器水平扩展
        main_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)


        # 添加到布局
        self.layout .addWidget(main_container,1)


        self.content_container = None
        self.create_content_container()
    def extract_column_headers(self):
        """从‘降雨参数’中提取时间维度作为列头"""
        self.column_labels = ["降雨参数"]
        for item in self.data:
            if item['name'] == '降雨参数':
                unit_str = item['unit']
                try:
                    unit_str =json.loads(unit_str)
                    logging.info(unit_str)
                    for key,value in unit_str.items():
                        self.column_labels.append(value)
                except Exception as e:
                    print("解析 unit 出错:", e)
                break

    def extract_row_names(self):
        """提取所有非‘降雨参数’的 name 字段作为行名"""
        self.row_names.clear()
        for item in self.data:
            name = item['name']
            if name != '降雨参数':
                self.row_names.append(name)

    def populate_table(self):
        """填充表格内容"""
        for row_index, row_name in enumerate(self.row_names):
            # 设置第一列（行名）
            name_item = QTableWidgetItem(row_name)
            self.table_widget.setItem(row_index, 0, name_item)

            # 填入默认空值或原始值
            for col_index in range(1, self.table_widget.columnCount()):
                cell_value = ""
                background_color = self.background_colors[row_index % len(self.background_colors)]

                # 查找原始数据中的 value
                for item in self.data:
                    if item['name'] == row_name:
                        cell_value = str(item['value'])
                        break

                cell_item = QTableWidgetItem(cell_value)
                cell_item.setBackground(background_color)
                self.table_widget.setItem(row_index, col_index, cell_item)

    def on_cell_changed(self, row, column):
        """单元格变化事件"""
        if column == 0:  # 忽略第一列
            return

        row_name = self.row_names[row]
        if row_name in ['降雨量（mm/h）', 'Cv', 'Cs']:
            self.update_percentages()

    def safe_float(self,value, default=None):
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def update_storm_decay_index(self):
        data =self.get_all_values()
        logging.info(data)
        x_rain_1_10m = self.safe_float(data['百年一遇sp']['10min降雨量'])
        x_rain_1_1h = self.safe_float(data['百年一遇sp']['1h降雨量'])
        x_rain_2_10m = self.safe_float(data['五十年一遇sp']['10min降雨量'])
        x_rain_2_1h = self.safe_float(data['五十年一遇sp']['1h降雨量'])
        if x_rain_1_10m is None or x_rain_1_1h is None or x_rain_2_10m is None or x_rain_2_1h is None:
            return
        index1 = self.calculate_storm_decay_index(x_rain_1_10m, x_rain_1_1h)
        index2 = self.calculate_storm_decay_index(x_rain_2_10m, x_rain_2_1h)
        index1 =round(index1,4)
        index2 = round(index2,4)
        self.HeavyRainData["%1storm_decay_index"] = index1
        self.HeavyRainData["%2storm_decay_index"] = index2
        self.decay_index_label_1.setText(str(index1))
        self.decay_index_label_2.setText(str(index2))

    def update_percentages(self):
        """模拟公式计算并更新 1% 和 2%"""
        for col_index in range(1, self.table_widget.columnCount()):
            val_rain = self.get_cell_value_by_name("降雨量（mm/h）", col_index)
            val_cv = self.get_cell_value_by_name("Cv", col_index)
            val_cs = self.get_cell_value_by_name("Cs", col_index)

            try:
                rain = float(val_rain)
                cv = float(val_cv)
                cs = float(val_cs)
                self.pearson_iii_module.set_parameters(rain, cv, cs)
                p1 = self.pearson_iii_module.calculate_x_by_frequency(1)
                p2 = self.pearson_iii_module.calculate_x_by_frequency(2)

            except ValueError:
                p1 = ""
                p2 = ""

            col_name = self.table_widget.horizontalHeaderItem(col_index).text()
            """因为只有1小时候降雨量的sp数据才会用来计算，所以只有这里才会更新HeavyRainData的数据"""
            if col_name == "1h降雨量":
                self.HeavyRainData["%1sp"] = p1
                self.HeavyRainData["%2sp"] = p2
            self.set_cell_value_by_name("百年一遇sp", col_index, str(p1))
            self.set_cell_value_by_name("五十年一遇sp", col_index, str(p2))
        """更新暴雨衰减指数"""
        self.update_storm_decay_index()


    def get_cell_value_by_name(self, name, col_index):
        row_index = self.row_names.index(name)
        item = self.table_widget.item(row_index, col_index)
        return item.text() if item else ""

    def set_cell_value_by_name(self, name, col_index, value):
        row_index = self.row_names.index(name)
        item = self.table_widget.item(row_index, col_index)
        if item:
            item.setText(str(value))
    def get_heavy_rain_data(self):
        return self.HeavyRainData
    def get_all_values(self):
        """获取当前所有值"""
        result = {}
        for row_index, row_name in enumerate(self.row_names):
            row_data = {}
            for col_index in range(1, self.table_widget.columnCount()):
                col_name = self.table_widget.horizontalHeaderItem(col_index).text()
                item = self.table_widget.item(row_index, col_index)
                row_data[col_name] = item.text() if item else ""
            result[row_name] = row_data
        return result
    def set_all_clac_data(self,data:dict):
        index1 = data["%1storm_decay_index"]
        index2 = data["%2storm_decay_index"]
        self.decay_index_label_1.setText(str(index1))
        self.decay_index_label_2.setText(str(index2))
    def get_all_clac_data(self):
        result = {}
        result["五十年一遇sp"] = self.HeavyRainData["%2sp"]
        result["百年一遇sp"] = self.HeavyRainData["%1sp"]
        result["百年一遇衰减指数"] = self.HeavyRainData["%1storm_decay_index"]
        result["五十年一遇衰减指数"] = self.HeavyRainData["%2storm_decay_index"]
        return result

    def set_heavy_rain_data(self, data):
        """设置新的数据源并刷新界面"""
        for row_name, columns in data.items():
            if row_name not in self.row_names:
                continue  # 跳过无效行名

            row_index = self.row_names.index(row_name)

            for col_key, value in columns.items():
                if col_key not in self.column_labels:
                    continue  # 跳过无效列名

                col_index = self.column_labels.index(col_key)

                # 更新对应单元格内容
                item = self.table_widget.item(row_index, col_index)
                if item:
                    item.setText(str(value))

    def create_content_container(self):
        """创建一个带边框和表单布局的容器来显示暴雨衰减指数及相关参数"""
        self.content_container = QFrame()
        self.content_container.setFrameShape(QFrame.Box)  # 设置边框
        self.content_container.setStyleSheet("padding: 10px;")

        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(10, 10, 10, 10)

        title_label = QLabel("")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        # container_layout.addWidget(title_label)

        form_layout = QFormLayout()
        row_index = 0
        tmp_widget = create_form_row(QLabel("降雨特征值"), None, row_index)
        form_layout.addRow(tmp_widget)
        row_index += 1
        # 暴雨衰减指数
        self.decay_index_label_1 = QLabel("数据不足，请完善降雨数据")
        self.decay_index_label_2 = QLabel("数据不足，请完善降雨数据")
        tmp_widget = create_form_row(QLabel("百年一遇衰减指数"), self.decay_index_label_1, row_index)
        form_layout.addRow(tmp_widget)
        row_index += 1
        tmp_widget = create_form_row(QLabel("五十年一遇衰减指数"), self.decay_index_label_2, row_index)
        form_layout.addRow(tmp_widget)
        row_index += 1


        # 主雨历时 H 输入框
        self.input_main_duration = QLineEdit()
        self.input_main_duration.setPlaceholderText("请输入主雨历时（分钟）")
        self.input_main_duration.setObjectName("inputMainDuration")
        tmp_widget = create_form_row(QLabel("主雨历时 H (min)"), self.input_main_duration, row_index)
        form_layout.addRow(tmp_widget)
        row_index += 1

        # 主雨量 hp 输入框
        self.input_main_rainfall = QLineEdit()
        self.input_main_rainfall.setPlaceholderText("请输入主雨量（mm）")
        self.input_main_rainfall.setObjectName("inputMainRainfall")
        tmp_widget = create_form_row(QLabel("主雨量 hp (mm)"), self.input_main_rainfall, row_index)
        form_layout.addRow(tmp_widget)
        row_index += 1

        # 加入主布局
        container_layout.addLayout(form_layout)
        self.content_container.setLayout(container_layout)

        # 将容器加入主布局
        self.layout.addWidget(self.content_container,1)
    def calculate_storm_decay_index(self, value_10m, value_1h):
        """"""
        """
        计算暴雨衰减指数
        参数：
            value_10m: 10分钟预计降雨量
            value_1h: 1小时预计降雨量
        返回：
           衰减指数
        """
        ratio = value_10m / value_1h
        decay_index = 1 + 1.285 * math.log10(ratio)

        return round(decay_index, 2)

    def get_name(self):
        return self.name