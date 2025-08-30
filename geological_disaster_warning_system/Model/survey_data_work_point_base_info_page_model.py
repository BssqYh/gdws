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


class SurveyDataWorkPointBaseInfoPageModel(MyBaseModel):



    # =======================#
    #      ❌ 私有方法        #
    # =======================#

    # =========================== #
    #      ✅ 公用方法或者重载      #
    # =========================== #

    def get_menu_content(self, menu_id,railway_line_id=None):
        query = f"SELECT table_name from menu where id = {menu_id}"
        re = self.db.db_manger_do_sql(query)
        tmp = MyUtils.cal_sql_data(re)
        try:
            if tmp:
                table_name = tmp[0]['table_name']
                if menu_id not in self.menu_content or self.menu_content[menu_id] is None:
                    query = f"SELECT * FROM {table_name}"
                    re = self.db.db_manger_do_sql(query)
                    self.menu_content[menu_id] = MyUtils.cal_sql_data(re)
                    self._generate_work_point_common_data(self.menu_content[menu_id],railway_line_id)
                return self.menu_content.get(menu_id)
        except:
            return None

    # def upsert_work_point_info(self,data: dict):
    #     work_point_id = data['work_point_id']
    #     query = f"SELECT id FROM work_point_info WHERE work_point_id = '{work_point_id}'"
    #     re = self.db.db_manger_do_sql(query)
    #     tmp_data = MyUtils.cal_sql_data(re)
    #     important_num = data['important_num']
    #     weight = data['weight']
    #     score = data['score']
    #     content_value = {k: self.convert_value(v) for k, v in data['content_value'].items()}
    #     content_value = json.dumps(content_value, ensure_ascii=False, separators=(',', ':'))
    #     image_path = None
    #     if data['image_path'] =="NULL":
    #         image_path = "NULL"
    #     else:
    #         image_path =  {k: self.convert_value(v) for k, v in data['image_path'].items()}
    #         image_path = json.dumps(image_path, ensure_ascii=False, separators=(',', ':'))
    #     query = ""
    #     if len(tmp_data) == 0 :
    #         #不存在，那么就要执行插入
    #         query = (f"INSERT INTO work_point_score(work_point_id,menu_id,important_num,weight,score,content_value,image_path)  VALUES ({work_point_id},{menu_id},"
    #                  f"{important_num},{weight},{score},'{content_value}'"
    #                  f",'{image_path}');")
    #     else:
    #         query = (f"update work_point_score set important_num = {important_num},"
    #                  f"weight = {weight},score ={score},content_value ='{content_value}'"
    #                  f",image_path ='{image_path}' where work_point_id = '{work_point_id}' and menu_id = '{menu_id}';")
    #     re =self.db.db_manger_do_sql(query)