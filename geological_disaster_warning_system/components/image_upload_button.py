# image_uploader/uploader.py

import os
import hashlib
import time
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QFileDialog
)

"""
上传图片组件：

使用方法：
uploader = ImageUploaderButton()
uploader.set_folder("avatars")
uploader.upload_successful.connect(on_upload_success)

layout.addWidget(uploader)
"""
class ImageUploaderButton(QWidget):
    upload_successful = Signal(str)

    def __init__(self, parent=None, folder_name=""):
        super().__init__(parent)

        self.folder_name = folder_name

        # 创建按钮
        self.button = QPushButton("上传图片")
        self.button.setStyleSheet("""
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

        # 连接信号
        self.button.clicked.connect(self.upload_image)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.ensure_images_dir()

    def set_folder(self, folder_name):
        """ 设置图片保存的子文件夹 """
        self.folder_name = folder_name
        self.ensure_images_dir()

    def ensure_images_dir(self):
        """ 确保 images 目录及其子目录存在 """
        base_dir = "images"
        if self.folder_name:
            base_dir = os.path.join(base_dir, self.folder_name)
        os.makedirs(base_dir, exist_ok=True)

    def generate_md5_filename(self):
        """ 使用当前时间生成 MD5 文件名 """
        timestamp = str(time.time()).encode('utf-8')
        md5_hash = hashlib.md5(timestamp).hexdigest()
        return f"{md5_hash}.jpg"

    def get_save_path(self):
        """ 获取图片保存的完整路径和相对路径 """
        base_dir = "images"
        if self.folder_name:
            base_dir = os.path.join(base_dir, self.folder_name)

        filename = self.generate_md5_filename()
        full_path = os.path.join(base_dir, filename)
        relative_path = os.path.join(base_dir, filename)
        return full_path, relative_path

    def upload_image(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "选择图片",
                "",
                "Images (*.png *.xpm *.jpg *.bmp *.gif)"
            )
            if not file_path:
                print("未选择文件，操作取消")
                return

            full_save_path, relative_path = self.get_save_path()

            with open(file_path, 'rb') as src_file:
                with open(full_save_path, 'wb') as dst_file:
                    dst_file.write(src_file.read())

            self.upload_successful.emit(relative_path)

        except Exception as e:
            print("上传图片失败:", e)