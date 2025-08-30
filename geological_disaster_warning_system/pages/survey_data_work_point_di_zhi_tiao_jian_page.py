import logging
from PySide6.QtCharts import QChart, QPieSlice, QPieSeries, QChartView
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QLineEdit, QTextEdit, QComboBox, QCheckBox,
                               QFormLayout, QSizePolicy, QDialog, QMainWindow, QTableView, QAbstractScrollArea,
                               QHeaderView, QHBoxLayout, QGridLayout, QMessageBox)
from PySide6.QtCore import Qt, Slot, QAbstractTableModel, QSignalBlocker
from PySide6.QtGui import QPixmap, QBrush, QPainter, QColor, QLinearGradient, QGradient, QIntValidator
from Model.survey_data_work_point_qi_xiang_tiao_jian_page_model import SurveyDataWorkPointQiXiangTiaoJianPageModel
from pages.base_page import MyBasePage
from utils.utils import MyUtils

logging.basicConfig(format='%(levelname)s:[%(filename)s:%(lineno)d]:%(funcName)s:%(message)s', level=logging.DEBUG)

"""
地质条件页面
"""
class SurveyDataWorkPointDiZhiTiaoJianPage(MyBasePage):

    def create_model(self, main_window):
        return SurveyDataWorkPointQiXiangTiaoJianPageModel(main_window.get_db_manager())
    def setup_top_menu(self):
        """设置顶部菜单内容"""
        menu = self.components["top_menu"]
        menu.set_content("地质条件页面-待完善")
        # 初始化空菜单树

    def create_content_view(self):
        layout = QVBoxLayout()
        # layout.addWidget()

        # 创建主部件
        container = QWidget()
        container.setLayout(layout)
        return container

    def setup_content_area(self):
        content = self.components["content_area"]
        wget = self.create_content_view()
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
        image_area = self.components["image_area"]
        image_area.set_content([""])
        # if self.init_mark == 1:
        #     img_path = self.model.get_database_img()
        #     base_image = QPixmap(img_path)
        #     image_label = QLabel()
        #     image_label.setPixmap(base_image.scaled(500, 400, Qt.KeepAspectRatio))
        #     image_label.setAlignment(Qt.AlignCenter)
        #     image_label.setStyleSheet("border: 2px solid #e0e0e0; border-radius: 8px;")
        #     image_label.mousePressEvent = lambda e: self._show_full_image(base_image)
        #     # 设置内容
        #     image_area.set_content(image_label)

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
        # button_area.set_content([
        #     ("保存", "#4caf50"),
        #     ("智能分析", "#9c27b0"),
        #     ("重置", "#ff9800"),
        #     ("删除", "#f44336"),
        #     ("导出", "#2196f3"),
        #     ("帮助", "#607d8b")
        # ])


    def top_button_clicked(self,item):
        logging.debug(item)
        pass

    def bottom_button_clicked(self,item):
        logging.debug(item)
        pass

    def setup_page(self,**kwargs):
        """设置页面内容 - 统一入口方法"""
        self.init_mark = 1
        self.setup_left_nav()
        self.setup_top_menu()
        self.setup_content_area()
        self.setup_image_area()
        self.setup_button_area()