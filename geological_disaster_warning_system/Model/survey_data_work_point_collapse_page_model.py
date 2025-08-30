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


class SurveyDataWorkPointCollapsePageModel(MyBaseModel):
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.first_menu = []
        self.second_menu = []
        self.third_menu = []
        self.fourth_menu =[]
        self.image_path = None
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))  #
        self.load_data()
        self.work_point_name = None

    def get_collapse_first_menu(self):
        if len(self.first_menu) == 0:
            query = (f"SELECT collapse_menu.id AS id,collapse_menu.menu_id AS menu_id,"
                     f"menu.name AS menu_name "
                     f"FROM collapse_menu"
                     f" INNER JOIN menu "
                     f"ON collapse_menu.menu_id = menu.id"
                     f" WHERE collapse_menu.menu_level = 1; ")
            re = self.db.db_manger_do_sql(query)
            self.first_menu = MyUtils.cal_sql_data(re)
        return self.first_menu

    def get_collapse_second_menu(self):
        if len(self.second_menu) == 0:
            query = (f"SELECT collapse_menu.id AS id,"
                     f"collapse_menu.parent_id AS parent_id, "
                     f"collapse_menu.menu_id AS menu_id,"
                     f"menu.name AS menu_name "
                     f"FROM collapse_menu "
                     f" INNER JOIN menu "
                     f"ON collapse_menu.menu_id = menu.id "
                     f" WHERE collapse_menu.menu_level = 2; ")
            re = self.db.db_manger_do_sql(query)
            self.second_menu = MyUtils.cal_sql_data(re)
        logging.info(self.second_menu)
        return self.second_menu

    def get_collapse_third_menu(self):
        if len(self.third_menu) == 0:
            query = (f"SELECT collapse_menu.id AS id,"
                     f"collapse_menu.parent_id AS parent_id, "
                     f"collapse_menu.menu_id AS menu_id,"
                     f"menu.name AS menu_name "
                     f"FROM collapse_menu "
                     f" INNER JOIN menu "
                     f"ON collapse_menu.menu_id = menu.id "
                     f" WHERE collapse_menu.menu_level = 3; ")
            re = self.db.db_manger_do_sql(query)
            self.third_menu = MyUtils.cal_sql_data(re)
        return self.third_menu

    def get_collapse_fourth_menu(self):
        if len(self.fourth_menu) == 0:
            query = (f"SELECT collapse_menu.id AS id,"
                     f"collapse_menu.parent_id AS parent_id, "
                     f"collapse_menu.menu_id AS menu_id,"
                     f"menu.name AS menu_name "
                     f"FROM collapse_menu "
                     f" INNER JOIN menu "
                     f"ON collapse_menu.menu_id = menu.id "
                     f" WHERE collapse_menu.menu_level = 4; ")
            re = self.db.db_manger_do_sql(query)
            self.fourth_menu = MyUtils.cal_sql_data(re)
        return self.fourth_menu


    def get_menu_content(self, menu_id):
        query = f"SELECT name from menu where id = {menu_id}"
        re = self.db.db_manger_do_sql(query)
        tmp = MyUtils.cal_sql_data(re)
        logging.info(tmp)
        try:
            if tmp:
                table_name = tmp[0]['name']
                logging.info(table_name)
                if menu_id not in self.menu_content or self.menu_content[menu_id] is None:
                    query = f"SELECT * FROM {table_name} where disaster_id =2"
                    re = self.db.db_manger_do_sql(query)
                    self.menu_content[menu_id] = MyUtils.cal_sql_data(re)
                logging.info(self.menu_content.get(menu_id))
                return self.menu_content.get(menu_id)
        except:
            return None

    def get_collapse_work_point_score(self,work_point_id):
        query = f"select * from work_point_score where work_point_id='{work_point_id}'"
        re = self.db.db_manger_do_sql(query)
        data = MyUtils.cal_sql_data(re)
        # print(f"{query}----get_mudslide_work_point_score-{data}")
        """
        得出的数据结构是这样，我们需要将content_value，转换为字典
       [{'id': 1, 'work_point_id': 1, 'menu_id': 9, 'important_num': 2, 'weight': 0.22, 'score': 80.0, 'content_value': '{"1":"凸地形","2":82,"3":37,"4":90,"5":"高","67":"78.6"}'},
        {'id': 2, 'work_point_id': 1, 'menu_id': 10, 'important_num': 1, 'weight': 0.27, 'score': 90.0, 'content_value': '{"6":"层状结构","7":"软硬互层或强-中风化岩体为主","8":"无","67":90}'},
        {'id': 3, 'work_point_id': 1, 'menu_id': 11, 'important_num': 7, 'weight': 0.03, 'score': 60.0, 'content_value': '{"13":"褶皱、断裂构造较发育","14":"微弱，活动断裂不发育","15":"少","16":0.15,"67":60}'}
        ]
        """
        for item in data:
            content_json = item["content_value"]  #
            if item['content_value']!= "NULL":
                content_dict = json.loads(content_json)
                item["content_value"] = content_dict
            content_json = item["image_path"]  #
            if item['image_path'] != "NULL":
                content_dict = json.loads(content_json)
                item["image_path"] = content_dict
        # print(f"{query}----get_mudslide_work_point_score-{data}")
        return  data

    def get_mudslide_zhibiao_score(self,menu_id):
        query = f"select * from mudslide_zhibiao_dict where menu_id='{menu_id}'"
        re = self.db.db_manger_do_sql(query)
        data = MyUtils.cal_sql_data(re)
        return data

    def get_disaster_count_with_code(self,code):
        if len(self.all_work_pont_info) ==0:
            query = f"select * from work_point_info where 统一编码='{code}'"
            re = self.db.db_manger_do_sql(query)
            self.all_work_pont_info = MyUtils.cal_sql_data(re)
        return len(self.all_work_pont_info)

    def convert_value(self,val):
        try:
            # 尝试转成 int 或 float
            if '.' in str(val):
                return float(val)
            else:
                return int(val)
        except:
            return val

    def upsert_work_point_score(self,work_point_id,menu_id,data: dict):
        if work_point_id is None or menu_id is None:
            raise ValueError("缺少必要字段：work_point_id 或 menu_id")
            # 构造查询语句，检查是否存在记录
        query = f"SELECT id FROM work_point_score WHERE work_point_id = '{work_point_id}'  AND menu_id = '{menu_id}'"
        re = self.db.db_manger_do_sql(query)
        tmp_data = MyUtils.cal_sql_data(re)
        important_num = data['important_num']
        weight = data['weight']
        score = data['score']
        content_value = {k: self.convert_value(v) for k, v in data['content_value'].items()}
        content_value = json.dumps(content_value, ensure_ascii=False, separators=(',', ':'))
        image_path = None
        if data['image_path'] =="NULL":
            image_path = "NULL"
        else:
            image_path =  {k: self.convert_value(v) for k, v in data['image_path'].items()}
            image_path = json.dumps(image_path, ensure_ascii=False, separators=(',', ':'))
        query = ""
        if len(tmp_data) == 0 :
            #不存在，那么就要执行插入
            query = (f"INSERT INTO work_point_score(work_point_id,menu_id,important_num,weight,score,content_value,image_path)  VALUES ({work_point_id},{menu_id},"
                     f"{important_num},{weight},{score},'{content_value}'"
                     f",'{image_path}');")
        else:
            query = (f"update work_point_score set important_num = {important_num},"
                     f"weight = {weight},score ={score},content_value ='{content_value}'"
                     f",image_path ='{image_path}' where work_point_id = '{work_point_id}' and menu_id = '{menu_id}';")
        re =self.db.db_manger_do_sql(query)