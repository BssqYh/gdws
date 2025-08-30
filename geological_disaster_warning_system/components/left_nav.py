import logging
from cProfile import label

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame, QSizePolicy, QLabel, QComboBox, QFormLayout, \
    QScrollArea
from PySide6.QtCore import Qt, Signal

from components.query_combo_box import QueryComboBox

logging.basicConfig(format='%(levelname)s:[%(filename)s:%(lineno)d]:%(funcName)s:%(message)s', level=logging.DEBUG)
class LeftNav(QScrollArea):
    button_clicked = Signal(dict)  # 按钮点击信号
    query_changed = Signal(dict) #查询按钮改变信号

    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)  # 自动调整内部 widget 大小
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用水平滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 垂直滚动条按需显示

        # 创建原始 LeftNav 的内容容器
        self.content_frame = QFrame()
        self.content_frame.setStyleSheet("background-color: #e0f7fa; border: 1px solid #b2ebf2;")
        self.content_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 使用 QVBoxLayout
        self.layout = QVBoxLayout(self.content_frame)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(5)

        # 设置滚动区域内容
        self.setWidget(self.content_frame)

        self.current_button_text = None

    def handle_query_button_change(self,query_button):
        # print(f"handle_query_button_change--{query_button.current_id()}--{query_button.current_name()}")
        item={}
        item["name"] = query_button.current_display_name()
        item["id"] = query_button.current_id()
        self.query_changed.emit(item)

    def add_query_button(self, label_text,data,display_key, value_key=None):
        """添加导航按钮"""
        """
        :param label_text: 标签文字，如 "线路选择"
        :param data: 数据列表，如 [{'线别名称': '兰青线', '线别ID': 2}, ...]
        :param display_key: 显示字段名，如 '线别名称' 或 '里程K'
        :param value_key: 值字段名，如 '线别ID'，若不传则使用 display_key 的值作为 value
        """
        query_button = QueryComboBox(label_text,data,display_key, value_key)
        query_button.currentIndexChanged.connect(lambda _, cb=query_button: self.handle_query_button_change(cb))
        self.layout.addWidget(query_button)
        pass

    def add_button(self,text,menuItem = None):
        """添加导航按钮"""
        """      
        item = {}
        item["工点ID"] = data1[i]["工点ID"]
        item["统一编码"] = data1[i]["统一编码"]
        item["风险评估类型"] = data1[i]["风险评估类型"]
        这个item就是用来确定是什么按钮的，如果有，就是说明不是单纯的菜单按钮。
        """
        btn = QPushButton(text)
        btn.setProperty("menuItem", menuItem)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #26c6da;  /* 更深的蓝绿色 */
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
                background-color: #006064;  /* 深蓝色表示选中 */
                color: red;
                border-left: 4px solid #004d40;  /* 左侧高亮条 */
            }
            QPushButton::icon {
                margin-right: 8px;
            }
        """)
        btn.setCheckable(True)  # 设置为可选中状态
        btn.clicked.connect(self.on_button_clicked)
        self.layout.addWidget(btn)
        return btn

    def insert_button(self, index, text, menuItem=None):
        """
        在指定索引位置插入一个按钮
        :param index: 插入的位置（从0开始）
        :param text: 按钮显示文本
        :param menuItem: 按钮携带的数据对象
        """
        btn = QPushButton(text)
        btn.setProperty("menuItem", menuItem)
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
                color: red;
                border-left: 4px solid #004d40;
            }
            QPushButton::icon {
                margin-right: 8px;
            }
        """)
        btn.setCheckable(True)
        btn.clicked.connect(self.on_button_clicked)
        self.layout.insertWidget(index, btn)
        return btn

    def on_button_clicked(self):
        btn = self.sender()
        current_btn = btn
        text = btn.text()
        """按钮点击处理"""
        # 取消其他按钮的选中状态
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                if widget is not current_btn:
                    widget.setChecked(False)

        item={}
        item["按钮名称"] = text
        item["menuItem"] = btn.property("menuItem")
        self.current_button_text = text
        self.button_clicked.emit(item)
    def set_current_button_checked(self):
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                tmp_text = widget.text()
                if tmp_text == self.current_button_text:
                    widget.setChecked(True)
    def clear_content(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        pass

    def set_content(self, widgets):
        """设置导航内容"""
        # 清除现有内容
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 添加新内容
        for widget in widgets:
            if isinstance(widget, QWidget):
                self.layout.addWidget(widget)
            else:
                self.add_button(str(widget))