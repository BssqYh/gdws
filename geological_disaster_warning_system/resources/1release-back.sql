
-- 铁路局信息表
-- id: 唯一标识
-- national_railway_name: 铁路局名称
DROP TABLE IF EXISTS `nraprc_dict`;
CREATE TABLE nraprc_dict (
    id INTEGER PRIMARY KEY,
    "铁路局" TEXT NOT NULL
);
INSERT INTO nraprc_dict VALUES
(1,'青藏铁路公司');

-- 侧别
-- id: 唯一标识
-- railway_line_name: 线路名称
DROP TABLE IF EXISTS `cebie_dict`;
CREATE TABLE cebie_dict (
    id INTEGER PRIMARY KEY,
    "侧别" TEXT NOT NULL
);
INSERT INTO cebie_dict VALUES
(1,'左'),
(2,'右');

-- 灾害易发性
-- id: 唯一标识
-- railway_line_name: 线路名称
DROP TABLE IF EXISTS `disaster_yifa_level_dict`;
CREATE TABLE disaster_yifa_level_dict (
    id INTEGER PRIMARY KEY,
    "灾害易发性等级" TEXT NOT NULL
);
INSERT INTO disaster_yifa_level_dict VALUES
(1,'高易发'),
(2,'中易发'),
(3,'低易发');

-- 灾害易发性
-- id: 唯一标识
-- railway_line_name: 线路名称
DROP TABLE IF EXISTS `disaster_pinggu_level_dict`;
CREATE TABLE disaster_pinggu_level_dict (
    id INTEGER PRIMARY KEY,
    "灾害评估等级"  TEXT NOT NULL
);
INSERT INTO disaster_pinggu_level_dict VALUES
(1,'高风险'),
(2,'低风险'),
(3,'中风险');


-- 行别信息表
-- id: 唯一标识
-- train_direction_name: 行别
DROP TABLE IF EXISTS `train_direction_dict`;
CREATE TABLE train_direction_dict (
    id INTEGER PRIMARY KEY,
      "行别"  TEXT NOT NULL
);
INSERT INTO train_direction_dict VALUES
(1,'上行'),
(2,'下行'),
(3,'单线'),
(4,'上下行');


DROP TABLE IF EXISTS `database_info`;
CREATE TABLE database_info (
    id INTEGER PRIMARY KEY,
    "铁路局"  INTEGER NOT NULL,
    "线别"  INTEGER NOT NULL,
    image_path TEXT NOT NULL
);
INSERT INTO database_info VALUES
(1,1,1,'resources/homepage/兰青线.jpg'),
(2,1,2,'resources/homepage/兰青线.jpg')
;

-- 工点点信息表
-- id: 唯一标识
-- work_point_code: 工点编号
-- line_code：线路
-- start_location：开始地点
-- end_location：结束地点
-- direction：侧别：左、右
-- longitude：经度
-- latitude：纬度
-- image_path：图片路径

DROP TABLE IF EXISTS `work_point_info`;
CREATE TABLE work_point_info (
    "工点ID" INTEGER PRIMARY KEY,
    "工点名称"  TEXT NOT NULL,
    "统一编码"  TEXT NOT NULL,
    "铁路局"  INTEGER NOT NULL,
    "线别"  INTEGER NOT NULL,
    "区间开始站"  INTEGER NOT NULL,
    "区间结束站"  INTEGER NOT NULL,
    delete_mark INTEGER DEFAULT 0
);

INSERT INTO work_point_info("工点ID", "统一编码", "工点名称","铁路局","线别", "区间开始站","区间结束站") VALUES
(1,'01-LQ','六盘水-六枝',1, 2,1,5),
(2,'01-QZ','六枝-安顺',1, 2,1,5),
(3,'02-QZ','安顺-贵阳',2, 2,1,5),
(4,'02-LQ','贵阳-遵义',2, 2,1,5)
;

-- 风险点信息表
DROP TABLE IF EXISTS `disaster_point_info`;
CREATE TABLE disaster_point_info (
    "风险点ID" INTEGER PRIMARY KEY,
    "工点ID" INTEGER NOT NULL,
    "行别"  INTEGER NOT NULL,
    "里程K" TEXT NOT NULL,
    "里程开始位置" TEXT NOT NULL,
    "里程结束位置" TEXT NOT NULL,
    "侧别" INTEGER NOT NULL,
    "风险评估类型" INTEGER NOT NULL,
    "风险易发性" INTEGER NOT NULL,
    "风险评估等级" INTEGER NOT NULL,
    "经度" REAL NOT NULL,
    "纬度" REAL NOT NULL,
    "图片" TEXT NOT NULL,
    "省" TEXT,
    "市" TEXT ,
    "县" TEXT ,
    "乡" TEXT ,
    "具体地址" TEXT,
    delete_mark INTEGER DEFAULT 0
);
INSERT INTO disaster_point_info( "风险点ID","工点ID", "行别","里程K","里程开始位置", "里程结束位置","侧别","风险评估类型", "风险易发性","风险评估等级","经度", "纬度","图片") VALUES
(1,1,4,
 'K60','+022.5','+120',1,1,2,1,102.907751,
 36.3288835,'resources/disaster/01-LQ.jpg'),
(2,2,4,
 'K60','+006','',2,2,2,1,102.907751,
 36.3288835,'resources/disaster/01-LQ.jpg'),
(3,1,4,
 'K60','+022.5','+120',1,1,2,1,102.907751,
 36.3288835,'resources/disaster/01-LQ.jpg'),
(4,1,4,
 'K60','+022.5','+120',2,3,2,1,102.907751,
 36.3288835,'resources/disaster/01-LQ.jpg'),
(5,1,4,
 'K60','+022.5','+120',1,2,2,1,102.907751,
 36.3288835,'resources/disaster/01-LQ.jpg'),
(6,1,4,
 'K60','+022.5','+120',2,1,2,1,102.907751,
 36.3288835,'resources/disaster/01-LQ.jpg'),
(7,2,4,
 'K60','+022.5','+120',1,3,2,1,102.907751,
 36.3288835,'resources/disaster/01-LQ.jpg')
;

-- 灾害字典
-- id: 唯一标识
-- code: 代码，对应英文，值。
-- name：中文名
-- menu_level：菜单等级
-- db_name：对应数据表的名称，用来存储对应的菜单

DROP TABLE IF EXISTS `disaster_info_dict`;
CREATE TABLE disaster_info_dict (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    code TEXT NOT NULL,
    db_name TEXT NOT NULL
);

INSERT INTO disaster_info_dict VALUES
(1,'滑坡','mudslide','mudslide_menu'),
(2,'崩塌','collapse','collapse_menu'),
(3,'泥石流','landslide','landslide_menu'),
(4,'地裂缝','grand_fissure','grand_fissure_menu'),
(5,'溜坍','liu_tan','liu_tan_menu');


-- 工点灾害表：存储每个工点有多少
-- id: 唯一标识
-- work_point_id: 工点ID
-- name：中文名
-- disaster_id：灾害ID

DROP TABLE IF EXISTS `work_point_disaster`;
CREATE TABLE work_point_disaster (
    id INTEGER PRIMARY KEY,
    work_point_id INTEGER NOT NULL,
	disaster_id INTEGER NOT NULL
);

INSERT INTO work_point_disaster VALUES
(1,1,1),
(2,1,1),
(3,1,2),
(4,1,2),
(5,1,3),
(6,1,1),
(7,1,2),
(8,1,3)
;


--- 菜单列表
DROP TABLE IF EXISTS `menu`;
CREATE TABLE menu (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    table_name TEXT NOT NULL,
    icon_path TEXT NOT NULL
);

INSERT INTO menu VALUES
( 1,'灾害易发性指标','NULL', 'null'),
( 2,'灾害抑制性指标', 'NULL','null'),
( 3,'地质环境','NULL', 'null'),
( 4,'危岩体状态','NULL', 'null'),
( 5,'挡护范围', '挡护范围','null'),
( 6,'挡护形式适宜性', '挡护形式适宜性','null'),
( 7,'拦石墙状态', 'NULL','null'),
( 8,'边坡柔性防护网系统状态','NULL', 'null'),
( 9,'地形地貌', '地形地貌','null'),
( 10,'地层岩性', 'NULL','null'),
( 11,'地质构造', '地质构造','null'),
( 12,'坡体结构', '坡体结构','null'),
( 13,'水文地质', 'NULL','null'),
( 14,'边坡截排水情况', '边坡截排水情况','null'),
( 15,'周边环境', 'NULL','null'),
( 16,'危岩体体积', '危岩体体积','null'),
( 17,'落石运动轨迹上地形条件','落石运动轨迹上地形条件', 'null'),
( 18,'危岩体发育程度', '危岩体发育程度','null'),
( 19,'劣化情况', '劣化情况','null'),
( 20,'变形情况', '变形情况','null'),
( 21,'挡护基础状态', '挡护基础状态','null'),
( 22,'墙厚缓冲垫层', '墙厚缓冲垫层','null'),
( 23,'防护网位置', '防护网位置','null'),
( 24,'防护网设计', '防护网设计','null'),
( 25,'构建连接状态', '构建连接状态','null'),
( 26,'边坡柔性防护网基础状态','边坡柔性防护网基础状态', 'null'),
( 27,'底部顺倾结构面', '底部顺倾结构面','null'),
( 28,'底部悬空长度', '底部悬空长度','null'),
( 29,'危岩体后界', '危岩体后界','null'),
( 30,'底部岩体强度', '底部岩体强度','null'),
( 31,'危岩体侧界', '危岩体侧界','null'),
( 32,'冻融或者根劈作用', '冻融或者根劈作用','null'),
( 33,'最大24H点雨量', '最大24H点雨量','null'),
( 34,'人类活动', '人类活动','null'),
( 35,'挡护状态', 'NULL','null'),
( 36,'泄水孔状态', '泄水孔状态','null'),
( 37,'危岩体历史', '危岩体历史','null'),
( 38,'降雨数据', '降雨数据','null'),
( 39,'通用组件', '通用组件','null'),
( 40,'地层岩性土质', '地层岩性土质','null'),
( 41,'地层岩性岩质', '地层岩性岩质','null'),
( 42,'挡石墙基础状态', '挡石墙基础状态','null'),
( 43,'墙后缓冲垫层', '墙后缓冲垫层','null'),
( 44,'坡面汇流计算', '坡面汇流计算','null'),
( 45,'坡面汇流历时T1', '坡面汇流历时T1','null'),
( 46,'沟内汇流历时T2', '沟内汇流历时T2','null'),
( 47,'铁路水文勘测规范', '铁路水文勘测规范','null'),
( 48,'1、计算产流因子k1', '产流因子k1','null'),
( 49,'2、计算损失因子k2', '损失因子k2','null'),
( 50,'3、随暴雨衰减指数n变化指数n''', '随暴雨衰减指数n变化指数n','null'),
( 51,'4、造峰因子k3', '造峰因子k3','null'),
( 52,'5、计算主河槽流速系数A1', '主河槽流速系数A1','null'),
( 53,'6、河槽汇流因子K1', '河槽汇流因子K1','null'),
( 54,'7、流域坡面平均长度L2', '流域坡面平均长度L2','null'),
( 55,'8、山坡汇流因子K2', '山坡汇流因子K2','null'),
( 56,'9、河槽和山坡综合汇流因子x', '河槽和山坡综合汇流因子x','null'),
( 57,'10、反映流域汇流特征的指数y', '反映流域汇流特征的指数y','null'),
( 58,'11、设计坡面径流量Qp', '设计坡面径流量Qp','null'),
( 59,'断面扩散系数α0', '断面扩散系数α0','null'),
( 60,'计算洪峰流量Qp', '计算洪峰流量Qp','null'),
( 61,'按照铁路工务手册计算设计径流量', '按照铁路工务手册计算设计径流量','null'),
( 62,'2、铁路路基设计规范计算', '铁路路基设计规范计算','null'),
( 63,'3、铁路工程水文勘测设计规范', '铁路工程水文勘测设计规范','null'),
( 64,'确定清水流量Qp', '确定清水流量Qp','null'),
( 65,'坡面泥石流计算', '坡面泥石流计算','null'),
( 66,'计算泥石流流量Qc', '计算泥石流流量Qc','null'),
( 67,'计算稀性泥石流流速vc', '计算稀性泥石流流速vc','null'),
( 68,'计算黏性泥石流流速', '计算黏性泥石流流速','null'),
( 69,'一次泥石流过流总量Q', '一次泥石流过流总量Q','null'),
( 70,'一次泥石流冲出固体物QH(m3)', '一次泥石流冲出固体物QH','null'),
( 71,'泥石流中石块运动速度vs', '泥石流中石块运动速度vs','null'),
( 72,'泥石流最大冲起高度△H和受沟床阻力影响爬高△h', '泥石流最大冲起高度△H和受沟床阻力影响爬高△h','null'),
( 73,'工点基础信息', '工点基础信息','null')
;

--- 滑坡调查表内容

-- 滑坡指标体系：对应程序就是显示菜单
-- id: 唯一标识
-- menu_id: 菜单ID，具体信息从menu表中获取
-- parent_id：如果是二级或者下级，需要有父节点
-- menu_level：当前指标级数
DROP TABLE IF EXISTS `mudslide_menu`;
CREATE TABLE mudslide_menu (
    id INTEGER PRIMARY KEY,
    menu_id INTEGER NOT NULL,
	parent_id INTEGER NOT NULL,
    menu_level INTEGER NOT NULL
);

INSERT INTO mudslide_menu VALUES
(1,1,0,1),
(2,2,0,1),
(3,9,1,2),
(4,10,1,2),
(5,11,1,2),
(6,12,1,2),
(7,13,1,2),
(8,33,1,2),
(9,34,1,2),
(10,14,1,2),
(11,5,2,2),
(12,6,2,2),
(13,35,2,2),
(14,8,2,2),
(15,19,35,3),
(16,20,35,3),
(17,21,35,3),
(18,36,35,3),
(19,23,8,3),
(20,24,8,3),
(21,25,8,3),
(22,26,8,3)
;


DROP TABLE IF EXISTS `liu_tan_menu`;
CREATE TABLE liu_tan_menu (
    id INTEGER PRIMARY KEY,
    menu_id INTEGER NOT NULL,
	parent_id INTEGER NOT NULL,
    menu_level INTEGER NOT NULL
);

INSERT INTO liu_tan_menu VALUES
(1,1,0,1),
(2,2,0,1),
(3,9,1,2),
(4,10,1,2),
(5,11,1,2),
(6,12,1,2),
(7,13,1,2),
(8,33,1,2),
(9,34,1,2),
(10,14,1,2),
(11,5,2,2),
(12,6,2,2),
(13,35,2,2),
(14,8,2,2),
(15,19,35,3),
(16,20,35,3),
(17,21,35,3),
(18,36,35,3),
(19,23,8,3),
(20,24,8,3),
(21,25,8,3),
(22,26,8,3)
;
-- 崩塌指标体系：对应程序就是显示菜单
-- id: 唯一标识
-- menu_id: 菜单ID，具体信息从menu表中获取
-- parent_id：如果是二级或者下级，需要有父节点
-- menu_level：当前指标级数

DROP TABLE IF EXISTS `collapse_menu`;
CREATE TABLE collapse_menu (
    id INTEGER PRIMARY KEY,
    menu_id INTEGER NOT NULL,
	parent_id INTEGER NOT NULL,
    menu_level INTEGER NOT NULL
);

INSERT INTO collapse_menu VALUES
(1,1,0,1),
(2,2,0,1),
(3,3,1,2),
(4,4,1,2),
(5,5,2,2),
(6,6,2,2),
(7,7,2,2),
(8,8,2,2),
(9,9,3,3),
(10,10,3,3),
(11,11,3,3),
(12,12,3,3),
(13,13,3,3),
(14,14,3,3),
(15,15,3,3),
(16,16,4,3),
(17,37,4,3),
(18,17,4,3),
(19,18,4,3),
(20,19,7,3),
(21,20,7,3),
(22,21,7,3),
(23,22,7,3),
(24,23,8,3),
(25,24,8,3),
(26,25,8,3),
(27,26,8,3),
(28,27,17,4),
(29,28,17,4),
(30,29,17,4),
(31,30,17,4),
(32,31,17,4),
(33,32,17,4)
;


-- 工点菜单的值
-- id: 唯一标识
-- work_point_id:工点ID，来自于work_point_info
-- menu_id: 菜单ID，来自于menu表
-- important_num 重要性排序
-- weight：权重
-- score：得分
DROP TABLE IF EXISTS `disaster_point_score`;
CREATE TABLE disaster_point_score (
    id INTEGER PRIMARY KEY,
    work_point_id INTEGER NOT NULL,
    menu_id INTEGER NOT NULL,
    important_num INTEGER NOT NULL,
    weight REAL NOT NULL,
    score REAL NOT NULL,
    content_value TEXT,
    image_path TEXT default NULL,
    delete_mark INTEGER DEFAULT 0,
        UNIQUE (
        work_point_id,
        menu_id
    )
);
INSERT INTO disaster_point_score(id,work_point_id,menu_id,important_num,weight,score,content_value,image_path) VALUES
(1,1,9,2,0.22,80,'{"1":"凸地形","2":37,"3":90,"4":"高"}','{"1":"images\\mudslide\\e9087611ba510339b4ceb1cb8581bc6e.png","2":"images\\mudslide\\68850c5072fd78d8e6beaa969fe5be22.jpg","3":"images\\mudslide\\9caa857b895c1b69f6af566c24d055f8.jpg"}'),
(2,1,10,1,0.27,90,'{"土质1":{"1":"测试","2":"","3":"","4":"","5":"","6":"","7":""},"岩质1":{"1":"测试2","2":"","3":"","4":"","5":"","6":"","7":""}}','NULL'),
(3,1,11,7,0.03,60,'{"1":"褶皱、断裂构造发育","2":"强烈","3":"频发","4":10.0}','NULL'),
(4,1,12,4,0.14,80,'{"1":"发育","2":"有明显软弱夹层","3":"有","4":"有","5":"倒悬"}}','NULL'),
(5,1,13,0,0,0,'NULL','NULL'),
(6,1,33,5,0.1,25,'{"1":10.0}','NULL'),
(7,1,34,3,0.18,60,'{"1":"居民活动","2":"小"}','NULL'),
(8,1,14,6,0.06,80,'{"1":"无明显","2":"湿润","3":"堵塞"}','NULL'),
(9,1,5,1,0.56,80,'{"1":"全面","2":"足够","3":"存在一定不足","4":"存在多处危岩、溜坍、暗沟、冲沟、风化剥落"}','NULL'),
(10,1,6,2,0.33,70,'{"1":"设计的工程措施对危岩拦截能力和挡护能力不足要求，拦挡结构自身稳定性不足"}','NULL'),
(11,1,35,0,0,0,'NULL','NULL'),
(13,1,19,0,0,0,'{"1":"局部强风化","2":"有","3":"松散","4":"30%以上脱离","5":"发育"}','NULL'),
(14,1,20,0,0,0,'NULL','NULL'),
(15,1,21,0,0,0,'{"1":"基础埋深不足，多处悬空","2":"有明显开裂、隆起等现象"}','NULL'),
(16,1,36,0,0,0,'{"1":"孔径过小、数量不足，或大部分堵塞、长草","2":"大片渗水"}','NULL'),
(17,1,23,3,0.19,60,'{"1":"不合理，不能有效拦截；应设未设"}','NULL'),
(18,1,24,4,0.06,90,'{"1":"不符合现行标准,防护网设计能级明显不符合现场实际"}','NULL'),
(19,1,25,2,0.31,60,'{"1":"严重锈蚀、破损、失效"}','NULL'),
(20,1,26,1,0.44,100,'{}','NULL')
;

DROP TABLE IF EXISTS `mudslide_zhibiao_dict`;
CREATE TABLE mudslide_zhibiao_dict (
    id INTEGER PRIMARY KEY,
    menu_id INTEGER NOT NULL,
    "分级标准" TEXT,
    "分值范围" TEXT
);
INSERT INTO mudslide_zhibiao_dict VALUES
(1,9,'坡形为凹地形；地面相对高差>200m；地面坡度>25°为主；植被覆盖度低，坡面裸露；','70-100'),
(2,9,'坡形为凸地形；地面相对高差50m～200m；地面坡度8~25°为主；植被覆盖度中等，坡面局部裸露；','31-69'),
(3,9,'坡形为直线型；地面相对高差<50m；地面坡度小于8°；坡面植被覆盖度高；','0-30'),
(4,10,'碎裂-散体结构，覆盖层小于5m，以软岩或全－强风化岩体为主','70-100'),
(5,10,'层状结构，覆盖层大于5m，以软硬互层或强-中风化岩体为主','31-69'),
(6,10,'整体块状结构，基岩出露，岩体风化程度弱','0-30'),
(7,11,'褶皱、断裂构造发育，新构造运动强烈，地震频发，地震峰值加速A>0.15g','70-100'),
(8,11,'褶皱、断裂构造较发育，新构造运动较强烈，地震较频发，地震峰值加速度0.05g<A≤0.15g','31-69'),
(9,11,'地质构造简单，新构造运动微弱，活动断裂不发育，地震少，地震峰值加速度A≤0.05g','0-30'),
(10,12,'顺向结构面发育,坡体有明显软弱夹层，有顺层滑动迹象，土岩基覆面错动；岩土体倒悬','70-100'),
(11,12,'顺向结构面较发育,坡体有软弱夹层，顺层滑动迹象不明显，土岩基覆面错动不明显；岩土体局部倒悬','31-69'),
(12,12,'顺向结构面不发育,坡体无软弱夹层，无顺层滑动迹象，无土岩基覆面错动；岩土体无倒悬','0-30'),
(13,13,'',''),
(14,13,'',''),
(15,13,'',''),
(16,33,'',''),
(17,33,'',''),
(18,33,'',''),
(19,15,'',''),
(20,15,'',''),
(21,15,'',''),
(22,5,'',''),
(23,5,'',''),
(24,5,'',''),
(25,6,'',''),
(26,6,'',''),
(27,6,'',''),
(28,19,'',''),
(29,19,'',''),
(30,19,'','')
;


--- 泥石流调查表内容

-- 泥石流指标体系：对应程序就是显示菜单或者内容
-- id: 唯一标识
-- menu_id: 菜单ID，具体信息从menu表中获取
-- parent_id：如果是二级或者下级，需要有父节点
-- menu_level：当前指标级数

DROP TABLE IF EXISTS `debrisflow_menu`;
CREATE TABLE debrisflow_menu (
    id INTEGER PRIMARY KEY,
    menu_id INTEGER NOT NULL,
	parent_id INTEGER NOT NULL,
    menu_level INTEGER NOT NULL
);

INSERT INTO debrisflow_menu VALUES
(1,38,0,1),
(2,44,0,1),
(3,47,0,1),
(4,60,0,1),
(5,65,0,1),

(6,45,44,2),
(7,46,44,2),
(8,44,44,2),

(9,48,47,2),
(10,49,47,2),
(11,50,47,2),
(12,51,47,2),
(13,52,47,2),
(14,53,47,2),
(15,54,47,2),
(16,55,47,2),
(17,56,47,2),
(18,57,47,2),
(19,58,47,2),

(20,61,60,2),
(23,64,60,2),

(24,66,65,2),
(25,67,65,2),
(26,68,65,2),
(27,69,65,2),
(28,70,65,2),
(29,71,65,2),
(30,72,65,2)

;

DROP TABLE IF EXISTS `debrisflow_menu_content`;
CREATE TABLE debrisflow_menu_content (
    id INTEGER PRIMARY KEY,
    menu_id INTEGER NOT NULL,
	menu_content_id INTEGER NOT NULL
);
INSERT INTO debrisflow_menu_content VALUES
(1,38,75),
(2,38,76),
(3,38,77),
(4,38,78),
(5,38,79),
(6,38,80),
(7,38,81),
(8,38,82),
(9,38,83),
(10,38,84),
(11,38,85),
(12,38,86),
(13,38,87),
(14,38,88),
(15,38,89),
(16,38,90),
(17,38,91),
(18,38,92)
;