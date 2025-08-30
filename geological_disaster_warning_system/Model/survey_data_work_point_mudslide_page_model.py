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


class SurveyDataWorkPointMudslidePageModel(MyBaseModel):
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.first_menu = []
        self.second_menu = []
        self.third_menu = []
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))  #
        self.load_data()

    def get_mudslide_first_menu(self):
        if len(self.first_menu) == 0:
            query = (f"SELECT mudslide_menu.id AS id,mudslide_menu.menu_id AS menu_id,"
                     f"menu.name AS menu_name "
                     f"FROM mudslide_menu"
                     f" INNER JOIN menu "
                     f"ON mudslide_menu.menu_id = menu.id"
                     f" WHERE mudslide_menu.menu_level = 1; ")
            re = self.db.db_manger_do_sql(query)
            self.first_menu = MyUtils.cal_sql_data(re)
        return self.first_menu

    def get_mudslide_second_menu(self):
        if len(self.second_menu) == 0:
            query = (f"SELECT mudslide_menu.id AS id,"
                     f"mudslide_menu.parent_id AS parent_id, "
                     f"mudslide_menu.menu_id AS menu_id,"
                     f"menu.name AS menu_name "
                     f"FROM mudslide_menu "
                     f" INNER JOIN menu "
                     f"ON mudslide_menu.menu_id = menu.id "
                     f" WHERE mudslide_menu.menu_level = 2; ")
            re = self.db.db_manger_do_sql(query)
            self.second_menu = MyUtils.cal_sql_data(re)
        return self.second_menu

    def get_mudslide_third_menu(self):
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

    def get_mudslide_zhibiao_score(self,menu_id):
        query = f"select * from mudslide_zhibiao_dict where menu_id='{menu_id}'"
        re = self.db.db_manger_do_sql(query)
        data = MyUtils.cal_sql_data(re)
        return data

    def get_menu_content(self, menu_id):
        query = f"SELECT table_name from menu where id = {menu_id}"
        re = self.db.db_manger_do_sql(query)
        tmp = MyUtils.cal_sql_data(re)
        try:
            if tmp:
                table_name = tmp[0]['table_name']
                if menu_id not in self.menu_content or self.menu_content[menu_id] is None:
                    query = f"SELECT * FROM {table_name} where disaster_id =1"
                    re = self.db.db_manger_do_sql(query)
                    self.menu_content[menu_id] = MyUtils.cal_sql_data(re)
                return self.menu_content.get(menu_id)
        except:
            return None
