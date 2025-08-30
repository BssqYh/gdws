# database/manager.py（新增数据库模块）
import logging
import sqlite3
from PySide6.QtGui import QPixmap
from pathlib import Path

from PySide6.QtSql import QSqlDatabase, QSqlQuery


class DatabaseManager:
    def __init__(self, db_path="demo.db"):
        self.db_is_open = None
        self.db_path = Path(__file__).parent.parent / db_path
        self.db = None
    def init_connection(self,db_path):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(db_path)
        self.db_is_open= self.db.open()

    #有些模型需要自己构建查询语句。
    def db_manger_do_sql(self,sql_query,return_last_id=False):
        """执行查询并返回结果"""
        try:
            if self.db_is_open:
                query = QSqlQuery(self.db)
                success = query.exec(sql_query)
                if success:
                    if return_last_id and sql_query.strip().upper().startswith("INSERT"):
                        last_id = query.lastInsertId()
                        if last_id is not None:
                            return int(last_id)
                        else:
                            query2 = QSqlQuery(self.db)
                            query2.exec("SELECT last_insert_rowid()")
                            if query2.next():
                                return query2.value(0)
                    return query
                else:
                    error = query.lastError().text()
                    logging.error(f"查询失败: {error}")
                    return None
            else:
                logging.error(f"数据库打开失败:")
                self.db.open()
                return None
        except sqlite3.Error as e:
            logging.error(f"数据库更新失败: {str(e)}")
            return False

