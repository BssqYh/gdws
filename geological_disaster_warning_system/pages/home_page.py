import colorsys
import logging
import random

from PySide6.QtCharts import QChart, QPieSlice, QPieSeries, QChartView
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QLineEdit, QTextEdit, QComboBox, QCheckBox,
                               QFormLayout, QSizePolicy, QDialog, QMainWindow, QTableWidget, QTableWidgetItem,
                               QAbstractItemView, QHeaderView, QHBoxLayout)
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap, QBrush, QPainter, QColor, QLinearGradient, QGradient

from Model.home_page_model import HomePageModel
from utils.utils import MyUtils

logging.basicConfig(format='%(levelname)s:[%(filename)s:%(lineno)d]:%(funcName)s:%(message)s', level=logging.DEBUG)


class HomePage:
    PAGE_NAME = "home_page"
    def __init__(self, main_window):
        self.page_mapping = None
        self.detail_series = None
        self.main_series = None
        self.window = main_window
        self.components = main_window.get_components()
        self.name =""
        self.model = HomePageModel(main_window.get_db_manager())
        self.init_mark = 0

        self.color_pool = self.generate_color_palette(20)
        self.used_colors = {}  # 记录已经使用的颜色类型


        self.pie_data =None
        # 设置测试内容
        self.setup_left_nav()
        self.setup_top_menu()
        self.setup_content_area()
        self.setup_image_area()
        self.setup_button_area()

    def generate_color_palette(self, num_colors):
        """动态生成可扩展的颜色方案"""
        palette = []

        # 使用HSV颜色空间生成基本方案
        for i in range(num_colors):
            # 主色系方案：20度间隔（避免使用0-30度的红色区域）
            hue = ((i * 25) % 360 + 30) % 360
            saturation = 0.7 + random.random() * 0.2  # 饱和度70%-90%
            value = 0.8 + random.random() * 0.15  # 明度80%-95%

            # 转换为RGB
            r, g, b = colorsys.hsv_to_rgb(hue / 360, saturation, value)
            palette.append(QColor(int(r * 255), int(g * 255), int(b * 255)))

        # 为常见灾害类型预留特定颜色
        self.special_colors = {
            '滑坡': QColor('#FF6B6B'),  # 红色系
            '崩塌': QColor('#4ECDC4'),  # 青色系
            '泥石流': QColor('#FFA502'),  # 橙色系
            '地裂缝': QColor('#9B59B6'),  # 紫色系
        }

        return palette

    def get_color_for_type(self, hazard_type):
        """为特定灾害类型获取或分配颜色"""
        # 如果是已知灾害类型，返回预留颜色
        if hazard_type in self.special_colors:
            return self.special_colors[hazard_type]

        # 如果是新灾害类型，分配新颜色
        if hazard_type not in self.used_colors:
            # 如果有可用颜色则使用，否则创建新颜色
            if self.color_pool:
                self.used_colors[hazard_type] = self.color_pool.pop(0)
            else:
                # 动态创建新颜色
                hue = (len(self.used_colors) * 20) % 360
                saturation = 0.6 + random.random() * 0.3
                value = 0.7 + random.random() * 0.2
                r, g, b = colorsys.hsv_to_rgb(hue / 360, saturation, value)
                self.used_colors[hazard_type] = QColor(int(r * 255), int(g * 255), int(b * 255))

        return self.used_colors[hazard_type]

    def create_main_chart(self):
        # 计算每个统一编码的总灾害数
        site_totals = {}
        for site, _, count in self.pie_data:
            site_totals[site] = site_totals.get(site, 0) + count

        # 创建饼图数据系列
        series = QPieSeries()
        series.setPieSize(0.7)
        series.setHoleSize(0.1)

        total_hazards = sum(site_totals.values())

        # 创建颜色渐变方案
        gradient = QLinearGradient(0, 0, 1, 1)
        gradient.setCoordinateMode(QGradient.ObjectMode)
        gradient.setColorAt(0, QColor("#4A90E2"))
        gradient.setColorAt(1, QColor("#2B6CB0"))

        for i, (site, total) in enumerate(site_totals.items()):
            # percentage = (total / total_hazards) * 100
            # slice = QPieSlice(f"{site}\n{total}个({percentage:.1f}%)", total)
            slice = QPieSlice(f"{site}\n{total}个", total)
            slice.setLabelVisible(True)
            slice.setLabelArmLengthFactor(0.15)
            slice.setLabelPosition(QPieSlice.LabelOutside)

            # 使用渐变方案
            slice_color = self.color_pool[i % len(self.color_pool)]
            slice.setBrush(QBrush(slice_color))

            slice.setProperty("site_code", site)  # 存储站点代码
            series.append(slice)

        # 连接信号处理
        series.clicked.connect(self.on_main_slice_clicked)
        series.hovered.connect(self.on_main_slice_hovered)

        # 创建图表
        chart = QChart()
        chart.setTheme(QChart.ChartThemeLight)
        chart.addSeries(series)
        chart.setTitle(f"{self.name}风险项分布")
        title_font = chart.titleFont()  # 获取当前标题字体
        title_font.setPointSize(16)  # 设置字体大小为16
        title_font.setBold(True)  # 设置粗体
        title_font.setFamily("Microsoft YaHei")  # 设置字体类型

        chart.setTitleFont(title_font)
        chart.setTitleBrush(Qt.black)
        chart.legend().setVisible(False)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        self.main_series = series
        # 创建图表视图
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        return chart_view

    def create_detail_chart(self, site_code):
        # 获取该统一编码下的灾害类型数据
        type_counts = {}
        for site, hazard_type, count in self.pie_data:
            if site == site_code:
                type_counts[hazard_type] = type_counts.get(hazard_type, 0) + count

        # 创建饼图数据系列
        series = QPieSeries()
        series.setPieSize(0.7)

        # 添加数据到饼图系列
        total_types = sum(type_counts.values())

        for hazard_type, count in type_counts.items():
            slice = QPieSlice(f"{hazard_type}\n{count}个", count)
            slice.setLabelVisible(True)
            slice.setLabelArmLengthFactor(0.1)
            slice.setLabelPosition(QPieSlice.LabelOutside)

            # 为灾害类型分配颜色
            slice_color = self.get_color_for_type(hazard_type)
            slice.setBrush(QBrush(slice_color))

            series.append(slice)

        series.hovered.connect(self.on_detail_slice_hovered)
        series.clicked.connect(self.on_detail_slice_clicked)
        # 创建图表
        chart = QChart()
        chart.setTheme(QChart.ChartThemeLight)
        chart.addSeries(series)
        chart.setTitle(f"{site_code} 风险项类型统计")

        title_font = chart.titleFont()  # 获取当前标题字体
        title_font.setPointSize(16)  # 设置字体大小为16
        title_font.setBold(True)  # 设置粗体
        title_font.setFamily("Microsoft YaHei")  # 设置字体类型

        chart.setTitleFont(title_font)

        chart.setTitleBrush(Qt.black)
        chart.legend().setVisible(False)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        self.detail_series = series
        
        # 创建图表视图
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        return chart_view

    @Slot(QPieSlice)
    def on_main_slice_clicked(self, slice):
        # 获取站点编码
        site_code = slice.property("site_code")
        if site_code:
            # 显示详细图表
            self.show_detail_chart(site_code)
        else:
            print("错误: 无法获取站点代码")

    @Slot(QPieSlice, bool)
    def on_main_slice_hovered(self, slice, state):
        # 悬停效果 - 突出显示
        slice.setExploded(state)
        if state:
            slice.setExplodeDistanceFactor(0.05)

    @Slot(QPieSlice, bool)
    def on_detail_slice_hovered(self, slice, state):
        # 详情图表悬停效果
        slice.setExploded(state)
        if state:
            slice.setExplodeDistanceFactor(0.05)

    def on_detail_slice_clicked(self):
        self.show_main_chart()

    def setup_left_nav(self):
        """设置左侧导航内容"""
        nav = self.components["left_nav"]
        nav.add_button("项目信息",self.PAGE_NAME)
        nav.add_button("调查数据",self.PAGE_NAME)
        nav.add_button("评估计算",self.PAGE_NAME)
        nav.add_button("数据可视化",self.PAGE_NAME)
        if self.page_mapping is None:
            self.page_mapping = {
                "项目信息": "homepage",
                "评估计算": "",
                "调查数据":"survey_data_page",
                "数据可视化":""
            }

    def setup_top_menu(self):
        """设置顶部菜单内容"""
        menu = self.components["top_menu"]
        text ="欢迎使用"+self.name.split(".")[0]+"地质灾害风险评估系统"
        menu.set_content(text)
        pass
    def show_main_chart(self):
        content = self.components["content_area"]
        if self.init_mark == 1:
            main_chart = self.create_main_chart()
            main_chart_container = QWidget()
            main_chart_layout = QVBoxLayout()
            main_chart_layout.addWidget(main_chart)
            main_chart_container.setLayout(main_chart_layout)
            main_chart_container.setStyleSheet("border: 1px solid #ccc; background-color: white;")
            content.set_content([main_chart_container])
        pass
    def show_detail_chart(self,site_code):
        content = self.components["content_area"]
        if self.init_mark == 1:
            main_chart = self.create_detail_chart(site_code)
            main_chart_container = QWidget()
            main_chart_layout = QVBoxLayout()
            main_chart_layout.addWidget(main_chart)
            main_chart_container.setLayout(main_chart_layout)
            main_chart_container.setStyleSheet("border: 1px solid #ccc; background-color: white;")
            content.set_content([main_chart_container])
        pass

    def show_main_data(self):
        content = self.components["content_area"]
        if self.init_mark == 1:
            data = self.model.get_display_work_point_and_disaster_point_info()
            logging.info(f"开始准备展示数据{data}")

            """
            这个主视图是由多个表合成，第一个表就是。基础信息
            """
            basic_columns = [
                "工点ID", "统一编码", "铁路局", "区间开始站", "区间结束站", "行别", "线别",
                "里程", "省或直辖市", "市", "县或区", "乡或镇", "具体地址", "经度", "纬度",
                "风险评估类型", "风险易发性", "风险评估等级"
            ]

            fixed_column_count = len(basic_columns)
            all_menu_columns = set()
            flat_data = []

            for work_point in data:
                menu_data = work_point.get("menu_data", [])
                extracted_menu = MyUtils.extract_menu_data(menu_data)
                merged_row = {**work_point, **extracted_menu}
                flat_data.append(merged_row)
                all_menu_columns.update(extracted_menu.keys())

            all_menu_columns.discard("menu_data")
            all_menu_columns = list(all_menu_columns)  # 转为列表方便操作

            # 创建主表格和冻结表格容器
            main_widget = QWidget()
            layout = QHBoxLayout(main_widget)
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)

            # 主表格
            main_table = QTableWidget()
            main_table.setRowCount(len(flat_data))

            # 冻结表格
            frozen_table = QTableWidget()
            frozen_table.setRowCount(len(flat_data))

            # 主表只显示 menu_data 字段
            main_table.setColumnCount(len(all_menu_columns))
            main_table.setHorizontalHeaderLabels(all_menu_columns)

            # 冻结表只显示基础字段
            frozen_table.setColumnCount(fixed_column_count)
            frozen_table.setHorizontalHeaderLabels(basic_columns)

            # 公共设置
            for table in [main_table, frozen_table]:
                table.verticalHeader().setVisible(False)
                table.setSelectionBehavior(QAbstractItemView.SelectRows)
                table.setEditTriggers(QTableWidget.NoEditTriggers)
                table.setStyleSheet("""
                       QTableWidget::item:selected {
                           background-color: #d4ecff;
                           color: black;
                       }
                   """)

            # 同步选中行
            def sync_selection(selected, _):
                row = selected.top()
                main_table.selectRow(row)
                frozen_table.selectRow(row)

            frozen_table.clicked.connect(sync_selection)
            main_table.clicked.connect(sync_selection)

            # 同步滚动条
            frozen_table.verticalScrollBar().valueChanged.connect(
                lambda value: main_table.verticalScrollBar().setValue(value)
            )
            main_table.verticalScrollBar().valueChanged.connect(
                lambda value: frozen_table.verticalScrollBar().setValue(value)
            )

            # 填充数据
            for row, work_point in enumerate(flat_data):
                # 填充冻结表（基础字段）
                for col, key in enumerate(basic_columns):
                    value = str(work_point.get(key, ""))
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(Qt.AlignCenter)
                    frozen_table.setItem(row, col, item)

                # 填充主表（menu_data 字段）
                for col, key in enumerate(all_menu_columns):
                    value = str(work_point.get(key, ""))
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(Qt.AlignCenter)
                    main_table.setItem(row, col, item)

            # 设置列宽
            header = main_table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeToContents)

            for col in range(len(basic_columns)):
                width = main_table.columnWidth(col)
                max_width = 150
                if width > max_width:
                    width = max_width
                main_table.setColumnWidth(col, width)

            for col in range(fixed_column_count):
                width = frozen_table.columnWidth(col)
                max_width = 150
                if width > max_width:
                    width = max_width
                frozen_table.setColumnWidth(col, width)

            # 设置冻结列宽度不可变
            frozen_table.horizontalHeader().setSectionsMovable(False)
            frozen_table.verticalHeader().setDefaultSectionSize(main_table.verticalHeader().defaultSectionSize())
            # 添加到布局
            layout.addWidget(frozen_table)
            layout.addWidget(main_table)
            content.set_content([main_widget])

    def setup_content_area(self):
        # self.pie_data = self.model.get_work_point_diaster_type()
        # self.show_main_chart()
        self.show_main_data()

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

    def lef_nav_button_clicked(self,item):
        """"""
        """每个页面自己实现自己的各个点击事件"""
        button_text = item["按钮名称"]
        logging.debug(button_text)
        self.window.get_page_manager().switch_page(self.page_mapping[button_text])
        nav = self.components["left_nav"]
        nav.set_current_button_checked()
        pass

    def bottom_button_clicked(self,item):
        print("home_page......bottom_button_clicked")
        pass

    def setup_button_area(self):
        """设置按钮区域"""
        button_area = self.components["button_area"]

        # 自定义按钮
        button_area.set_content([
            ("保存", "#4caf50"),
            ("重置", "#ff9800"),
            ("删除", "#f44336"),
            ("导出", "#9c27b0"),
            ("帮助", "#2196f3")
        ])
    def setup_page(self,**kwargs):
        """设置页面内容 - 统一入口方法"""
        self.name = kwargs["db_name"].split(".")[0]
        self.init_mark = 1
        # self.window.set_middle_components_stretch(self.components["content_area"], 5)
        # self.window.set_middle_components_stretch(self.components["image_area"], 0)
        self.window.display_left_top_content_area()
        self.setup_left_nav()
        self.setup_top_menu()
        self.setup_content_area()
        self.setup_image_area()
        self.setup_button_area()