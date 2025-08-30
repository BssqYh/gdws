import logging
from PySide6.QtCharts import QChart, QPieSlice, QPieSeries, QChartView
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QLineEdit, QTextEdit, QComboBox, QCheckBox,
                               QFormLayout, QSizePolicy, QDialog, QMainWindow, QTableView, QAbstractScrollArea,
                               QHeaderView)
from PySide6.QtCore import Qt, Slot, QAbstractTableModel
from PySide6.QtGui import QPixmap, QBrush, QPainter, QColor, QLinearGradient, QGradient

from Model.survey_data_page_model import SurveyDataPageModel
from components.add_work_point_dialog import WorkPointInfoDialog
from components.chinese_message_box import ChineseMessageBox
from pages.base_page import MyBasePage

logging.basicConfig(format='%(levelname)s:[%(filename)s:%(lineno)d]:%(funcName)s:%(message)s', level=logging.DEBUG)

class TableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def get_row_data(self, row):
        if 0 <= row < len(self._data):
            return self._data[row]
        return None

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            key = self._headers[col]
            return str(self._data[row].get(key, ""))

        # 居中对齐
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            return ""

class SurveyDataPage(MyBasePage):
    PAGE_NAME = "survey_data_page"
    init_mark = 0
    add_work_point_info_dialog = None
    edit_work_point_info_dialog = None

    def create_model(self, main_window):
        return SurveyDataPageModel(main_window.get_db_manager())

    def has_dynamic_disaster_buttons(self):
        """"""
        """需要显示动态风险按钮"""
        return self.init_mark

    def setup_left_nav(self):
        """设置左侧导航内容"""
        nav = self.components["left_nav"]
        nav.add_button("项目信息")
        nav.add_button("调查数据")

        if self.init_mark == 1:
            data = self.model.get_line_data()
            nav.add_query_button("线别",data,"线别名称","线别ID")
            data = self.model.get_mileage_data()
            nav.add_query_button("里程",data,"里程K")
            data = self.model.get_diaster_type_data()
            nav.add_query_button("风险类型",data,"name","id")
        nav.add_button("评估计算")
        nav.add_button("数据可视化")

    def setup_top_menu(self):
        """设置顶部菜单内容"""
        menu = self.components["top_menu"]
        if self.init_mark == 1:
            #这两个按钮只需要第一次进来的时候不需要创建，因为实例初始化的时候会创建
            # menu.clear_content()
            menu.add_first_level_menu_button(1,"详情","survey_data_page")
            menu.add_first_level_menu_button(2,"增加","survey_data_page")
            menu.add_first_level_menu_button(3, "修改", "survey_data_page")
            menu.add_first_level_menu_button(4, "删除", "survey_data_page")
            menu.show_menu_by_root("survey_data_page")


    def create_content_view(self):
        headers = list(  self.data [0].keys()) if   self.data  else []
        self.table_model = TableModel(self.data, headers)
        # 创建表格视图
        self.table = QTableView()
        self.table.setModel(self.table_model)

        # 设置表格属性
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setEditTriggers(QTableView.NoEditTriggers)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        # 设置列宽自适应（先拉伸后调整）
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("""
            QTableView::item:selected {
                background-color: #FFD700;
                color: black;
            }
        """)

        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)

        # 设置行高
        self.table.verticalHeader().setDefaultSectionSize(30)
        layout = QVBoxLayout()
        layout.addWidget(self.table)

        # 创建主部件
        container = QWidget()
        container.setLayout(layout)
        return container

    def setup_content_area(self):
        if self.init_mark == 1:
            content = self.components["content_area"]
            wget = self.create_content_view()
            content.set_content([wget])

    def setup_image_area(self):
        """设置图片区域"""
        image_area = self.components["image_area"]
        image_area.set_content([""])

    def _show_full_image(self, pixmap):
        """显示完整尺寸图片"""
        window = self.window
        dialog = QDialog(window)
        dialog.setWindowTitle("完整尺寸图片")
        dialog.setWindowModality(Qt.ApplicationModal)

        # 计算适合屏幕的尺寸
        screen_size = window.screen().availableGeometry()
        max_width = screen_size.width() - 100
        max_height = screen_size.height() - 100

        # 保持原始比例调整尺寸
        scaled_pixmap = pixmap.scaled(
            max_width, max_height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        label = QLabel()
        label.setPixmap(scaled_pixmap)
        label.setAlignment(Qt.AlignCenter)

        # 自适应内容尺寸
        dialog.resize(scaled_pixmap.width() + 20, scaled_pixmap.height() + 20)

        layout = QVBoxLayout(dialog)
        layout.addWidget(label)
        dialog.exec()

    # def lef_nav_button_clicked(self,item):
    #     """"""
    #     """每个页面自己实现自己的各个点击事件"""
    #     button_text = item["按钮名称"]
    #     logging.debug(button_text)
    #     self.window.get_page_manager().switch_page(self.page_mapping[button_text])
    #     pass

    def on_nav_query_button_change(self,item):
        """"""
        """自己页面注册了什么，就要实现什么"""
        logging.debug(item)
        self.update_data(typeName =  item["name"],id = item["id"])
        pass
    def top_button_clicked(self,item):
        button_text = item["按钮名称"]
        data = self.get_selected_row_data()
        logging.debug(f"item = {item}, data = {data}")

        if button_text == "详情":
            if data is not None:
                self.window.get_page_manager().switch_page("survey_data_work_point_base_info_page",work_point_id=data["工点ID"],disaster_point_id = data["风险点ID"])
        elif button_text == "修改":
            if data is not None:
                work_point_id = data["工点ID"]
                if self.edit_work_point_info_dialog is None:
                    menu_data = self.model.get_work_point_common_content(73)
                    self.edit_work_point_info_dialog = WorkPointInfoDialog(menu_data)
                self.edit_work_point_info_dialog.set_form_data(data)
                work_point_info_dialog_data = self.edit_work_point_info_dialog.show_dialog()
                if work_point_info_dialog_data:
                    self.model.upsert_work_point_info(work_point_info_dialog_data,work_point_id=work_point_id)
                    self.data = self.model.get_display_work_point_and_disaster_point_info(0, 0)
                    self.setup_content_area()
            else:
                tmp_msg = ChineseMessageBox("提示", "当前没有选中工点", button0_text="好的")
                tmp_msg.exec_()
        elif button_text == "增加":
            if self.add_work_point_info_dialog is None:
                menu_data = self.model.get_work_point_common_content(73)
                self.add_work_point_info_dialog = WorkPointInfoDialog(menu_data)
                self.add_work_point_info_dialog.add_work_info_value_changed.connect(
                    lambda dynamic_form_name, dynamic_component_name, val: self._update_add_work_point_info(dynamic_form_name,
                                                                                                   dynamic_component_name,
                                                                                                   val))
            work_point_info_dialog_data = self.add_work_point_info_dialog.show_dialog()
            if work_point_info_dialog_data:
                self.model.upsert_work_point_info(work_point_info_dialog_data)
                self.data = self.model.get_display_work_point_and_disaster_point_info(0,0)
                self.setup_content_area()
            pass
        elif button_text == "删除":
            if data is not None:
                self.model.delete_work_point_info(disaster_point_id=data["工点ID"])
                self.data = self.model.get_display_work_point_and_disaster_point_info()  # 重新获取最新数据
                self.setup_content_area()  # 重新设置表格区域
            pass
        pass

    def _update_add_work_point_info(self, dynamic_form_name,dynamic_component_name, val):
        #TODO
        """"""
        """注意：这里是根据具体的表来使用不同的计算方法。这里不能通用。而且如果某一天某个结构改了名字
        那么这边也要对应更新"""
        # logging.info(f"{dynamic_form_name}, {dynamic_component_name}, {val}")
        railway_lines = self.model.get_railway_line()
        railway_id =  next((s['id'] for s in railway_lines if s['线路'] == val), None)
        logging.debug(f"从线路数据-{railway_lines}-中找到线路-{val}- 对应ID ： {railway_id}")
        combox_data = self.model.get_combobox_value('区间开始站',railway_line_id=railway_id)
        if combox_data:
            self.add_work_point_info_dialog.set_form_data_by_name("区间开始站",combox_data)
            self.add_work_point_info_dialog.set_form_data_by_name("区间结束站", combox_data)

    def bottom_button_clicked(self,item):
        pass
    def setup_button_area(self):
        """设置按钮区域"""
        button_area = self.components["button_area"]
        button_area.set_content([])
        # 自定义按钮
        # button_area.set_content([
        #     ("保存", "#4caf50"),
        #     ("重置", "#ff9800"),
        #     ("删除", "#f44336"),
        #     ("导出", "#9c27b0"),
        #     ("帮助", "#2196f3")
        # ])

    def get_selected_row_data(self):
        if not self.table:
            return None

        selected_indexes = self.table.selectedIndexes()
        if not selected_indexes:
            return None

        row = selected_indexes[0].row()
        return self.table_model.get_row_data(row)

    def update_data(self,**kwargs):
        typeName = kwargs["typeName"]
        id = kwargs["id"]
        self.queryData[typeName] = id
        self.data = self.model.get_query_work_point_data(self.queryData)
        pass

        self.setup_content_area()

    def setup_page(self,**kwargs):
        """设置页面内容 - 统一入口方法"""
        """进入页面就要加载数据"""
        self.data = self.model.get_display_work_point_and_disaster_point_info(0,0)
        self.init_mark = 1
        self.window.display_left_top_content_area()
        self.setup_left_nav()
        self.setup_top_menu()
        self.setup_content_area()
        self.setup_image_area()
        self.setup_button_area()