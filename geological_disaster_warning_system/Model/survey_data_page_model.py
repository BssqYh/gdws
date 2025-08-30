import logging
import os
import shutil
import uuid
from datetime import datetime
from PIL import Image, ImageOps
from PySide6.QtSql import QSqlQuery

from Model.base_model import MyBaseModel
from utils.utils import MyUtils


class SurveyDataPageModel(MyBaseModel):
    survey_data_page_menu_content = {}  # 菜单数据缓存
    def load_data(self):
        pass

    def get_all_work_point_info_by_line(self, line):
        query = f"select * from work_point_info where \"线别\"={line} and delete_mark =0 "
        re = self.db.db_manger_do_sql(query)
        data = MyUtils.cal_sql_data(re)
        work_point_data = self.get_display_work_point_and_disaster_point_info(0,0)
        processed_data = []
        for disaster_item in work_point_data:
            for work_point_item in data:
                if disaster_item["工点ID"] == work_point_item["工点ID"]:
                    processed_data.append(disaster_item)
                    break
        return processed_data

    def get_all_work_point_info_by_mileage(self, mileage):
        query = f"select * from disaster_point_info where \"里程K\"='{mileage}' and delete_mark =0 "
        re = self.db.db_manger_do_sql(query)
        data = MyUtils.cal_sql_data(re)
        logging.info(f"<UNK>{mileage}----{data}<UNK>")
        work_point_data = self.get_display_work_point_and_disaster_point_info(0,0)
        processed_data = []
        for work_point_item in data:
            for disaster_item in work_point_data:
                if disaster_item["工点ID"] == work_point_item["工点ID"]:
                    if  work_point_item["里程K"] in disaster_item["里程"]:
                        processed_data.append(disaster_item)
                        break
        return processed_data

    def get_all_work_point_info_by_disaster(self, disaster):
        query = f"select * from disaster_point_info where \"风险评估类型\"='{disaster}' and delete_mark =0 "
        re = self.db.db_manger_do_sql(query)
        data = MyUtils.cal_sql_data(re)
        logging.info(f"<UNK>{disaster}----{data}<UNK>")
        work_point_data = self.get_display_work_point_and_disaster_point_info(0,0)
        processed_data = []
        for disaster_item in work_point_data:
            for work_point_item in data:
                if disaster_item["工点ID"] == work_point_item["工点ID"]:
                    disaster_info = self.get_disaster_info()
                    if disaster_item["风险评估类型"] == disaster_info[work_point_item['风险评估类型'] - 1]['name']:
                        processed_data.append(disaster_item)
                        break
        return processed_data

    def get_query_work_point_data(self,queryData:dict):
        base_query = """
            SELECT d.* 
            FROM disaster_point_info d
            JOIN work_point_info w ON d.工点ID = w.工点ID
            WHERE d.delete_mark = 0
        """
        processed_data =[]
        conditions = []
        all_disaster_point_data = self.get_display_work_point_and_disaster_point_info(0, 0)
        for typeName,value in queryData.items():
            if value:
                if typeName == "线别名称":
                    conditions.append(f"w.线别 = '{value}'")
                elif  typeName == "里程K":
                    conditions.append(f"d.\"里程K\" = '{value}'")
                elif typeName == "name":
                    conditions.append(f"d.\"风险评估类型\" = '{value}'")
                else:
                    pass
        if conditions:
            where_clause = " AND ".join(conditions)
            final_query = f"{base_query} AND ({where_clause})"
        else:
            final_query = base_query
        re = self.db.db_manger_do_sql(final_query)
        data = MyUtils.cal_sql_data(re)
        for all_disaster_item in all_disaster_point_data:
            for disaster_item in data:
                if disaster_item["风险点ID"] == all_disaster_item["风险点ID"]:
                    processed_data.append(all_disaster_item)
                    break
        return processed_data

    def get_work_point_common_content(self, menu_id):
        query = f"SELECT table_name from menu where id = {menu_id}"
        re = self.db.db_manger_do_sql(query)
        tmp = MyUtils.cal_sql_data(re)
        try:
            if tmp:
                table_name = tmp[0]['table_name']
                if menu_id not in self.survey_data_page_menu_content or self.survey_data_page_menu_content[menu_id] is None:
                    query = f"SELECT * FROM {table_name} where is_work_point =1 "
                    re = self.db.db_manger_do_sql(query)
                    self.survey_data_page_menu_content[menu_id] = MyUtils.cal_sql_data(re)
                    self._generate_work_point_common_data(self.survey_data_page_menu_content[menu_id])
                logging.info(self.survey_data_page_menu_content.get(menu_id))
                return self.survey_data_page_menu_content.get(menu_id)
        except:
            return None