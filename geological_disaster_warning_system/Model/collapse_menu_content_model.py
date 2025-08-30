import sqlite3
from typing import List, Dict, Any
import threading

from PySide6.QtCore import QObject


from database.manager import DatabaseManager

import logging

logging.basicConfig(format='%(levelname)s:%(funcName)s:%(message)s', level=logging.DEBUG)

class MenuItem(QObject):
    """菜单项数据模型（适配字典结构）"""

    def __init__(self, data_dict, parent=None):
        super().__init__(parent)
        self._data = data_dict
        self.children = [MenuItem(child) for child in data_dict.get('children', [])]

        # 生成唯一ID（使用名称哈希）
        # name_hash = hashlib.md5(data_dict['name'].encode()).hexdigest()[:8]
        self.menu_id = data_dict['menu_id']

    @property
    def name(self):
        return self._data['name']

    @property
    def icon(self):
        return self._data.get('icon')

    @property
    def level(self):
        return self._data['menu_level']

    @property
    def has_children(self):
        return self._data['has_children']

class CollapseMenuContentModel:
    def __init__(self):
        self.cache = {}  # 缓存数据结构 {menu_id: content_data}
        self.lock = threading.Lock()  # 线程安全锁
        self.db = DatabaseManager()
        self.root_items = None
        self.table_name = "collapse_menu"

    def _generate_menu_dict(self, menu_structure, menu_info):
        """"""
        """
        生成菜单字典，包含菜单级别、名称、图标及是否有子菜单
        :param menu_structure: 菜单结构数据，格式 [(id, menu_id, parents_id, menu_level), ...]
        :param menu_info: 菜单详细信息，格式 [(id, name, icon), ...]
        :return: 嵌套字典结构，包含菜单详细信息及子菜单状态
        """
        # Step 1: 构建菜单信息映射字典 {menu_id: (name, icon)}
        info_map = {item[0]: (item[1], item[2]) for item in menu_info}
        # Step 2: 构建父子关系映射 {parent_id: [child_menu_dicts]}
        parent_child_map = {}
        for item in menu_structure:
            _, menu_id, parent_id, _ = item
            if parent_id not in parent_child_map:
                parent_child_map[parent_id] = []
            parent_child_map[parent_id].append(menu_id)

        # Step 3: 生成基础菜单字典 {menu_id: menu_item}
        menu_dict = {}
        for item in menu_structure:
            _, menu_id, parent_id, menu_level = item
            name, icon = info_map.get(menu_id, ("未知菜单", "null"))

            # 判断是否有子菜单
            has_children = menu_id in parent_child_map

            menu_dict[menu_id] = {
                "menu_level": menu_level+1,
                "menu_id": menu_id,
                "name": name,
                "icon": icon if icon != 'null' else None,
                "has_children": has_children,
                "children": []
            }

        # Step 4: 构建嵌套层级关系
        for item in menu_structure:
            _, menu_id, parent_id, _ = item
            if parent_id in menu_dict:
                menu_dict[parent_id]["children"].append(menu_dict[menu_id])

        # 提取根节点 (parent_id=0)
        root_menus = [menu_dict[child_id] for child_id in parent_child_map.get(0, [])]
        logging.debug(f"root_menus--{root_menus}")
        return root_menus
    def get_menus(self):
        if self.root_items is None:
            data = self.db.get_disaster_menu(self.table_name)
            data2 = self.db.get_disaster_menu_info()
            self.root_items = self._generate_menu_dict(data, data2)
        return self.root_items

    def get_contents(self, menu_id: int) -> List[Dict[str, Any]]:
        """获取内容数据（带缓存功能）"""
        # 先尝试从缓存读取
        if menu_id in self.cache:
            return self.cache[menu_id]

        # 缓存未命中时加锁查询数据库
        with self.lock:
            # 双重检查锁定（防止多个线程同时进入）
            if menu_id in self.cache:
                return self.cache[menu_id]

            # 执行数据库查询
            data = self._query_database(menu_id)

            # 写入缓存
            self.cache[menu_id] = data
            return data

    def _query_database(self, menu_id: int) -> List[Dict[str, Any]]:
        try:
            # 获取关联的 menu_content_id,即：内容显示的标签ID
            query = f"SELECT menu_content_id FROM mudslide_menu_content WHERE menu_id =  {menu_id}"
            menu_content_data = self.db.db_manger_do_sql(query)
            content_ids = [row['menu_content_id'] for row in menu_content_data]
            if not content_ids:
                return []
            # 批量获取 menu_content的具体内容。即标签内容：比如在menu_id地形地貌里面，获取到的就是坡形、危岩体与铁路线路垂距、地面坡度、地面相对高差等
            placeholders = ", ".join(["?"] * len(content_ids))  # 生成 ?, ?, ?, ...
            query = f"""
                SELECT id, name, type, content_unit 
                FROM menu_content 
                WHERE id IN ({placeholders})
            """
            menu_content_data_info = self.db.db_manger_do_sql(query,content_ids)
            contents = {row['id']: dict(row) for row in menu_content_data_info}
            # 批量获取预定义值，获取每一个指标的值
            value_types = [
                cid for cid, c in contents.items()
                if c['type'] in ('QCheckBox', 'QComboBox')
            ]
            values_map = {}
            if value_types:
                placeholders = ','.join(['?'] * len(value_types))
                query = f"""SELECT id,menu_content, content_value FROM content_value WHERE menu_content IN ({placeholders})"""
                menu_content_data_info_value = self.db.db_manger_do_sql(query,value_types)
                for row in menu_content_data_info_value:
                    cid = row['menu_content']
                    value_id = row['id']
                    value = row['content_value']
                    if cid not in values_map:
                        values_map[cid] = {}
                    values_map[cid][value_id] = value
            # 构建结果
            return [
                {
                    "menu_id": menu_id,
                    "menu_content_id": contents[cid]["id"],
                    "menu_content_name": contents[cid]['name'],
                    "menu_content_type": contents[cid]['type'],
                    "menu_content_unit": contents[cid]['content_unit'],
                    "menu_content_value": values_map.get(cid, {})
                }
                for cid in content_ids if cid in contents
            ]
        except sqlite3.Error as e:
            logging.error(f"mudslidemodel _query_database 失败: {str(e)}")
            return None

    def update_menu_content(self,menu_content_info):
        """"""
        """数据格式如下
      [{'work_point_id': 1, 'work_point_mudslide_id': 1, 'menu_id': 9, 'menu_content_id': 2, 'value': '1'},
       {'work_point_id': 1, 'work_point_mudslide_id': 1, 'menu_id': 9, 'menu_content_id': 4, 'value': '2'}]
        """
        try:
            for item in menu_content_info:
                sql = f"""INSERT into disaster_menu_content_info (
                            work_point_id,
                            work_point_disaster_id,
                            menu_id,
                            menu_content_id,
                            disaster_value
                        ) 
                        VALUES ({item["work_point_id"]},{item["work_point_disaster_id"]}, {item["menu_id"]}, {item["menu_content_id"]},{item["value"]})
                        ON CONFLICT (work_point_id, work_point_disaster_id, menu_id, menu_content_id) 
                        DO UPDATE SET disaster_value = excluded.disaster_value;"""
                self.db.db_manger_do_sql(sql)
            return 0
        except sqlite3.Error as e:
            logging.error(f"mudslidemodel _update_menu_content <UNK>: {str(e)}")
        pass

    def clear_cache(self, menu_id: int = None):
        """清理缓存"""
        with self.lock:
            if menu_id:
                self.cache.pop(menu_id, None)
            else:
                self.cache.clear()