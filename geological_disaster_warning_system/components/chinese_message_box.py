from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt

"""
中文消息框。
使用方法：
1.只需要一个按钮：
result = ChineseMessageBox.show_message("提示", "这是一个单按钮提示框", button0="知道了", parent=self)
2.两个按钮：
result = ChineseMessageBox.show_message(
    "项目打开成功",
    "项目打开",
    button0="进入系统",
    button1="返回",
    parent=self
)

if result == 0:
    self.hide()
    self.main_window.main_window_show(db_path)
else:
    print("用户点击了 返回")

"""
class ChineseMessageBox(QDialog):
    def __init__(self, title, message, button0_text=None, button1_text=None, parent=None):
        """
        :param title: 对话框标题
        :param message: 提示信息
        :param button0_text: 第一个按钮文本（主按钮）
        :param button1_text: 第二个按钮文本（可选）
        :param parent: 父窗口
        """
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowModality(Qt.ApplicationModal)
        self.result = None  # 存储用户点击的按钮索引

        layout = QVBoxLayout(self)

        # 消息标签
        self.label = QLabel(message)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # 按钮布局
        button_layout = QHBoxLayout()

        if button0_text:
            self.button0 = QPushButton(button0_text)
            self.button0.clicked.connect(lambda: self.done(0))
            button_layout.addWidget(self.button0)

        if button1_text:
            self.button1 = QPushButton(button1_text)
            self.button1.clicked.connect(lambda: self.done(1))
            button_layout.addWidget(self.button1)

        layout.addLayout(button_layout)

    @staticmethod
    def show_message(title, message, button0="确定", button1=None, parent=None):
        """
        静态方法显示对话框
        :param title: 标题
        :param message: 提示内容
        :param button0: 主按钮文本（必填）
        :param button1: 副按钮文本（可选）
        :param parent: 父窗口
        :return: 用户点击的按钮索引（0 或 1）
        """
        dialog = ChineseMessageBox(title, message, button0, button1, parent)
        result_code = dialog.exec_()
        return result_code  # 返回 0 或 1