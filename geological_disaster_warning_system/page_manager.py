import logging
from time import sleep

from PySide6.QtCore import QObject, Signal

from pages.load_page import LoadPage


class PageManager(QObject):
    """管理页面切换的类"""
    page_changed = Signal(str)  # 页面改变信号

    def __init__(self,main_window):
        super().__init__()
        self.main_window = main_window
        self.pages = {}  # 存储所有页面 {page_name: page_instance}
        self.page_cache = {}
        self.current_page = None
        self.current_page_instance = None  # 当前页面实例
        self.current_page_name = None

    def register_page(self, name: str, page_class):
        """注册页面"""
        self.pages[name] = page_class

    def get_page(self, name):
        """获取页面实例"""
        return self.pages.get(name)

    def get_cached_page(self, page_name):
        """获取缓存的页面实例"""
        # 如果页面已在缓存中，直接返回
        if page_name in self.page_cache:
            logging.info(f"使用缓存页面: {page_name}")
            return self.page_cache[page_name]
        # 创建新页面实例
        logging.info(f"创建新页面: {page_name}")
        page_instance = self.pages[page_name](self.main_window)
        # 添加到缓存
        self.page_cache[page_name] = page_instance
        return page_instance

    def switch_page(self, page_name,**kwargs):
        """切换到指定页面"""
        if page_name in self.pages:
            # 创建新页面实例
            page = self.pages[page_name]
            # print("0000000000000000000000000000000000000000")
            self.current_page_instance = self.get_cached_page(page_name)
            disaster_point_id = kwargs.get("disaster_point_id")
            work_point_id = kwargs.get("work_point_id")
            if self.current_page_instance and hasattr(self.current_page_instance, 'set_data'):
                self.current_page_instance.set_data(work_point_id,disaster_point_id)
            self.current_page_name = page_name
            # # 发射页面实例
            self.page_changed.emit(self.current_page_instance)
            return True
        return False
    def get_current_page_name(self):
        return self.current_page_name

    def get_current_page(self):
        """获取当前页面名称"""
        return self.current_page_instance
    def show_load_page(self):
        load_page =LoadPage()
        load_page.show()