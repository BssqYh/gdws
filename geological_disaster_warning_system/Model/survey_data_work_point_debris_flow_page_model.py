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


class SurveyDataWorkPointDebrisFlowPageModel(MyBaseModel):
    def __init__(self, db_manager):

        super().__init__(db_manager)
        self.db = db_manager
        self._data = {}
        self.work_point_data = []
        self.disaster_point_data = []
        self.all_disaster_point_data = []
        self.display_work_point_and_disaster_point_data = []
        self.first_menu = []
        self.second_menu = []
        self.baoyu_menu = []
        self.cal_all_work_pont_info = []#处理过后的，仅仅包含中文名了
        self.work_point_id = 0
        self.image_path = None
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))  #

    def get_debris_flow_first_menu(self):
        if len(self.first_menu) == 0:
            query = (f"SELECT debrisflow_menu.id AS id,debrisflow_menu.menu_id AS menu_id,"
                     f"menu.name AS menu_name "
                     f"FROM debrisflow_menu"
                     f" INNER JOIN menu "
                     f"ON debrisflow_menu.menu_id = menu.id"
                     f" WHERE debrisflow_menu.menu_level = 1; ")
            re = self.db.db_manger_do_sql(query)
            self.first_menu = MyUtils.cal_sql_data(re)
        return self.first_menu

    def get_debris_flow_second_menu(self):
        if len(self.second_menu) == 0:
            query = (f"SELECT debrisflow_menu.id AS id,"
                     f"debrisflow_menu.parent_id AS parent_id, "
                     f"debrisflow_menu.menu_id AS menu_id,"
                     f"menu.name AS menu_name "
                     f"FROM debrisflow_menu "
                     f" INNER JOIN menu "
                     f"ON debrisflow_menu.menu_id = menu.id "
                     f" WHERE debrisflow_menu.menu_level = 2; ")
            re = self.db.db_manger_do_sql(query)
            self.second_menu = MyUtils.cal_sql_data(re)
        return self.second_menu

    def get_debris_third_menu(self):
        if len(self.third_menu) == 0:
            query = (f"SELECT mudslide_menu.id AS id,"
                     f"mudslide_menu.parent_id AS parent_id, "
                     f"mudslide_menu.menu_id AS menu_id,"
                     f"menu.name AS menu_name "
                     f"FROM mudslide_menu "
                     f" INNER JOIN menu "
                     f"ON mudslide_menu.menu_id = menu.id "
                     f" WHERE mudslide_menu.menu_level = 3; ")
            re = self.db.db_manger_do_sql(query)
            self.third_menu = MyUtils.cal_sql_data(re)
        return self.third_menu

    def get_sub_menu_content(self,menu_id):
        query = f"SELECT name,table_name from menu where id = {menu_id}"
        re = self.db.db_manger_do_sql(query)
        tmp = MyUtils.cal_sql_data(re)
        try:
            if tmp:
                table_name = tmp[0]['table_name']
                query = f"SELECT * FROM {table_name}"
                re = self.db.db_manger_do_sql(query)
                data= MyUtils.cal_sql_data(re)
                return data,table_name
        except:
            return None,None
        return None,None

    def get_menu_content(self, menu_id):
        query = f"SELECT name,table_name from menu where id = {menu_id}"
        re = self.db.db_manger_do_sql(query)
        tmp = MyUtils.cal_sql_data(re)
        logging.info(tmp)
        try:
            if tmp:
                table_name = tmp[0]['table_name']
                query = f"SELECT * FROM {table_name}"
                re = self.db.db_manger_do_sql(query)
                self.baoyu_menu= MyUtils.cal_sql_data(re)

                return self.baoyu_menu
        except:
            return None