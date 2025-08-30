import logging

from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, Signal

from components.add_disaster_point_dialog import DisasterPointInfoDialog
from components.loading_spinner import LoadingSpinner
from components.table_select_dialog import TableSelectDialog
from components.task_worker import TaskWorker
from utils.utils import MyUtils

logging.basicConfig(format='%(levelname)s:[%(filename)s:%(lineno)d]:%(funcName)s:%(message)s', level=logging.DEBUG)

"""
所有页面的父类
其中：
1.setup_left_nav 子类不用管，因为每个页面左边显示是一样的。
2.子类自己实现的方法：
has_dynamic_disaster_buttons：决定是否显示风险按钮。即动态按钮。
self.setup_top_menu() ：顶部菜单区域，子类自己实现
self.setup_content_area() ：内容区域，子类自己实现
self.setup_image_area()：：图片区域，子类自己实现
self.setup_button_area()：：底部按钮区域，子类自己实现，并且需要自己实现对应的响应事件。
on_set_data：当页面切换的时候，会调用set_data方法存储工点、风险点。如果子类有自己的需求，则实现这个方法。
"""
class MyBasePage:
    button_clicked = Signal(dict)

    def __init__(self, main_window):
        self.disasterPointInfoDialog = None
        self.window = main_window
        self.components = main_window.get_components()
        self.model = self.create_model(main_window)
        self.base_button_index = 0
        self.work_point_id = 0
        self.disaster_point_id = 0
        self.nav_button_cnt = 0
        self._init_ui()
        self._current_worker = TaskWorker()
        self._current_worker.finished.connect(self.on_save_done)
        self._setup_add_diaster_dialog() #增加风险对话框
        self.page_mapping = {
            "基本信息": "survey_data_work_point_base_info_page",
            "地质环境条件": "survey_data_work_point_di_zhi_tiao_jian_page",
            "气象条件": "survey_data_work_point_qi_xiang_tiao_jian_page",
            "崩塌": "survey_data_work_point_collapse_page",
            "滑坡": "survey_data_work_point_mudslide_page",
            "泥石流": "survey_data_work_point_debris_flow_page",
            "地裂缝": "survey_data_work_point_grand_fissure_page",
            "增加风险项": "",
            "返回": "survey_data_page",

            "项目信息": "homepage",
            "评估计算": "",
            "调查数据": "survey_data_page",
            "数据可视化": ""
        }

    def create_model(self, main_window):
        raise NotImplementedError

    def _init_ui(self):
        """初始化 UI 入口"""
        self.setup_left_nav()
        self.setup_top_menu()
        self.setup_content_area()
        self.setup_image_area()
        self.setup_button_area()

    def _setup_add_diaster_dialog(self):
        self.add_diaster_dialog = TableSelectDialog()
        diaster_info = self.model.get_disaster_info()
        logging.info(f"diaster info: {diaster_info}")
        for diaster in diaster_info:
            logging.info(f"diaster: {diaster['name']}-{diaster['db_name']}")
            self.add_diaster_dialog.add_button(diaster['name'], diaster['db_name'])
        self.add_diaster_dialog.table_selected.connect(self._handle_add_disaster_selected)

    def save_disaster_point(self,data):
        re = self.model.upsert_disaster_point_info(data, self.work_point_id)
        self.model.update_all_disaster_point_data(self.work_point_id)
        self.nav_button_cnt = self.model.get_work_point_disaster_count(self.work_point_id)

    def on_save_done(self, result):
        spinner = LoadingSpinner.instance()
        spinner.stop_animate()  # 动画结束
        self.setup_left_nav()


    def _handle_add_disaster_selected(self,item):
        name = item["name"]
        logging.info(f"<UNK><UNK>-点击了增加-{name}<UNK>")
        menu_value = self.model.get_display_work_point_info(self.work_point_id)
        if self.disasterPointInfoDialog is None:
            menu_data = self.model.get_work_point_common_content(73)
            self.disasterPointInfoDialog = DisasterPointInfoDialog(menu_data)
        menu_value[0]['风险评估类型'] = name
        logging.info(f"<UNK><UNK>-<UNK>-{ menu_value[0]}<UNK>")
        self.disasterPointInfoDialog.set_form_data(menu_value[0])

        data = self.disasterPointInfoDialog.show_dialog()
        if data:
            self._current_worker.set_task(lambda: self.save_disaster_point(data))
            self._current_worker.start()
            spinner = LoadingSpinner.instance()
            spinner.start_animate("正在保存...")


    def set_data(self, work_point_id, disaster_point_id):
        """设置工点ID和风险点ID"""
        self.work_point_id = work_point_id
        self.disaster_point_id = disaster_point_id
        self.nav_button_cnt = self.model.get_work_point_disaster_count(work_point_id)
        self.on_set_data(work_point_id, disaster_point_id)

    def setup_page(self, **kwargs):
        pass

    def on_set_data(self, work_point_id, disaster_point_id):
        """子类可重写此方法以执行额外初始化逻辑"""
        pass

    def setup_left_nav(self):
        """统一左侧导航栏构建逻辑"""
        nav = self.components["left_nav"]
        nav.clear_content()
        # 默认基础按钮
        base_buttons = ["基本信息", "地质环境条件", "气象条件"]
        for btn_text in base_buttons:
            nav.add_button(btn_text)
        self.base_button_index = len(base_buttons)
        # 固定按钮
        self.update_left_nav_with_dynamic_disaster_buttons()
        nav.add_button("增加风险项")
        nav.add_button("返回")

    def update_left_nav_with_dynamic_disaster_buttons(self):
        if not self.has_dynamic_disaster_buttons():
            return
        nav = self.components["left_nav"]
        data = self.model.get_all_disaster_point_data(self.work_point_id)
        disaster_dict = self.model.get_disaster_info()
        insert_index = self.base_button_index
        for i in range(self.nav_button_cnt):
            item = data[i]
            disaster_name = next((info["name"] for info in disaster_dict if info["id"] == item["风险评估类型"]), "")
            if item['里程K'] is None or item['里程K']=="":
                text= text = f"风险项{i + 1}-等待完善-{disaster_name}"
            else:
                text = f"风险项{i + 1}-{item['里程K']}{item['里程开始位置']}{item['里程结束位置']}-{disaster_name}"
            if insert_index is not None:
                logging.info(f"work point {self.work_point_id}插入{insert_index}:按钮： {text}")
                nav.insert_button(insert_index + i, text, item)
    def get_page_mapping(self):
        return

    def has_dynamic_disaster_buttons(self):
        return self.nav_button_cnt != 0

    def setup_top_menu(self):
        pass

    def setup_content_area(self):
        pass

    def setup_image_area(self):
        pass

    def setup_button_area(self):
        pass

    def top_button_clicked(self, item):
        pass

    def lef_nav_button_clicked(self, item):
        button_text = item["按钮名称"]
        tmp_button_text = ["基本信息", "地质环境条件", "气象条件", "返回"]
        survey_button_text = ["项目信息", "调查数据", "评估计算", "数据可视化"]
        if button_text in tmp_button_text:
            self.window.get_page_manager().switch_page(
                self.page_mapping[button_text],
                work_point_id=self.work_point_id,
                disaster_point_id=self.disaster_point_id
            )
        elif button_text in survey_button_text:
            self.window.get_page_manager().switch_page(self.page_mapping[button_text])
        elif button_text == "增加风险项":
            self.add_diaster_dialog.popup()
        else:
            re_text = button_text.split("-")[2]
            menu_item = item["menuItem"]
            self.window.get_page_manager().switch_page(
                self.page_mapping[re_text],
                work_point_id=menu_item["工点ID"],
                disaster_point_id=menu_item["风险点ID"]
            )
        nav = self.components["left_nav"]
        nav.set_current_button_checked()

    def bottom_button_clicked(self, item):
        pass