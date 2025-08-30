import json
import logging
from PySide6.QtCharts import QChart, QPieSlice, QPieSeries, QChartView
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QLineEdit, QTextEdit, QComboBox, QCheckBox,
                               QFormLayout, QSizePolicy, QDialog, QMainWindow, QTableView, QAbstractScrollArea,
                               QHeaderView, QHBoxLayout, QGridLayout, QMessageBox)
from PySide6.QtCore import Qt, Slot, QAbstractTableModel, QSignalBlocker
from PySide6.QtGui import QPixmap, QBrush, QPainter, QColor, QLinearGradient, QGradient, QIntValidator
from pandas.core.groupby.ops import check_result_array

from Model.survey_data_work_point_debris_flow_page_model import SurveyDataWorkPointDebrisFlowPageModel
from components.calc_heavy_rain import CalcHeavyRainView
from components.calc_hydrological_survey_specifaications import CalcHydrologicalSurveySpecificationsView
from components.calc_overland_debrisflow_flow import CalcOverlandDebrisFlowView
from components.calc_overland_flow import CalcOverlandFlowView
from components.calc_peak_flow import CalcPeakFlowView
from components.chinese_message_box import ChineseMessageBox
from components.dynamic_form_widget import DynamicFormWidget
from components.formula_calculator import extract_variables, calc_formula
from pages.base_page import MyBasePage
from utils.utils import MyUtils

logging.basicConfig(format='%(levelname)s:[%(filename)s:%(lineno)d]:%(funcName)s:%(message)s', level=logging.DEBUG)

"""
泥石流页面
"""
class SurveyDataWorkPointDebrisFlowPage(MyBasePage):
    PAGE_NAME = "debris_flow_page"
    init_mark = 0
    def __init__(self, main_window):
        super().__init__(main_window)
        # 存储菜单名称的字典
        self.menu_name_map = {}
        # 存储所有可改变状态的控件
        self.value_widgets = []
        # 存储控件的字典
        self.content_controls = {}
        self.current_widget = None
        self.current_menu_id = 0
        self.data ={}
        self.current_data = {}
        self.current_check_data_value = {}

    def create_model(self, main_window):
        return SurveyDataWorkPointDebrisFlowPageModel(main_window.get_db_manager())

    def has_dynamic_disaster_buttons(self):
        """"""
        """需要显示动态风险按钮"""
        return self.init_mark

    def setup_top_menu(self):
        """设置顶部菜单内容"""
        menu = self.components["top_menu"]
        if self.init_mark == 1:
            data = self.model.get_debris_flow_first_menu()
            for item in data:
                menu.add_first_level_menu_button(item["menu_id"], item["menu_name"],"debrisflow_page")
            data = self.model.get_debris_flow_second_menu()
            for item in data:
                menu.add_second_level_menu_button(item["menu_id"], item["menu_name"],parent_id=item["parent_id"], root_name= "debrisflow_page")
        menu.show_menu_by_root("debrisflow_page")

    def create_content_view(self):
        layout = QVBoxLayout()
        # layout.addWidget()

        # 创建主部件
        container = QWidget()
        container.setLayout(layout)
        return container

    def setup_content_area(self):
        content = self.components["content_area"]
        # wget = self.create_content_view()
        content.set_content([""])

    def setup_button_area(self):
        """设置按钮区域"""
        button_area = self.components["button_area"]
        button_area.set_content([])
        # # 自定义按钮
        button_area.set_content([
            ("保存", "#4caf50"),
            ("智能分析", "#9c27b0"),
            ("重置", "#ff9800"),
            ("删除", "#f44336"),
            ("导出", "#2196f3"),
            ("帮助", "#607d8b")
        ])
    def _generate_heavy_rain_data(self,widget,menu_id):
        data = self.model.get_disaster_point_score(self.disaster_point_id,menu_id)
        logging.info(f"{data}")
        content_value = data[0]["content_value"]
        table_data = content_value["表格数据"]
        widget.set_heavy_rain_data(table_data)
        logging.info(f"{content_value}")
        pass
    def update_content_area_for_heavy_rain(self,menu_id,menu_name):
        content = self.components["content_area"]
        data = self.model.get_menu_content(menu_id)
        widget = CalcHeavyRainView(data)
        self.current_widget = widget
        self._generate_heavy_rain_data(widget,menu_id)
        content.set_content([widget])
    def find_menu_name_by_menu_id(self, menu_id):
        """"""
        """从一个menu_id找到对应的名称"""
        data = self.model.get_debris_flow_first_menu()
        for item in data:
            if str(item['menu_id']) == str(menu_id):
                return item['menu_name']
        data = self.model.get_debris_flow_second_menu()
        for item in data:
            if str(item['menu_id']) == str(menu_id):
                return item['menu_name']
        return None
    def _generate_and_set_content_area_data(self,widget,menu_id):
        data = self.model.get_disaster_point_score(self.disaster_point_id,menu_id)
        logging.info(f"{data}")
        content_value = data[0]["content_value"]
        widget.set_data(content_value)
        logging.info(f"{content_value}")
        pass
    def update_content_area_for_overland_flow(self,menu_id,menu_name):
        content = self.components["content_area"]
        data = self.model.get_menu_content(menu_id)
        wget = CalcOverlandFlowView(self.model,data)
        self._generate_and_set_content_area_data(wget,menu_id)
        self.current_widget = wget
        content.set_content([wget])
        pass
    def _check_data_before_update(self,tmp_need_checked_data,menu_name):
        logging.info(tmp_need_checked_data)
        """当前需要检查的数据每次都要清空。以便每次重新设置key-value"""
        for key,value in tmp_need_checked_data.items():
            if value:
                for item in value:
                    if key not in self.data:
                        warning_text = f"当前指标{menu_name}需要提前计算指标{key}！"
                        tmp_msg = ChineseMessageBox("提示",warning_text,button0_text="好的")
                        tmp_msg.exec_()
                        return False
                    else:
                        if self.data[key][item] == "" or  self.data[key][item] ==None:
                            warning_text = f"当前指标{menu_name}需要提前计算指标{key}内容{item}"
                            tmp_msg = ChineseMessageBox("提示", warning_text, button0_text="我知道了")
                            tmp_msg.exec_()
                            return False

        return True
    def update_content_area_for_hydrological_survey_specifications(self,menu_id,menu_name):
        content = self.components["content_area"]
        data = self.model.get_menu_content(menu_id)
        wget = CalcHydrologicalSurveySpecificationsView(self.model,data)
        tmp_need_checked_data = wget.get_need_checked_data()
        check_result = self._check_data_before_update(tmp_need_checked_data,menu_name)
        if check_result:
            self.current_widget = wget
            self.current_check_data_value = MyUtils.extract_target_values(self.data,tmp_need_checked_data)
            wget.set_values(self.current_check_data_value)
            content.set_content([wget])

    def update_content_area_for_peak_flow(self,menu_id,menu_name):
        content = self.components["content_area"]
        data = self.model.get_menu_content(menu_id)
        wget = CalcPeakFlowView(self.model,data)
        self.current_widget = wget
        content.set_content([wget])

    def update_content_area_for_overland_debrisflow(self,menu_id,menu_name):
        content = self.components["content_area"]
        data = self.model.get_menu_content(menu_id)
        wget = CalcOverlandDebrisFlowView(self.model,data)
        self.current_widget = wget
        content.set_content([wget])

    def update_content_area(self, menu_id):
        name = self.find_menu_name_by_menu_id(menu_id)
        if  name =="降雨数据":
            self.update_content_area_for_heavy_rain(menu_id,name)
        else:
            data = self.model.get_menu_content(menu_id)
            if data:
                form_widget = DynamicFormWidget(data,validator_func=self._validator_widgets)
                content_area = self.components["content_area"]
                form_widget.value_changed.connect(
                    lambda dynamic_form_name, dynamic_component_name, val,calc_func: self._dynamic_form_value_change(
                        dynamic_form_name, dynamic_component_name, val,calc_func))
                self.current_widget = form_widget
                content_area.set_content([form_widget])
        pass

    def _dynamic_form_value_change(self, dynamic_form_name,dynamic_component_name, val,calc_func):
        #TODO
        """"""
        """注意：这里是根据具体的表来使用不同的计算方法。
        如果提供了计算方法就按照提供的计算方法来实现"""
        logging.info(f"{dynamic_form_name}, {dynamic_component_name}, {val},{calc_func}")
        if calc_func:
            for key,value  in calc_func.items():
                logging.info(f"开始获取公式：{key}, {value}")
                variables = extract_variables(value)
                logging.info(f"获取到需要的组件名称：{variables}")
                components_values = {}
                cal_mark =1 #计算标识，需要所有的值都有，如果没有，那么就不能计算
                for variables_name,variables_func_name in variables.items():
                    components_values[variables_func_name] = self.current_widget.get_value_by_name(variables_name)
                    if components_values[variables_func_name] =="" or components_values[variables_func_name] == None:
                        cal_mark = 0
                        break
                logging.info(f"计算公式:{value}，需要的值{components_values}")
                if cal_mark:
                    result = calc_formula(value, **components_values)
                    result = round(result, 2)
                    result_str = f"{result:.2f}"
                    self.current_widget.set_value_by_name(key, result_str)

    def _get_current_menu_value(self,menu_id):
        self.current_data = self.model.get_disaster_point_score(self.disaster_point_id,menu_id)
    def _validator_widgets(self,validator_dict):
        need_warning = 0
        warning_msg = ""
        current_menu_name = self.find_menu_name_by_menu_id(self.current_menu_id)
        for key,value in validator_dict.items():
            logging.info(f"获取到需要判断前置条件的组件：{key}{value}")
            value = json.loads(value)
            if need_warning:
                break
            for validator_type,validator_values in value.items():
                if validator_type == "存在性":
                    for validator_menu_id,validator_column in validator_values.items():
                        logging.info(f"获取到前置条件{validator_type}-前置菜单ID：{validator_menu_id}-前置字段：{validator_column}")
                        name = self.find_menu_name_by_menu_id(validator_menu_id)
                        menu_value = self.model.get_disaster_point_score(self.disaster_point_id,validator_menu_id)
                        if menu_value and menu_value[0]:
                            menu_content_value = menu_value[0].get("content_value")
                            logging.info(f"读取到content_value：{menu_content_value}")
                            if validator_menu_id == "38":
                                """如果是降雨数据，需要特殊处理一下"""
                                tmp_CalcHeavyRainView = menu_content_value.get("CalcHeavyRainView",None)
                                logging.info(f"<遇到特殊情况-降雨数据>{tmp_CalcHeavyRainView}")
                                desc_value = tmp_CalcHeavyRainView.get(key,None)
                            else:
                                desc_value = menu_content_value.get(validator_column,None)
                            logging.info(f"读取到{key}-值为:{desc_value}")
                            if desc_value:
                                self.current_widget.set_value_by_name(key, desc_value)
                            else:
                                self.current_widget.set_value_by_name(key, "")
                                need_warning = 1
                                warning_msg = f"计算{current_menu_name}值{key}需要先计算{name},否则后续数据无法计算"
                        else:
                            need_warning = 1
                            self.current_widget.set_value_by_name(key, "")
                            warning_msg = f"计算{current_menu_name}值{key}需要先计算{name},否则后续数据无法计算"
                elif validator_type == "判断性":
                    pass
        if need_warning==1:
            ChineseMessageBox.show_message("提示", warning_msg, button0="我知道了")

    def _set_current_menu_with_value(self):
        logging.info(f"{self.current_data}<UNK>")
        if self.current_data and self.current_data[0]:
            content_value = self.current_data[0]['content_value']
            if content_value != None:
                self.current_widget.set_values(content_value)
        self.current_widget.validate()
        self.current_widget.shou_dong_diao_yong_ji_suan()

    def top_button_clicked(self,item):
        logging.debug(item)
        menu_id = item["menuItem"]["menu_id"]
        menu_name =item["按钮名称"]
        display_content = item["display_content"]
        if display_content:
            self.current_menu_id = menu_id
            self._get_current_menu_value(menu_id)
            self.update_content_area(menu_id)
            self._set_current_menu_with_value()
        pass

    def bottom_button_clicked(self,item):
        logging.debug(item)
        button_text = item["按钮名称"]
        if button_text =="保存":
            sava_result ={}
            class_name = self.current_widget.__class__.__name__
            name = self.current_widget.get_name()
            if class_name == "CalcHeavyRainView":
                data = self.current_widget.get_all_values()
                rain_data = self.current_widget.get_all_clac_data()
                tmp_result = {
                    "CalcHeavyRainView": rain_data,
                    "表格数据":data,
                }
                sava_result["content_value"] = tmp_result
            else:
                data = self.current_widget.get_values()
                sava_result["content_value"] = data
            logging.info(f"class_name {class_name}-{name} :--sava_result {sava_result}")
            self.model.upsert_disaster_point_score(self.disaster_point_id,self.current_menu_id,sava_result)
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