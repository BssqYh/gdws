import logging

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QFrame,
    QSizePolicy, QPushButton, QVBoxLayout,
    QSpacerItem
)
from PySide6.QtCore import Qt, Signal
"""

使用方法：
data = self.model.get_collapse_first_menu()
[{'id': 1, 'menu_id': 1, 'menu_name': '灾害易发性指标'},
{'id': 2, 'menu_id': 2, 'menu_name': '灾害抑制性指标'}]

for item in data:
    menu.add_first_level_menu_button(item["menu_id"],item["menu_name"],"collapse")
data = self.model.get_collapse_second_menu()
[{'id': 3, 'parent_id': 1, 'menu_id': 3, 'menu_name': '地质环境'}, 
{'id': 4, 'parent_id': 1, 'menu_id': 4, 'menu_name': '危岩体状态'}, 
{'id': 5, 'parent_id': 2, 'menu_id': 5, 'menu_name': '挡护范围'},
{'id': 6, 'parent_id': 2, 'menu_id': 6, 'menu_name': '挡护形式适宜性'},
{'id': 7, 'parent_id': 2, 'menu_id': 7, 'menu_name': '拦石墙状态'}, 
{'id': 8, 'parent_id': 2, 'menu_id': 8, 'menu_name': '边坡柔性防护网系统状态'}]

for item in data:
    menu.add_second_level_menu_button(item["menu_id"], item["menu_name"],parent_id=item["parent_id"], root_name="collapse")
data = self.model.get_collapse_third_menu()
for item in data:
    menu.add_third_level_menu_button(item["menu_id"], item["menu_name"], parent_id=item["parent_id"], root_name="collapse")
data = self.model.get_collapse_fourth_menu()
for item in data:
    menu.add_fourth_level_menu_button(item["menu_id"], item["menu_name"], parent_id=item["parent_id"], root_name="collapse")
menu.show_menu_by_root("collapse")

"""
logging.basicConfig(format='%(levelname)s:[%(filename)s:%(lineno)d]:%(funcName)s:%(message)s', level=logging.DEBUG)
class TopMenu(QFrame):
    top_menu_button_clicked = Signal(dict)  # 按钮点击信号

    def __init__(self):
        super().__init__()
        # 存储菜单数据：{root_name: {level: {parent_id: {menu_id: button}}}}
        self.menu_cache = {}  # 多 root 支持
        self.current_root = "default"  # 当前操作的 root 名称
        self.visible_levels = 1  # 当前可见的层级数
        self.current_parents = {1: 0}  # 当前每级菜单的父菜单ID

        # 初始化默认 root
        self._init_root(self.current_root)

        # 设置样式
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("background-color: #c8e6c9; border: 1px solid #a5d6a7;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setFixedHeight(60)  # 初始高度

        # 主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(0)

        # 内容标签
        self.content_label = QLabel()
        self.content_label.setAlignment(Qt.AlignCenter)
        self.content_label.setVisible(False)
        self.content_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.main_layout.addWidget(self.content_label)

        # 创建四层菜单容器
        self.menu_levels = {}
        for level in range(1, 5):
            # 每一级菜单的容器
            level_widget = QWidget()
            level_layout = QHBoxLayout(level_widget)
            level_layout.setContentsMargins(5, 5, 5, 5)
            level_layout.setAlignment(Qt.AlignLeft)

            # 左侧的标题标签
            text = ""
            if level == 1:
                text = "一级指标"
            elif level == 2:
                text = "二级指标"
            elif level == 3:
                text = "三级指标"
            elif level == 4:
                text = "四级指标"
            title_label = QLabel(text)
            title_label.setStyleSheet("font-weight: bold; color: #2e7d32;")
            level_layout.addWidget(title_label)

            # 菜单项容器
            buttons_container = QHBoxLayout()
            buttons_container.setAlignment(Qt.AlignLeft)
            buttons_container.setSpacing(10)
            level_layout.addLayout(buttons_container)

            # 右侧弹簧
            spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            level_layout.addItem(spacer)

            # 将容器添加到主布局
            self.main_layout.addWidget(level_widget)
            self.menu_levels[level] = {
                'widget': level_widget,
                'title': title_label,
                'container': buttons_container
            }

        # 默认只显示一级菜单
        for level in [2, 3, 4]:
            self.menu_levels[level]['widget'].setVisible(False)

    def set_content(self, text):
        """设置内容模式，只显示一行文本"""
        # 隐藏所有菜单
        for level in [1, 2, 3, 4]:
            self.menu_levels[level]['widget'].setVisible(False)

        # 显示内容标签
        self.content_label.setText(text)
        self.content_label.setVisible(True)

        # 调整高度
        self.setFixedHeight(40)

    def clear_content(self):
        """切换回菜单模式"""
        self.content_label.setVisible(False)
        for tmp_level in [1, 2, 3, 4]:
            self.menu_levels[tmp_level]['widget'].setVisible(tmp_level == 1)
        self.setFixedHeight(60)

    def _create_button(self, text, level, menu_id, parent_id=0):
        """创建菜单按钮"""
        btn = QPushButton(text)
        btn.setProperty('menu_level', level)
        btn.setProperty('menu_id', menu_id)
        btn.setProperty('parent_id', parent_id)
        btn.setStyleSheet(self._get_button_style(level))
        btn.setFixedHeight(35)
        btn.clicked.connect(self._handle_button_click)
        return btn

    def _get_button_style(self, level):
        """根据层级返回按钮样式"""
        colors = {
            1: "#4db6ac",  # 青绿色
            2: "#81c784",  # 浅绿色
            3: "#aed581",  # 黄绿色
            4: "#dce775"  # 柠檬黄
        }

        border_colors = {
            1: "#00897b",
            2: "#43a047",
            3: "#7cb342",
            4: "#c0ca33"
        }

        return f"""
            QPushButton {{
                background-color: {colors.get(level, "#ffffff")};
                color: #000000;
                border: 1px solid {border_colors.get(level, "#a5d6a7")};
                border-radius: 4px;
                padding: 5px 8px;
                min-width: 70px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: #e8f5e9;
            }}
            QPushButton:checked {{
                background-color: {border_colors.get(level, "#00897b")};
                color: white;
                font-weight: bold;
            }}
        """

    def _handle_button_click(self):
        """处理菜单按钮点击事件"""
        btn = self.sender()
        level = btn.property('menu_level')
        menu_id = btn.property('menu_id')
        parent_id = btn.property('parent_id')
        text = btn.text()
        display_content = 1
        root_cache = self.menu_cache[self.current_root]
        logging.info(f"[点击] 当前层级={level}, menu_id={menu_id}, parent_id={parent_id}, 当前root={self.current_root}")
        # 如果是一级菜单点击
        if level == 1:
            if text not in ("详情", "增加"):
                # 清除所有下级菜单
                self.clear_levels_below(2)
                self.visible_levels = 1

                # 设置当前一级菜单ID
                self.current_parents[1] = menu_id
                # DEBUG 输出
                logging.info(f"[点击] 检查是否存在二级菜单：{menu_id} 是否在 root_cache[2].keys()？")
                logging.info(f"存在的二级菜单 parent_id 列表: {list(root_cache[2].keys())}")
                # 检查是否有二级菜单
                if menu_id in root_cache[2]:
                    self._show_level(2, menu_id)
                    self.visible_levels = 2
                    display_content =0

        # 如果是二级菜单点击
        elif level == 2:
            # 清除所有下级菜单
            self.clear_levels_below(3)
            self.visible_levels = 2

            # 检查是否有三级菜单
            if menu_id in root_cache[3]:
                self._show_level(3, menu_id)
                self.visible_levels = 3
                display_content =0

        # 如果是三级菜单点击
        elif level == 3:
            # 清除所有下级菜单
            self.clear_levels_below(4)
            self.visible_levels = 3

            # 检查是否有四级菜单
            if menu_id in root_cache[4]:
                self._show_level(4, menu_id)
                self.visible_levels = 4
                display_content =0

        if text not in ("详情", "增加"):
            # 更新高度
            self.setFixedHeight(60 * self.visible_levels)

        # 如果有子菜单，那么display_content 为0，如果没有，那么就是1，直接显示
        item = {"按钮名称": text, "display_content":display_content,"menuItem": {"menu_id": menu_id}}
        self.top_menu_button_clicked.emit(item)

    def clear_levels_below(self, start_level):
        """清除指定层级以下的菜单"""
        for level in range(start_level, 5):
            # 清除容器内容
            container = self.menu_levels[level]['container']
            while container.count():
                child = container.takeAt(0)
                if child.widget():
                    child.widget().setParent(None)

            # 隐藏容器
            self.menu_levels[level]['widget'].setVisible(False)

    def _show_level(self, level, parent_id):
        """显示指定层级的菜单"""
        root_cache = self.menu_cache[self.current_root]
        # 获取父菜单的子菜单
        menu_items = root_cache[level].get(parent_id, {})

        # 清除当前层级容器的内容
        container = self.menu_levels[level]['container']
        while container.count():
            child = container.takeAt(0)
            if child.widget():
                child.widget().setParent(None)

        # 添加菜单项
        for menu_id, btn in menu_items.items():
            container.addWidget(btn)

        # 显示容器
        self.menu_levels[level]['widget'].setVisible(True)

    def _init_root(self, root_name):
        """初始化某个 root_name 的菜单缓存"""
        if root_name not in self.menu_cache:
            self.menu_cache[root_name] = {
                level: {} for level in range(1, 5)
            }
            self.menu_cache[root_name][1][0] = {}  # 一级菜单直接挂 parent_id=0

    def set_current_root(self, root_name):
        """设置当前操作的 root_name"""
        self.current_root = root_name
        self._init_root(root_name)

    def show_menu_by_root(self, root_name):
        """显示指定 root_name 的菜单树"""
        self.clear_content()
        self.current_root = root_name
        self._init_root(root_name)

        # 清除当前显示的所有菜单
        self.clear_levels_below(1)

        root_cache = self.menu_cache[self.current_root]
        # 显示一级菜单
        if 0 in root_cache[1]:
            for btn in root_cache[1][0].values():
                self.menu_levels[1]['container'].addWidget(btn)
            self.menu_levels[1]['widget'].setVisible(True)
            self.setFixedHeight(60)

    def add_first_level_menu_button(self, menu_id, text, root_name):
        """添加一级菜单按钮，并指定所属 root_name"""
        if root_name is None:
            root_name = self.current_root
        self.current_root = root_name
        self._add_menu_button(root_name, 1, menu_id, text, 0)

    def add_second_level_menu_button(self, menu_id, text, parent_id, root_name=None):
        """添加二级菜单按钮"""
        self._add_menu_button(root_name, 2, menu_id, text, parent_id)

    def add_third_level_menu_button(self, menu_id, text, parent_id, root_name=None):
        """添加三级菜单按钮"""
        self._add_menu_button(root_name, 3, menu_id, text, parent_id)

    def add_fourth_level_menu_button(self, menu_id, text, parent_id, root_name=None):
        """添加四级菜单按钮"""
        self._add_menu_button(root_name, 4, menu_id, text, parent_id)

    def _add_menu_button(self, root_name, level, menu_id, text, parent_id):
        """添加菜单按钮到缓存，按 root_name 隔离"""
        self._init_root(root_name)  # 确保该 root 存在

        # 切换回菜单模式
        if self.content_label.isVisible():
            self.content_label.setVisible(False)
            for tmp_level in [1, 2, 3, 4]:
                self.menu_levels[tmp_level]['widget'].setVisible(tmp_level == 1)
            self.setFixedHeight(60)

        root_cache = self.menu_cache[root_name]

        # 创建或获取按钮
        if parent_id in root_cache[level] and menu_id in root_cache[level][parent_id]:
            btn = root_cache[level][parent_id][menu_id]
            btn.setText(text)
        else:
            btn = self._create_button(text, level, menu_id, parent_id)

            # 存储到缓存
            if parent_id not in root_cache[level]:
                root_cache[level][parent_id] = {}
            root_cache[level][parent_id][menu_id] = btn

        # 如果是一级菜单，直接显示
        if level == 1:
            container = self.menu_levels[1]['container']
            found = False
            for i in range(container.count()):
                item = container.itemAt(i)
                if item.widget() is btn:
                    found = True
                    break
            if not found:
                container.addWidget(btn)

            self.menu_levels[1]['widget'].setVisible(True)