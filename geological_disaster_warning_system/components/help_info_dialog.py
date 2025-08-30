import json
import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QTextEdit, QTableWidget, QTableWidgetItem, QSizePolicy, QStyledItemDelegate
)
from PySide6.QtGui import QPixmap, QFont, QColor, QPainter
import sqlite3
import os

from utils.utils import MyUtils
class BorderColorDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter: QPainter, option, index):
        # 获取背景色
        bg_color = index.data(Qt.BackgroundRole)
        if bg_color:
            painter.fillRect(option.rect, bg_color)

        # 绘制文本
        text = index.data(Qt.DisplayRole)
        if text is not None:
            painter.drawText(option.rect, Qt.AlignCenter, str(text))

        # 绘制边框
        pen = painter.pen()
        pen.setColor(Qt.GlobalColor.gray)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRect(option.rect)
"""
帮助信息显示组件
dataSource：
    dbtable：从数据库读取表显示
    image：显示图片
    text：显示文件内容
name:
    对应的文件名
    
注意：！！！！！！！！！！！
调用设置db，来获取数据库，如果没有db，那么dbtable源将不可用。

使用方法：
    # 示例：只创建一次实例
    comp = DataSourceComponent()
    comp.set_data_source('text', 'example.txt')
     comp.show()
"""
class HelpInfoDialog(QWidget):
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(HelpInfoDialog, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # 防止重复初始化
        if self._initialized:
            return
        self._initialized = True
        # 手动调用父类初始化
        super(HelpInfoDialog, self).__init__()
        self._initialized = True
        self.db =None
        """这里是为了引起注意：layout这个变量不能随意使用，因为会与QWidget 本身的layout冲突
        """
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.dataSource = None
        self.name = None
        self.current_table = None  # 新增字段
        self.base_font_size = 20
        self.min_font_size = 12
        self.max_font_size = 50
        self.background_colors = [  # 每一行的背景色
            QColor("#f9f9f9"),
            QColor("#eef6ff"),
            QColor("#f9f9f9"),
            QColor("#eef6ff"),
            QColor("#f9f9f9")
        ]

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_font_sizes()

    def update_font_sizes(self):
        # 根据窗口宽度动态调整字体大小
        """"""
        """800,600是主窗口设置的大小"""
        width_scale = self.width() / 800
        height_scale = self.height() / 600
        scale = min(width_scale, height_scale)

        font_size = max(self.min_font_size, min(int(self.base_font_size * scale), self.max_font_size))

        self.apply_font_recursive(self, font_size)

        if self.current_table and isinstance(self.current_table, QTableWidget):
            row_height = int(50 * scale)
            col_width = int(200 * scale)

            for row_idx in range(self.current_table.rowCount()):
                self.current_table.setRowHeight(row_idx, row_height)
            for col_idx in range(self.current_table.columnCount()):
                self.current_table.setColumnWidth(col_idx, col_width)

    def apply_font_recursive(self, widget, font_size):
        font = QFont()
        font.setPointSize(font_size)
        widget.setFont(font)

        if isinstance(widget, QWidget):
            for child in widget.children():
                if isinstance(child, QWidget):
                    self.apply_font_recursive(child, font_size)

    def set_data_source(self, dataSource, name):
        self.dataSource = dataSource
        self.setWindowTitle(name)
        self.name = name
        self.clear_content()
        self.load_data()

    def clear_content(self):
        # 清除旧内容
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def load_data(self):
        if self.dataSource == 'dbtable':
            self.load_db_table(self.name)
        elif self.dataSource == 'image':
            self.load_image(self.name)
        elif self.dataSource == 'text':
            self.load_text_file(self.name)

    def set_db(self, db):
        self.db = db

    def handle_selection_changed(self):
        table = self.current_table
        if not table:
            return

        selected_items = table.selectedItems()
        if not selected_items:
            return

        selected_item = selected_items[0]
        selected_row = selected_item.row()
        selected_col = selected_item.column()

        # 恢复所有单元格颜色
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item:
                    bg_color = self.background_colors[row % len(self.background_colors)]
                    item.setBackground(bg_color)

        # 加深当前行的颜色
        for col in range(table.columnCount()):
            item = table.item(selected_row, col)
            if item:
                item.setBackground(QColor("#99ebf1"))

        # 加深当前列的颜色（可选）
        for row in range(table.rowCount()):
            item = table.item(row, selected_col)
            if item:
                item.setBackground(QColor("#cbcce8"))
    def create_table_view(self, data):
        # 分离表头和数据
        header_row = next((item for item in data if item['type'] == '表头字段'), None)
        data_rows = [item for item in data if item['type'] == '数据字段']

        if not header_row:
            label = QLabel("没有找到表头信息")
            self.main_layout.addWidget(label)
            return

        try:
            # 解析 value 字段中的 JSON
            header_values = json.loads(header_row['value'])
        except json.JSONDecodeError:
            label = QLabel("表头字段 value 解析失败")
            self.main_layout.addWidget(label)
            return

        # 构建列名列表（第一列为 name，其余为 value 的 key）
        columns = [header_row['name']] + list(header_values.values())

        # 创建表格控件
        table = QTableWidget()
        self.current_table = table
        table.setRowCount(len(data_rows))
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)

        # 使用自定义的 Delegate 来绘制边框和背景颜色
        delegate = BorderColorDelegate(table)
        table.setItemDelegate(delegate)

        # 隐藏左侧的行号
        table.verticalHeader().setVisible(False)

        # 设置行高和列宽
        for row_idx in range(table.rowCount()):
            table.setRowHeight(row_idx, 50)
        for col_idx in range(table.columnCount()):
            table.setColumnWidth(col_idx, 200)

        value_keys = list(header_values.keys())  # 如 ["1"]

        for row_idx, row_data in enumerate(data_rows):
            # 设置第一列：name
            name_item = QTableWidgetItem(row_data['name'])
            name_item.setBackground(self.background_colors[row_idx % len(self.background_colors)])
            table.setItem(row_idx, 0, name_item)

            # 解析 value JSON
            try:
                values = json.loads(row_data['value'])
            except json.JSONDecodeError:
                for col_idx in range(1, len(columns)):
                    error_item = QTableWidgetItem("解析错误")
                    error_item.setBackground(self.background_colors[row_idx % len(self.background_colors)])
                    table.setItem(row_idx, col_idx, error_item)
                continue

            # 填充剩余列
            for col_idx, key in enumerate(value_keys, start=1):
                cell_value = values.get(key, "")
                cell_item = QTableWidgetItem(str(cell_value))
                cell_item.setBackground(self.background_colors[row_idx % len(self.background_colors)])
                table.setItem(row_idx, col_idx, cell_item)

        # 设置不可编辑的单元格
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item:
                    # item.setFlags(Qt.NoItemFlags)  # 所有单元格都不可编辑
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled) #允许选中，但是不可以编辑
        #监听，用来当选中单元格的时候，加深显示
        table.itemSelectionChanged.connect(self.handle_selection_changed)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(table)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        container.setLayout(layout)
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.main_layout.addWidget(container)
    def load_db_table(self, table_name):
        if self.db is None:
            conn = sqlite3.connect('example.db')
            cursor = conn.cursor()
            try:
                i = 0
            except Exception as e:
                label = QLabel(f"数据库错误: {str(e)}")
                self.main_layout.addWidget(label)
            finally:
                conn.close()
        else:
            query = f"SELECT * FROM {table_name}"
            res = self.db.db_manger_do_sql(query)
            data = MyUtils.cal_sql_data(res)
            # TODO
            logging.info(f"帮助表：{table_name}----获取的数据、{data}")
            self.create_table_view(data)

    def load_image(self, image_path):
        label = QLabel()
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            label.setPixmap(pixmap)
            label.setScaledContents(True)
        else:
            label.setText("图片不存在")
        self.main_layout.addWidget(label)

    def load_text_file(self, file_path):
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            text_edit.setText(text)
        except Exception as e:
            text_edit.setText(f"读取失败: {str(e)}")
        self.main_layout.addWidget(text_edit)

