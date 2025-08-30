import json
import logging
import os
import shutil
import uuid
from datetime import datetime
from PIL import Image, ImageOps
from PySide6.QtSql import QSqlQuery

from Model.base_model import MyBaseModel
from utils.utils import MyUtils


class HomePageModel:
    # 动态处理特殊菜单项
    # TODO: 特殊菜单处理配置，后续新增特殊菜单请在此处添加
    SPECIAL_MENU_HANDLERS = {
        10: {  # 地层岩性
            'tables': ['地层岩性土质', '地层岩性岩质'],
            'fields': ['id', 'name'],
            'menu_ids': [40, 41],
            'names': ['土质', '岩质']
        }
    }
    def __init__(self, db_manager):
        self.cal_all_work_pont_info = []
        self.db = db_manager
        self.dict_model = MyBaseModel(db_manager)
        self._data = {}
        self.base_data =[]
        self.work_point_data = []  # 原始的工点信息，里面数据都是ID
        self.disaster_point_data = []  # 处理过后的，仅仅包含中文名了
        self.display_work_point_and_disaster_point_data = []
        self.work_point_id = 0
        self.image_path = None
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))  #
        self.load_data()
        self.menu_content = {}

    def load_data(self):
        if len(self.base_data) ==0:
            query = f"select * from database_info"
            re = self.db.db_manger_do_sql(query)
            self.base_data = MyUtils.cal_sql_data(re)
        self.get_work_point_info()
        self.get_disaster_point_info()
        self.dict_model.get_nraprc_dict()
        self.dict_model.get_disaster_info()
        self.dict_model.get_disaster_yifa_level()
        self.dict_model.get_disaster_pinggu_level()
        # self.dict_model.get_train_station()
        self.dict_model.get_train_direction()
        self.dict_model.get_railway_line()
        self.dict_model.get_line_data()
        self.dict_model.get_mileage_data()
        self.dict_model.get_diaster_type_data()
        return self.base_data

    def update_work_point_data(self):
        query = f"select * from work_point_info where delete_mark =0 "
        re = self.db.db_manger_do_sql(query)
        self.work_point_data = MyUtils.cal_sql_data(re)
    def get_work_point_info(self):
        if len(self.work_point_data) == 0:
            self.update_work_point_data()
        return self.work_point_data

    def update_disaster_point_data(self):
        query = f"select * from disaster_point_info where delete_mark =0 "
        re = self.db.db_manger_do_sql(query)
        self.disaster_point_data = MyUtils.cal_sql_data(re)

    def get_disaster_point_info(self):
        if len(self.disaster_point_data) == 0:
            self.update_disaster_point_data()
        return self.disaster_point_data

    def get_menu_content(self, menu_id,disaster_id):
        query = f"SELECT name from menu where id = {menu_id}"
        re = self.db.db_manger_do_sql(query)
        tmp = MyUtils.cal_sql_data(re)
        try:
            if tmp:
                table_name = tmp[0]['name']
                if menu_id not in self.menu_content or self.menu_content[menu_id] is None:
                    query = f"SELECT * FROM {table_name} where disaster_id ={disaster_id}"
                    re = self.db.db_manger_do_sql(query)
                    self.menu_content[menu_id] = MyUtils.cal_sql_data(re)
                return self.menu_content.get(menu_id)
        except:
            return None

    def load_menu_data(self, tb_name, disaster_id):
        # 查询原始菜单数据
        query = (f"SELECT {tb_name}.id AS id,"
                 f" {tb_name}.parent_id AS parent_id, "
                 f" {tb_name}.menu_id AS menu_id,"
                 f" menu.name AS menu_name "
                 f"FROM {tb_name} "
                 f"INNER JOIN menu ON {tb_name}.menu_id = menu.id;")

        re = self.db.db_manger_do_sql(query)
        menu_data = MyUtils.cal_sql_data(re)

        # 构建菜单字典，便于查找父子关系
        menu_dict = {item['menu_id']: item for item in menu_data}

        # 存储每个菜单项的内容（叶子节点）
        content_map = {}

        # 获取所有菜单项的内容
        for item in menu_data:
            data = self.get_menu_content(item['menu_id'], disaster_id)
            if data:
                content_map[item['menu_id']] = [{'id': d['id'], 'name': d['name']} for d in data]


        def build_tree(menu_items, parent_id=0):
            nodes = []
            for item in menu_items:
                if item['parent_id'] == parent_id:
                    node = {
                        'menu_id': item['menu_id'],
                        'menu_name': item['menu_name'],
                        'children': []
                    }

                    # 判断是否为特殊菜单项
                    if item['menu_id'] in self.SPECIAL_MENU_HANDLERS:
                        handler = self.SPECIAL_MENU_HANDLERS[item['menu_id']]
                        for i in range(len(handler['tables'])):
                            table = handler['tables'][i]
                            sub_query = f"SELECT {','.join(handler['fields'])} FROM `{table}`;"
                            tmp_re  = self.db.db_manger_do_sql(sub_query)
                            sub_data =MyUtils.cal_sql_data(tmp_re)
                            if sub_data:
                                child_node = {
                                    'menu_id': handler['menu_ids'][i],
                                    'menu_name': handler['names'][i],
                                    'children': [{'id': d['id'], 'name': d['name']} for d in sub_data]
                                }
                                node['children'].append(child_node)

                    else:
                        # 正常递归构建子节点
                        children = build_tree(menu_items, item['menu_id'])
                        if item['menu_id'] in content_map:
                            # 当前节点是叶子节点
                            node['children'] = content_map[item['menu_id']]
                        else:
                            node['children'] = children

                    nodes.append(node)

            return nodes

        # 构建一级菜单
        tree = build_tree(menu_data)

        return tree
    def load_work_point_diaster_data(self,disaster_point_id):
        query = f"select * from disaster_point_score where disaster_point_id='{disaster_point_id}' and delete_mark = 0"
        re = self.db.db_manger_do_sql(query)
        data = MyUtils.cal_sql_data(re)
        # for item in data:

        return data

    def load_work_point_detail(self, processed_data: dict, tb_name, disaster_point_id, disaster_id):
        menu_data = []
        disaster_data = []

        try:
            # 加载菜单结构
            menu_data = self.load_menu_data(tb_name, disaster_id)
            logging.info(f"menu_data = {menu_data}")
        except Exception as e:
            logging.error("加载 menu_data 出错", exc_info=True)

        try:
            # 加载灾害点数据
            disaster_data = self.load_work_point_diaster_data(disaster_point_id)
            logging.info(f"获取对应：disaster_data = {disaster_data}")
        except Exception as e:
            logging.warning("加载 disaster_data 出错或为空", exc_info=True)

        try:
            # 构建 content_value 映射表
            disaster_map = {}
            for item in disaster_data:
                if item.get('content_value') and item['content_value'] not in ('NULL', 'null'):
                    try:
                        content_dict = json.loads(item['content_value'])
                        disaster_map[item['menu_id']] = content_dict
                    except json.JSONDecodeError:
                        logging.warning(
                            f"JSON 解析失败，menu_id={item['menu_id']}, content_value={item['content_value']}")
                        continue
                    except Exception as e:
                        logging.warning(f"解析 content_value 异常，menu_id={item['menu_id']}", exc_info=True)
            logging.info(f"disaster_map = {disaster_map}")
        except Exception as e:
            logging.warning("构建 disaster_map 出错", exc_info=True)

        try:
            # 预处理 menu_data 建立叶子节点映射表
            leaf_node_map = {}  # {(parent_menu_id, id): node}

            def build_leaf_map(items, parent_id=None):
                for item in items:
                    current_parent_id = item.get('menu_id') or parent_id
                    if 'children' in item:
                        for child in item['children']:
                            build_leaf_map([child], current_parent_id)

                    elif 'id' in item and parent_id is not None:
                        key = (parent_id, int(item['id']))
                        leaf_node_map[key] = item

            build_leaf_map(menu_data)

            # 根据 disaster_map 更新 menu_data 叶子节点
            for parent_menu_id, content_dict in disaster_map.items():
                for key, value in content_dict.items():
                    try:
                        key_int = int(key)
                        if (parent_menu_id, key_int) in leaf_node_map:
                            leaf_node_map[(parent_menu_id, key_int)]['value'] = value
                    except ValueError:
                        continue  # 忽略非数字键值

            logging.info(f"更新后的 menu_data = {menu_data}")

        except Exception as e:
            logging.warning("将 disaster_map 映射到 menu_data 时出错", exc_info=True)
        processed_data["menu_data"] = menu_data
        return menu_data

    def get_display_work_point_and_disaster_point_info(self):
        self.get_work_point_info()
        self.get_disaster_point_info()
        processed_data = []
        disaster_dict = self.dict_model.get_disaster_info()
        for disaster_item in self.disaster_point_data:
            for work_point_item in self.work_point_data:
                if disaster_item["工点ID"] == work_point_item["工点ID"]:
                # 创建处理后的新条目
                    """这里因为id都是顺序的，所以可以用-1的方式直接查询，其实正确的做法是循环遍历"""
                    db_name =disaster_dict[disaster_item['风险评估类型'] - 1]['db_name']
                    railway_line_id =work_point_item['线别']
                    train_stations = self.dict_model.get_train_station(railway_line_id)
                    processed = {
                        '风险点ID': disaster_item['风险点ID'],
                        '统一编码':work_point_item['统一编码'],
                        '铁路局': self.dict_model.get_nraprc_dict()[work_point_item['铁路局']-1]['铁路局'],
                        '线别': self.dict_model.get_railway_line()[work_point_item['线别'] - 1]['线路'],
                        '区间开始站': next(
                            (s['火车站名'] for s in train_stations if s['id'] == work_point_item['区间开始站']),
                            None),
                        '区间结束站': next(
                            (s['火车站名'] for s in train_stations if s['id'] == work_point_item['区间结束站']),
                            None),
                        '里程': disaster_item['里程K']+disaster_item['里程开始位置']+"~"+disaster_item['里程结束位置'],
                        '行别': self.dict_model.get_train_direction()[disaster_item['行别']-1]['行别'],
                        '风险评估类型': self.dict_model.get_disaster_info()[disaster_item['风险评估类型']-1]['name'],
                        '风险易发性': self.dict_model.get_disaster_yifa_level()[disaster_item['风险易发性']-1]['灾害易发性等级'],
                        '风险评估等级':self.dict_model.get_disaster_pinggu_level()[disaster_item['风险评估等级']-1]['灾害评估等级']
                    }
                    self.load_work_point_detail(processed,db_name,disaster_item['风险点ID'],disaster_item['风险评估类型'])
                    processed_data.append(processed)
        self.display_work_point_and_disaster_point_data = processed_data
        return self.display_work_point_and_disaster_point_data

    def get_work_point_diaster_type(self):
        # 创建灾害类型ID到中文名的映射字典
        disaster_map = {item['id']: item['name'] for item in self.dict_model.get_disaster_info()}

        # 创建分组统计字典
        # 结构：{统一编码: {风险类型ID: 计数}}
        count_dict = {}

        for workpoint in self.all_work_pont_info:
            unify_code = workpoint['统一编码']
            risk_type = workpoint['风险评估类型']

            if unify_code not in count_dict:
                count_dict[unify_code] = {}

            if risk_type not in count_dict[unify_code]:
                count_dict[unify_code][risk_type] = 0

            count_dict[unify_code][risk_type] += 1

        # 构建结果列表
        result = []

        for unify_code, risk_counts in count_dict.items():
            for risk_id, count in risk_counts.items():
                # 获取风险类型中文名，如果找不到则使用"未知类型"
                risk_name = disaster_map.get(risk_id, f"未知类型(ID:{risk_id})")
                result.append([unify_code, risk_name, count])
        return result