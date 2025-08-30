
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

-- 线路信息表
-- id: 唯一标识
-- railway_line_name: 线路名称
DROP TABLE IF EXISTS `railway_line_dict`;
CREATE TABLE railway_line_dict (
    id INTEGER PRIMARY KEY,
    "线路" TEXT NOT NULL
);
INSERT INTO railway_line_dict VALUES
(1,'青藏线'),
(2,'兰青线');

-- 站点信息表
-- id: 唯一标识
-- railway_line_name: 线路名称
DROP TABLE IF EXISTS `train_station_dict`;
CREATE TABLE train_station_dict (
    id INTEGER PRIMARY KEY,
    "火车站名" TEXT NOT NULL
);
INSERT INTO train_station_dict VALUES
(1,'海石湾站'),
(2,'老鸦城站'),
(3,'大侠站'),
(4,'平安驿站'),
(5,'水车湾站');

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

-- 工点信息表
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
    "统一编码"  TEXT NOT NULL,
    "铁路局"  INTEGER NOT NULL,
    "线别"  INTEGER NOT NULL,
    "区间开始站"  INTEGER NOT NULL,
    "区间结束站"  INTEGER NOT NULL,
    "行别"  INTEGER NOT NULL,
    "里程K" TEXT NOT NULL,
    "里程开始位置" TEXT NOT NULL,
    "里程结束位置" TEXT NOT NULL,
    "侧别" TEXT NOT NULL,
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
    "具体地址" TEXT
);

INSERT INTO work_point_info("工点ID", "统一编码","铁路局","线别", "区间开始站","区间结束站","行别","里程K","里程开始位置", "里程结束位置", "侧别", "风险评估类型","风险易发性","风险评估等级","经度","纬度","图片" ) VALUES
(1,'01-LQ',1,
 2,1,5,4,
 'K60','+022.5','+120','右',1,2,1,102.907751,
 36.3288835,'resources/disaster/01-LQ.jpg'),
(2,'01-LQ',1,
 2,1,5,4,
 'K60','+006','','右',2,2,1,102.907751,
 36.3288835,'resources/disaster/01-LQ.jpg'),
(3,'01-QZ',1,
 2,1,5,4,
 'K60','+022.5','+120','右',1,2,1,102.907751,
 36.3288835,'resources/disaster/01-LQ.jpg'),
(4,'01-QZ',1,
 2,1,5,4,
 'K60','+022.5','+120','右',3,2,1,102.907751,
 36.3288835,'resources/disaster/01-LQ.jpg'),
(5,'02-QZ',1,
 2,1,5,4,
 'K60','+022.5','+120','右',2,2,1,102.907751,
 36.3288835,'resources/disaster/01-LQ.jpg'),
(6,'01-LQ',1,
 2,1,5,4,
 'K60','+022.5','+120','右',1,2,1,102.907751,
 36.3288835,'resources/disaster/01-LQ.jpg'),
(7,'02-LQ',1,
 2,1,5,4,
 'K60','+022.5','+120','右',3,2,1,102.907751,
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
(4,'地裂缝','grand_fissure','grand_fissure_menu');


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
    icon_path TEXT NOT NULL
);

INSERT INTO menu VALUES
( 1,'灾害易发性指标', 'null'),
( 2,'灾害抑制性指标', 'null'),
( 3,'地质环境', 'null'),
( 4,'危岩体状态', 'null'),
( 5,'挡护范围', 'null'),
( 6,'挡护形式适宜性', 'null'),
( 7,'拦石墙状态', 'null'),
( 8,'边坡柔性防护网系统状态', 'null'),
( 9,'地形地貌', 'null'),
( 10,'地层岩性', 'null'),
( 11,'地质构造', 'null'),
( 12,'坡体结构', 'null'),
( 13,'水文地质', 'null'),
( 14,'边坡截排水情况', 'null'),
( 15,'周边环境', 'null'),
( 16,'危岩体体积', 'null'),
( 17,'落石运动轨迹上地形条件', 'null'),
( 18,'危岩体发育程度', 'null'),
( 19,'劣化情况', 'null'),
( 20,'变形情况', 'null'),
( 21,'基础状态', 'null'),
( 22,'墙厚缓冲垫层', 'null'),
( 23,'防护网位置和范围', 'null'),
( 24,'防护网设计', 'null'),
( 25,'构建连接状态', 'null'),
( 26,'基础状态', 'inull'),
( 27,'底部顺倾结构面', 'null'),
( 28,'底部悬空长度', 'null'),
( 29,'危岩体后界', 'null'),
( 30,'底部岩体强度', 'null'),
( 31,'危岩体侧界', 'null'),
( 32,'冻融或者根劈作用', 'null'),
( 33,'最大24H点雨量', 'null'),
( 34,'人类活动', 'nullg'),
( 35,'挡护状态', 'null'),
( 36,'泄水孔状态', 'null'),
( 37,'危岩体历史', 'null'),
( 38,'根据水文手册查算暴雨值', 'null')
;

--- 菜单内容取值
DROP TABLE IF EXISTS `content_value`;
CREATE TABLE content_value (
    id INTEGER PRIMARY KEY,
    content_value TEXT NOT NULL,
	menu_content INTEGER NOT NULL
);
INSERT INTO content_value VALUES
(1,'凸地形',1),
(2,'凹地形',1),
(3,'折线形',1),
(4,'直线形',1),
(5,'低，坡面裸露',5),
(6,'中等，坡面局部裸露',5),
(7,'高',5),
(8,'碎裂-散体结构',6),
(9,'层状结构',6),
(10,'整体块状结构',6),
(11,'软岩或全－强风化岩体为主',7),
(12,'软硬互层或强-中风化岩体为主',7),
(13,'基岩出露，岩体风化程度弱',7),
(14,'新黄土',8),
(15,'老黄土',8),
(16,'膨胀土',8),
(17,'无',8),
(18,'发育',9),
(19,'无',9),
(20,'发育',10),
(21,'无',10),
(22,'发育',11),
(23,'无',11),
(24,'发育',12),
(25,'无',12),
(26,'褶皱、断裂构造发育',13),
(27,'褶皱、断裂构造较发育',13),
(28,'地质构造简单',13),
(29,'强烈',14),
(30,'较强烈',14),
(31,'微弱，活动断裂不发育',14),


(32,'顺向坡',17),
(33,'斜向破',17),
(34,'横向破',17),
(35,'逆向坡',17),
(36,'近水平层状坡',17),
(37,'块状结构斜坡',17),


(38,'发育',18),
(39,'较发育',18),
(40,'不发育',18),

(41,'有明显软弱夹层',19),
(42,'有软弱夹层',19),
(43,'无软弱夹层',19),

(44,'有',20),
(45,'无',20),
(46,'不明显',20),

(47,'有',21),
(48,'不明显',21),
(49,'无',21),

(50,'倒悬',22),
(51,'局部倒悬',22),
(52,'无倒悬',22),

(53,'有',26),
(54,'无明显',26),
(55,'无',26),


(56,'湿润',27),
(57,'局部有喜水植物生长',27),
(58,'较干燥',27),

(59,'明显应设未设',28),
(60,'位置不当',28),
(61,'顺接不畅',28),
(62,'状态不良',28),
(63,'局部破损',28),
(64,'堵塞',28),
(65,'完善',28),

(66,'严重',29),
(67,'较严重',29),
(68,'无',29),


(69,'池塘',31),
(70,'洼地',31),
(71,'蓄水池',31),

(72,'大',32),
(73,'小',32),
(74,'无',32),

(75,'公路',33),
(76,'居民活动',33),
(77,'耕种',33),

(78,'大',34),
(79,'小',34),
(80,'无',34),


(81,'十年内发生过崩塌落石',36),
(82,'坡面存在历史遗留的落石、岩块',36),
(83,'以往崩塌落石迹象不明显',36),

(84,'存在冲沟或凹槽',37),
(85,'凸形斜坡或者折线形',37),
(86,'直线形，存在自然宽缓平台或天然凹形落石坑',37),

(87,'有',40),
(88,'无',40),

(89,'有',41),
(90,'局部贯通或者不贯通',41),

(91,'张开下错迹象明显或者有陡倾贯通结构面',43),
(92,'表层分离裂缝贯通',43),
(93,'表层分离裂缝不贯通',43),

(94,'软岩破碎',44),
(95,'硬岩破碎',44),
(96,'块状硬岩',44),

(97,'明显',46),
(98,'较明显',46),
(99,'不明显',46),

(100,'全面',47),
(101,'明显缺失',47),
(102,'一定缺失',47),


(103,'足够',48),
(104,'明显不足',48),
(105,'存在一定不足',48),

(106,'足够',49),
(107,'明显不足',49),
(108,'存在一定不足',49),

(109,'存在多处危岩、溜坍、暗洞、冲沟、风化剥落',50),
(110,'存在少量危岩、溜坍、暗洞、冲沟、风化剥落',50),
(111,'无问题',50),

(112,'设计的工程措施对危岩拦截能力和挡护能力不足要求，拦挡结构自身稳定性不足',51),
(113,'设计的工程措施对危岩拦截能力严重和挡护能力基本满足要求，拦挡结构自稳能力基本符合要求',51),
(114,'适宜',51),

(115,'局部强风化',52),
(116,'强－中风化',52),
(117,'弱－微风化',52),

(118,'有',53),
(119,'无',53),
(120,'多处',53),

(121,'松散',54),
(122,'基本密实',54),
(123,'密实',54),

(124,'30%以上脱离',55),
(125,'10%～30%脱落',55),
(126,'基本无脱离',55),

(127,'发育',56),
(128,'较发育',56),
(129,'不发育',56),

(130,'轻微',57),
(131,'明显',57),
(132,'无',57),

(133,'严重损坏',58),
(134,'轻微损坏',58),
(135,'无',58),

(136,'基础埋深不足，多处悬空',59),
(137,'基础有悬空，但程度较轻',59),
(138,'无悬空',59),

(139,'有明显开裂、隆起等现象',60),
(140,'有开裂、隆起等现象',60),
(141,'无',60),

(142,'厚度不足',61),
(143,'厚度适宜',61),
(144,'无',61),

(145,'不符合现行标准',62),
(146,'符合现行标准',62),

(147,'不符合现场实际',63),
(148,'符合现场实际',63),

(149,'严重锈蚀、破损、失效',64),
(150,'锈蚀、破损',64),
(151,'正常',64),


(152,'基础变形破坏不符合设计要求',65),
(153,'基础局部变形',65),
(154,'正常',65),

(155,'被拉出',66),
(156,'松动',66),
(157,'正常',66),

(158,'频发',15),
(159,'较频发',15),
(160,'少',15),

(161,'孔径过小、数量不足，或大部分堵塞、长草',69),
(162,'部分已堵塞、长草',69),
(163,'状态正常',69),

(164,'大片渗水',70),
(165,'少量渗水',70),
(166,'无渗水',70),

(164,'不合理，不能有效拦截；应设未设',71),
(165,'欠合理',71),
(166,'合理',71);




---菜单内容列表
DROP TABLE IF EXISTS `menu_content`;
CREATE TABLE menu_content (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
	content_unit TEXT
);

INSERT INTO menu_content VALUES
( 1,'坡形', 'QCheckBox','NULL'),
( 2,'危岩体与铁路线路垂距', 'Number','米'),
( 3,'地面坡度', 'Number','度'),
( 4,'地面相对高差', 'Number','米'),
( 5,'植被覆盖度', 'QComboBox','NULL'),
( 6,'结构', 'QComboBox','NULL'),
( 7,'岩体类型', 'QComboBox','NULL'),
( 8,'土质崩塌', 'QCheckBox','NULL'),
( 9,'陡坎', 'QComboBox','NULL'),
( 10,'探头', 'QComboBox','NULL'),
( 11,'湿陷性', 'QComboBox','NULL'),
( 12,'塌穴', 'QComboBox','NULL'),
( 13,'构造', 'QComboBox','NULL'),
( 14,'新构造运动', 'QComboBox','NULL'),
( 15,'地震', 'QComboBox','NULL'),
( 16,'地震峰值加速', 'Number','g'),
( 17,'坡类型', 'QComboBox','NULL'),
( 18,'顺向结构面', 'QComboBox','NULL'),
( 19,'坡体', 'QComboBox','NULL'),
( 20,'顺层滑动迹象', 'QComboBox','NULL'),
( 21,'土岩基覆面错动', 'QComboBox','NULL'),
( 22,'岩土体结构', 'QComboBox','NULL'),
( 23,'岩层倾向与坡向夹角', 'Number','度'),
( 24,'岩层倾角', 'Number','度'),
( 25,'节理裂隙分布', 'Number','条/m'),
( 26,'地下水出露', 'QComboBox','NULL'),
( 27,'坡面', 'QComboBox','NULL'),
( 28,'边坡截排水系统', 'QCheckBox','NULL'),
( 29,'挡护设备浸水', 'QComboBox','NULL'),
( 30,'最大24小时点雨量', 'Number','mm'),
( 31,'边坡上部有', 'QCheckBox','NULL'),
( 32,'向坡体渗透可能性', 'QComboBox','NULL'),
( 33,'边坡上存在', 'QCheckBox','NULL'),
( 34,'汛期界外水侵入、影响边坡稳定可能性', 'QComboBox','NULL'),
( 35,'危岩体体积', 'Number','立方米'),
( 36,'危岩体历史', 'QComboBox','NULL'),
( 37,'落石运动轨迹上地形条件', 'QComboBox','NULL'),
( 38,'危岩体发育程度', 'Number','分'),
( 39,'倾角', 'Number','度'),
( 40,'夹层', 'QComboBox','NULL'),
( 41,'贯通', 'QComboBox','NULL'),
( 42,'底部悬空长度', 'Number','米'),
( 43,'危岩体后界', 'QComboBox','NULL'),
( 44,'底部岩体强度', 'QComboBox','NULL'),
( 45,'贯通度', 'Number','%'),
( 46,'冻融或者根劈作用', 'QComboBox','NULL'),
( 47,'边坡防护', 'QComboBox','NULL'),
( 48,'防护高度', 'QComboBox','NULL'),
( 49,'宽度', 'QComboBox','NULL'),
( 50,'坡体', 'QComboBox','NULL'),
( 51,'既有挡护形式', 'QComboBox','NULL'),
( 52,'片石材质', 'QComboBox','NULL'),
( 53,'片石连山贯通缝', 'QComboBox','NULL'),
( 54,'砂浆', 'QComboBox','NULL'),
( 55,'勾缝', 'QComboBox','NULL'),
( 56,'墙体上杂灌', 'QComboBox','NULL'),
( 57,'墙体错断、裂缝、鼓胀、下沉等结构性损坏迹象', 'QComboBox','NULL'),
( 58,'沉降缝', 'QComboBox','NULL'),
( 59,'基础悬空', 'QComboBox','NULL'),
( 60,'基础周边侧沟和岩土体', 'QComboBox','NULL'),
( 61,'墙后缓冲垫层', 'QComboBox','NULL'),
( 62,'防护网设计', 'QComboBox','NULL'),
( 63,'防护网设计能级', 'QComboBox','NULL'),
( 64,'构件、连接件和消能装置', 'QComboBox','NULL'),
( 65,'基础状态', 'QComboBox','NULL'),
( 66,'锚杆', 'QComboBox','NULL'),
( 67,'评估得分', 'Number','分'),
( 68,'权重排序', 'Number','NULL'),
( 69,'泄水孔', 'QComboBox','NULL'),
( 70,'墙面', 'QComboBox','NULL'),
( 71,'设置位置', 'QComboBox','NULL'),
( 72,'指标评价', 'QLabel','NULL'),
( 73,'权重系数', 'QLabel','NULL'),
( 74,'建议得分', 'QLabel','NULL'),

( 75,'10min降雨量', 'Number','mm/h'),
( 76,'10min降雨量Cv', 'Number','NULL'),
( 77,'10min降雨量Cs', 'Number','NULL'),
( 78,'30min降雨量', 'Number','mm/h'),
( 79,'30min降雨量Cv', 'Number','NULL'),
( 80,'30min降雨量Cs', 'Number','NULL'),
( 81,'1h降雨量', 'Number','mm/h'),
( 82,'1h降雨量Cv', 'Number','NULL'),
( 83,'1h降雨量Cs', 'Number','NULL'),
( 84,'6h降雨量', 'Number','mm/h'),
( 85,'6h降雨量Cv', 'Number','NULL'),
( 86,'6h降雨量Cs', 'Number','NULL'),
( 87,'24h降雨量', 'Number','mm/h'),
( 88,'24h降雨量Cv', 'Number','NULL'),
( 89,'24h降雨量Cs', 'Number','NULL'),
( 90,'72h降雨量', 'Number','mm/h'),
( 91,'72h降雨量Cv', 'Number','NULL'),
( 92,'72h降雨量Cs', 'Number','NULL'),

( 93,'土类', 'Number','NULL'),
( 94,'土的成因', 'Number','NULL'),
( 95,'土的密实度', 'Number','NULL'),
( 96,'土的状态', 'Number','NULL'),
( 97,'土层厚度', 'Number','NULL'),
( 98,'土的强度', 'Number','NULL'),
( 99,'地质时代', 'Number','NULL'),
( 100,'岩石类型', 'Number','NULL'),
( 101,'岩体结构', 'Number','NULL'),
( 102,'岩石风化', 'Number','NULL'),
( 103,'岩层产状', 'Number','NULL'),
( 104,'岩体强度', 'Number','NULL'),
( 105,'补充描述', 'Number','NULL'),
( 106,'增加土层', 'QPushButton','NULL'),
( 107,'增加岩层', 'QPushButton','NULL')

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


DROP TABLE IF EXISTS `mudslide_menu_content`;
CREATE TABLE mudslide_menu_content (
    id INTEGER PRIMARY KEY,
    menu_id INTEGER NOT NULL,
	menu_content_id INTEGER NOT NULL
);

INSERT INTO mudslide_menu_content VALUES
(1,9,1),
(2,9,2),
(3,9,3),
(4,9,4),
(5,9,5),
(6,10,6),
(7,10,7),
(8,10,8),
(9,11,13),
(10,11,14),
(11,11,15),
(12,11,16),
(13,12,18),
(14,12,19),
(15,12,20),
(16,12,21),
(17,12,22),
(18,14,26),
(19,14,27),
(20,14,28),
(21,33,30),
(22,34,33),
(23,34,34),

(24,9,67),
(25,10,67),
(26,11,67),
(27,12,67),
(28,14,67),
(29,33,67),
(30,34,67),

(31,9,68),
(32,10,68),
(33,11,68),
(34,12,68),
(35,14,68),
(36,33,68),
(37,34,68),


(38,5,47),
(39,5,48),
(40,5,49),
(41,5,50),
(42,5,67),
(43,5,68),
(44,6,51),
(45,6,67),
(46,6,68),
(47,19,52),
(48,19,53),
(49,19,54),
(50,19,55),
(51,19,56),
(52,19,67),
(53,19,68),
(54,20,57),
(55,20,58),
(56,20,67),
(57,20,68),
(58,21,59),
(59,21,60),
(60,21,67),
(61,21,68),
(62,36,69),
(63,36,70),
(64,36,67),
(65,36,68),
(66,24,62),
(67,24,63),
(68,24,67),
(69,24,68),
(70,23,71),
(71,23,67),
(72,23,68),
(73,25,64),
(74,25,67),
(75,25,68),

(76,26,65),
(77,26,66),
(78,26,67),
(79,26,68),

(80,9,72),
(81,10,72),
(82,11,72),
(83,12,72),
(84,14,72),
(85,33,72),
(86,34,72),
(87,5,72),
(88,19,72),
(89,6,72),
(90,20,72),
(91,21,72),
(92,36,72),
(93,24,72),
(94,23,72),
(95,25,72),
(96,26,72),

(97,9,73),
(98,10,73),
(99,11,73),
(100,12,73),
(101,14,73),
(102,33,73),
(103,34,73),
(104,5,73),
(105,19,73),
(106,6,73),
(107,20,73),
(108,21,73),
(109,36,73),
(110,24,73),
(111,23,73),
(112,25,73),
(113,26,73)
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


-- 工点灾害值：
-- work_point_disaster_id:
-- menu_id: 菜单ID，具体信息从menu表中获取
-- menu_content_id：如果是二级或者下级，需要有父节点
-- disaster_value：当前指标级数

DROP TABLE IF EXISTS `disaster_menu_content_info`;
CREATE TABLE disaster_menu_content_info (
    work_point_id INTEGER NOT NULL,
    work_point_disaster_id INTEGER NOT NULL,
    menu_id INTEGER NOT NULL,
    menu_content_id INTEGER NOT NULL,
    disaster_value TEXT NOT NULL,
    UNIQUE (
        work_point_id,
        work_point_disaster_id,
        menu_id,
        menu_content_id
    )
);
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
    disaster_point_id INTEGER NOT NULL,
    menu_id INTEGER NOT NULL,
    important_num INTEGER NOT NULL,
    weight REAL NOT NULL,
    score REAL NOT NULL,
    content_value TEXT,
    image_path TEXT default NULL,
        UNIQUE (
        work_point_id,
        menu_id
    )
);
INSERT INTO disaster_point_score VALUES
(1,1,9,2,0.22,80,'{"1":"凸地形","3":37,"4":90,"5":"高","67":"78.6"}','NULL'),
(2,1,10,1,0.27,90,'{"6":"层状结构","7":"软硬互层或强-中风化岩体为主","8":"无","67":90}','NULL'),
(3,1,11,7,0.03,60,'{"13":"褶皱、断裂构造较发育","14":"微弱，活动断裂不发育","15":"少","16":0.15,"67":60}','NULL'),
(4,1,12,4,0.14,80,'{"18":"顺向坡","19":"有明显软弱夹层","20":"无","21":"有","22":"局部倒悬","67":80}','NULL'),
(5,1,13,0,0,0,'NULL','NULL'),
(6,1,33,5,0.1,25,'{"30":"大","31":"蓄水池","32":"小","67":25}','NULL'),
(7,1,34,3,0.18,60,'{"33":"居民活动","34":"小","67":60}','NULL'),
(8,1,14,6,0.06,80,'{"26":"无明显","27":"湿润","28":"堵塞","67":80}','NULL'),
(9,1,5,1,0.56,80,'{"47":"全面","48":"足够","49":"存在一定不足","50":"存在多处危岩、溜坍、暗洞、冲沟、风化剥落","67":80}','NULL'),
(10,1,6,2,0.33,70,'{"51":"设计的工程措施对危岩拦截能力严重和挡护能力基本满足要求，拦挡结构自稳能力基本符合要求","67":70}','NULL'),
(11,1,35,0,0,0,'NULL','NULL'),
(12,1,8,3,0.11,79.4,'{"19":"无软弱夹层","20":"无","21":"不明显","22":"无倒悬","67":79.4}','NULL'),
(13,1,19,0,0,0,'NULL','NULL'),
(14,1,20,0,0,0,'NULL','NULL'),
(15,1,21,0,0,0,'NULL','NULL'),
(16,1,36,0,0,0,'NULL','NULL'),
(17,1,23,3,0.19,60,'{"71":"合理","67":60}','NULL'),
(18,1,24,4,0.06,90,'{"62":"符合现行标准","63":"符合现场实际","67":90}','NULL'),
(19,1,25,2,0.31,60,'{"64":"锈蚀、破损","67":60}','NULL'),
(20,1,26,1,0.44,100,'{"65":"正常","66":"正常","67":100}','NULL')
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
(1,38,0,1)
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