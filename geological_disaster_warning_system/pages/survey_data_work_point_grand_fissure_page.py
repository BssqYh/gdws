import logging
from PySide6.QtCharts import QChart, QPieSlice, QPieSeries, QChartView
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QLineEdit, QTextEdit, QComboBox, QCheckBox,
                               QFormLayout, QSizePolicy, QDialog, QMainWindow, QTableView, QAbstractScrollArea,
                               QHeaderView, QHBoxLayout, QGridLayout, QMessageBox)
from PySide6.QtCore import Qt, Slot, QAbstractTableModel, QSignalBlocker
from PySide6.QtGui import QPixmap, QBrush, QPainter, QColor, QLinearGradient, QGradient, QIntValidator
from Model.survey_data_work_point_base_info_page_model import SurveyDataWorkPointBaseInfoPageModel
from utils.utils import MyUtils

logging.basicConfig(format='%(levelname)s:[%(filename)s:%(lineno)d]:%(funcName)s:%(message)s', level=logging.DEBUG)

"""
地裂缝页面
"""
class SurveyDataWorkPointGrandFissurePage:
    def __init__(self, main_window):
        self.page_mapping = None
        self.work_point_id = 0 #决定页面显示那个
        self.work_point_code = ""
        self.nav_button_cnt = 0  # 决定页面有多少个风险项
        self.init_mark = 0
        self.window = main_window
        self.components = main_window.get_components()
        self.model = SurveyDataWorkPointBaseInfoPageModel(main_window.get_db_manager())

        # 设置测试内容
        self.setup_left_nav()
        self.setup_top_menu()
        self.setup_content_area()
        self.setup_image_area()
        self.setup_button_area()

    def setup_left_nav(self):
        """设置左侧导航内容"""
        nav = self.components["left_nav"]
        nav.clear_content()
        nav.add_button("基本信息")
        nav.add_button("地质环境条件")
        nav.add_button("气象条件")
        #每个页面自己定义每个按钮对应的页面

        if self.page_mapping is None:
            self.page_mapping = {
                "基本信息": "survey_data_work_point_base_info_page",
                "地质环境条件": "survey_data_work_point_di_zhi_tiao_jian_page",
                "气象条件": "survey_data_work_point_qi_xiang_tiao_jian_page",
                "崩塌": "survey_data_work_point_collapse_page",
                "滑坡": "survey_data_work_point_mudslide_page",
                "泥石流": "survey_data_work_point_debris_flow_page",
                "地裂缝": "survey_data_work_point_grand_fissure_page",
                "增加风险项": "",
                "返回": "survey_data_page"
            }

        if self.init_mark == 1  and self.nav_button_cnt !=0 :
            data = self.model.get_cal_all_work_pont_info()
            data1 = self.model.get_all_work_pont_info()
            for i in range(self.nav_button_cnt):
                item = {}
                item["工点ID"] = data1[i]["工点ID"]
                item["统一编码"] = data1[i]["统一编码"]
                item["风险评估类型"] = data1[i]["风险评估类型"]
                text = "风险项" + str(i+1) + "-"+data1[i]["里程K"] +data1[i]["里程开始位置"] +data1[i]["里程结束位置"] +"-"+data[i]["风险评估类型"]
                nav.add_button(text,item)
            # 设置当前选中的按钮
        nav.add_button("增加风险项")
        nav.add_button("返回")

        for i in range(nav.layout.count()):
            widget = nav.layout.itemAt(i).widget()
            if isinstance(widget, QPushButton) and widget.text() == "基本信息":
                widget.setChecked(True)

    def setup_top_menu(self):
        """设置顶部菜单内容"""
        menu = self.components["top_menu"]
        menu.set_content("地裂缝页面-待完善")
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

    def set_data(self,code,work_point_id):
        self.work_point_code = code
        self.nav_button_cnt = self.model.get_disaster_count_with_code(code)
        print(f"suvery_data_work_point_mudslide_page:{self.nav_button_cnt}")
        self.set_work_point_id(work_point_id)
        pass
    def set_work_point_id(self,num):
        self.work_point_id = num
        self.menu_score = {}#存储每个菜单的排序、系数、分数、后期会增加value
        data = self.model.get_mudslide_work_point_score(num)
        for item in data:
            self.menu_score[item["menu_id"]]={
                "important_num": item["important_num"],
                "weight": item["weight"],
                "score": item["score"],
                "content_value": item["content_value"]
            }
        print(f"set_work_point_id---{self.menu_score}")
        pass

    def top_button_clicked(self,item):
        logging.debug(item)
        pass
    def lef_nav_button_clicked(self,item):
        button_text = item["按钮名称"]
        tmp_button_text = ["基本信息", "地质环境条件", "气象条件", "返回"]
        if button_text in tmp_button_text:
            logging.debug(item)
            self.window.get_page_manager().switch_page(self.page_mapping[button_text],work_point_id= self.work_point_id ,code = self.work_point_code)
        elif button_text =="增加风险项":
            logging.debug(item)
        else:
            logging.debug(item)
            re_text = button_text.split("-")[2]
            logging.debug(re_text)
            self.window.get_page_manager().switch_page(self.page_mapping[re_text],work_point_id= self.work_point_id ,code = self.work_point_code)
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