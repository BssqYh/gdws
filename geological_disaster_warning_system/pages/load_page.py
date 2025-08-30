import ctypes
import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QDialog, QDialogButtonBox, QFileDialog, QMessageBox, QSpacerItem, QSizePolicy, QSystemTrayIcon
)
from PySide6.QtGui import QPixmap, QFont, QPainter, QBrush, QColor, QIcon
from PySide6.QtCore import Qt, QSize
from PySide6.QtSql import QSqlDatabase

from components.create_project import ProjectFormDialog
from utils.utils import MyUtils


class LoadPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_window = None
        self.setWindowTitle("地质灾害风险评估系统")
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon(":/resources/icon.ico"))

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(":/resources/icon.ico")

        # 创建主窗口部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 主布局 - 使用垂直布局确保内容居中
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setSpacing(40)

        # 添加上方弹性空间，使内容垂直居中
        self.main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # 标题标签
        self.title_label = QLabel("欢迎使用地质灾害风险评估系统")
        self.title_label.setFont(QFont("Microsoft YaHei", 24, QFont.Bold))
        self.title_label.setStyleSheet("""
            color: #2c3e50;
            background-color: rgba(180, 255, 180, 180);
            padding: 15px;
            border-radius: 10px;
        """)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setMinimumSize(600, 80)  # 设置最小尺寸确保文本完整显示

        # 进入系统按钮
        self.enter_button = QPushButton("进入系统")
        self.enter_button.setFont(QFont("Microsoft YaHei", 16))
        self.enter_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 15px 30px;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
        """)
        self.enter_button.setFixedSize(200, 60)
        self.enter_button.clicked.connect(self.show_database_dialog)

        # 创建垂直容器，确保标签和按钮一起居中
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setAlignment(Qt.AlignCenter)
        self.content_layout.setSpacing(40)
        self.content_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        self.content_layout.addWidget(self.enter_button, alignment=Qt.AlignCenter)

        # 将内容容器添加到主布局
        self.main_layout.addWidget(self.content_container, alignment=Qt.AlignCenter)

        # 添加下方弹性空间，使内容垂直居中
        self.main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # 底部信息
        self.bottom_label = QLabel("© 2025 地质灾害风险评估系统 | 版本 1.0.0")
        self.bottom_label.setFont(QFont("Microsoft YaHei", 13))
        self.bottom_label.setStyleSheet("""
            color: #2c3e50;
            background-color: rgba(180, 200, 180, 180);
            padding: 15px;
            border-radius: 10px;
        """)
        self.bottom_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.bottom_label)

        # 加载背景图片
        self.background_image = QPixmap(":/resources/background.png")
        if self.background_image.isNull():
            # 如果没有图片资源，创建渐变背景
            self.background_image = QPixmap(1, 1)
            self.background_image.fill(QColor("#f0f2f5"))

    def paintEvent(self, event):
        """绘制自适应背景图片"""
        painter = QPainter(self)

        # 计算缩放后的图片尺寸
        scaled = self.background_image.scaled(
            self.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )

        # 计算绘制位置使图片居中
        x = (self.width() - scaled.width()) / 2
        y = (self.height() - scaled.height()) / 2

        # 绘制背景
        painter.drawPixmap(int(x), int(y), scaled)

        # 添加半透明覆盖层
        # painter.setBrush(QBrush(QColor(255, 255, 255, 200)))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        super().paintEvent(event)
    def set_main_window(self, main_window):
        self.main_window = main_window

    def show_database_dialog(self):
        """显示数据库选择对话框"""
        dialog = DatabaseDialog(self)
        dialog.set_main_window(self.main_window)
        if dialog.exec() == QDialog.Accepted:
            db_path = dialog.selected_db_path
            if db_path:
                self.open_database(db_path)

    def open_database(self, db_path):
        """打开数据库文件"""
        # 创建SQLite数据库连接
        # db = QSqlDatabase.addDatabase("QSQLITE")
        # db.setDatabaseName(db_path)
        # if db.open():
        #这里不打开，需要的时候才打开
        if 1 :
            info = f"项目打开"
            box = QMessageBox(QMessageBox.Information, self.tr("项目打开成功"), self.tr(info), QMessageBox.NoButton,self)
            yr_btn = box.addButton(self.tr("进入系统"), QMessageBox.YesRole)
            box.addButton(self.tr("返回"), QMessageBox.NoRole)
            box.exec_()
            if box.clickedButton() == yr_btn:
                self.hide()
                self.main_window.main_window_show(db_path)
                return
            else:
                print("...")
            # 这里可以添加页面跳转逻辑
            # self.show_main_application()
        else:
            QMessageBox.critical(
                self,
                "项目打开失败",
                f"无法打开项目文件:\n{db_path}\n\n"
                f"错误信息: {db.lastError().text()}"
            )


class DatabaseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.project_form_widget = None
        self.main_window = None
        self.setWindowTitle("项目操作")
        self.setFixedSize(400, 250)
        self.selected_db_path = None

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)  # 确保对话框内容居中

        # 对话框标题
        title_label = QLabel("选择项目操作")
        title_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")

        # 新建数据库按钮
        new_db_button = QPushButton("新建项目")
        new_db_button.setFont(QFont("Microsoft YaHei", 12))
        new_db_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 12px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #219653;
            }
        """)
        new_db_button.clicked.connect(self.create_new_database)

        # 打开数据库按钮
        open_db_button = QPushButton("打开已有项目")
        open_db_button.setFont(QFont("Microsoft YaHei", 12))
        open_db_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 12px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
        """)
        open_db_button.clicked.connect(self.open_existing_database)

        # 按钮容器 - 使用垂直布局确保按钮居中
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setSpacing(15)
        button_layout.addWidget(new_db_button)
        button_layout.addWidget(open_db_button)

        # 添加到布局
        layout.addWidget(title_label)
        layout.addWidget(button_container, alignment=Qt.AlignCenter)

    def show_load_page(self):
        self.show()

    def create_new_database(self):
        """创建新数据库（暂未实现）"""
        # QMessageBox.information(
        #     self,
        #     "新建项目",
        #     "新建项目功能正在开发中，敬请期待！"
        # )
        dialog = ProjectFormDialog(self)  # 创建对话框
        dialog.setWindowModality(Qt.WindowModal)  # 模态：阻塞父窗口
        dialog.project_created.connect(lambda name, path: print(f"✅ 成功: {name} -> {path}"))
        dialog.project_creation_failed.connect(lambda err: print(f"❌ 失败: {err}"))

        if dialog.exec() == QDialog.Accepted:
            # 获取返回结果
            project_name, db_path = dialog.get_result()

            # 处理创建成功逻辑
            box = QMessageBox(
                QMessageBox.Information,
                "项目创建成功",
                f"项目 '{project_name}' "
                f"路径'{db_path}' "
                f"已创建，是否进入系统？",
                QMessageBox.NoButton,
                self
            )
            enter_btn = box.addButton("进入系统", QMessageBox.YesRole)
            back_btn = box.addButton("返回", QMessageBox.NoRole)
            box.exec_()

            if box.clickedButton() == enter_btn:
                # 进入主系统（假设你生成或保存了 .gdws 文件）
                # db_path = ...
                # self.selected_db_path = db_path
                self.accept()  # 关闭当前 DatabaseDialog
                self.main_window.main_window_show(db_path)
            # else: 用户点“返回”，继续停留
        else:
            # 用户取消
            print("用户取消了新建项目")


    def set_main_window(self,main_window):
        self.main_window = main_window

    def open_existing_database(self):
        """打开已有数据库"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "打开项目文件",
            "",
            "地质灾害项目文件 (*.gdws);;所有文件 (*)"
        )

        if file_path:
            # 验证文件扩展名
            if not file_path.lower().endswith('.gdws'):
                info = f"您选择文件格式不对:\n\n{file_path}\n\n"f"请重新选择！"
                box = QMessageBox(QMessageBox.Warning, self.tr("项目打开失败"), self.tr(info),
                                  QMessageBox.NoButton, self)
                yr_btn = box.addButton(self.tr("我知道了"), QMessageBox.YesRole)
                box.addButton(self.tr("返回"), QMessageBox.NoRole)
                box.exec_()
                if box.clickedButton() == yr_btn:
                    print("...")
                    return
                else:
                    print("...")
                    return
            self.selected_db_path = file_path
            self.accept()