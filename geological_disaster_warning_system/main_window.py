import ctypes
import logging
import os

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter

from AI.ai_module import AIEvaluationModule
from components.help_info_dialog import HelpInfoDialog
from components.left_nav import LeftNav
from components.top_menu import TopMenu
from components.content_area import ContentArea
from components.image_area import ImageArea
from components.button_area import ButtonArea
from database.manager import DatabaseManager
from page_manager import PageManager
from utils.utils import MyUtils

# 初始窗口大小
INITIAL_WIDTH = 800
INITIAL_HEIGHT = 600

# 各组件初始尺寸比例（基于 800x600）
LEFT_NAV_WIDTH_RATIO = 1 / 5
RIGHT_CONTAINER_WIDTH_RATIO = 4 / 5

TOP_MENU_HEIGHT_RATIO = 1 / 5
MIDDLE_CONTAINER_HEIGHT_RATIO = 3 / 5
BUTTON_AREA_HEIGHT_RATIO = 1 / 5

CONTENT_AREA_WIDTH_RATIO = 3 / 5  # 占右侧容器宽度
IMAGE_AREA_WIDTH_RATIO = 2 / 5    # 占右侧容器宽度


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_path = None
        self.load_page = None
        self.setWindowTitle("地质灾害风险评估系统")
        self.resize(INITIAL_WIDTH, INITIAL_HEIGHT)
        self.setWindowIcon(QIcon(":/resources/icon.ico"))
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

        # 初始化页面管理器和数据库
        self.page_manager = PageManager(self)
        self.db = DatabaseManager()
        tmp = HelpInfoDialog()
        tmp.set_db(self.db)
        self.ai_module = AIEvaluationModule()

        # 创建主窗口中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # 左右分割器
        self.splitter = QSplitter(Qt.Horizontal)  # 水平方向分割左右两部分
        self.splitter.setChildrenCollapsible(False)  # 不允许折叠

        # 左侧导航栏
        self.left_nav = LeftNav()
        self.left_nav.setMinimumWidth(150)
        self.splitter.addWidget(self.left_nav)

        # 右侧内容容器
        self.right_container = QWidget()
        self.right_layout = QVBoxLayout(self.right_container)
        self.right_layout.setSpacing(10)
        self.right_layout.setContentsMargins(0, 0, 0, 0)

        # 右侧顶部菜单
        self.top_menu = TopMenu()
        self.top_menu.setMinimumHeight(50)
        self.right_layout.addWidget(self.top_menu)

        # 中间内容+图片水平分割器
        self.middle_splitter = QSplitter(Qt.Horizontal)
        self.middle_splitter.setChildrenCollapsible(False)

        self.content_area = ContentArea()
        self.image_area = ImageArea()
        self.middle_splitter.addWidget(self.content_area)
        self.middle_splitter.addWidget(self.image_area)

        self.right_layout.addWidget(self.middle_splitter)

        # 底部按钮区
        self.button_area = ButtonArea()
        self.button_area.setMinimumHeight(60)
        self.right_layout.addWidget(self.button_area)

        # 添加到 splitter
        self.splitter.addWidget(self.right_container)

        # 设置初始比例（左侧占1/5）
        total_width = INITIAL_WIDTH
        self.splitter.setSizes([total_width // 5, total_width * 4 // 5])

        # 设置 content_area 和 image_area 初始比例 (3:2)
        right_container_width = int(INITIAL_WIDTH * RIGHT_CONTAINER_WIDTH_RATIO)
        self.middle_splitter.setSizes([
            int(right_container_width * CONTENT_AREA_WIDTH_RATIO),
            int(right_container_width * IMAGE_AREA_WIDTH_RATIO)
        ])

        # 添加到主布局
        self.main_layout.addWidget(self.splitter)

        # 最小窗口尺寸限制
        self.setMinimumSize(800, 600)

        self.left_nav.button_clicked.connect(self.on_nav_button_clicked)
        self.left_nav.query_changed.connect(self.on_nav_query_button_change)
        self.top_menu.top_menu_button_clicked.connect(self.on_top_menu_clicked)
        self.button_area.button_clicked.connect(self.on_bottom_button_clicked)

        # 连接事件（示例）
        self._setup_menu()
        self.page_manager.page_changed.connect(self.on_page_changed)

    def get_components(self):
        """返回所有组件实例"""
        return {
            "left_nav": self.left_nav,
            "top_menu": self.top_menu,
            "content_area": self.content_area,
            "image_area": self.image_area,
            "button_area": self.button_area
        }

    def _setup_menu(self):
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("文件(&F)")
        re_open = QAction("打开数据库", self)
        re_open.triggered.connect(self.reload_load_data)
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.reload_load_page)
        file_menu.addAction(re_open)
        file_menu.addAction(exit_action)

        # View Menu
        view_menu = menu_bar.addMenu("视图(&V)")
        view_menu.addAction("刷新界面")

        # Help Menu
        help_menu = menu_bar.addMenu("帮助(&H)")
        about_action = QAction("关于", self)
        help_menu.addAction(about_action)

    def reload_load_data(self):
        pass

    def reload_load_page(self):
        self.close()

    def get_page_manager(self):
        """返回页面管理器"""
        return self.page_manager

    def on_top_menu_clicked(self, item):
        self.page_manager.get_current_page().top_button_clicked(item)

    def on_nav_query_button_change(self, item):
        self.page_manager.get_current_page().on_nav_query_button_change(item)

    def on_nav_button_clicked(self, item):
        """导航按钮点击事件处理"""
        self.page_manager.get_current_page().lef_nav_button_clicked(item)

    def clear_all_areas(self):
        """清除所有区域内容"""
        self.top_menu.clear_content()
        self.left_nav.clear_content()

    def main_window_show(self, db_manager):
        self.db_path = os.path.basename(db_manager)
        print(f"<UNK>{self.db_path}")
        self.db.init_connection(db_manager)
        self.show()
        self.page_manager.switch_page("homepage")

    def set_load_page(self, load_page):
        self.load_page = load_page

    def get_db_manager(self):
        return self.db

    def get_ai_module(self):
        return self.ai_module

    def on_bottom_button_clicked(self, item):
        print("on_bottom_button_clicked")
        self.page_manager.get_current_page().bottom_button_clicked(item)

    def on_page_changed(self):
        """页面切换事件处理"""
        self.clear_all_areas()
        self.reset_display()
        self.page_manager.get_current_page().setup_page(db_name=self.db_path)

    def reset_display(self):
        """恢复标准布局"""
        self.left_nav.setVisible(True)
        self.top_menu.setVisible(True)
        self.content_area.setVisible(True)
        self.image_area.setVisible(True)
        self.button_area.setVisible(True)
        # 重置 middle_splitter 到默认比例（content_area : image_area = 3:2）
        right_container_width = self.right_container.width()
        self.middle_splitter.setSizes([
            int(right_container_width * CONTENT_AREA_WIDTH_RATIO),
            int(right_container_width * IMAGE_AREA_WIDTH_RATIO)
        ])

    def display_left_top_content_area(self):
        """仅显示左侧导航、顶部菜单、内容区域"""
        self.left_nav.setVisible(True)
        self.top_menu.setVisible(True)
        self.content_area.setVisible(True)
        self.image_area.setVisible(False)
        self.button_area.setVisible(False)

        # 调整 middle_container 宽度比例
        self.middle_splitter.setSizes([self.right_container.width(), 0])

    def display_left_top_content_button_area(self):
        """显示左侧导航、顶部菜单、内容区和按钮区"""
        self.left_nav.setVisible(True)
        self.top_menu.setVisible(True)
        self.content_area.setVisible(True)
        self.image_area.setVisible(False)
        self.button_area.setVisible(True)

        # 调整 middle_container 宽度比例
        self.middle_splitter.setSizes([self.right_container.width(), 0])