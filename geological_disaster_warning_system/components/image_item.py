from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog,
    QDialog, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QMessageBox, QSizePolicy, QApplication
)
from PySide6.QtGui import QPixmap, QIcon, QMouseEvent, QFont, QPainter
from PySide6.QtCore import Signal, Qt, QSize

class ZoomableView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self.setDragMode(QGraphicsView.ScrollHandDrag)  # 支持拖动
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        self.original_pixmap = None  # 原始图像
        self.pixmap_item = None      # 图像项
        self.scale_factor = 1.0
        self.min_scale = 0.1
        self.max_scale = 10.0

    def wheelEvent(self, event):
        # 获取滚轮方向
        delta = event.angleDelta().y()
        if delta > 0:
            factor = 1.2  # 放大
        else:
            factor = 1 / 1.2  # 缩小

        new_scale = self.scale_factor * factor

        # 限制缩放范围
        # if new_scale < self.min_scale or new_scale > self.max_scale:
        #     return

        self.scale(factor, factor)
        self.scale_factor = new_scale

    def setPixmapItem(self, pixmap_item):
        self.pixmap_item = pixmap_item

    def reset_view(self):
        """恢复原始尺寸"""
        self.resetTransform()
        self.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        self.scale_factor = 1.0

    def mouseDoubleClickEvent(self, event):
        """双击恢复原始大小"""
        if event.button() == Qt.LeftButton:
            self.reset_view()
        super().mouseDoubleClickEvent(event)

class ClickableLabel(QLabel):
    """支持点击事件的 QLabel"""
    clicked = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


"""

图片组件。使用方法：

    widget = ImageItemWidget("example.jpg")
    widget.set_item_data({"id": 1, "name": "测试图片"})
    widget.operation_signal.connect(handle_operation)
    layout.addWidget(widget)

def handle_operation(op_type, item_data):
    print(f"操作类型: {op_type}, 数据: {item_data}")

"""



class ImageItemWidget(QWidget):
    # 自定义信号：传递操作类型 ("update" 或 "delete") 和 item_data
    operation_signal = Signal(str, object)

    def __init__(self, image_path=None, parent=None):
        super().__init__(parent)

        if not image_path or QPixmap(image_path).isNull():
            raise ValueError("无效的图片路径")

        self.image_path = image_path
        self.item_data = None  # 存储传入的item数据
        self.default_size = QSize(480, 320)  # 更大一些更美观

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 图片标签（可点击）
        self.image_label = ClickableLabel()
        self.image_label.setFixedSize(self.default_size)
        self.image_label.setScaledContents(True)
        pixmap = QPixmap(self.image_path).scaled(
            self.default_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.image_label.setPixmap(pixmap)
        self.image_label.clicked.connect(self.show_full_image)

        # 按钮布局
        btn_layout = QHBoxLayout()
        self.update_btn = QPushButton("更新")
        self.delete_btn = QPushButton("删除")

        # 设置图标（假设你有资源文件 qrc 或本地图标文件）
        self.update_btn.setIcon(QIcon("icons/update.png"))  # 替换为你自己的图标路径
        self.delete_btn.setIcon(QIcon("icons/delete.png"))

        # 美化按钮样式
        button_style = """
        QPushButton {
            background-color: #f0f0f0;
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 5px 10px;
            font-size: 12px;
        }
        QPushButton:hover {
            background-color: #e0e0e0;
        }
        QPushButton:pressed {
            background-color: #d0d0d0;
        }
        """
        self.update_btn.setStyleSheet(button_style)
        self.delete_btn.setStyleSheet(button_style)

        self.update_btn.clicked.connect(self.on_update_clicked)
        self.delete_btn.clicked.connect(self.on_delete_clicked)

        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)

        # 总体布局
        layout.addWidget(self.image_label)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def set_image_size(self, size: QSize):
        """设置图片显示的大小"""
        self.default_size = size
        self.image_label.setFixedSize(size)
        pixmap = QPixmap(self.image_path).scaled(
            size, Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.image_label.setPixmap(pixmap)

    def show_full_image(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("查看大图")

        # 创建场景和图像项
        scene = QGraphicsScene()
        pixmap = QPixmap(self.image_path)

        if pixmap.isNull():
            QMessageBox.critical(dialog, "错误", "无法加载图片")
            return

        pixmap_item = QGraphicsPixmapItem(pixmap)
        scene.addItem(pixmap_item)

        # 创建自定义可缩放视图
        view = ZoomableView(scene, dialog)
        view.setDragMode(QGraphicsView.ScrollHandDrag)
        view.setBackgroundBrush(Qt.darkGray)  # 设置背景色更美观
        view.setFrameShape(QGraphicsView.NoFrame)  # 去掉边框
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # 初始缩放适配
        # view.fitInView(pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        # view.scale_factor = 1.0

        # 设置视图撑满整个 layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # 去除边距
        layout.addWidget(view)
        dialog.setLayout(layout)

        # 设置合理的窗口大小（不超过屏幕大小）
        screen_rect = QApplication.primaryScreen().availableGeometry()
        max_width = int(screen_rect.width() * 0.9)
        max_height = int(screen_rect.height() * 0.9)

        target_width = min(pixmap.width(), max_width)
        target_height = min(pixmap.height(), max_height)

        dialog.resize(target_width, target_height)

        dialog.exec()
    def set_item_data(self, data: dict):
        """设置与该组件关联的数据项"""
        self.item_data = data

    def on_update_clicked(self):
        """处理更新按钮点击事件"""
        new_path, _ = QFileDialog.getOpenFileName(self, "选择新图片", "", "Images (*.png *.jpg *.bmp)")
        if new_path:
            self.image_path = new_path
            pixmap = QPixmap(self.image_path).scaled(
                self.default_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.image_label.setPixmap(pixmap)
            self.operation_signal.emit("update", self.item_data)

    def on_delete_clicked(self):
        """处理删除按钮点击事件"""
        reply = QMessageBox.question(self, "确认删除", "确定要删除这个图片吗？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.operation_signal.emit("delete", self.item_data)
            self.setParent(None)  # 从父级中移除自己
            self.deleteLater()   # 销毁组件
        self.operation_signal.emit("delete", self.item_data)