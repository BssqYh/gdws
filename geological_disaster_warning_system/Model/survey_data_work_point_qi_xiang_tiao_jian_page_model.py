import logging
import os
import shutil
import uuid
from datetime import datetime
from PIL import Image, ImageOps
from PySide6.QtSql import QSqlQuery

from Model.base_model import MyBaseModel
from utils.utils import MyUtils


class SurveyDataWorkPointQiXiangTiaoJianPageModel(MyBaseModel):
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.baoyu_menu = []

    def get_menu_content(self, menu_id):
        """"""
        """因为暴雨数据和其余不一样没有风险的区别，因此需要重载"""
        if len(self.baoyu_menu) ==0:
            query = f"SELECT * from menu where id = {menu_id}"
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
        return self.baoyu_menu



