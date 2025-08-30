import json
import logging

from PySide6.QtSql import QSqlQuery
from typing import Optional, List, Dict, Any
from utils.utils import MyUtils

logging.basicConfig(format='%(levelname)s:[%(filename)s:%(lineno)d]:%(funcName)s:%(message)s', level=logging.DEBUG)

"""
模型数据父类，所有模型集成于它。
并且存放字典
"""
class MyBaseModel:
    _dict_cache = {}
    def __init__(self, db_manager):
        self.db = db_manager
        self._data_cache = {}   # 普通数据缓存
        self.load_data()
        self.menu_content = {} #菜单数据缓存

    def load_data(self):
        """子类可重写此方法以加载特定数据"""
        pass

    # =======================#
    #      ❌ 私有方法        #
    # =======================#

    def _convert_value(self,val):
        try:
            # 尝试转成 int 或 float
            if '.' in str(val):
                f_val = round(float(val), 2)
                return f_val
            else:
                return int(val)
        except:
            return val

    def _update_cache(self, table_name: str) -> List[Dict]:
        query = f"SELECT * FROM {table_name}"
        result = self.db.db_manger_do_sql(query)
        self._dict_cache[table_name] = MyUtils.cal_sql_data(result)
        return self._dict_cache[table_name]

    def _get_dict(self, table_name: str) -> List[Dict]:
        """"""
        """
        获取指定表名的字典数据，并缓存结果
        :param table_name: 表名（如 'disaster_info_dict'）
        :return: 字典数据列表
        """
        if table_name not in self._dict_cache or not self._dict_cache[table_name]:
            self._update_cache(table_name)
        return self._dict_cache[table_name]


    def _generate_work_point_common_data(self,menu_data:list[dict],railway_line_id=None):
        """"""
        """因为工点基础信息的界面从数据读取，但是其中设计、线别、火车站等信息，需要从数据库读取。因此
        增加这个方法,而且，value值从数据库读取是字符串，因此，这里需要字符串"""
        for item in menu_data:
            name = item['name']
            datas = self.get_combobox_value(name,railway_line_id)
            # logging.info(f"<UNK>:{name},<UNK>:{datas}")
            # result = {str(i + 1): data for i, data in enumerate(datas)}
            # result_str = json.dumps(datas, ensure_ascii=False)  # 确保中文字符正常显示
            result_str = json.dumps(datas, ensure_ascii=False)  # 确保中文字符正常显示
            item['value'] = result_str
        logging.info(f"最终生成的菜单数据{menu_data}")
    def _find_leaf_menu_ids(self,menu_data):
        """
        找出所有没有子菜单的 menu_id（叶子节点）
        :param menu_data: 菜单数据列表，如你提供的 [{'id': 1, 'menu_id': 1, 'parent_id': 0, ...}, ...]
        :return: 叶子节点的 menu_id 列表
        """
        all_menu_ids = {item['menu_id'] for item in menu_data}
        parent_ids = {item['parent_id'] for item in menu_data}

        # 叶子节点：在 all_menu_ids 中，但不在 parent_ids 中（且 parent_id != menu_id 自引用检查）
        leaf_menu_ids = [mid for mid in all_menu_ids if mid not in parent_ids]

        return leaf_menu_ids

    def _insert_disaster_point_score(self,disaster_point_id,disaster_type_id):
        """"""
        """disaster_type_id这里需要注意一下，因为这个id是顺序的，因此，只需要-1，就可以得到正确的灾害类型
        ，如果以后不连续了，这里一定要更改，只能通过循环来进行
        """
        disaster_type_id = int(disaster_type_id)-1
        data = self.get_disaster_info()
        disaster_db_name = data[disaster_type_id]['db_name']
        query = f"SELECT * FROM {disaster_db_name}"
        re = self.db.db_manger_do_sql(query)
        menu_data = MyUtils.cal_sql_data(re)
        des_menu_data =self._find_leaf_menu_ids(menu_data)
        for tmp_id in des_menu_data:
            menu_id = int(tmp_id)
            query = (
                f"INSERT INTO disaster_point_score(disaster_point_id,menu_id,important_num,weight,score,content_value,image_path)  VALUES ({disaster_point_id},{menu_id},"
                f"{0},{0},{0},'NULL'"
                f",'NULL');")
            self.db.db_manger_do_sql(query)

    def get_train_station_combobox(self,railway_line_id):
        datas = self.get_train_station(railway_line_id)
        # station_dict = {str(data['id']): data['火车站名'] for data in datas}
        return datas

    def get_combobox_value(self,key_value,railway_line_id=None):
        #这里不需要所有的数据，只需要将铁路局的具体值返回就可以了
        logging.info(f"get_combobox_value:{key_value}----{railway_line_id}")
        data ={}
        if key_value == '铁路局':
                data = self.get_nraprc_dict()
        elif key_value== '线别':
                data = self.get_railway_line()
                key_value = '线路'
        elif key_value =='行别':
                data = self.get_train_direction()
        elif key_value =='侧别':
                data = self.get_cebie_dict()
        elif key_value == '风险评估类型':
                data = self.get_disaster_info()
                key_value = 'name'
        elif key_value == '风险易发性':
                data = self.get_disaster_yifa_level()
                key_value = '灾害易发性等级'
        elif key_value =='风险评估等级':
                data = self.get_disaster_pinggu_level()
                key_value = '灾害评估等级'
        elif key_value == '区间开始站':
                data = self.get_train_station_combobox(railway_line_id)
                key_value = '火车站名'
        elif key_value == '区间结束站':
                data = self.get_train_station_combobox(railway_line_id)
                key_value = '火车站名'
        else:
                pass
        logging.info(f"get_combobox_value:{data}")
        result = {str(item['id']): item[key_value] for item in data}
        # return MyUtils.extract_values(data, key_value)
        return result
    # =======================#
    # ✅ 公共字典数据获取接口   #
    # =======================#

    def get_disaster_info(self):
        return self._get_dict("disaster_info_dict")

    def get_disaster_pinggu_level(self):
        return self._get_dict("disaster_pinggu_level_dict")

    def get_disaster_yifa_level(self):
        return self._get_dict("disaster_yifa_level_dict")

    def get_train_direction(self):
        return self._get_dict("train_direction_dict")

    def get_train_station(self,railway_line_id):
        """"""
        """站点不能缓存，因为太多太大了"""
        # return self._get_dict("train_station_dict")
        query = f"select id,火车站名 from train_station_dict where 线路ID={railway_line_id}"
        re = self.db.db_manger_do_sql(query)
        data = MyUtils.cal_sql_data(re)
        logging.info(f"获取当前线路{railway_line_id}的站点数据{data}")
        return data

    def get_nraprc_dict(self):
        return self._get_dict("nraprc_dict")

    def get_railway_line(self):
        return self._get_dict("railway_line_dict")

    def get_cebie_dict(self):
        return self._get_dict("cebie_dict")

    # =======================#
    #      ✅ 通用方法接口     #
    # =======================#

    """
    更新缓存，当调用了保存或者更新过后，就要调用更新。否则缓存会不一致。
    """
    def _update_db_data(self, cache_key: str, query: str) -> List[Dict]:
        result = self.db.db_manger_do_sql(query)
        self._data_cache[cache_key] = MyUtils.cal_sql_data(result)
        return self._data_cache[cache_key]

    def _get_db_data(self, cache_key: str, query: str) -> List[Dict]:
        """带缓存的数据库查询"""
        if cache_key not in self._data_cache or not self._data_cache[cache_key]:
            self._update_db_data(cache_key, query)
        return self._data_cache[cache_key]

    def get_line_data(self):
        query = f"SELECT dict.id AS \"线别ID\",dict.\"线路\" AS \"线别名称\" FROM (SELECT DISTINCT \"线别\" FROM work_point_info) AS unique_line INNER JOIN railway_line_dict AS dict ON unique_line.\"线别\" = dict.id;"
        return self._get_db_data(f"line_data", query)

    def get_mileage_data(self):
        query = f"select DISTINCT \"里程K\" from disaster_point_info  where delete_mark =0 "
        return self._get_db_data(f"mileage_data", query)

    def get_diaster_type_data(self):
        query = f"select DISTINCT id,name from disaster_info_dict"
        return self._get_db_data(f"diaster_type_data", query)

    def get_work_point_disaster_count(self, work_point_id: int) -> int:
        query = f"SELECT COUNT(*) FROM disaster_point_info WHERE 工点ID = {work_point_id} AND delete_mark = 0"
        re = self.db.db_manger_do_sql(query)
        data = MyUtils.cal_sql_data(re)
        return data[0]['COUNT(*)'] if data else 0

    def update_all_disaster_point_data(self,work_point_id: int):
        query = f"SELECT * FROM disaster_point_info WHERE 工点ID = {work_point_id} AND delete_mark = 0"
        self._update_db_data(f"all_disaster_point_in_{work_point_id}", query)
    def get_all_disaster_point_data(self, work_point_id: int) -> List[Dict]:
        query = f"SELECT * FROM disaster_point_info WHERE 工点ID = {work_point_id} AND delete_mark = 0"
        return self._get_db_data(f"all_disaster_point_in_{work_point_id}", query)

    def update_work_point_info(self,work_point_id):
        query = None
        if work_point_id == 0:
            """0表示获取全部"""
            query = f"SELECT * FROM work_point_info WHERE delete_mark = 0"
        else:
            query = f"SELECT * FROM work_point_info WHERE 工点ID={work_point_id} AND delete_mark = 0"
        self._update_db_data(f"work_point_{work_point_id}", query)

    def get_work_point_info(self, work_point_id: int) -> List[Dict]:
        query =None
        if work_point_id == 0:
            """0表示获取全部"""
            query = f"SELECT * FROM work_point_info WHERE delete_mark = 0"
        else:
            query = f"SELECT * FROM work_point_info WHERE 工点ID={work_point_id} AND delete_mark = 0"
        return self._get_db_data(f"work_point_{work_point_id}", query)

    def get_disaster_point_info(self, disaster_point_id: int) -> List[Dict]:
        query =None
        if disaster_point_id == 0:
            query = f"SELECT * FROM disaster_point_info WHERE delete_mark = 0"
        else:
            query = f"SELECT * FROM disaster_point_info WHERE 风险点ID = {disaster_point_id} AND delete_mark = 0"
        return self._get_db_data(f"disaster_point_{disaster_point_id}", query)

    def get_display_work_point_info(self, work_point_id: int) -> List[Dict]:
        work_point_data = self.get_work_point_info(work_point_id)
        processed_data = []
        for work_point_item in work_point_data:
            railway_line_id = work_point_item.get('线别')
            train_station_dict = self.get_train_station(railway_line_id)
            processed = {
                '工点ID': work_point_item['工点ID'],
                '工点名称': work_point_item['工点名称'],
                '统一编码': work_point_item['统一编码'],
                '铁路局': self.get_nraprc_dict()[work_point_item['铁路局'] - 1]['铁路局'],
                '线别': self.get_railway_line()[work_point_item['线别'] - 1]['线路'],
                '区间开始站': next((s['火车站名'] for s in train_station_dict if s['id'] == work_point_item['区间开始站']), None),
                '区间结束站': next((s['火车站名'] for s in train_station_dict if s['id'] == work_point_item['区间结束站']), None),
            }
            processed_data.append(processed)
        return processed_data
    def get_display_work_point_and_disaster_point_info(self, work_point_id: int, disaster_point_id: int) -> List[Dict]:
        """"""
        """
        获取需要显示的工点和风险点信息
        :param work_point_id:  0表示全部
        :param disaster_point_id:  0表示全部
        :return: 
        """
        work_point_data = self.get_work_point_info(work_point_id)
        disaster_point_data = self.get_disaster_point_info(disaster_point_id)


        # 安全获取字典值的辅助函数，因为就这里使用，因此不独立出去
        def safe_get_dict_value(dict_list, index, key_name, default=''):
            try:
                if index is not None and index > 0 and len(dict_list) >= index:
                    return dict_list[index - 1][key_name]
                return default
            except (IndexError, KeyError, TypeError):
                return default

        nraprc_dict = self.get_nraprc_dict()
        railway_line_dict = self.get_railway_line()
        train_direction_dict = self.get_train_direction()
        cebie_dict = self.get_cebie_dict()
        disaster_info_dict = self.get_disaster_info()
        yifa_level_dict = self.get_disaster_yifa_level()
        pinggu_level_dict = self.get_disaster_pinggu_level()

        """将 disaster_point_data 按工点ID分组，便于查找"""
        disaster_point_map = {}
        if disaster_point_data:
            for disaster_item in disaster_point_data:
                work_point_id_key = disaster_item["工点ID"]
                if work_point_id_key not in disaster_point_map:
                    disaster_point_map[work_point_id_key] = []
                disaster_point_map[work_point_id_key].append(disaster_item)

        processed_data = []

        for work_point_item in work_point_data:
            work_point_id_key = work_point_item["工点ID"]
            """获取该工点对应的所有风险点,如果没有，就是空，然后为每个风险点（包括空的）创建一条记录"""
            disaster_items = disaster_point_map.get(work_point_id_key, [])
            railway_line_id =work_point_item.get('线别')
            train_station_dict = self.get_train_station(railway_line_id)
            if not disaster_items:
                disaster_items = [{}]
            for disaster_item in disaster_items:
                try:
                    processed = {
                        '工点ID': work_point_item.get('工点ID', ''),
                        '工点名称': work_point_item.get('工点名称', ''),
                        '风险点ID': disaster_item.get('风险点ID', '') if disaster_item else "暂无风险点",
                        '统一编码': work_point_item.get('统一编码', ''),
                        '铁路局': safe_get_dict_value(nraprc_dict, work_point_item.get('铁路局'), '铁路局'),
                        '线别': safe_get_dict_value(railway_line_dict, work_point_item.get('线别'), '线路'),
                        '线别ID':railway_line_id,
                        '区间开始站': next(
                            (s['火车站名'] for s in train_station_dict if s['id'] == work_point_item['区间开始站']),
                            None),
                        '区间结束站': next(
                            (s['火车站名'] for s in train_station_dict if s['id'] == work_point_item['区间结束站']),
                            None),
                        '里程': f"{disaster_item.get('里程K', '')}{disaster_item.get('里程开始位置', '')}~{disaster_item.get('里程结束位置', '')}" if disaster_item else '',
                        '行别': safe_get_dict_value(train_direction_dict,
                                                    disaster_item.get('行别') if disaster_item else None, '行别'),
                        '侧别': safe_get_dict_value(cebie_dict, disaster_item.get('侧别') if disaster_item else None,
                                                    '侧别'),
                        '风险评估类型': safe_get_dict_value(disaster_info_dict, disaster_item.get(
                            '风险评估类型') if disaster_item else None, 'name'),
                        '风险易发性': safe_get_dict_value(yifa_level_dict,
                                                          disaster_item.get('风险易发性') if disaster_item else None,
                                                          '灾害易发性等级'),
                        '风险评估等级': safe_get_dict_value(pinggu_level_dict, disaster_item.get(
                            '风险评估等级') if disaster_item else None, '灾害评估等级'),
                        '省或直辖市': disaster_item.get('省', '') if disaster_item else '',
                        '市': disaster_item.get('市', '') if disaster_item else '',
                        '县或区': disaster_item.get('县', '') if disaster_item else '',
                        '乡或镇': disaster_item.get('乡', '') if disaster_item else '',
                        '具体地址': disaster_item.get('具体地址', '') if disaster_item else '',
                        '经度': disaster_item.get('经度', '') if disaster_item else '',
                        '纬度': disaster_item.get('纬度', '') if disaster_item else ''
                    }
                    processed_data.append(processed)
                except Exception as e:
                    logging.error(
                        f"Unexpected error when processing work point {work_point_item} with disaster item {disaster_item}: {e}")

        return processed_data

    def get_menu_content(self, menu_id):
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
                return self.menu_content.get(menu_id)
        except:
            return None

    def get_work_point_common_content(self, menu_id):
        query = f"SELECT table_name from menu where id = {menu_id}"
        re = self.db.db_manger_do_sql(query)
        tmp = MyUtils.cal_sql_data(re)
        try:
            if tmp:
                table_name = tmp[0]['table_name']
                if menu_id not in self.menu_content or self.menu_content[menu_id] is None:
                    query = f"SELECT * FROM {table_name} "
                    re = self.db.db_manger_do_sql(query)
                    self.menu_content[menu_id] = MyUtils.cal_sql_data(re)
                    self._generate_work_point_common_data(self.menu_content[menu_id])
                logging.info(self.menu_content.get(menu_id))
                return self.menu_content.get(menu_id)
        except:
            return None

    def get_common_content(self, menu_id):
        query = f"SELECT table_name from menu where id = {menu_id}"
        re = self.db.db_manger_do_sql(query)
        tmp = MyUtils.cal_sql_data(re)
        try:
            if tmp:
                table_name = tmp[0]['table_name']
                if menu_id not in self.menu_content or self.menu_content[menu_id] is None:
                    query = f"SELECT * FROM {table_name} "
                    re = self.db.db_manger_do_sql(query)
                    self.menu_content[menu_id] = MyUtils.cal_sql_data(re)
                logging.info(self.menu_content.get(menu_id))
                return self.menu_content.get(menu_id)
        except:
            return None

    def upsert_work_point_info(self, data:dict,work_point_id =None):
        """
        """
        """函数变量名是中文拼音"""
        gong_dian_ming_cheng = MyUtils.safe_get_string(data, '工点名称',"")
        tong_yi_bian_ma = MyUtils.safe_get_string(data, '统一编码', "")
        tie_lu_ju = int(MyUtils.safe_get_number(data, '铁路局', 1))
        xian_bie = int(MyUtils.safe_get_number(data, '线别', 1))
        qu_jian_kai_shi_zhan = int(MyUtils.safe_get_number(data, '区间开始站', 1))
        qu_jian_jie_shu_zhan = int(MyUtils.safe_get_number(data, '区间结束站', 1))
        if work_point_id :
            query = (f"update work_point_info set 工点名称 = '{gong_dian_ming_cheng}',"
                     f"统一编码 = '{tong_yi_bian_ma}',铁路局 ={tie_lu_ju},线别 ={xian_bie}"
                     f",区间开始站 ={qu_jian_kai_shi_zhan},区间结束站={qu_jian_jie_shu_zhan}"
                     f" where 工点ID = {work_point_id};")
        else:
            query = (
                f"INSERT INTO work_point_info(工点名称,统一编码,铁路局,线别,区间开始站,区间结束站) VALUES ("
                f" '{gong_dian_ming_cheng}','{tong_yi_bian_ma}',{tie_lu_ju},{xian_bie},{qu_jian_kai_shi_zhan}"
                f",{qu_jian_jie_shu_zhan});")
        logging.info(query)
        re = self.db.db_manger_do_sql(query)
        self.update_work_point_info(work_point_id)

    def upsert_disaster_point_info(self,data: dict,work_point_id,disaster_point_id=None):
        """
        """
        """函数变量名是中文拼音"""
        hang_bie = MyUtils.safe_get_number(data,'行别',1)
        licheng_k,licheng_kai_shi,licheng_jie_shu = MyUtils.split_mileage_format(data['里程'])
        ce_bie = MyUtils.safe_get_number(data,'侧别',1)
        feng_xian_ping_gu_lei_xing = MyUtils.safe_get_number(data,'风险评估类型', 1)
        feng_xian_yi_fa_xing =  MyUtils.safe_get_number(data,'风险易发性', 1)
        feng_xian_ping_gu_deng_ji = MyUtils.safe_get_number(data,'风险评估等级',1)
        jing_du =  MyUtils.safe_get_number(data,'经度', 0)
        wei_du = MyUtils.safe_get_number(data,'纬度',0)
        sheng_value = MyUtils.safe_get_string(data,'省', "")
        shi_value = MyUtils.safe_get_string(data,'市', "")
        xian_value = MyUtils.safe_get_string(data,'县', "")
        xiang_value = MyUtils.safe_get_string(data,'乡', "")
        ju_ti_di_zhi =MyUtils.safe_get_string(data,'具体地址', "")
        need_insert_disaster_point_score = False
        if disaster_point_id:
            query = (f"update disaster_point_info set 行别 = {hang_bie},"
                     f"里程K = '{licheng_k}',里程开始位置 ={licheng_kai_shi}',里程结束位置 ='{licheng_jie_shu}'"
                     f",侧别 ={ce_bie},风险评估类型={feng_xian_ping_gu_lei_xing},风险易发性={feng_xian_yi_fa_xing},"
                     f"风险评估等级={feng_xian_ping_gu_deng_ji},"
                     f",经度={jing_du},纬度={wei_du},"
                     f"省='{sheng_value}',市='{shi_value}',县='{xian_value}',乡='{xiang_value}',具体地址='{ju_ti_di_zhi}',"
                     f" where disaster_point_id = '{disaster_point_id}';")
        else:
            query = (f"INSERT INTO disaster_point_info(工点ID,行别,里程K,里程开始位置,里程结束位置,侧别,风险评估类型,风险易发性,风险评估等级,"
                     f"经度,纬度,省,市,县,乡,具体地址,图片) VALUES ("
                     f" {work_point_id},{hang_bie},'{licheng_k}','{licheng_kai_shi}','{licheng_jie_shu}',{ce_bie},{feng_xian_ping_gu_lei_xing},"
                     f"{feng_xian_yi_fa_xing},{feng_xian_ping_gu_deng_ji},{jing_du},{wei_du},'{sheng_value}','{shi_value}',"
                     f"'{xian_value}','{xiang_value}','{ju_ti_di_zhi}','NULL')")
            need_insert_disaster_point_score = True
        re =self.db.db_manger_do_sql(query,return_last_id =need_insert_disaster_point_score)
        if re:
            if need_insert_disaster_point_score:
                new_disaster_id = re
                self._insert_disaster_point_score(new_disaster_id,feng_xian_ping_gu_lei_xing)
        return re

    def upsert_disaster_point_score(self,disaster_point_id,menu_id,data: dict):
        if disaster_point_id is None or menu_id is None:
            raise ValueError("缺少必要字段：work_point_id 或 menu_id")
            # 构造查询语句，检查是否存在记录
        query = f"SELECT id FROM disaster_point_score WHERE disaster_point_id = '{disaster_point_id}'  AND menu_id = '{menu_id}' and delete_mark =0"
        re = self.db.db_manger_do_sql(query)
        tmp_data = MyUtils.cal_sql_data(re)
        important_num = data.get('important_num',0)
        weight = data.get('weight',0)
        score = data.get('score',0)
        content_value = {k: v for k, v in data['content_value'].items()}
        # content_value = MyUtils.format_float_in_dict(content_value)
        content_value = json.dumps(content_value, ensure_ascii=False, separators=(',', ':'))
        image_path = data.get('image_path')
        if image_path =="NULL" or image_path is None:
            image_path = "NULL"
        else:
            image_path =  {k: self._convert_value(v) for k, v in image_path.items()}
            image_path = json.dumps(image_path, ensure_ascii=False, separators=(',', ':'))
        query = ""
        if len(tmp_data) == 0 :
            #不存在，那么就要执行插入
            query = (f"INSERT INTO disaster_point_score(disaster_point_id,menu_id,important_num,weight,score,content_value,image_path)  VALUES ({disaster_point_id},{menu_id},"
                     f"{important_num},{weight},{score},'{content_value}'"
                     f",'{image_path}');")
        else:
            query = (f"update disaster_point_score set important_num = {important_num},"
                     f"weight = {weight},score ={score},content_value ='{content_value}'"
                     f",image_path ='{image_path}' where disaster_point_id = '{disaster_point_id}' and menu_id = '{menu_id}';")
        logging.info(query)
        re =self.db.db_manger_do_sql(query)

    def get_disaster_point_score(self,disaster_point_id,menu_id = None):
        query = None
        if menu_id is None:
            query = f"select * from disaster_point_score where disaster_point_id='{disaster_point_id}'"
        else:
            query = f"select * from disaster_point_score where disaster_point_id='{disaster_point_id}' and menu_id = '{menu_id}'"
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
            logging.info(content_json)
            if item['content_value']!= "NULL":
                content_dict = json.loads(content_json)
                item["content_value"] = content_dict
            content_json = item["image_path"]  #
            if item['image_path'] != "NULL":
                content_dict = json.loads(content_json)
                item["image_path"] = content_dict
        # print(f"{query}----get_mudslide_work_point_score-{data}")
        return  data
