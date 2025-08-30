from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QHBoxLayout, QProgressBar)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor


class TestPage2:
    def __init__(self, main_window):
        self.window = main_window
        self.components = main_window.get_components()
        # 设置测试内容
        self.setup_left_nav()
        self.setup_top_menu()
        self.setup_content_area()
        self.setup_image_area()
        self.setup_button_area()

    def setup_left_nav(self):
        """设置左侧导航内容"""
        """设置左侧导航内容"""
        nav = self.components["left_nav"]
        nav.clear_content()
        nav.add_button("基本信息")
        nav.add_button("评估计算")
        nav.add_button("调查数据")
        nav.add_button("测试页面2")
        # 设置当前选中的按钮
        for i in range(nav.layout.count()):
            widget = nav.layout.itemAt(i).widget()
            if isinstance(widget, QPushButton) and widget.text() == "测试页面2":
                widget.setChecked(True)

    def setup_top_menu(self):
        """设置顶部菜单内容"""
        menu = self.components["top_menu"]
        menu.set_content([
            "项目", "任务", "团队", "报告", "设置"
        ])

    def setup_content_area(self):
        """设置内容区域"""
        content = self.components["content_area"]

        # 创建表格内容
        table = QTableWidget()
        table.setRowCount(5)
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["任务名称", "负责人", "进度", "状态"])

        # 填充表格数据
        data = [
            ["UI设计", "张三", 75, "进行中"],
            ["后端开发", "李四", 90, "测试中"],
            ["前端开发", "王五", 60, "进行中"],
            ["测试", "赵六", 30, "未开始"],
            ["部署", "钱七", 0, "未开始"]
        ]

        for row, row_data in enumerate(data):
            for col, cell_data in enumerate(row_data):
                if col == 2:  # 进度列
                    progress = QProgressBar()
                    progress.setValue(cell_data)
                    progress.setStyleSheet("""
                        QProgressBar {
                            border: 1px solid #b0bec5;
                            border-radius: 5px;
                            text-align: center;
                        }
                        QProgressBar::chunk {
                            background-color: #4caf50;
                        }
                    """)
                    table.setCellWidget(row, col, progress)
                else:
                    item = QTableWidgetItem(str(cell_data))
                    item.setTextAlignment(Qt.AlignCenter)
                    table.setCellWidget(row, col, QLabel(str(cell_data)))

        # 设置表格样式
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)

        # 设置内容
        content.set_content([table])

    def setup_image_area(self):
        """设置图片区域"""
        image_area = self.components["image_area"]

        # 创建统计图表
        chart_widget = QWidget()
        chart_layout = QVBoxLayout(chart_widget)

        title = QLabel("项目进度统计 (页面2)")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1565c0;")
        title.setAlignment(Qt.AlignCenter)
        chart_layout.addWidget(title)

        # 添加模拟图表
        chart_data = [
            ("UI设计", 75, "#4caf50"),
            ("后端开发", 90, "#2196f3"),
            ("前端开发", 60, "#ff9800"),
            ("测试", 30, "#f44336"),
            ("部署", 0, "#9e9e9e")
        ]

        for name, value, color in chart_data:
            row = QWidget()
            row_layout = QHBoxLayout(row)

            label = QLabel(name)
            label.setFixedWidth(100)
            row_layout.addWidget(label)

            bar = QProgressBar()
            bar.setValue(value)
            bar.setStyleSheet(f"""
                QProgressBar {{
                    border: 1px solid #b0bec5;
                    border-radius: 3px;
                    text-align: center;
                }}
                QProgressBar::chunk {{
                    background-color: {color};
                }}
            """)
            row_layout.addWidget(bar)

            value_label = QLabel(f"{value}%")
            value_label.setFixedWidth(50)
            row_layout.addWidget(value_label)

            chart_layout.addWidget(row)

        # 设置内容
        image_area.set_content(chart_widget)

    def setup_button_area(self):
        """设置按钮区域"""
        button_area = self.components["button_area"]

        # 自定义按钮
        button_area.set_content([
            ("新建任务", "#4caf50"),
            ("编辑任务", "#2196f3"),
            ("完成任务", "#9c27b0"),
            ("删除任务", "#f44336"),
            ("导出报告", "#ff9800")
        ])
    def setup_page(self,**kwargs):
        """设置页面内容 - 统一入口方法"""
        self.setup_left_nav()
        self.setup_top_menu()
        self.setup_content_area()
        self.setup_image_area()
        self.setup_button_area()