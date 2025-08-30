import logging
from PySide6.QtCharts import QChart, QPieSlice, QPieSeries, QChartView
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QLineEdit, QTextEdit, QComboBox, QCheckBox,
                               QFormLayout, QSizePolicy, QDialog, QMainWindow, QTableView, QAbstractScrollArea,
                               QHeaderView, QHBoxLayout, QGridLayout, QMessageBox)
from PySide6.QtCore import Qt, Slot, QAbstractTableModel, QSignalBlocker
from PySide6.QtGui import QPixmap, QBrush, QPainter, QColor, QLinearGradient, QGradient, QIntValidator
from Model.survey_data_work_point_base_info_page_model import SurveyDataWorkPointBaseInfoPageModel
from Model.survey_data_work_point_qi_xiang_tiao_jian_page_model import SurveyDataWorkPointQiXiangTiaoJianPageModel
from components.calc_heavy_rain import CalcHeavyRainView
from components.pearson_III_module import PearsonIIIModule
from pages.base_page import MyBasePage
from utils.utils import MyUtils

logging.basicConfig(format='%(levelname)s:[%(filename)s:%(lineno)d]:%(funcName)s:%(message)s', level=logging.DEBUG)

"""
气象条件页面
"""
class SurveyDataWorkPointQiXiangTiaoJianPage(MyBasePage):
    PAGE_NAME = "survey_data_work_point_qi_xiang_tiao_jian_page"
    init_mark = 0

    def __init__(self, main_window):
        super().__init__(main_window)
        self.pearson_widget = PearsonIIIModule()

    def create_model(self, main_window):
        return SurveyDataWorkPointQiXiangTiaoJianPageModel(main_window.get_db_manager())
    def setup_top_menu(self):
        """设置顶部菜单内容"""
        menu = self.components["top_menu"]
        menu.set_content("气象条件页面")
        # 初始化空菜单树

    def create_content_view(self):
        layout = QVBoxLayout()
        data = self.model.get_menu_content(38)
        # 创建主部件
        container = QWidget()
        container.setLayout(layout)
        return container

    def update_content_area_heavy_rain(self):
        if self.init_mark == 1:
            content = self.components["content_area"]
            data = self.model.get_menu_content(38)
            logging.info(data)
            wget = CalcHeavyRainView(data)
            content.set_content([wget])

    def setup_content_area(self):
        if self.init_mark == 1:
            content = self.components["content_area"]
            data = self.model.get_menu_content(38)
            logging.info(data)
            wget = CalcHeavyRainView(data)
            content.set_content([wget])

    def setup_content_area_eg(self):
        """设置内容区域"""
        content = self.components["content_area"]
        data = self.model.load_data()

        # 创建表单内容
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(15)

        # 标题
        title = QLabel("用户信息表单 (页面1)")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #5d4037;")
        form_layout.addRow(title)

        # 表单字段
        form_layout.addRow(QLabel("用户名:"), QLineEdit())
        form_layout.addRow(QLabel("邮箱:"), QLineEdit())

        user_type = QComboBox()
        user_type.addItems(["普通用户", "VIP用户", "管理员"])
        form_layout.addRow(QLabel("用户类型:"), user_type)

        notes = QTextEdit()
        notes.setMaximumHeight(100)
        form_layout.addRow(QLabel("备注:"), notes)

        agree_check = QCheckBox("我同意服务条款")
        form_layout.addRow(agree_check)

        # 设置内容
        content.set_content([form_widget])
    def setup_image_area(self):
        """设置图片区域"""
        # image_area = self.components["image_area"]
        # image_area.set_content([self.pearson_widget])

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

    def setup_button_area(self):
        """设置按钮区域"""
        button_area = self.components["button_area"]
        button_area.set_content([])
        # # 自定义按钮
        button_area.set_content([
            ("保存", "#4caf50"),
            ("查询分布曲线", "#9c27b0"),
            ("重置", "#ff9800"),
            ("删除", "#f44336"),
            ("导出", "#2196f3"),
            ("帮助", "#607d8b")
        ])
    def top_button_clicked(self,item):
        logging.debug(item)
        pass
    def bottom_button_clicked(self,item):
        logging.debug(item)
        button_text = item["按钮名称"]
        if button_text == "查询分布曲线":
            self.pearson_widget.show()
        pass

    def setup_page(self,**kwargs):
        """设置页面内容 - 统一入口方法"""
        self.window.display_left_top_content_button_area()
        self.init_mark = 1
        self.setup_left_nav()
        self.setup_top_menu()
        self.setup_content_area()
        self.setup_image_area()
        self.setup_button_area()