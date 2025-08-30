import json
import os
import re
import sys


class MyUtils:
    @staticmethod
    def cal_sql_data(query_re) -> list[dict]:
        """
        将 QSqlQuery 结果转换为字典列表

        参数:
            query (QSqlQuery): 已执行的查询对象

        返回:
            list[dict]: 查询结果字典列表，每行对应一个字典
        """
        if not query_re or query_re is None:
            return []
        record = query_re.record()
        if not record or record is None:
            return []
        column_count = record.count()
        column_names = [record.fieldName(i) for i in range(column_count)]

        data = []
        # 遍历所有结果行
        while query_re.next():
            row = {}
            for i in range(column_count):
                # 获取列名和对应值
                column_name = column_names[i]
                value = query_re.value(i)

                # 处理特殊类型（可选）
                if isinstance(value, memoryview):
                    value = bytes(value).decode('utf-8')

                row[column_name] = value
            data.append(row)
        return data

    def simplify_tree(node):
        result = {}
        for name, child in node.items():
            if isinstance(child, dict):
                inner = {}
                if "children" in child and child["children"]:
                    inner.update(MyUtils.simplify_tree(child["children"]))
                if "contents" in child and child["contents"]:
                    inner.update({c: set() for c in child["contents"]})
                result[child["name"]] = inner
        return result


    def add_root_menu(menu_tree, root_name, root_id):
        """
        向菜单树中添加一个根菜单项。

        :param menu_tree: 当前的菜单树 (dict)
        :param root_name: 根菜单项的显示名称 (str)
        :param root_id: 根菜单项的唯一标识符 (hashable, 如 str 或 int)
        """
        if root_id in menu_tree:
            print(f"警告：ID '{root_id}' 已存在，不会重复添加。")
            return

        menu_tree[root_id] = {
            "name": root_name,
            "children": {}  # 用于后续添加子菜单
        }

    def add_first_menu(menu_tree, parent_id, child_name, child_id):
        """
        向指定的父菜单中添加一个第一级子菜单项。

        :param menu_tree: 菜单树 (dict)
        :param parent_id: 父菜单的 ID (str 或 int)
        :param child_name: 子菜单项的显示名称 (str)
        :param child_id: 子菜单项的唯一标识符 (hashable)
        """
        if parent_id not in menu_tree:
            print(f"错误：父菜单 '{parent_id}' 不存在。")
            return

        parent_menu = menu_tree[parent_id]

        if "children" not in parent_menu:
            parent_menu["children"] = {}

        if child_id in parent_menu["children"]:
            print(f"警告：子菜单 '{child_id}' 已存在，不会重复添加。")
            return

        parent_menu["children"][child_id] = {
            "name": child_name,
            "children": {}  # 可用于后续添加二级菜单等
        }
    def add_second_menu(menu_tree, parent_id, child_name, child_id):
        """
        向指定的一级菜单中添加一个二级菜单项。

        :param menu_tree: 菜单树 (dict)
        :param parent_id: 一级菜单的 ID（必须存在于某个父菜单的 children 中）
        :param child_name: 二级菜单项的显示名称 (str)
        :param child_id: 二级菜单项的唯一标识符 (hashable)
        """

        # 遍历整个菜单树查找 parent_id 所在的位置
        found = False
        for root_key in menu_tree:
            root_menu = menu_tree[root_key]
            if "children" in root_menu:
                parent_menu = root_menu["children"].get(parent_id)
                if parent_menu:
                    # 找到了一级菜单
                    if "children" not in parent_menu:
                        parent_menu["children"] = {}

                    if child_id in parent_menu["children"]:
                        print(f"警告：二级菜单 '{child_id}' 已存在，不会重复添加。")
                        return

                    parent_menu["children"][child_id] = {
                        "name": child_name,
                        "children": {}  # 可用于后续添加三级菜单
                    }
                    found = True
                    break

        if not found:
            print(f"错误：未找到 ID 为 '{parent_id}' 的一级菜单。")

    def add_third_menu(menu_tree, parent_id, child_name, child_id):
        """
        向指定的二级菜单中添加一个三级菜单项。

        :param menu_tree: 菜单树 (dict)
        :param parent_id: 二级菜单的 ID（必须存在于某一级菜单的 children 中）
        :param child_name: 三级菜单项的显示名称 (str)
        :param child_id: 三级菜单项的唯一标识符 (hashable)
        """
        found = False

        # 遍历根菜单下的所有一级菜单
        for root_key in menu_tree:
            root_menu = menu_tree[root_key]
            if "children" in root_menu:
                # 遍历一级菜单中的二级菜单
                for first_menu_id, first_menu in root_menu["children"].items():
                    if "children" not in first_menu:
                        continue

                    # 查找目标 parent_id 是否在二级菜单中
                    if parent_id in first_menu["children"]:
                        parent_menu = first_menu["children"][parent_id]

                        if "children" not in parent_menu:
                            parent_menu["children"] = {}

                        if child_id in parent_menu["children"]:
                            print(f"警告：三级菜单 '{child_id}' 已存在，不会重复添加。")
                            return

                        parent_menu["children"][child_id] = {
                            "name": child_name,
                            "children": {}  # 可用于后续添加四级菜单
                        }
                        found = True
                        break
                if found:
                    break

        if not found:
            print(f"错误：未找到 ID 为 '{parent_id}' 的二级菜单。")

    def add_fourth_menu(menu_tree, parent_id, child_name, child_id):
        """
        向指定的三级菜单中添加一个四级菜单项。
        :param menu_tree: 菜单树 (dict)
        :param parent_id: 三级菜单的 ID（必须存在于某二级菜单的 children 中）
        :param child_name: 四级菜单项的显示名称 (str)
        :param child_id: 四级菜单项的唯一标识符 (hashable)
        """
        found = False
        # 遍历根菜单下的所有一级菜单
        for root_key in menu_tree:
            root_menu = menu_tree[root_key]
            if "children" in root_menu:
                # 遍历一级菜单中的二级菜单
                for first_menu_id, first_menu in root_menu["children"].items():
                    if "children" not in first_menu:
                        continue
                    # 遍历二级菜单中的三级菜单
                    for second_menu_id, second_menu in first_menu["children"].items():
                        if "children" not in second_menu:
                            continue
                        third_menus = second_menu["children"]
                        if parent_id in third_menus:
                            parent_menu = third_menus[parent_id]
                            # 确保该三级菜单有 children 字段
                            if "children" not in parent_menu:
                                parent_menu["children"] = {}
                            # 检查是否已经存在该 child_id
                            if child_id in parent_menu["children"]:
                                print(f"警告：四级菜单 '{child_id}' 已存在，不会重复添加。")
                                return
                            # 添加四级菜单
                            parent_menu["children"][child_id] = {
                                "name": child_name,
                                "children": {}  # 可用于后续扩展
                            }
                            found = True
                            break
                    if found:
                        break
            if found:
                break
        if not found:
            print(f"错误：未找到 ID 为 '{parent_id}' 的三级菜单。")
    def add_end_content_to_second(menu_tree, parent_id, child_name):
        """
        在指定的二级菜单中添加一个无子菜单的最终项。

        :param menu_tree: 菜单树 (dict)
        :param parent_id: 二级菜单的 ID
        :param child_name: 最终项显示名称 (str)
        """
        found = False

        for root_key in menu_tree:
            root_menu = menu_tree[root_key]
            if "children" in root_menu:
                for first_menu_id, first_menu in root_menu["children"].items():
                    if "children" not in first_menu:
                        continue
                    second_menus = first_menu["children"]
                    if parent_id in second_menus:
                        parent_menu = second_menus[parent_id]

                        # 确保是空字典或者已有 children 字段
                        if "children" not in parent_menu:
                            parent_menu["children"] = {}

                        # 使用固定格式生成 child_id，也可以根据需要改为参数传入
                        child_id = child_name.replace(" ", "_").lower()

                        if child_id in parent_menu["children"]:
                            print(f"警告：'{child_id}' 已存在。")
                            return

                        parent_menu["children"][child_id] = {
                            "name": child_name,
                            "children": None  # 表示这是最终项，不能再有子菜单
                        }
                        found = True
                        break
                if found:
                    break

        if not found:
            print(f"错误：未找到 ID 为 '{parent_id}' 的二级菜单。")
    def add_end_content_to_third(menu_tree, parent_id, child_name):
        """
        在指定的三级菜单中添加一个无子菜单的最终项。

        :param menu_tree: 菜单树 (dict)
        :param parent_id: 三级菜单的 ID
        :param child_name: 最终项显示名称 (str)
        """
        found = False

        for root_key in menu_tree:
            root_menu = menu_tree[root_key]
            if "children" in root_menu:
                for first_menu_id, first_menu in root_menu["children"].items():
                    if "children" not in first_menu:
                        continue
                    for second_menu_id, second_menu in first_menu["children"].items():
                        if "children" not in second_menu:
                            continue
                        third_menus = second_menu["children"]
                        if parent_id in third_menus:
                            parent_menu = third_menus[parent_id]

                            # 使用固定格式生成 child_id
                            child_id = child_name.replace(" ", "_").lower()

                            if child_id in parent_menu["children"]:
                                print(f"警告：'{child_id}' 已存在。")
                                return

                            parent_menu["children"][child_id] = {
                                "name": child_name,
                                "children": None
                            }
                            found = True
                            break
                    if found:
                        break
            if found:
                break

        if not found:
            print(f"错误：未找到 ID 为 '{parent_id}' 的三级菜单。")


    def add_image_path(menu_score_item, new_path):
        """"""
        """
        向 menu_score 的某个 item 中添加 image_path 字段，并保持编号递增。

        参数:
            menu_score_item (dict): 某个菜单项的数据，如：
                {
                    'important_num': 2,
                    'weight': 0.22,
                    'score': 80.0,
                    'content_value': {'1': '凸地形', ...},
                    'image_path': 'NULL' or {1: 'path1.jpg', ...}
                }
            new_path (str): 要添加的新图片路径
        """
        # 如果没有 image_path 字段或值为 'NULL'
        if 'image_path' not in menu_score_item or menu_score_item['image_path'] == 'NULL':
            menu_score_item['image_path'] = {1: new_path}

        # 如果 image_path 是字典，继续编号
        elif isinstance(menu_score_item['image_path'], dict):
            current_keys = menu_score_item['image_path'].keys()
            int_keys = [int(k) for k in current_keys]
            max_key = max(int_keys, default=0)
            next_key = max_key + 1
            menu_score_item['image_path'][next_key] = new_path

        # 兼容旧版本字段格式（字符串路径）
        elif isinstance(menu_score_item['image_path'], str):
            # 原来只存了一个路径，转换成字典格式
            menu_score_item['image_path'] = {1: menu_score_item['image_path']}
            menu_score_item['image_path'][2] = new_path

        else:
            # 不合法类型，直接覆盖为新路径
            menu_score_item['image_path'] = {1: new_path}

        return menu_score_item

    def extract_values(data, key):
        """
        从列表中的字典中提取指定键的值。

        :param data: 包含字典的列表
        :param key: 要提取的键名
        :return: 提取后的值列表 ["",""]
        """
        return [item[key] for item in data if key in item]


    def extract_menu_data(menu_data):
        """"""
        """递归提取 menu_data 中的所有 name - value
        [{'工点ID': 1, '统一编码': '01-LQ', '铁路局': '青藏铁路公司', '区间开始站': '海石湾站', '区间结束站': '水车湾站', '行别': '上下行', '线别': '兰青线', '里程': 'K60+022.5~+120', '省或直辖市': '', '市': '', '县或区': '', '乡或镇': '', '具体地址': '', '经度': 102.907751, '纬度': 36.3288835, '风险评估类型': '滑坡', '风险易发性': '中易发', '风险评估等级': '高风险',
         'menu_data': 
         [{'menu_id': 1, 'menu_name': '灾害易发性指标',
          'children': [{'menu_id': 9, 'menu_name': '地形地貌',
           'children': [{'id': 1, 'name': '坡形', 'value': '凸地形'}, {'id': 2, 'name': '地面坡度', 'value': 37}, {'id': 3, 'name': '地面相对高差', 'value': 90}, {'id': 4, 'name': '植被覆盖度', 'value': '高'}]}, 
        {'menu_id': 10, 'menu_name': '地层岩性', 'children': [{'menu_id': 40, 'menu_name': '土质', 'children': [{'id': 1, 'name': '土类'}, {'id': 2, 'name': '土的成因'}, {'id': 3, 'name': '土的密实度'}, {'id': 4, 'name': '土的状态'}, {'id': 5, 'name': '土层厚度'}, {'id': 6, 'name': '土的强度'}, {'id': 7, 'name': '补充描述'}, {'id': 8, 'name': '土类'}, {'id': 9, 'name': '土的成因'}, {'id': 10, 'name': '土的密实度'}, {'id': 11, 'name': '土的状态'}, {'id': 12, 'name': '土层厚度'}, {'id': 13, 'name': '土的强度'}, {'id': 14, 'name': '补充描述'}]}, {'menu_id': 41, 'menu_name': '岩质', 'children': [{'id': 1, 'name': '地质时代'}, {'id': 2, 'name': '岩石类型'}, {'id': 3, 'name': '岩体结构'}, {'id': 4, 'name': '岩石风化'}, {'id': 5, 'name': '岩层产状'}, {'id': 6, 'name': '岩体强度'}, {'id': 7, 'name': '补充描述'}, {'id': 8, 'name': '地质时代'}, {'id': 9, 'name': '岩石类型'}, {'id': 10, 'name': '岩体结构'}, {'id': 11, 'name': '岩石风化'}, {'id': 12, 'name': '岩层产状'}, {'id': 13, 'name': '岩体强度'}, {'id': 14, 'name': '补充描述'}]}]},
        {'menu_id': 11, 'menu_name': '地质构造', 'children': [{'id': 1, 'name': '构造', 'value': '褶皱、断裂构造发育'}, {'id': 2, 'name': '新构造运动', 'value': '强烈'}, {'id': 3, 'name': '地震', 'value': '频发'}, {'id': 4, 'name': '地震峰值加速', 'value': 10.0}]}, {'menu_id': 12, 'menu_name': '坡体结构', 'children': [{'id': 1, 'name': '顺向结构面', 'value': '发育'}, {'id': 2, 'name': '坡体', 'value': '有明显软弱夹层'}, {'id': 3, 'name': '顺层滑动迹象', 'value': '有'}, {'id': 4, 'name': '土岩基覆面错动', 'value': '有'}, {'id': 5, 'name': '岩土体结构', 'value': '倒悬'}]}, {'menu_id': 13, 'menu_name': '水文地质', 'children': []}, {'menu_id': 33, 'menu_name': '最大24H点雨量', 'children': [{'id': 1, 'name': '最大24小时点雨量', 'value': 10.0}]}, {'menu_id': 34, 'menu_name': '人类活动', 'children': [{'id': 1, 'name': '边坡上存在', 'value': '居民活动'}, {'id': 2, 'name': '汛期界外水侵入、影响边坡稳定可能性', 'value': '小'}]}, {'menu_id': 14, 'menu_name': '边坡截排水情况', 'children': [{'id': 1, 'name': '地下水出露', 'value': '无明显'}, {'id': 2, 'name': '坡面', 'value': '湿润'}, {'id': 3, 'name': '边坡截排水系统', 'value': '堵塞'}]}]}, {'menu_id': 2, 'menu_name': '灾害抑制性指标', 'children': [{'menu_id': 5, 'menu_name': '挡护范围', 'children': [{'id': 1, 'name': '边坡防护', 'value': '全面'}, {'id': 2, 'name': '防护高度', 'value': '足够'}, {'id': 3, 'name': '宽度', 'value': '存在一定不足'}, {'id': 4, 'name': '坡体', 'value': '存在多处危岩、溜坍、暗沟、冲沟、风化剥落'}]}, {'menu_id': 6, 'menu_name': '挡护形式适宜性', 'children': [{'id': 1, 'name': '既有挡护形式', 'value': '设计的工程措施对危岩拦截能力和挡护能力不足要求，拦挡结构自身稳定性不足'}]}, {'menu_id': 35, 'menu_name': '挡护状态', 'children': [{'menu_id': 19, 'menu_name': '劣化情况', 'children': [{'id': 1, 'name': '片石材质', 'value': '局部强风化'}, {'id': 2, 'name': '片石连山贯通缝', 'value': '有'}, {'id': 3, 'name': '砂浆', 'value': '松散'}, {'id': 4, 'name': '勾缝', 'value': '30%以上脱离'}, {'id': 5, 'name': '墙体上杂灌', 'value': '发育'}]}, {'menu_id': 20, 'menu_name': '变形情况', 'children': [{'id': 1, 'name': '墙体错断、裂缝、鼓胀、下沉等结构性损坏迹象'}, {'id': 2, 'name': '沉降缝'}]}, {'menu_id': 21, 'menu_name': '挡护基础状态', 'children': [{'id': 1, 'name': '基础悬空', 'value': '基础埋深不足，多处悬空'}, {'id': 2, 'name': '基础周边侧沟和岩土体', 'value': '有明显开裂、隆起等现象'}]}, {'menu_id': 36, 'menu_name': '泄水孔状态', 'children': [{'id': 1, 'name': '泄水孔', 'value': '孔径过小、数量不足，或大部分堵塞、长草'}, {'id': 2, 'name': '墙面', 'value': '大片渗水'}]}]}, {'menu_id': 8, 'menu_name': '边坡柔性防护网系统状态', 'children': [{'menu_id': 23, 'menu_name': '防护网位置', 'children': [{'id': 1, 'name': '设置位置', 'value': '不合理，不能有效拦截；应设未设'}]}, {'menu_id': 24, 'menu_name': '防护网设计', 'children': [{'id': 1, 'name': '防护网设计', 'value': '不符合现行标准,防护网设计能级明显不符合现场实际'}]}, {'menu_id': 25, 'menu_name': '构建连接状态', 'children': [{'id': 1, 'name': '构件、连接件和消能装置', 'value': '严重锈蚀、破损、失效'}]}, {'menu_id': 26, 'menu_name': '边坡柔性防护网基础状态', 'children': []}]}]}]}
        """
        result = {}

        def recursive_extract(items):
            for item in items:
                if 'value' in item:
                    result[item['name']] = item['value']
                if 'children' in item:
                    recursive_extract(item['children'])

        recursive_extract(menu_data)
        return result

    def generate_input_regex(config: dict) -> str:
        """"""
        """
        根据 config 字典生成匹配指定范围的正则表达式字符串
        支持 int 和 float 类型的范围定义
        {"int1":"1","int2":"100"} 
        {"float1":"1","float2":"100"} 
        {"int5":"1","int2":"10"}
        """
        keys = list(config.keys())

        if not keys:
            raise ValueError("配置不能为空")

        input_type = None
        for key in keys:
            if key.startswith("int"):
                input_type = "int"
                break
            elif key.startswith("float"):
                input_type = "float"
                break

        if input_type is None:
            raise ValueError("未识别输入类型，请使用 'int*' 或 'float*' 开头的键名")

        values = list(map(float, config.values()))  # 统一转为浮点处理
        min_val, max_val = sorted(values)

        if input_type == "int":
            return MyUtils._generate_int_regex(int(min_val), int(max_val))
        elif input_type == "float":
            return MyUtils._generate_float_regex(min_val, max_val)
        else:
            raise ValueError("不支持的输入类型")

    def _generate_int_regex(min_val: int, max_val: int) -> str:
        """生成整数范围的正则表达式"""
        if min_val > max_val:
            min_val, max_val = max_val, min_val

        if min_val == max_val:
            return f"^{min_val}$"

        parts = []
        for i in range(min_val, max_val + 1):
            parts.append(str(i))

        return f"^({'|'.join(parts)})$"

    def _generate_float_regex(min_val: float, max_val: float, decimal_places=2) -> str:
        """生成浮点数范围的正则表达式，最多保留 decimal_places 位小数"""
        if min_val > max_val:
            min_val, max_val = max_val, min_val

        if int(min_val) == min_val and int(max_val) == max_val:
            min_val = int(min_val)
            max_val = int(max_val)
            return f"^(?:{max_val}(?:\\.0+)?|(?:(?:[1-9]\\d?)|(?:{min_val})))(?:\\.\\d{{1,{decimal_places}}})?)$"

        integer_range = range(int(min_val), int(max_val) + 1)

        regex_parts = []

        for integer in integer_range:
            if integer == int(min_val) and integer == int(max_val):
                left = min_val - integer
                right = max_val - integer
                regex_parts.append(f"{integer}(?:\\.([1-9]\\d{{0,{decimal_places - 1}}}))?")  # 只在范围内
            elif integer == int(min_val):
                left = min_val - integer
                regex_parts.append(f"{integer}(?:\\.([1-9]\\d{{0,{decimal_places - 1}}}))?")
            elif integer == int(max_val):
                right = max_val - integer
                regex_parts.append(f"{integer}(?:\\.([0-9]{1, {decimal_places} }))?")  # 全部允许
            else:
                regex_parts.append(f"{integer}(?:\\.([0-9]{1, {decimal_places} }))?")

        return "^(" + "|".join(regex_parts) + ")$"

    def _generate_need_checked_data(raw_value:str):
        """"""
        """
        将QLabel的value解析为需要检查的数据
        """
        data_store ={}
        try:
            parsed = json.loads(raw_value)
            # 确保数据符合规范
            if not isinstance(parsed, dict):
                raise ValueError("顶层结构必须是对象")

            # 处理所有区块
            for category, items in parsed.items():
                # 非字典区块直接存储
                if not isinstance(items, dict):
                    data_store[category] = items
                    continue
                # 字典类型深入处理
                for key, value in items.items():
                    # 使用两级结构
                    data_store.setdefault(category, {})[key] = value
            return data_store
        except Exception as e:
            return  None
    def safe_strip(value):
        """"""
        """
        将一个字符安全的转换为字符。
        因为又可能是float
        :return: 
        """
        if value is None:
            return ''
        if isinstance(value, (int, float)):
            return str(value)
        return str(value).strip()

    def split_mileage_format(text):
        """"""
        """
        格式化里程数据
        将里程转换为里程K，开始，结束
        例如：K60+220~-0.25 ,返回K60，+220，-0.25
        """
        match = re.match(r'^([^+-~]+)([+-][^~]+)~([+-][^~]+)$', text)
        if match:
            return match.group(1), match.group(2), match.group(3)
        else:
            return "", "", ""

    def safe_get_string(data: dict, key: str, default: str = "") -> str:
        """"""
        """
        安全地获取字符串值
        :param data: 字典数据
        :param key: 要获取的键
        :param default: 默认值（如果不存在或为空则返回）
        :return: 字符串
        """
        value = data.get(key)
        if value is None or not isinstance(value, (str, int, float)):
            return default
        return str(value).strip()

    def safe_get_number(data: dict, key: str, default: float = 0.0) -> float:
        """"""
        """
        安全地获取数值（int 或 float）
        :param data: 字典数据
        :param key: 要获取的键
        :param default: 默认值（如果不存在或无法转换则返回）
        :return: 数值
        """
        value = data.get(key)
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    def extract_target_values(data, extraction_config)-> dict:
        """
        灵活的数据提取函数
        :param data: 原始数据
        :param extraction_config: 提取配置，可以是：
            1. 路径映射字典: {'主键': ['子键1', '子键2']}
            2. 直接键列表: ['键1', '键2']
        :return: 提取的值字典
        """
        result = {}

        # 如果是字典形式的配置（指定路径）
        if isinstance(extraction_config, dict):
            for main_key, sub_keys in extraction_config.items():
                if main_key in data and isinstance(data[main_key], dict):
                    main_data = data[main_key]
                    for sub_key in sub_keys:
                        if sub_key in main_data:
                            result[sub_key] = main_data[sub_key]

        # 如果是列表形式的配置（直接搜索）
        elif isinstance(extraction_config, list):
            def recursive_search(d, keys_list):
                if isinstance(d, dict):
                    for key, value in d.items():
                        if key in keys_list:
                            result[key] = value
                        elif isinstance(value, dict):
                            recursive_search(value, keys_list)

            recursive_search(data, extraction_config)

        return result

    def format_float_in_dict(d:dict):
        """
        将字典进行格式化，如果是float，那么就要保留2位小数
        :return:
        """
        result = {}
        for k, v in d.items():
            if isinstance(v, float):
                result[k] = f"{v:.2f}"  # 转为字符串，保留 2 位
            elif isinstance(v, dict):
                result[k] = MyUtils.format_float_in_dict(v)
            else:
                result[k] = v
        return result