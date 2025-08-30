import logging
from PySide6.QtCharts import QChart, QPieSlice, QPieSeries, QChartView
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QLineEdit, QTextEdit, QComboBox, QCheckBox,
                               QFormLayout, QSizePolicy, QDialog, QMainWindow, QTableView, QAbstractScrollArea,
                               QHeaderView, QHBoxLayout, QGridLayout, QMessageBox, QFrame, QDoubleSpinBox)
from PySide6.QtCore import Qt, Slot, QAbstractTableModel, QSignalBlocker
from PySide6.QtGui import QPixmap, QBrush, QPainter, QColor, QLinearGradient, QGradient, QIntValidator
from Model.survey_data_work_point_base_info_page_model import SurveyDataWorkPointBaseInfoPageModel
from components.China_area_selector import ChinaAreaSelector
from components.dynamic_form_widget import DynamicFormWidget
from components.form_row import create_form_row
from pages.base_page import MyBasePage
from utils.utils import MyUtils

logging.basicConfig(format='%(levelname)s:[%(filename)s:%(lineno)d]:%(funcName)s:%(message)s', level=logging.DEBUG)

"""
基本信息页面
"""
class SurveyDataWorkPointBaseInfoPage(MyBasePage):
    PAGE_NAME = "base_info_page"
    init_mark = 0
    PAGE_TABLE_ID = 73
    dynamic_form =None

    def create_model(self, main_window):
        return SurveyDataWorkPointBaseInfoPageModel(main_window.get_db_manager())

    def has_dynamic_disaster_buttons(self):
        """"""
        """需要显示动态风险按钮"""
        return self.init_mark
    def on_set_data(self, work_point_id, disaster_point_id):
        self.update_left_nav_with_dynamic_disaster_buttons()
    def setup_top_menu(self):
        """设置顶部菜单内容"""
        menu = self.components["top_menu"]
        menu.set_content("工点基础信息")
        # 初始化空菜单树

    def create_frame(self,data:dict):
        ####  ---------------------------------------
        ####  此方法已经废弃
        ####  -++++++++++++++++++++------------------
        frame = QFrame()
        layout = QFormLayout()

        layout.setSpacing(5)
        layout.setContentsMargins(20, 20, 20, 20)
        widgets = {}  # 保存控件便于后续获取数据
        add_area_mark = 0
        row_index = 0
        for key, value in data.items():
            logging.info(f"{key}:{value}")
            label = QLabel(key)

            if key == '工点ID':
                line_edit = QLineEdit(str(value))
                line_edit.setReadOnly(True)
                wrapped = create_form_row(label, line_edit, row_index)
                layout.addRow(wrapped)
                widgets[key] = line_edit

            elif key in ['统一编码', '具体地址','里程']:
                line_edit = QLineEdit(str(value))
                validator_rule = None
                if key == '里程':
                    validator_rule = r'^\s*([a-zA-Z][a-zA-Z0-9]*)\s*([+-])\s*(\d+(\.\d+)?)\s*(?:~\s*([+-])\s*(\d+(\.\d+)?))?\s*$'
                wrapped = create_form_row(label, line_edit, row_index,validator_rule =validator_rule )
                layout.addRow(wrapped)
                widgets[key] = line_edit

            elif key in ['经度', '纬度']:
                spin_box = QDoubleSpinBox()
                spin_box.setDecimals(7)
                spin_box.setRange(-180.0, 180.0)
                spin_box.setValue(float(value))
                wrapped = create_form_row(label, spin_box, row_index)
                layout.addRow(wrapped)
                widgets[key] = spin_box

            elif key in ['省或直辖市', '市', '县或区', '乡或镇', '具体地址']:
                if add_area_mark == 0:
                    area_selectors = ChinaAreaSelector()
                    wrapped = create_form_row(QLabel("地区选择"), area_selectors, row_index)
                    layout.addRow(wrapped)
                    widgets["地区选择"] = area_selectors
                    add_area_mark = 1
            elif key in ['铁路局', '线别','行别','侧别','风险评估类型', '风险易发性', '风险评估等级']:
                combo_box = QComboBox()
                data = self.model.get_combobox_value(key)
                combo_box.addItems(data)
                index = combo_box.findText(str(value), Qt.MatchFixedString)
                if index >= 0:
                    combo_box.setCurrentIndex(index)
                wrapped = create_form_row(label, combo_box, row_index)
                layout.addRow(wrapped)
                widgets[key] = combo_box
            elif key in ['区间开始站', '区间结束站']:
                # railway_line_id = 1
                # tmp_wifget = widgets['线别']
                # railway_line_id
                # combo_box = QComboBox()
                # data = self.model.get_train_station_combobox(railway_line_id)
                pass

            row_index += 1
        frame.setLayout(layout)
        return frame, widgets  # 返回frame和控件字典用于后续获取值

    def setup_content_area(self):
        content = self.components["content_area"]
        if self.init_mark == 1:
            menu_data = self.model.get_display_work_point_and_disaster_point_info(self.work_point_id,
                                                                                  self.disaster_point_id)
            menu = self.model.get_menu_content(self.PAGE_TABLE_ID,railway_line_id=menu_data[0]['线别ID'])
            logging.info(f"<UNK------------>:{menu}")
            self.dynamic_form = DynamicFormWidget(menu)
            self.dynamic_form.set_values(menu_data[0])
            content.set_content([self.dynamic_form])

    def setup_image_area(self):
        """设置图片区域"""
        image_area = self.components["image_area"]
        image_area.set_content([""])

    def setup_button_area(self):
        """设置按钮区域"""
        button_area = self.components["button_area"]
        button_area.set_content([
            ("保存", "#4caf50"),
            ("重置", "#ff9800"),
            ("导出", "#2196f3"),
            ("帮助", "#607d8b")
        ])

    def top_button_clicked(self,item):
        logging.debug(item)
        pass

    def bottom_button_clicked(self,item):
        logging.debug(item)
        datas = self.dynamic_form.get_values()
        # logging.debug(datas)
        self.model.upsert_work_point_info(datas,self.work_point_id)
        pass

    def setup_page(self,**kwargs):
        """设置页面内容 - 统一入口方法"""
        self.init_mark = 1
        self.window.display_left_top_content_button_area()
        self.setup_left_nav()
        self.setup_top_menu()
        self.setup_content_area()
        self.setup_image_area()
        self.setup_button_area()