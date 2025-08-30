import json
import logging
import os
import re

from PySide6.QtCharts import QChart, QPieSlice, QPieSeries, QChartView
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QLineEdit, QTextEdit, QComboBox, QCheckBox,
                               QFormLayout, QSizePolicy, QDialog, QMainWindow, QTableView, QAbstractScrollArea,
                               QHeaderView, QHBoxLayout, QGridLayout, QMessageBox)
from PySide6.QtCore import Qt, Slot, QAbstractTableModel, QSignalBlocker, QUrl
from PySide6.QtGui import QPixmap, QBrush, QPainter, QColor, QLinearGradient, QGradient, QIntValidator

from AI.ai_module import AIEvaluationModule
from Model.survey_data_work_point_mudslide_page_model import SurveyDataWorkPointMudslidePageModel
from components.dynamic_form_widget import DynamicFormWidget
from components.flow_layou import FlowLayout
from components.form_row import create_form_row
from components.image_item import ImageItemWidget
from components.image_upload_button import ImageUploaderButton
from components.table_select_dialog import TableSelectDialog
from export.excel_exporter import ExcelExporter
from pages.base_page import MyBasePage
from utils.utils import MyUtils
import plotly.express as px
import pandas as pd

logging.basicConfig(format='%(levelname)s:[%(filename)s:%(lineno)d]:%(funcName)s:%(message)s', level=logging.DEBUG)


class SurveyDataWorkPointMudslidePage(MyBasePage):
    SPECIAL_TABLE_TYPE_MAP = {
        "地层岩性土质": {
            "type_name": "土质",
            "menu_id": 40,
            "display_name": "增加土层"
        },
        "地层岩性岩质": {
            "type_name": "岩质",
            "menu_id": 41,
            "display_name": "增加岩层"
        },
    }
    PAGE_NAME = "mudslide_page"
    init_mark = 0
    """
    menu_count
    #存储各级菜单的个数，使用方法为self.menu_count[self.current_parent_menu_id]
    {1: 8, 2: 4, 35: 4, 8: 4}
    菜单ID为1的，拥有8个子菜单。那么对于菜单为1的子菜单，它的所有排序范围就是0-8
    """
    menu_counts_mark = 0  # 这是一个标识符号。
    menu_count = {}
    menu_map = {}
    def __init__(self, main_window):
        super().__init__(main_window)
        """"""
        """用来存储岩质或者土质的数量, 用来判断。不用更改太多的地方。
        有新增类型只需要在这里添加就可以了.记得和SPECIAL_TABLE_TYPE_MAP，一起更改噢
        """
        self.type_counter = {
            '土质': 0,
            '岩质': 0,
        }
        self.nav_button_cnt = 0#决定页面有多少个风险项
        self.ai_module = main_window.get_ai_module()
        self.ai_module.evaluation_finished.connect(self.on_ai_evaluation_finished)
        self.exporter = ExcelExporter() #导出设置
        self.current_parent_menu_id = 0#当前的父菜单id，配合menu_count一起使用
        self.current_menu_id = 0
        """
        menu_score，最后要存数据库
        #存储每个菜单的排序、系数、分数、后期会增加value
        {9: {'important_num': 2, 'weight': 0.22, 'score': 80.0}, 
        10: {'important_num': 1, 'weight': 0.27, 'score': 90.0},
         11: {'important_num': 7, 'weight': 0.03, 'score': 60.0}, 
         12: {'important_num': 4, 'weight': 0.14, 'score': 80.0}, 
        26: {'important_num': 1, 'weight': 0.44, 'score': 100.0}}
        """
        self.menu_score = {}
        self.common_frame_widgets = {}
        self.current_content_frame = {} #为什么要用字典，因为如果是地层岩性，那么可能有多个frame
        self.menu_tree={}

        self._setup_special_dialog()
        self.special_data ={}#存储临时的数据，只有点保存了才会保存。否则第二次进来就会没有了

    def create_model(self, main_window):
        return SurveyDataWorkPointMudslidePageModel(main_window.get_db_manager())

    def has_dynamic_disaster_buttons(self):
        """"""
        """需要显示动态风险按钮"""
        return self.init_mark

    def _setup_special_dialog(self):
        self.special_dialog = TableSelectDialog()
        for table_key, config in self.SPECIAL_TABLE_TYPE_MAP.items():
            display_name = config.get("display_name") or table_key
            self.special_dialog.add_button(display_name, table_key)
        self.special_dialog.table_selected.connect(self._handle_table_selected)

    def calculate_menu_counts(self, menu_data):
        """统计不同 parent_id 的数量并存储到 self.menu_count 字典"""
         # 遍历所有菜单项
        for item in menu_data:
            parent_id = item["parent_id"]
            menu_id = item["menu_id"]
            # 若 parent_id 已在字典中则累加，否则初始化为1
            if parent_id in self.menu_count:
                self.menu_count[parent_id] += 1
            else:
                self.menu_count[parent_id] = 1
                # 更新菜单映射表
            if parent_id in self.menu_map:
                # 以逗号分隔的形式添加新的menu_id
                self.menu_map[parent_id] += f",{menu_id}"
            else:
                # 创建新的父ID项
                self.menu_map[parent_id] = str(menu_id)
        # print(self.menu_map)
    def setup_top_menu(self):
        """设置顶部菜单内容"""
        menu = self.components["top_menu"]
        # 初始化空菜单树
        if self.init_mark == 1:
            data = self.model.get_mudslide_first_menu()
            for item in data:
                menu.add_first_level_menu_button(item["menu_id"],item["menu_name"],self.PAGE_NAME)
            data = self.model.get_mudslide_second_menu()
            for item in data:
                menu.add_second_level_menu_button(item["menu_id"], item["menu_name"],parent_id=item["parent_id"], root_name=self.PAGE_NAME)
            data = self.model.get_mudslide_third_menu()

            for item in data:
                menu.add_third_level_menu_button(item["menu_id"], item["menu_name"], parent_id=item["parent_id"], root_name=self.PAGE_NAME)
        menu.show_menu_by_root(self.PAGE_NAME)
        if self.menu_counts_mark == 0:
            #只需要计算1次就可以了。要不就会重复计算了
            data = self.model.get_mudslide_second_menu()
            self.calculate_menu_counts(data)
            data = self.model.get_mudslide_third_menu()
            self.calculate_menu_counts(data)
            self.menu_counts_mark  = 1

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
        image_area = self.components["image_area"]

    def setup_image_area1(self):
        """设置图片区域"""
        image_area = self.components["image_area"]

        # image_area.set_content([""])
        if self.init_mark == 1:
            plot_data = []
            ids = []
            scores = []
            weights = []
            total_score = 0
            # 遍历原始数据
            for key, value in self.menu_score.items():
                ids.append(self.find_menu_name_by_menu_id(key))
                scores.append(value['score'])
                weights.append(value['weight'])
                total_score +=  value['score'] * value['weight']

            plot_data = {
                'ID': ids,
                'Score': scores,
                'Weight': weights
            }

            df = pd.DataFrame(plot_data)

            # 创建柱状图
            tt = f"总分{total_score}"
            fig = px.bar(df, x='ID', y='Score', title=tt)
            fig.write_html("plot.html")  # 保存为HTML文件
            # 创建浏览器组件
            self.browser = QWebEngineView()

            # 获取当前目录下的 plot.html 路径
            html_path = os.path.abspath("plot.html")

            # 加载 HTML 文件
            self.browser.setUrl(QUrl.fromUserInput(f"file:///plot.html"))

            # 设置主窗口布局
            container = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(self.browser)
            container.setLayout(layout)
            image_area.set_content(container)

    def _set_common_form_data(self):
        important_num =  self.menu_score[self.current_menu_id]['important_num']
        weight =self.menu_score[self.current_menu_id]['weight']
        score =  self.menu_score[self.current_menu_id]['score']
        self.common_frame_widgets[1].setText(str(important_num))
        self.common_frame_widgets[2].setText(str(weight))
        self.common_frame_widgets[4].setText(str(score))

        pass

    def _create_default_mudslide_menu_score(self):
        """"""
        """对于新创建的，就需要构建空数据
        每个类型，只需要自己更新这里就可以了
        """
        data = self.model.get_mudslide_second_menu()
        for item in data:
            self.menu_score[item["menu_id"]] = {
                    "important_num": 0,
                    "weight":0,
                    "score": 0,
                    "content_value": {},
                    "image_path": {}
                }
        data = self.model.get_mudslide_third_menu()
        for item in data:
            self.menu_score[item["menu_id"]] = {
                    "important_num": 0,
                    "weight":0,
                    "score": 0,
                    "content_value": {},
                    "image_path": {}
                }
        pass
    def _get_and_update_current_menu_score(self):
        logging.info(f"<UNK>---{self.menu_score[self.current_menu_id]}")
        menu_name = self.find_menu_name_by_menu_id(self.current_menu_id)
        important_num = self.common_frame_widgets[1].text()
        weight = self.common_frame_widgets[2].text()
        score = self.common_frame_widgets[4].text()
        try:
            important_num = int(important_num) if important_num.strip() else 0
        except:
            important_num = 0
        try:
            weight = float(weight) if weight.strip() else 0.0
        except:
            weight = 0.0
        try:
            score = float(score) if score.strip() else 0.0
        except:
            score = 0.0
        # 更新 menu_score 中的基本字段
        self.menu_score[self.current_menu_id]['important_num'] = important_num
        self.menu_score[self.current_menu_id]['weight'] = weight
        self.menu_score[self.current_menu_id]['score'] = score
        if self._judge_is_special_menu(menu_name) == 2:
            converted_data = self.menu_score[self.current_menu_id]['content_value']
            if converted_data == "NULL":
                converted_data={}
            for key,item in self.current_content_frame.items():
                data = item.get_values()
                converted_data[key] = data
            self.menu_score[self.current_menu_id]['content_value'] = converted_data
        else:
            data = self.current_content_frame[0].get_values()
            # 处理 data 的 key 转换为字符串，并统一值格式
            converted_data = {}
            for k, v in data.items():
                if isinstance(v, list):
                    converted_data[str(k)] = v[0]  # 如 {1: ['凸地形', '凹地形']} → 取第一个值
                elif isinstance(v, (int, float)):
                    converted_data[str(k)] = v  # 如 37.0 → 保留原值
                else:
                    converted_data[str(k)] = str(v)  # 其他情况转字符串
            # 更新 content_value
            self.menu_score[self.current_menu_id]['content_value'] = converted_data

        logging.info(f"<UNK>---{self.menu_score[self.current_menu_id]}")
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
#---------------------------权重相关函数----------------------------------------------------------------------------------------------------
    def _calc_weight(self, weight_num):
        weight_num= int(weight_num)
        """计算权重系数（占位函数，根据实际需求实现）"""
        if weight_num == 0:
            return 0.0
        n = self.menu_count[self.current_parent_menu_id]
        logging.info(f"<UNK>---{self.menu_score[self.current_menu_id]}")
        """不直接更新self.menu_count[self.current_parent_menu_id]的原因是：
        虽然用户在某个时间将某个指标重要性设置为0，但是有可能会进行更新。比如将0->1,这时触发
        self.menu_count[self.current_parent_menu_id] 更新反而麻烦。直接在计算的时候使用就可以了"""
        for key in self.menu_map[self.current_parent_menu_id].split(","):
            if int(key) == self.current_menu_id:
                """1.因为首先当前菜单有判定，不能输入0，所以肯定是正确的值
                2.然后，可能会出现未定义其余的情况，因此，当需要跳过当前key的判定。
                """
                continue
            item = self.menu_score[int(key)]
            tmp = item["important_num"]
            if int(tmp) == 0:
                #如果重要性排序是0，那么就不参与计算，对应就是，总数减1
                n = n -1
        m = weight_num
        if m>=n :
            """这是因为，如果存在某一指标重要性为0，如果总排序为0-8，实际上最大只能是7，
            如果输入8，那么算法就会出错，因此需要将排序置为7.如果是<7,则不会影响"""
            m =n
        return (2*n-2*m+1)/(n*n)

    def update_weight_coefficient(self, weight_num):
        """更新权重系数显示"""
        if weight_num == 0:
            self.common_frame_widgets[2].setText("0.00")
            self.menu_score[self.current_menu_id]["weight"] = 0.0
        else:
            weight = self._calc_weight(weight_num)
            self.menu_score[self.current_menu_id]["weight"] = round(weight, 2)
            self.common_frame_widgets[2].setText(f"{weight:.2f}")
    def find_menu_name_by_menu_id(self, menu_id):
        """"""
        """从一个menu_id找到对应的名称"""
        data = self.model.get_mudslide_first_menu()
        for item in data:
            if str(item['menu_id']) == str(menu_id):
                return item['menu_name']
        data = self.model.get_mudslide_second_menu()
        for item in data:
            if str(item['menu_id']) == str(menu_id):
                return item['menu_name']
        data = self.model.get_mudslide_third_menu()
        for item in data:
            if str(item['menu_id']) == str(menu_id):
                return item['menu_name']
        return None

    def on_weight_order_changed(self):
        """处理权重排序变化的槽函数"""
        widget = self.common_frame_widgets[1] #获取权重系数的组件
        menu_id = self.current_menu_id
        if not widget or not isinstance(widget, QLineEdit):
            return
        menu_name = self.find_menu_name_by_menu_id(menu_id)
        weight_text = int(widget.text())
        print(f"当前输入：------{weight_text}--{menu_id}")
        try:
            weight_num = int(weight_text) if weight_text != "" else 0
        except ValueError:
            weight_num = 0

        if weight_num<0 or weight_num>self.menu_count[self.current_parent_menu_id]:
            QMessageBox.warning(self.window, "输入错误", f"当前指标[{menu_name}\可选范围只能是0-{self.menu_count[self.current_parent_menu_id]}")
            widget.setFocus()
            # 恢复之前的值
            prev_value = widget.property("current_order")
            if prev_value is not None:
                widget.setText(str(prev_value))
            else:
                widget.setText("0")
            return

        for key in self.menu_map[self.current_parent_menu_id].split(","):
            item = self.menu_score[int(key)]
            tmp = int(item["important_num"])
            if int(weight_num) == tmp:
                #表示冲突了。
                info = f"当前排序：{weight_num}\n已经被指标[{self.find_menu_name_by_menu_id(key)}]使用\n是否继续设置？"
                box = QMessageBox(QMessageBox.Warning, "排序冲突", info, QMessageBox.NoButton)
                yr_btn = box.addButton(("确认继续使用"), QMessageBox.YesRole)
                box.addButton(("取消"), QMessageBox.NoRole)
                box.exec_()
                if box.clickedButton() == yr_btn:
                    widget.setText(str(weight_num))
                    item["important_num"] = weight_num
                    item["weight"] = 0
                    self.menu_score[self.current_menu_id]["important_num"] = weight_num
                else:
                    prev_value = widget.property("current_order")
                    if prev_value is not None:
                        widget.setText(str(prev_value))
                    else:
                        widget.setText("0")
                    return

        # 更新权重系数
        self.update_weight_coefficient(weight_num)
#--------------------------------------------------------------------------------------------------------------------------------------

    def _on_value_changed(self):
        """当任意选项改变时调用此方法"""
        pass

    def _update_evaluation_content(self):
        """更新指标评价内容"""
        #暂时返回
        # return

        evaluation_groups = {}

        data = self.current_content_frame[0].get_values()
        evaluation_items = []
        for k, v in data.items():
            evaluation_items.append(f"{k}: {v}")
        # 生成评价文本

        # 更新指标评价标签
        evaluation_text = "; ".join(evaluation_items)
        evaluation_widget = self.common_frame_widgets[5]
        # print(f"evaluation_text-------{evaluation_text}")

        #调用AI模块进行打字机输出
        criteria =self.model.get_mudslide_zhibiao_score(self.current_menu_id)
        # logging.debug(criteria)
        # if evaluation_widget is not None:
        #     self.ai_module.set_criteria(criteria)
        #     self.ai_module.evaluate(evaluation_text, widget=evaluation_widget)
        # else:
        #     print("警告：控件尚未加载，无法启动 AI 分析")
        # return
        # 弹出输入框让用户添加额外要求
        dialog = QDialog(self.window)
        dialog.setWindowTitle("地质灾害风险评估助手")
        layout = QVBoxLayout(dialog)

        input_edit = QTextEdit()  # 支持多行输入
        layout.addWidget(input_edit)

        btn_layout = QHBoxLayout()
        confirm_btn = QPushButton("开始分析")
        btn_layout.addStretch()
        btn_layout.addWidget(confirm_btn)

        layout.addLayout(btn_layout)
        extra_data = [""]  # 使用列表保存额外要求
        def on_confirm():
            extra_requirements = input_edit.toPlainText().strip()
            if extra_requirements:
                extra_data[0] = extra_requirements
            dialog.accept()

        confirm_btn.clicked.connect(on_confirm)

        if dialog.exec_() == QDialog.Accepted:
            if evaluation_widget is not None:
                self.ai_module.set_criteria(criteria)
                self.ai_module.evaluate(evaluation_text,extra_data[0], widget=evaluation_widget)
            else:
                print("警告：控件尚未加载，无法启动 AI 分析")

    def setup_button_area(self):
        """设置按钮区域"""
        button_area = self.components["button_area"]

        # 自定义按钮
        button_area.set_content([
            ("保存", "#4caf50"),
            ("智能分析", "#9c27b0"),
            ("AI助手", "#ff9800"),
            ("删除", "#f44336"),
            ("导出", "#2196f3"),
            ("帮助", "#607d8b")
        ])
    def on_set_data(self,work_point_id,disaster_point_id):
        self.update_menu_score()
        pass
    def update_menu_score(self):
        self.menu_score = {}#存储每个菜单的排序、系数、分数、后期会增加value
        data = self.model.get_disaster_point_score(self.disaster_point_id)
        if data is None or len(data) == 0:
            #没有数据，那么就根据滑坡创建数据
            self._create_default_mudslide_menu_score()
        else:
            for item in data:
                self.menu_score[item["menu_id"]]={
                    "important_num": item["important_num"],
                    "weight": item["weight"],
                    "score": item["score"],
                    "content_value": item["content_value"],
                    "image_path": item["image_path"]
                }
        pass

    def find_parent_id_by_menu_id(self,target_menu_id):
        """"""
        """根据 menu_id 查找对应的 parent_id,并且存储在"""
        data = self.model.get_mudslide_second_menu()
        for item in data:
            if str(item['menu_id']) == str(target_menu_id):
                self.current_parent_menu_id = item["parent_id"]
                return
        data = self.model.get_mudslide_third_menu()
        for item in data:
            if str(item['menu_id']) == str(target_menu_id):
                self.current_parent_menu_id = item["parent_id"]
                return

    def _handel_upload_image(self,path):
        MyUtils.add_image_path(self.menu_score[self.current_menu_id],path)
        logging.info(f"<UNK>{self.menu_score[self.current_menu_id]}")
        self.update_image_area()

    def handle_image_operation(self, op_type, item_data):
        path = item_data.get("path", "")
        if op_type == "update":
            logging.info(f"图片更新: {path}")
            # 可以在这里重新加载或刷新图片
        elif op_type == "delete":
            logging.info(f"图片删除: {path}")
            # 删除对应文件或数据库记录等操作

    def update_image_area(self):
        # 设置内容区域
        if self.current_menu_id not in self.menu_score:
            logging.info(f"当前menu_score = {self.menu_score} ")
            logging.info(f"菜单ID {self.current_menu_id} 不存在于 menu_score 中，可能是父菜单，跳过加载图片区域。")
            return

        image_area = self.components["image_area"]
        current_record = self.menu_score[self.current_menu_id]

        if not current_record or 'image_path' not in current_record:
            return
        # 处理菜单内容的图片
        image_values = current_record['image_path']
        container = QWidget()
        layout = FlowLayout(container)
        layout.setSpacing(10)

        # 添加上传按钮
        uploader = ImageUploaderButton()
        uploader.set_folder("mudslide")
        uploader.upload_successful.connect(self._handel_upload_image)

        # 如果有已存在的图片，则先全部添加到布局中
        if image_values != "NULL" and isinstance(image_values, dict):
            for key, value in image_values.items():
                print(f"{key}:{value}")
                image_item = ImageItemWidget(value)
                image_item.set_item_data({"key": key, "path": value})
                image_item.operation_signal.connect(self.handle_image_operation)
                layout.addWidget(image_item)

        layout.addWidget(uploader)

        # 设置内容区域
        image_area.set_content(container.children())

    def _build_common_form(self):
        """"""
        """创建评价指标之类的通用表格"""
        common_data = self.model.get_common_content(39)
        common_form_widget = QWidget()
        common_form_layout = QFormLayout(common_form_widget)
        common_form_layout.setSpacing(15)
        menu_id = self.current_menu_id
        row_index = 0
        for item in common_data:
            field_id = item['id']
            name = item['name']
            field_type = item['type']
            unit = item['unit']
            value = item['value']
            need_help = item['need_help']
            label = QLabel(name)
            label.setStyleSheet("font-weight: bold;")
            label.setAlignment(Qt.AlignLeft)
            # 关键设置：开启自动换行并设置最大宽度
            label.setWordWrap(True)  # 启用自动换行
            label.setMaximumWidth(220)  #
            widget = None
            if name=="权重排序":
                h_widget = QWidget()
                h_layout = QHBoxLayout(h_widget)
                h_layout.setContentsMargins(0, 0, 0, 0)
                h_layout.setSpacing(5)

                # 排序输入框
                edit = QLineEdit()
                edit.setValidator(QIntValidator())
                edit.setFixedWidth(60)
                edit.setPlaceholderText("请输入权重排序")
                edit.setProperty("menu_id", menu_id)
                edit.setProperty("parent_menu_id", self.current_parent_menu_id)  # 存储父菜单ID

                # 添加信号处理
                edit.editingFinished.connect(self.on_weight_order_changed)
                weight_waring_label = QLabel(f"当前指标请在0-{self.menu_count[self.current_parent_menu_id]}之间排序")
                # 权重系数显示标签
                coef_name_label = QLabel("权重系数")
                coef_label = QLabel("0.00")
                coef_label.setFixedWidth(60)
                coef_label.setStyleSheet("background-color: #f0f0f0; padding: 2px;")

                h_layout.addWidget(edit)
                h_layout.addWidget(weight_waring_label)
                h_layout.addWidget(coef_name_label)
                h_layout.addWidget(coef_label)

                # 存储控件
                self.common_frame_widgets[1] = edit
                self.common_frame_widgets[2] = coef_label
                # form_layout.addRow(label, h_widget)

                tmp_widget = create_form_row(label, h_widget, row_index)
                common_form_layout.addRow(tmp_widget)
            elif name =="评估得分":
                # 评估得分，需要在后面增加一个推荐得分
                h_widget = QWidget()
                h_layout = QHBoxLayout(h_widget)
                h_layout.setContentsMargins(0, 0, 0, 0)
                h_layout.setSpacing(5)

                edit = QLineEdit()
                edit.setValidator(QIntValidator())
                edit.setPlaceholderText("请输入得分")
                edit.setFixedWidth(100)  # 设置固定宽度为100像素

                label1 = QLabel("建议得分")
                label2 = QLabel("暂无得分，请点击智能分析")

                h_layout.addWidget(edit)
                h_layout.addWidget(label1)
                h_layout.addWidget(label2)
                self.common_frame_widgets[4] = edit
                self.common_frame_widgets[6] = label2
                widget = create_form_row(label, h_widget, row_index)
            elif name in["权重系数","建议得分"]:
                continue
            elif name == "指标评价":
                edit = QTextEdit()
                edit.setPlaceholderText("暂无分析请点击智能分析")
                self.common_frame_widgets[5] = edit
                widget = create_form_row(label, edit, row_index)
            row_index += 1

            if widget:
                common_form_layout.addRow(widget)
        return common_form_widget

    def _handle_table_selected(self,item):
        table_name = item["db_name"]
        mapping = self.SPECIAL_TABLE_TYPE_MAP.get(table_name)
        if not mapping:
            return
        type_name = mapping["type_name"]
        menu_id = mapping["menu_id"]
        self.type_counter[type_name] += 1
        mark_index = f"{type_name}{self.type_counter[type_name]}"
        self.special_data[mark_index] = self.model.get_menu_content(menu_id)
        self.update_content_area_for_special_menu()

    def _handel_special_buttons(self):
        self.special_dialog.popup()

    def update_content_area_for_special_menu(self):
        """"""
        """为专门的菜单更新内容区域"""
        content_area = self.components["content_area"]
        button = QPushButton("增加")
        button.clicked.connect(self._handel_special_buttons)
        button.setStyleSheet("""
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
                border-left: 4px solid #004d40;
            }
            QPushButton::icon {
                margin-right: 8px;
            }
        """)

        widget_list= []
        current_record = self.menu_score[self.current_menu_id]
        if not current_record or 'content_value' not in current_record:
            if len(self.special_data) == 0:
                content_area.set_content([button])
        else:
            content_values = current_record['content_value']
            if content_values == "NULL":
                if len(self.special_data) != 0:
                    for key, item in self.special_data.items():
                        form_widget = DynamicFormWidget(item, key)
                        self.current_content_frame[key] = form_widget
                        widget_list.append(form_widget)
                    form_widget2 = self._build_common_form()
                    self._set_common_form_data()
                    widget_list.append(form_widget2)
                widget_list.append(button)
                content_area.set_content(widget_list)
            else:
                for key, value in content_values.items():
                    tmp_menu_id = 0
                    for table_key, config in self.SPECIAL_TABLE_TYPE_MAP.items():
                        type_name = config["type_name"]
                        if type_name not in key:  #例如：土质在土质1里面,岩质不在岩质1里面
                            continue
                        tmp_menu_id = config["menu_id"]
                        tmp_num= int(re.search(r'\d+$', key).group())
                        if  self.type_counter[type_name]<tmp_num:
                            self.type_counter[type_name] =tmp_num
                    data = self.model.get_menu_content(tmp_menu_id)
                    form_widget = DynamicFormWidget(data, key)
                    self.current_content_frame[key] = form_widget
                    form_widget.set_values(value)
                    widget_list.append(form_widget)
                # 处理菜单内容具体的值
                if len(self.special_data) != 0:
                    for key,item in self.special_data.items():
                        form_widget = DynamicFormWidget(item,key)
                        self.current_content_frame[key] = form_widget
                        widget_list.append(form_widget)
                form_widget2 = self._build_common_form()
                widget_list.append(form_widget2)
                widget_list.append(button)
                self._set_common_form_data()
                content_area.set_content(widget_list)

    def _judge_is_special_menu(self,menu_name):
        """"""
        """这个方法的目的就是：以后对于特殊页面，就不需要每个地方都改了。"""
        if menu_name in ["水文地质"]:
            return 1
        elif menu_name in ["地层岩性"]:
            #可能有多个内容
            return 2
        else:
            return 0

    def update_content_area(self):
        menu_id = self.current_menu_id
        self.find_parent_id_by_menu_id(menu_id)
        menu_name = self.find_menu_name_by_menu_id(menu_id)
        data = self.model.get_menu_content(menu_id)
        self.current_content_frame = {}
        self.common_frame_widgets = {}
        if data is not None:
            form_widget = None
            if self._judge_is_special_menu(menu_name) == 1:
                form_widget = None
            elif self._judge_is_special_menu(menu_name) == 2:
                self.update_content_area_for_special_menu()
                return
            else:
                #切换了内容区域，因此要将特殊区域的数据清空
                self.special_data={}
                for key in self.type_counter:
                    self.type_counter[key] = 0

                form_widget = DynamicFormWidget(data)
                self.current_content_frame[0]  = form_widget
            if form_widget:
                current_menu_id = int(menu_id)
                if current_menu_id not in self.menu_score:
                    logging.info(f"当前menu_score = {self.menu_score} ")
                    logging.info(f"菜单ID {current_menu_id} 不存在于 menu_score 中，可能是父菜单，跳过加载。")
                    return

                current_record = self.menu_score[current_menu_id]
                logging.info(f"<UNK>menu_score = {self.menu_score}-\n-current_record:{current_record} ")
                if not current_record or 'content_value' not in current_record:
                    return
                content_values = current_record['content_value']
                logging.info(f"<UNK>content_value:{content_values} ")
                form_widget.set_values(content_values)
            form_widget2 =self._build_common_form()
            self._set_common_form_data()
            content_area = self.components["content_area"]
            content_area.set_content([form_widget,form_widget2])
        else:
            if self._judge_is_special_menu(menu_name) == 2:
                self.update_content_area_for_special_menu()
                return
            else:
                content_area = self.components["content_area"]
                content_area.set_content([])

    def on_ai_evaluation_finished(self, result):
        evaluation_widget = self.common_frame_widgets[5]
        if isinstance(evaluation_widget, QTextEdit):
            evaluation_widget.setPlainText(result["指标评价"])
        control_widget = self.common_frame_widgets[6]
        if isinstance(control_widget, QLabel):
            control_widget.setText(result["建议得分"])

    def top_button_clicked(self,item):
        logging.debug(item)
        menu_id = item["menuItem"]["menu_id"]
        self.current_menu_id = menu_id
        self.update_content_area()
        self.update_image_area()
        pass

    def bottom_button_clicked(self,item):
        logging.debug(item)
        name = item["按钮名称"]
        if name == "智能分析":
            print(f"suvey_data_work_point_mudslide_page......bottom_button_clicked--{name}")
            self._update_evaluation_content()
        elif name == "导出":
            self.export_data()
        elif name == "AI助手":
            pass
        elif name == "保存":
            self._get_and_update_current_menu_score()
            self.model.upsert_disaster_point_score(self.disaster_point_id,self.current_menu_id,self.menu_score[self.current_menu_id])
            self.update_menu_score()
        pass
    def _init_export_data(self):
        self.exporter.set_file_name("测试")
        self.exporter.set_header(["测试"])
        self.exporter.set_menu_tree_head(self.menu_tree)
        # self.exporter.add_data_row([1, "产品A", 10000, "2025-04-01"])
        # self.exporter.add_data_row([2, "产品B", 15000, "2025-04-02"])
    def export_data(self):
        self._init_export_data()
        self.exporter.export_to_excel()
        pass
    def setup_page(self,**kwargs):
        """设置页面内容 - 统一入口方法"""
        logging.info("--------------begin")
        self.init_mark = 1
        self.setup_left_nav()
        self.setup_top_menu()
        self.setup_content_area()
        self.setup_image_area()
        self.setup_button_area()
        logging.info("--------------end")
