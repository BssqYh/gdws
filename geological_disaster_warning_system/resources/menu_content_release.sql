DROP TABLE IF EXISTS 工点基础信息;
CREATE TABLE 工点基础信息 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    is_work_point INTEGER NOT NULL DEFAULT 1,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 工点基础信息 VALUES
(1,'工点ID','QLineEdit','NULL',null,1,0),
(2,'工点名称','QLineEdit','NULL',null,1,0),
(3,'统一编码','QLineEdit','NULL',null,1,0),
(4,'铁路局','QComboBox','NULL',null,1,0),
(5,'线别','QComboBox','NULL',null,1,0),
(6,'侧别','QComboBox','NULL',null,0,0),
(7,'区间开始站','QComboBox','NULL',null,1,0),
(8,'区间结束站','QComboBox','NULL',null,1,0),
(9,'里程','QLineEdit','NULL',null,0,0),
(10,'行别','QComboBox','NULL',null,0,0),
(11,'风险评估类型','QComboBox','NULL',null,0,0),
(12,'风险易发性','QComboBox','NULL',null,0,0),
(13,'风险评估等级','QComboBox','NULL',null,0,0),
(14,'地区选择','ChinaAreaSelector','NULL',null,0,0),
(15,'具体地址','QLineEdit','NULL',null,0,0),
(16,'经度','Number','NULL',null,0,0),
(17,'纬度','Number','NULL',null,0,0)
;


-- ----------------------------
-- 表: 地形地貌 (menu_id=9)
-- ----------------------------
DROP TABLE IF EXISTS 地形地貌;
CREATE TABLE 地形地貌 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 地形地貌 VALUES
(1,1,'坡形','QCheckBox','NULL','{1:"凸地形",2:"凹地形",3:"折线形",4:"直线形"}',0),
(2,1,'地面坡度','Number','°',null,0),
(3,1,'地面相对高差','Number','m',null,0),
(4,1,'植被覆盖度','QComboBox','NULL','{1:"低，坡面裸露",2:"中等，坡面局部裸露",3:"高"}',0),
(5,2,'坡形','QCheckBox','NULL','{1:"凸地形",2:"凹地形",3:"折线形",4:"直线形"}',0),
(6,2,'危岩体与铁路线路的垂距','Number','m',null,0),
(7,2,'地面坡度','Number','°',null,0),
(8,2,'植被覆盖度','QComboBox','NULL','{1:"低，坡面裸露",2:"中等，坡面局部裸露",3:"高"}',0)
;

-- ----------------------------
-- 表: 地层岩性 (menu_id=10)
-- ----------------------------
-- 土质岩质 ：1表示土质 2表示岩质
DROP TABLE IF EXISTS 地层岩性土质;
CREATE TABLE 地层岩性土质 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 地层岩性土质 VALUES
(1,1,'土类', 'QTextEdit','NULL',null,0),
(2,1,'土的成因','QTextEdit','NULL',null,0),
(3,1,'土的密实度', 'QTextEdit','NULL',null,0),
(4,1,'土的状态', 'QTextEdit','NULL',null,0),
(5,1,'土层厚度', 'QTextEdit','NULL',null,0),
(6,1,'土的强度', 'QTextEdit','NULL',null,0),
(7,1,'补充描述', 'QTextEdit','NULL',null,0),
(8,2,'土类', 'QTextEdit','NULL',null,0),
(9,2,'土的成因','QTextEdit','NULL',null,0),
(10,2,'土的密实度', 'QTextEdit','NULL',null,0),
(11,2,'土的状态', 'QTextEdit','NULL',null,0),
(12,2,'土层厚度', 'QTextEdit','NULL',null,0),
(13,2,'土的强度', 'QTextEdit','NULL',null,0),
(14,2,'补充描述', 'QTextEdit','NULL',null,0)
;

DROP TABLE IF EXISTS 地层岩性岩质;
CREATE TABLE 地层岩性岩质 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 地层岩性岩质 VALUES
(1,1,'地质时代', 'QTextEdit','NULL',null,0),
(2,1,'岩石类型','QTextEdit','NULL',null,0),
(3,1,'岩体结构', 'QTextEdit','NULL',null,0),
(4,1,'岩石风化', 'QTextEdit','NULL',null,0),
(5,1,'岩层产状', 'QTextEdit','NULL',null,0),
(6,1,'岩体强度', 'QTextEdit','NULL',null,0),
(7,1,'补充描述', 'QTextEdit','NULL',null,0),
(8,2,'地质时代', 'QTextEdit','NULL',null,0),
(9,2,'岩石类型','QTextEdit','NULL',null,0),
(10,2,'岩体结构', 'QTextEdit','NULL',null,0),
(11,2,'岩石风化', 'QTextEdit','NULL',null,0),
(12,2,'岩层产状', 'QTextEdit','NULL',null,0),
(13,2,'岩体强度', 'QTextEdit','NULL',null,0),
(14,2,'补充描述', 'QTextEdit','NULL',null,0)
;
-- ----------------------------
-- 表: 地质构造 (menu_id=11)
-- ----------------------------
DROP TABLE IF EXISTS 地质构造;
CREATE TABLE 地质构造 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 地质构造 VALUES
(1,1,'构造','QComboBox','NULL','{1:"褶皱、断裂构造发育",2:"褶皱、断裂构造较发育",3:"地质构造简单"}',0),
(2,1,'新构造运动','QComboBox','NULL','{1:"强烈",2:"较强烈",3:"微弱，活动断裂不发育"}',0),
(3,1,'地震','QComboBox','NULL','{1:"频发",2:"较频发",3:"少"}',0),
(4,1,'地震峰值加速','Number','g',null,0),
(5,2,'构造','QComboBox','NULL','{1:"褶皱、断裂构造发育",2:"褶皱、断裂构造较发育",3:"地质构造简单"}',0),
(6,2,'新构造运动','QComboBox','NULL','{1:"强烈",2:"较强烈",3:"微弱，活动断裂不发育"}',0),
(7,2,'地震','QComboBox','NULL','{1:"频发",2:"较频发",3:"少"}',0),
(8,2,'地震峰值加速','Number','g',null,0)
;

-- ----------------------------
-- 表: 坡体结构 (menu_id=12)
-- ----------------------------
DROP TABLE IF EXISTS 坡体结构;
CREATE TABLE 坡体结构 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 坡体结构 VALUES
(1,1,'顺向结构面','QComboBox','NULL','{1:"发育",2:"较发育",3:"不发育"}',0),
(2,1,'坡体','QComboBox','NULL','{1:"有明显软弱夹层",2:"有软弱夹层",3:"无软弱夹层"}',0),
(3,1,'顺层滑动迹象','QComboBox','NULL','{1:"有",2:"无",3:"不明显"}',0),
(4,1,'土岩基覆面错动','QComboBox','NULL','{1:"有",2:"无",3:"不明显"}',0),
(5,1,'岩土体结构','QComboBox','NULL','{1:"倒悬",2:"局部倒悬",3:"无倒悬"}',0),
(6,2,'顺向结构面','QComboBox','NULL','{1:"发育",2:"较发育",3:"不发育"}',0),
(7,2,'岩层倾向与坡向夹角','Number','°',null,0),
(8,2,'岩层倾角','Number','°',null,0),
(9,2,'节理裂隙分布','Number','条/m',null,0),
(10,2,'坡体','QComboBox','NULL','{1:"有明显软弱夹层",2:"有软弱夹层",3:"无软弱夹层"}',0),
(11,2,'岩土体结构','QComboBox','NULL','{1:"倒悬",2:"局部倒悬",3:"无倒悬"}',0)
;

-- ----------------------------
-- 表: 最大24H点雨量 (menu_id=33)
-- ----------------------------
DROP TABLE IF EXISTS 最大24H点雨量;
CREATE TABLE 最大24H点雨量 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 最大24H点雨量 VALUES
(1,1,'最大24小时点雨量','Number','mm',null,0),
(2,2,'最大24小时点雨量','Number','mm',null,0)
;


-- ----------------------------
-- 表: 人类活动 (menu_id=34)
-- ----------------------------
DROP TABLE IF EXISTS 人类活动;
CREATE TABLE 人类活动 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 人类活动 VALUES
(1,1,'边坡上存在','QCheckBox','NULL','{1:"公路",2:"居民活动",3:"耕种"}',0),
(2,1,'汛期界外水侵入、影响边坡稳定可能性','QComboBox','NULL','{1:"大",2:"小",3:"无"}',0),
(3,2,'岩体稳定性受地下采矿、露天采石等影响','QComboBox','NULL','{1:"大",2:"受影响",3:"无"}',0),
(4,2,'位置','QCheckBox','NULL','{1:"曲线",2:"隧道口",3:"滨河路堤",4:"高陡路堤",5:"其他复杂场所"}',0),
(5,2,'边坡上存在','QCheckBox','NULL','{1:"公路",2:"居民活动",3:"耕种",4:"采矿",5:"采石"}',0),
(6,2,'汛期界外水侵入、影响边坡稳定可能性','QComboBox','NULL','{1:"大",2:"小",3:"无"}',0)
;
-- ----------------------------
-- 表: 边坡截排水情况 (menu_id=14)
-- ----------------------------
DROP TABLE IF EXISTS 边坡截排水情况;
CREATE TABLE 边坡截排水情况 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 边坡截排水情况 VALUES
(1,1,'地下水出露','QCheckBox','NULL','{1:"有",2:"无",3:"无明显"}',0),
(2,1,'坡面','QComboBox','NULL','{1:"湿润",2:"局部有喜水植物生长",3:"较干燥"}',0),
(3,1,'边坡截排水系统','QComboBox','NULL','{1:"明显应设未设",2:"位置不当",3:"顺接不畅",4:"状态不良",5:"局部破损",6:"堵塞",7:"完善"}',0),
(4,2,'边坡截排水系统','QComboBox','NULL','{1:"明显应设未设",2:"位置不当",3:"顺接不畅",4:"状态不良",5:"局部破损",6:"堵塞",7:"完善"}',0),
(5,2,'挡护设备','QComboBox','NULL','{1:"浸水严重",2:"浸水较严重",3:"无地下水出露，坡面较干燥"}',0)
;


-- ----------------------------
-- 表: 挡护范围 (menu_id=5)
-- ----------------------------
DROP TABLE IF EXISTS 挡护范围;
CREATE TABLE 挡护范围 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 挡护范围 VALUES
(1,1,'边坡防护','QComboBox','NULL','{1:"全面",2:"明显缺失",3:"一定缺失"}',0),
(2,1,'防护高度','QComboBox','NULL','{1:"足够",2:"明显不足",3:"存在一定不足"}',0),
(3,1,'宽度','QComboBox','NULL','{1:"足够",2:"明显不足",3:"存在一定不足"}',0),
(4,1,'坡体','QComboBox','NULL','{1:"存在多处危岩、溜坍、暗沟、冲沟、风化剥落",2:"存在少量危岩、溜坍、暗沟、冲沟、风化剥落",3:"无问题"}',0),
(5,2,'边坡防护','QComboBox','NULL','{1:"全面",2:"明显缺失，防护高度和宽度明显不足，应防护未防护",3:"存在一定的防护高度和宽度不足问题"}',0),
(6,2,'坡体','QComboBox','NULL','{1:"坡体存在多处危岩和风化剥落",2:"坡体存在少量危岩和风化等问题",3:"无问题"}',0)
;

-- ----------------------------
-- 表: 挡护形式适宜性 (menu_id=6)
-- ----------------------------
DROP TABLE IF EXISTS 挡护形式适宜性;
CREATE TABLE 挡护形式适宜性 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 挡护形式适宜性 VALUES
(1,1,'既有挡护形式','QComboBox','NULL','{1:"设计的工程措施对危岩拦截能力和挡护能力不足要求，拦挡结构自身稳定性不足",2:"设计的工程措施对危岩拦截能力严重和挡护能力基本满足要求，拦挡结构自稳能力基本符合要求",3:"适宜"}',0)
;

-- ----------------------------
-- 表: 危岩体发育程度 (menu_id=19)
-- ----------------------------
DROP TABLE IF EXISTS 危岩体发育程度;
CREATE TABLE 危岩体发育程度 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 危岩体发育程度 VALUES
(1,1,'片石材质','QComboBox','NULL','{1:"局部强风化",2:"强－中风化",3:"弱－微风化"}',0),
(2,1,'片石连山贯通缝','QComboBox','NULL','{1:"有",2:"无",3:"多处"}',0),
(3,1,'砂浆','QComboBox','NULL','{1:"松散",2:"基本密实",3:"密实"}',0),
(4,1,'勾缝','QComboBox','NULL','{1:"30%以上脱离",2:"10%～30%脱落",3:"基本无脱离"}',0),
(5,1,'墙体上杂灌','QComboBox','NULL','{1:"发育",2:"较发育",3:"不发育"}',0)
;

-- ----------------------------
-- 表: 劣化情况 (menu_id=20)
-- ----------------------------
DROP TABLE IF EXISTS 劣化情况;
CREATE TABLE 劣化情况 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 劣化情况 VALUES
(1,1,'片石材质','QComboBox','NULL','{1:"局部强风化",2:"强－中风化",3:"弱－微风化"}',0),
(2,1,'片石连山贯通缝','QComboBox','NULL','{1:"有",2:"无",3:"多处"}',0),
(3,1,'砂浆','QComboBox','NULL','{1:"松散",2:"基本密实",3:"密实"}',0),
(4,1,'勾缝','QComboBox','NULL','{1:"30%以上脱离",2:"10%～30%脱落",3:"基本无脱离"}',0),
(5,1,'墙体上杂灌','QComboBox','分','{1:"发育",2:"较发育",3:"不发育"}',0),
(6,2,'片石材质','QComboBox','NULL','{1:"局部强风化",2:"强－中风化",3:"弱－微风化"}',0),
(7,2,'片石连山贯通缝','QComboBox','NULL','{1:"有",2:"无",3:"多处"}',0),
(8,2,'砂浆','QComboBox','NULL','{1:"松散",2:"基本密实",3:"密实"}',0),
(9,2,'勾缝','QComboBox','NULL','{1:"30%以上脱离",2:"10%～30%脱落",3:"基本无脱离"}',0),
(10,2,'墙体上杂灌','QComboBox','分','{1:"发育",2:"较发育",3:"不发育"}',0)
;
-- ----------------------------
-- 表: 变形情况 (menu_id=21)
-- ----------------------------
DROP TABLE IF EXISTS 变形情况;
CREATE TABLE 变形情况 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 变形情况 VALUES
(1,1,'墙体错断、裂缝、鼓胀、下沉等结构性损坏迹象','QComboBox','NULL','{1:"轻微",2:"明显",3:"无"}',0),
(2,1,'沉降缝','QComboBox','NULL','{1:"严重损坏",2:"轻微损坏",3:"无"}',0),
(3,2,'墙体错断、裂缝、鼓胀、下沉等结构性损坏迹象','QComboBox','NULL','{1:"轻微",2:"明显",3:"无"}',0),
(4,2,'沉降缝','QComboBox','NULL','{1:"严重损坏",2:"轻微损坏",3:"无"}',0)
;


-- ----------------------------
-- 表: 挡石墙基础状态 (menu_id=42)
-- ----------------------------
DROP TABLE IF EXISTS 挡石墙基础状态;
CREATE TABLE 挡石墙基础状态 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 挡石墙基础状态 VALUES
(1,2,'基础','QComboBox','NULL','{1:"埋深不足，多处悬空",2:"有悬空，但程度较轻",3:"无悬空"}',0),
(2,2,'基础周边侧沟和岩土体','QComboBox','NULL','{1:"有明显开裂、隆起等现象",2:"有开裂、隆起等现象",3:"无开裂、隆起等现象"}',0)
;


-- ----------------------------
-- 表: 墙后缓冲垫层 (menu_id=43)
-- ----------------------------
DROP TABLE IF EXISTS 墙后缓冲垫层;
CREATE TABLE 墙后缓冲垫层 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 墙后缓冲垫层 VALUES
(1,2,'墙后缓冲垫层','QComboBox','NULL','{1:"墙后无缓冲垫层",2:"墙后缓冲垫层厚度不足",3:"墙后缓冲垫层厚度适宜"}',0)
;
-- ----------------------------
-- 表: 危岩体体积 (menu_id=36)
-- ----------------------------
DROP TABLE IF EXISTS 危岩体体积;
CREATE TABLE 危岩体体积 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 危岩体体积 VALUES
(1,2,'V','Number','m³',null,0)
;
-- ----------------------------
-- 表: 危岩体历史 (menu_id=36)
-- ----------------------------
DROP TABLE IF EXISTS 危岩体历史;
CREATE TABLE 危岩体历史 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 危岩体历史 VALUES
(1,2,'危岩体历史','QComboBox','NULL','{1:"十年内发生过崩塌落石",2:"坡面存在历史遗留的落石、岩块",3:"以往崩塌落石迹象不明显"}',0)
;

-- ----------------------------
-- 表: 落石运动轨迹上地形条件 (menu_id=17)
-- ----------------------------
DROP TABLE IF EXISTS 落石运动轨迹上地形条件;
CREATE TABLE 落石运动轨迹上地形条件 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 落石运动轨迹上地形条件 VALUES
(1,2,'地形','QComboBox','NULL','{1:"存在冲沟或凹槽",2:"凸形斜坡或者折线形",3:"直线形，存在自然宽缓平台或天然凹形落石坑"}',0)
;


-- ----------------------------
-- 表: 底部顺倾结构面 (menu_id=27)
-- ----------------------------
DROP TABLE IF EXISTS 底部顺倾结构面;
CREATE TABLE 底部顺倾结构面 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 底部顺倾结构面 VALUES
(1,2,'倾角','Number','°',null,0),
(2,2,'夹层','QComboBox','NULL','{1:"有",2:"无"}',0),
(3,2,'贯通性','QComboBox','NULL','{1:"贯通",2:"局部贯通",3:"不贯通"}',0)
;

-- ----------------------------
-- 表: 底部悬空长度 (menu_id=28)
-- ----------------------------
DROP TABLE IF EXISTS 底部悬空长度;
CREATE TABLE 底部悬空长度 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 底部悬空长度 VALUES
(1,2,'底部悬空长度','Number','m',null,0)
;
-- ----------------------------
-- 表: 危岩体后界 (menu_id=29)
-- ----------------------------
DROP TABLE IF EXISTS 危岩体后界;
CREATE TABLE 危岩体后界 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 危岩体后界 VALUES
(1,2,'危岩体后界','QComboBox','NULL','{1:"张开下错迹象明显或者有陡倾贯通结构面",2:"表层分离裂缝贯通",3:"表层分离裂缝不贯通"}',0)
;

-- ----------------------------
-- 表: 底部岩体强度 (menu_id=30)
-- ----------------------------
DROP TABLE IF EXISTS 底部岩体强度;
CREATE TABLE 底部岩体强度 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 底部岩体强度 VALUES
(1,2,'底部岩体强度','QComboBox','NULL','{1:"软岩破碎",2:"硬岩破碎",3:"块状硬岩"}',0)
;


-- ----------------------------
-- 表: 危岩体侧界 (menu_id=31)
-- ----------------------------
DROP TABLE IF EXISTS 危岩体侧界;
CREATE TABLE 危岩体侧界 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 危岩体侧界 VALUES
(1,2,'贯通度','Number','%',null,0)
;


-- ----------------------------
-- 表: 冻融或者根劈作用 (menu_id=32)
-- ----------------------------
DROP TABLE IF EXISTS 冻融或者根劈作用;
CREATE TABLE 冻融或者根劈作用 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 冻融或者根劈作用 VALUES
(1,2,'冻融或者根劈作用','QComboBox','NULL','{1:"明显",2:"较明显",3:"不明显"}',0)
;
-- ----------------------------
-- 表: 防护网设计 (menu_id=24)
-- ----------------------------
DROP TABLE IF EXISTS 防护网设计;
CREATE TABLE 防护网设计 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 防护网设计 VALUES
(1,1,'防护网设计','QComboBox','NULL','{1:"不符合现行标准,防护网设计能级明显不符合现场实际",2:"符合现行标准，但防护网设计能级不符合现场实际",3:"符合现行标准，设计能级符合现场实际"}',0),
(2,2,'防护网设计','QComboBox','NULL','{1:"不符合现行标准,防护网设计能级明显不符合现场实际",2:"符合现行标准，但防护网设计能级不符合现场实际",3:"符合现行标准，设计能级符合现场实际"}',0)
;

-- ----------------------------
-- 表: 防护网位置(menu_id=23)
-- ----------------------------
DROP TABLE IF EXISTS 防护网位置;
CREATE TABLE 防护网位置 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 防护网位置 VALUES
(1,1,'设置位置','QComboBox','NULL','{1:"不合理，不能有效拦截；应设未设",2:"欠合理",3:"合理"}',0),
(2,2,'边坡防护','QComboBox','NULL','{1:"明显缺失，防护高度和宽度明显不足，应防护未防护",2:"存在一定的防护高度和宽度不足问题",3:"全面"}',0)
;

-- ----------------------------
-- 表: 构建连接状态 (menu_id=25)
-- ----------------------------
DROP TABLE IF EXISTS 构建连接状态;
CREATE TABLE 构建连接状态 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 构建连接状态 VALUES
(1,1,'构件、连接件和消能装置','QComboBox','NULL','{1:"严重锈蚀、破损、失效",2:"锈蚀、破损",3:"正常"}',0),
(2,2,'构件、连接件和消能装置','QComboBox','NULL','{1:"严重锈蚀、破损、失效",2:"锈蚀、破损",3:"正常"}',0)
;

-- ----------------------------
-- 表: 基础状态 (menu_id=26)
-- ----------------------------
DROP TABLE IF EXISTS 挡护基础状态;
CREATE TABLE 挡护基础状态 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 挡护基础状态 VALUES
(1,1,'基础悬空','QComboBox','NULL','{1:"基础埋深不足，多处悬空",2:"基础有悬空，但程度较轻",3:"无悬空"}',0),
(2,1,'基础周边侧沟和岩土体','QComboBox','NULL','{1:"有明显开裂、隆起等现象",2:"有开裂、隆起等现象",3:"无"}',0)
;

DROP TABLE IF EXISTS 边坡柔性防护网基础状态;
CREATE TABLE 边坡柔性防护网基础状态 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 边坡柔性防护网基础状态 VALUES
(1,2,'基础状态','QComboBox','NULL','{1:"基础变形破坏不符合设计要求",2:"基础局部变形",3:"正常"}',0),
(2,2,'锚杆','QComboBox','NULL','{1:"被拉出",2:"松动",3:"正常"}',0)
;
-- ----------------------------
-- 表: 泄水孔状态 (menu_id=69)
-- ----------------------------
DROP TABLE IF EXISTS 泄水孔状态;
CREATE TABLE 泄水孔状态 (
    id INTEGER PRIMARY KEY,
    disaster_id INTEGER NOT NULL DEFAULT 1,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);

INSERT INTO 泄水孔状态 VALUES
(1,1,'泄水孔','QComboBox','NULL','{1:"孔径过小、数量不足，或大部分堵塞、长草",2:"部分已堵塞、长草",3:"状态正常"}',0),
(2,1,'墙面','QComboBox','NULL','{1:"大片渗水",2:"少量渗水",3:"无渗水"}',0)
;


DROP TABLE IF EXISTS 通用组件;
CREATE TABLE 通用组件 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 通用组件 VALUES
(1,'权重排序','Number','NULL',null,0),
(2,'权重系数','QLabel','NULL',null,0),
(3,'建议得分','QLabel','NULL',null,0),
(4,'评估得分','Number','分',null,0),
(5,'指标评价','QTextEdit','NULL',null,0)
;

DROP TABLE IF EXISTS 降雨数据;
CREATE TABLE 降雨数据 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 降雨数据 VALUES
(1,'降雨参数','TEXT','{"1":"10min降雨量","2":"30min降雨量","3":"1h降雨量","4":"6h降雨量","5":"24h降雨量","6":"72h降雨量"}',null,0),
(2,'降雨量（mm/h）','TEXT','NULL',null,0),
(3,'Cv','TEXT','NULL',null,0),
(4,'Cs','TEXT','分',null,0),
(5,'百年一遇sp','TEXT','mm/h',null,0),
(6,'五十年一遇sp','TEXT','mm/h',null,0)
;

DROP TABLE IF EXISTS 坡面汇流计算;
CREATE TABLE 坡面汇流计算 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    "前置条件" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 坡面汇流计算 VALUES
(1,'重现期','Number','年',null,null,null,0),
(2,'使用沟内汇流进行计算','ToggleButton','NULL','{"存在性-降雨历时":{"0":"45-坡面汇流历时T1","1":"100-测试"}}',null,null,0),
(3,'降雨历时','QLabel','min',null,null,'{"存在性":{"45":"坡面汇流历时T1"},"判断性":{"1":"5=6"}}',0),
(4,'重现期转换系数Cp','Number','NULL',null,null,null,1),
(5,'C₆₀','Number','NULL',null,null,null,0),
(6,'降雨历时转换系数Ct','Number','NULL',null,null,null,1),
(7,'I₅,₁₀','Number','NULL',null,null,null,0),
(8,'平均降雨强度','QLabel','NULL',null,'重现期转换系数Cp*降雨历时转换系数Ct*(I₅,₁₀)',null,0),
(9,'地表径流系数','Number','NULL',null,null,null,1),
(10,'汇水面积','Number','NULL',null,null,null,0),
(11,'设计径流量','QLabel','NULL',null,'16.67*平均降雨强度*地表径流系数*汇水面积*1.1',null,0),
(12,'五十年一遇洪峰流量','QLabel','NULL',null,'16.67*2.84*地表径流系数*汇水面积*1.1',null,0),
(13,'百年一遇洪峰流量','QLabel','NULL',null,'16.67*3.25*地表径流系数*汇水面积*1.1',null,0)
;

DROP TABLE IF EXISTS 坡面汇流历时T1;
CREATE TABLE 坡面汇流历时T1 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 坡面汇流历时T1 VALUES
(1,'地表粗度系数m1','Number','NULL',null,null,1),
(2,'坡面流的长度Ls','Number','NULL',null,null,0),
(3,'坡面流的坡度is','Number','NULL',null,null,0),
(4,'坡面汇流历时T1','QLabel','min',null,'1.445*(地表粗度系数m1*坡面流的长度Ls/(坡面流的坡度is**0.5))**0.467',0)
;
DROP TABLE IF EXISTS 沟内汇流历时T2;
CREATE TABLE 沟内汇流历时T2 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 沟内汇流历时T2 VALUES
(1,'第i段水沟长度','Number','m',null,null,0),
(2,'第i段沟平均流速','Number','m/s',null,null,0),
(3,'沟内汇流历时T2','QLabel','min',null,'第i段水沟长度/(20*第i段沟平均流速**0.6)/60',0)
;

DROP TABLE IF EXISTS 铁路水文勘测规范;
CREATE TABLE 铁路水文勘测规范 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 铁路水文勘测规范 VALUES
(1,'铁路水文勘测规范','有子表','NULL','{"1":"48","2":"49","3":"50","4":"51","5":"52","6":"53","7":"54","8":"55","9":"56","10":"57","11":"58"}',0)
;

DROP TABLE IF EXISTS 产流因子k1;
CREATE TABLE 产流因子k1 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    "前置条件" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 产流因子k1 VALUES
(1,'η值','Number','NULL',null,null,null,1),
(2,'汇水面积','QLabel','km2',null,null,'{"存在性":{"44":"汇水面积"},"判断性":{"1":"5=6"}}',0),
(3,'五十年一遇sp','QLabel','mm/h',null,null,'{"存在性":{"38":"五十年一遇sp"},"判断性":{"1":"5=6"}}',0),
(4,'五十年一遇产流因子K1','QLabel','NULL',null,'0.278*汇水面积*η值*五十年一遇sp',null,0),
(5,'百年一遇sp','QLabel','mm/h',null,null,'{"存在性":{"38":"百年一遇sp"},"判断性":{"1":"5=6"}}',0),
(6,'百年一遇产流因子K1','QLabel','NULL',null,'0.278*汇水面积*η值*百年一遇sp',null,0)
;

DROP TABLE IF EXISTS 损失因子k2;
CREATE TABLE 损失因子k2 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    "前置条件" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 损失因子k2 VALUES
(1,'损失指数R','Number','NULL',null,null,null,1),
(2,'损失指数r1','Number','NULL',null,null,null,1),
(3,'η值','QLabel','NULL',null,null,'{"存在性":{"48":"η值"},"判断性":{"1":"5=6"}}',1),
(4,'五十年一遇sp','QLabel','mm/h',null,null,'{"存在性":{"38":"五十年一遇sp"},"判断性":{"1":"5=6"}}',0),
(5,'五十年一遇损失因子k2','QLabel','NULL',null,'损失指数R*(η值*五十年一遇sp)**(损失指数r1-1)',null,0),
(6,'百年一遇sp','QLabel','mm/h',null,null,'{"存在性":{"38":"百年一遇sp"},"判断性":{"1":"5=6"}}',0),
(7,'百年一遇损失因子k2','QLabel','NULL',null,'损失指数R*(η值*百年一遇sp)**(损失指数r1-1)',null,0)
;

DROP TABLE IF EXISTS "随暴雨衰减指数n变化指数n";
CREATE TABLE "随暴雨衰减指数n变化指数n" (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    "前置条件" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO "随暴雨衰减指数n变化指数n" VALUES
(1,'损失指数r1','QLabel','NULL',null,null,'{"存在性":{"49":"损失指数r1"},"判断性":{"1":"5=6"}}',1),
(2,'五十年一遇衰减指数','QLabel','mm/h',null,null,'{"存在性":{"38":"五十年一遇衰减指数"},"判断性":{"1":"5=6"}}',0),
(3,'五十年一遇损失因子k2','QLabel','NULL',null,null,'{"存在性":{"49":"五十年一遇损失因子k2"},"判断性":{"1":"5=6"}}',0),
(4,'五十年一遇随暴雨衰减指数n变化指数','QLabel','NULL',null,'(1-损失指数r1*五十年一遇损失因子k2)/(1-五十年一遇损失因子k2)*五十年一遇衰减指数',null,0),
(5,'百年一遇衰减指数','QLabel','mm/h',null,null,'{"存在性":{"38":"百年一遇衰减指数"},"判断性":{"1":"5=6"}}',0),
(6,'百年一遇损失因子k2','QLabel','NULL',null,null,'{"存在性":{"49":"百年一遇损失因子k2"},"判断性":{"1":"5=6"}}',0),
(7,'百年一遇随暴雨衰减指数n变化指数','QLabel','NULL',null,'(1-损失指数r1*百年一遇损失因子k2)/(1-百年一遇损失因子k2)*百年一遇衰减指数',null,0)
;
DROP TABLE IF EXISTS 造峰因子k3;
CREATE TABLE 造峰因子k3 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    "前置条件" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 造峰因子k3 VALUES
(1,'五十年一遇随暴雨衰减指数n变化指数','QLabel','NULL',null,null,'{"存在性":{"50":"五十年一遇随暴雨衰减指数n变化指数"},"判断性":{"1":"5=6"}}',0),
(2,'五十年一遇造峰因子k3','QLabel','NULL',null,'(1-五十年一遇随暴雨衰减指数n变化指数)**(1-五十年一遇随暴雨衰减指数n变化指数)/((1-0.5*五十年一遇随暴雨衰减指数n变化指数)**(2-五十年一遇随暴雨衰减指数n变化指数))',null,0),
(3,'百年一遇随暴雨衰减指数n变化指数','QLabel','NULL',null,null,'{"存在性":{"50":"百年一遇随暴雨衰减指数n变化指数"},"判断性":{"1":"5=6"}}',0),
(4,'百年一遇造峰因子k3','QLabel','NULL',null,'(1-百年一遇随暴雨衰减指数n变化指数)**(1-百年一遇随暴雨衰减指数n变化指数)/((1-0.5*百年一遇随暴雨衰减指数n变化指数)**(2-百年一遇随暴雨衰减指数n变化指数))',null,0)
;

DROP TABLE IF EXISTS 主河槽流速系数A1;
CREATE TABLE 主河槽流速系数A1 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    "前置条件" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 主河槽流速系数A1 VALUES
(1,'主河床糙率系数m1','Number','NULL',null,null,null,1),
(3,'断面扩散系数α0','Number','NULL',null,null,null,1),
(4,'主河槽流速系数A1','QLabel','NULL',null,'0.0368*(主河床糙率系数m1**0.705)*(断面扩散系数α0**0.175/((断面扩散系数α0+0.5)**0.47))',null,0)
;

DROP TABLE IF EXISTS 河槽汇流因子K1;
CREATE TABLE 河槽汇流因子K1 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    "前置条件" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 河槽汇流因子K1 VALUES
(1,'主河床槽长度','Number','NULL','km',null,null,0),
(2,'主河槽平均坡率I1','Number','NULL',null,null,null,0),
(3,'主河槽流速系数A1','QLabel','NULL',null,null,'{"存在性":{"52":"主河槽流速系数A1"},"判断性":{"1":"5=6"}}',0),
(4,'河槽汇流因子K1','QLabel','NULL',null,'0.278*主河床槽长度/主河槽流速系数A1/(主河槽平均坡率I1**0.35)',null,0)
;
DROP TABLE IF EXISTS 流域坡面平均长度L2;
CREATE TABLE 流域坡面平均长度L2 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    "前置条件" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 流域坡面平均长度L2 VALUES
(1,'汇水面积','QLabel','km2',null,null,'{"存在性":{"44":"汇水面积"},"判断性":{"1":"5=6"}}',0),
(2,'支沟总长','Number','NULL',null,null,null,0),
(3,'主河床槽长度','QLabel','NULL',null,null,'{"存在性":{"53":"主河床槽长度"},"判断性":{"1":"5=6"}}',0),
(4,'流域坡面平均长度L2','QLabel','NULL',null,'(汇水面积/1.8)/(支沟总长+主河床槽长度)',null,0)
;

DROP TABLE IF EXISTS 山坡汇流因子K2;
CREATE TABLE 山坡汇流因子K2 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    "前置条件" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 山坡汇流因子K2 VALUES
(1,'坡面流速系数A2','Number','NULL',null,null,null,1),
(2,'流域坡面平均坡度I2','Number','NULL',null,null,null,0),
(3,'汇水面积','QLabel','km2',null,null,'{"存在性":{"44":"汇水面积"},"判断性":{"1":"5=6"}}',0),
(4,'流域坡面平均长度','QLabel','km2',null,null,'{"存在性":{"54":"流域坡面平均长度L2"},"判断性":{"1":"5=6"}}',0),
(5,'山坡汇流因子K2','QLabel','NULL',null,'0.278*(流域坡面平均长度**0.5)*(汇水面积**0.5)/坡面流速系数A2/(流域坡面平均坡度I2**0.333)',null,0)
;

DROP TABLE IF EXISTS 河槽和山坡综合汇流因子x;
CREATE TABLE 河槽和山坡综合汇流因子x (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    "前置条件" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 河槽和山坡综合汇流因子x VALUES
(1,'河槽汇流因子K1','QLabel','km2',null,null,'{"存在性":{"53":"河槽汇流因子K1"},"判断性":{"1":"5=6"}}',0),
(2,'山坡汇流因子K2','QLabel','km2',null,null,'{"存在性":{"55":"山坡汇流因子K2"},"判断性":{"1":"5=6"}}',0),
(3,'河槽和山坡综合汇流因子x','QLabel','NULL',null,'河槽汇流因子K1+山坡汇流因子K2',null,0)
;
DROP TABLE IF EXISTS 反映流域汇流特征的指数y;
CREATE TABLE 反映流域汇流特征的指数y(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    "前置条件" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 反映流域汇流特征的指数y VALUES
(1,'河槽汇流因子K1','QLabel','km2',null,null,'{"存在性":{"53":"河槽汇流因子K1"},"判断性":{"1":"5=6"}}',0),
(2,'山坡汇流因子K2','QLabel','km2',null,null,'{"存在性":{"55":"山坡汇流因子K2"},"判断性":{"1":"5=6"}}',0),
(3,'反映流域汇流特征的指数y','QLabel','NULL',null,'0.5-0.5*log10((3.12*河槽汇流因子K1/山坡汇流因子K2+1)/(1.246*河槽汇流因子K1/山坡汇流因子K2+1))',null,0)
;
DROP TABLE IF EXISTS 设计坡面径流量Qp;
CREATE TABLE 设计坡面径流量Qp (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    "前置条件" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 设计坡面径流量Qp VALUES
(1,'河槽和山坡综合汇流因子x','QLabel','NULL',null,null,'{"存在性":{"56":"河槽和山坡综合汇流因子x"},"判断性":{"1":"5=6"}}',0),
(2,'反映流域汇流特征的指数y','QLabel','NULL',null,null,'{"存在性":{"57":"反映流域汇流特征的指数y"},"判断性":{"1":"5=6"}}',0),
(3,'五十年一遇产流因子K1','QLabel','NULL',null,null,'{"存在性":{"48":"五十年一遇产流因子K1"},"判断性":{"1":"5=6"}}',0),
(4,'五十年一遇损失因子k2','QLabel','NULL',null,null,'{"存在性":{"49":"五十年一遇损失因子k2"},"判断性":{"1":"5=6"}}',0),
(5,'五十年一遇随暴雨衰减指数n变化指数','QLabel','NULL',null,null,'{"存在性":{"50":"五十年一遇随暴雨衰减指数n变化指数"},"判断性":{"1":"5=6"}}',0),
(6,'五十年一遇设计坡面径流量','QLabel','m3/s',null,'((五十年一遇产流因子K1*(1-五十年一遇损失因子k2)*五十年一遇随暴雨衰减指数n变化指数)/(河槽和山坡综合汇流因子x**五十年一遇随暴雨衰减指数n变化指数))*(1/(1-五十年一遇随暴雨衰减指数n变化指数*反映流域汇流特征的指数y))',null,0),
(7,'百年一遇产流因子K1','QLabel','NULL',null,null,'{"存在性":{"48":"百年一遇产流因子K1"},"判断性":{"1":"5=6"}}',0),
(8,'百年一遇损失因子k2','QLabel','NULL',null,null,'{"存在性":{"49":"百年一遇损失因子k2"},"判断性":{"1":"5=6"}}',0),
(9,'百年一遇随暴雨衰减指数n变化指数','QLabel','NULL',null,null,'{"存在性":{"50":"百年一遇随暴雨衰减指数n变化指数"},"判断性":{"1":"5=6"}}',0),
(10,'百年一遇设计坡面径流量','QLabel','m3/s',null,'((百年一遇产流因子K1*(1-百年一遇损失因子k2)*百年一遇随暴雨衰减指数n变化指数)/(河槽和山坡综合汇流因子x**百年一遇随暴雨衰减指数n变化指数))*(1/(1-百年一遇随暴雨衰减指数n变化指数*反映流域汇流特征的指数y))',null,0),
(11,'五十年一遇汇流时间H','QLabel','NULL',null,'(1-五十年一遇随暴雨衰减指数n变化指数)/(1-0.5*五十年一遇随暴雨衰减指数n变化指数)*河槽和山坡综合汇流因子x*(五十年一遇设计坡面径流量Qp**(-反映流域汇流特征的指数y))',null,0),
(12,'五十年一遇汇流时间S','QLabel','NULL',null,'五十年一遇汇流时间H*3600',null,0),
(13,'百年一遇汇流时间H','QLabel','NULL',null,'(1-百年一遇随暴雨衰减指数n变化指数)/(1-0.5*百年一遇随暴雨衰减指数n变化指数)*河槽和山坡综合汇流因子x*(百年一遇设计坡面径流量Qp**(-反映流域汇流特征的指数y))',null,0),
(14,'百年一遇汇流时间S','QLabel','NULL',null,'百年一遇汇流时间H*3600',null,0)
;

--######################################
-- TODO 计算洪峰流量Qp 相关数据表
--######################################
DROP TABLE IF EXISTS 按照铁路工务手册计算设计径流量;
CREATE TABLE 按照铁路工务手册计算设计径流量 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    "前置条件" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 按照铁路工务手册计算设计径流量 VALUES
(1,'汇水面积','QLabel','km2',null,null,'{"存在性":{"44":"汇水面积"},"判断性":{"1":"5=6"}}',0),
(2,'流域汇流时间','QLabel','NULL',null,'0.64*(汇水面积**0.34)',null,0),
(3,'洪峰径流系数','Number','NULL',null,null,null,0),
(4,'五十年一遇衰减指数','QLabel','mm/h',null,null,'{"存在性":{"38":"五十年一遇衰减指数"},"判断性":{"1":"5=6"}}',0),
(5,'五十年一遇sp','QLabel','mm/h',null,null,'{"存在性":{"38":"五十年一遇sp"},"判断性":{"1":"5=6"}}',0),
(6,'五十年一遇洪峰流量','QLabel','m3/s',null,'0.278*洪峰径流系数*五十年一遇sp*汇水面积/(流域汇流时间**五十年一遇衰减指数)',null,0),
(7,'百年一遇衰减指数','QLabel','mm/h',null,null,'{"存在性":{"38":"百年一遇衰减指数"},"判断性":{"1":"5=6"}}',0),
(8,'百年一遇sp','QLabel','mm/h',null,null,'{"存在性":{"38":"百年一遇sp"},"判断性":{"1":"5=6"}}',0),
(9,'百年一遇洪峰流量','QLabel','m3/s',null,'0.278*洪峰径流系数*百年一遇sp*汇水面积/(流域汇流时间**百年一遇衰减指数)',null,0)
;

DROP TABLE IF EXISTS 确定清水流量Qp;
CREATE TABLE 确定清水流量Qp (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    "前置条件" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 确定清水流量Qp VALUES
(1,'铁路工程水文勘测设计-五十年一遇洪峰流量','QLabel','mm/h',null,null,'{"存在性":{"61":"五十年一遇洪峰流量"},"判断性":{"1":"5=6"}}',0),
(2,'铁路路基设计设计-五十年一遇洪峰流量','QLabel','mm/h',null,null,'{"存在性":{"44":"五十年一遇洪峰流量"},"判断性":{"1":"5=6"}}',0),
(3,'铁路务工手册设计-五十年一遇洪峰流量','QLabel','mm/h',null,null,'{"存在性":{"58":"五十年一遇设计坡面径流量"},"判断性":{"1":"5=6"}}',0),
(4,'铁路工程水文勘测设计-百年一遇洪峰流量','QLabel','mm/h',null,null,'{"存在性":{"61":"百年一遇洪峰流量"},"判断性":{"1":"5=6"}}',0),
(5,'铁路路基设计设计-百年一遇洪峰流量','QLabel','mm/h',null,null,'{"存在性":{"44":"百年一遇洪峰流量"},"判断性":{"1":"5=6"}}',0),
(6,'铁路务工手册设计-百年一遇洪峰流量','QLabel','mm/h',null,null,'{"存在性":{"58":"百年一遇设计坡面径流量"},"判断性":{"1":"5=6"}}',0),
(7,'使用沟内汇流进行计算','ToggleButton','NULL','{"存在性-降雨历时":{"0":"45-坡面汇流历时T1","1":"100-测试"}}',null,null,0),
(8,'铁路路基设计设计-降雨历时','QLabel','min',null,null,'{"存在性":{"45":"坡面汇流历时T1"},"判断性":{"1":"5=6"}}',0),
(9,'铁路务工手册设计-降雨历时','QLabel','min',null,null,'{"存在性":{"61":"流域汇流时间"},"判断性":{"1":"5=6"}}',0),
(10,'五十年一遇洪峰流量','QLabel','m3/s',null,'max(铁路工程水文勘测设计-五十年一遇洪峰流量,铁路路基设计设计-五十年一遇洪峰流量,铁路务工手册设计-五十年一遇洪峰流量)',null,0),
(11,'百年一遇洪峰流量','QLabel','m3/s',null,'max(铁路工程水文勘测设计-百年一遇洪峰流量,铁路路基设计设计-百年一遇洪峰流量,铁路务工手册设计-百年一遇洪峰流量)',null,0),
(12,'汇水时间T','QLabel','m3/s',null,'max(铁路路基设计设计-降雨历时*60,铁路务工手册设计-降雨历时*60)',null,0)
;
-- ###################################################
-- 计算洪峰流量Qp 数据表结束
-- ###################################################

--######################################
-- TODO 坡面泥石流计算 相关数据表
--######################################
DROP TABLE IF EXISTS 计算泥石流流量Qc;
CREATE TABLE 计算泥石流流量Qc (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    "前置条件" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 计算泥石流流量Qc VALUES
(1,'五十年一遇洪峰流量','QLabel','NULL',null,null,'{"存在性":{"64":"五十年一遇洪峰流量"},"判断性":{"1":"5=6"}}',0),
(2,'百年一遇洪峰流量','QLabel','NULL',null,null,'{"存在性":{"64":"百年一遇洪峰流量"},"判断性":{"1":"5=6"}}',0),
(3,'泥石流容重','Number','t/m3',null,null,null,0),
(4,'清水容重','Number','t/m3',null,null,null,0),
(5,'泥石流中固体物质容重','Number','t/m3',null,null,null,0),
(6,'泥石流泥沙修正系数','QLabel','t/m3',null,'(泥石流容重-清水容重)/(泥石流中固体物质容重-泥石流容重)',null,0),
(7,'堵塞系数','Number','NULL',null,null,null,1),
(8,'五十年一遇泥石流洪峰流量','QLabel','m3/s',null,'五十年一遇洪峰流量*堵塞系数*(1+泥石流泥沙修正系数)',null,0),
(9,'百年一遇泥石流洪峰流量','QLabel','m3/s',null,'百年一遇洪峰流量*堵塞系数*(1+泥石流泥沙修正系数)',null,0)
;

DROP TABLE IF EXISTS 计算稀性泥石流流速vc;
CREATE TABLE 计算稀性泥石流流速vc (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    "前置条件" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 计算稀性泥石流流速vc VALUES
(1,'泥石流容重','QLabel','NULL',null,null,'{"存在性":{"66":"泥石流容重"},"判断性":{"1":"5=6"}}',0),
(2,'清水容重','QLabel','NULL',null,null,'{"存在性":{"66":"清水容重"},"判断性":{"1":"5=6"}}',0),
(3,'泥石流中固体物质容重','QLabel','NULL',null,null,'{"存在性":{"66":"泥石流中固体物质容重"},"判断性":{"1":"5=6"}}',0),
(4,'泥石流泥沙修正系数','QLabel','NULL',null,null,'{"存在性":{"66":"泥石流泥沙修正系数"},"判断性":{"1":"5=6"}}',0),
(5,'沟道糙率','Number','NULL',null,null,null,0),
(6,'水力半径','Number','m',null,null,null,0),
(7,'水力坡率','Number','NULL',null,null,null,1),
(8,'流速','QLabel','m/s',null,'清水容重/((泥石流中固体物质容重*泥石流泥沙修正系数+清水容重)**0.5)*沟道糙率*(水力半径**(2/3))*(水力坡率**0.5)',null,0)
;

DROP TABLE IF EXISTS 计算黏性泥石流流速;
CREATE TABLE 计算黏性泥石流流速 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 计算黏性泥石流流速 VALUES
(1,'黏性泥石流断面平均泥深Hc（m）','Number','NULL',null,0),
(2,'黏性泥石流糙率系数系数Mc','Number','NULL',null,1),
(3,'泥石流水力坡度Ic','QLabel','NULL',null,0)
;
DROP TABLE IF EXISTS 一次泥石流过流总量Q;
CREATE TABLE 一次泥石流过流总量Q (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    "前置条件" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 一次泥石流过流总量Q VALUES
(1,'泥石流排泄系数K','Number','NULL',null,null,null,1),
(2,'汇流时间','QLabel','s',null,null,'{"存在性":{"64":"汇水时间T"},"判断性":{"1":"5=6"}}',0),
(3,'五十年一遇泥石流洪峰流量','QLabel','s',null,null,'{"存在性":{"66":"五十年一遇泥石流洪峰流量"},"判断性":{"1":"5=6"}}',0),
(4,'百年一遇泥石流洪峰流量','QLabel','s',null,null,'{"存在性":{"66":"百年一遇泥石流洪峰流量"},"判断性":{"1":"5=6"}}',0),
(5,'50年一次泥石流过流总量Q','QLabel','m/s3',null,'泥石流排泄系数K*汇流时间*五十年一遇泥石流洪峰流量',null,0),
(6,'100年一次泥石流过流总量Q','QLabel','m/s3',null,'泥石流排泄系数K*汇流时间*百年一遇泥石流洪峰流量',null,0)
;

DROP TABLE IF EXISTS 一次泥石流冲出固体物QH;
CREATE TABLE 一次泥石流冲出固体物QH (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    "前置条件" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 一次泥石流冲出固体物QH VALUES
(1,'泥石流容重','QLabel','NULL',null,null,'{"存在性":{"66":"泥石流容重"},"判断性":{"1":"5=6"}}',0),
(2,'清水容重','QLabel','NULL',null,null,'{"存在性":{"66":"清水容重"},"判断性":{"1":"5=6"}}',0),
(3,'泥石流中固体物质容重','QLabel','NULL',null,null,'{"存在性":{"66":"泥石流中固体物质容重"},"判断性":{"1":"5=6"}}',0),
(4,'50年一次泥石流过流总量Q','QLabel','NULL',null,null,'{"存在性":{"69":"50年一次泥石流过流总量Q"},"判断性":{"1":"5=6"}}',0),
(5,'50年一遇一次泥石流冲出固体物QH','QLabel','m3',null,'50年一次泥石流过流总量Q*(泥石流容重-清水容重)/(泥石流中固体物质容重-清水容重)',null,0),
(6,'100年一次泥石流过流总量Q','QLabel','NULL',null,null,'{"存在性":{"69":"100年一次泥石流过流总量Q"},"判断性":{"1":"5=6"}}',0),
(7,'100年一遇一次泥石流冲出固体物QH','QLabel','m3',null,'100年一次泥石流过流总量Q*(泥石流容重-清水容重)/(泥石流中固体物质容重-清水容重)',null,0)
;

DROP TABLE IF EXISTS 泥石流中石块运动速度vs;
CREATE TABLE 泥石流中石块运动速度vs (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    "前置条件" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 泥石流中石块运动速度vs VALUES
(1,'全面考虑的摩擦系数','Number','NULL',null,null,null,1),
(2,'最大石块的粒径','Number','m',null,null,null,0),
(3,'泥石流中石块运动速度','QLabel','m/s',null,'全面考虑的摩擦系数*(最大石块的粒径**0.5)',null,0)
;


DROP TABLE IF EXISTS 泥石流最大冲起高度△H和受沟床阻力影响爬高△h;
CREATE TABLE 泥石流最大冲起高度△H和受沟床阻力影响爬高△h (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    "计算方法" TEXT,
    "前置条件" TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 泥石流最大冲起高度△H和受沟床阻力影响爬高△h VALUES
(1,'流速','QLabel','NULL',null,null,'{"存在性":{"67":"流速"},"判断性":{"1":"5=6"}}',0),
(2,'建筑物受力面与泥石流冲压力方向夹角','Number','°',null,null,null,0),
(3,'受沟床阻力影响爬高','QLabel','NULL',null,'(1.6*(流速**2)/2)/10*sin(建筑物受力面与泥石流冲压力方向夹角)',null,0)
;
-- ###################################################
-- 坡面泥石流计算 数据表结束
-- ###################################################
-- TODO 铁路水文设计规范 帮助表
DROP TABLE IF EXISTS 主河床糙率系数m1;
CREATE TABLE 主河床糙率系数m1 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 主河床糙率系数m1 VALUES
(1,'m1\\a0','表头字段','NULL','{"1":"1","2":"2","3":"3","4":"4","5":"5","6":"7","7":"10","8":"15","9":"20","10":"30","11":"50","12":"主河槽形态特征"}',0),
(2,'5','数据字段','NULL','{"1":"0.095","2":"0.084","3":"0.077","4":"0.071","5":"0.068","6":"0.062","7":"0.057","8":"0.050","9":"0.047","10":"0.041","11":"0.036","12":""}',0),
(3,'7','数据字段','NULL','{"1":"1.40","2":"1.25","3":"1.00","4":"0.77","5":"0.64","6":"0.50","7":"0.40","8":"0.34","9":"0.30","10":"0.22","11":"0.18","12":""}',0),
(4,'10','数据字段','NULL','{"1":"1.40","2":"1.25","3":"1.00","4":"0.80","5":"0.68","6":"0.55","7":"0.45","8":"0.39","9":"0.35","10":"0.26","11":"0.21","12":""}',0),
(5,'15','数据字段','NULL','{"1":"1.40","2":"1.25","3":"1.00","4":"0.82","5":"0.72","6":"0.59","7":"0.50","8":"0.44","9":"0.40","10":"0.30","11":"0.25","12":""}',0),
(6,'20','数据字段','NULL','{"1":"1.40","2":"1.25","3":"1.00","4":"0.84","5":"0.76","6":"0.63","7":"0.55","8":"0.50","9":"0.45","10":"0.34","11":"0.29","12":""}',0),
(7,'25','数据字段','NULL','{"1":"1.40","2":"1.25","3":"1.00","4":"0.87","5":"0.80","6":"0.68","7":"0.60","8":"0.55","9":"0.50","10":"0.39","11":"0.33","12":""}',0),
(8,'30','数据字段','NULL','{"1":"1.40","2":"1.25","3":"1.00","4":"0.87","5":"0.80","6":"0.68","7":"0.60","8":"0.55","9":"0.50","10":"0.39","11":"0.33","12":""}',0),
(9,'注：','注解字段','NULL','{"1":"1.40"}',0)
;


DROP TABLE IF EXISTS η值;
CREATE TABLE η值 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO η值 VALUES
(1,'F(km²)','表头字段','NULL','{"1":"η"}',0),
(2,'<10','数据字段','NULL','{"1":"1.00"}',0),
(3,'10','数据字段','NULL','{"1":"0.94"}',0),
(4,'12.5','数据字段','NULL','{"1":"0.93"}',0),
(5,'15','数据字段','NULL','{"1":"0.92"}',0),
(6,'20','数据字段','NULL','{"1":"0.91"}',0),
(7,'25','数据字段','NULL','{"1":"0.90"}',0),
(8,'30','数据字段','NULL','{"1":"0.89"}',0),
(9,'35','数据字段','NULL','{"1":"0.88"}',0),
(10,'40','数据字段','NULL','{"1":"0.87"}',0),
(11,'50','数据字段','NULL','{"1":"0.86"}',0),
(12,'60','数据字段','NULL','{"1":"0.84"}',0),
(13,'70','数据字段','NULL','{"1":"0.83"}',0),
(14,'80','数据字段','NULL','{"1":"0.82"}',0),
(15,'90','数据字段','NULL','{"1":"0.81"}',0),
(16,'100','数据字段','NULL','{"1":"0.80"}',0)
;
DROP TABLE IF EXISTS 损失指数r1;
CREATE TABLE 损失指数r1 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 损失指数r1 VALUES
(1,'损失等级','表头字段','NULL','{"1":"特征","2":"R","3":"r1"}',0),
(2,'II','数据字段','NULL','{"1":"黏土；地下水位较高（0.3m~0.5m）盐碱土地面；土层较薄的岩石地区；植被差、风化轻微的岩石地区","2":"0.93","3":"0.63"}',0),
(3,'III','数据字段','NULL','{"1":"植被差的砂黏土；戈壁滩；土层较厚的岩石山区；植被中等、风化中等的岩石地区；北方地区坡度不大的山间草地；黄土（Q₂）区","2":"1.02","3":"0.69"}',0),
(4,'IV','数据字段','NULL','{"1":"植被差的黏砂土；风化严重、土层厚的土石山区；杂草灌木较密的山丘区或草地；人工幼林或土层较薄中等密度的林区；黄土（Q₃、Q₄）区","2":"1.10","3":"0.76"}',0),
(5,'V','数据字段','NULL','{"1":"植被差的一般砂土地面；土层较厚森林较密的地区；有大面积水土保持措施、治理较好的土层山区","2":"1.18","3":"0.83"}',0),
(6,'VI','数据字段','NULL','{"1":"无植被的松散的砂土地面；茂密的并有枯枝落叶层的原始森林区","2":"1.25","3":"0.90"}',0)
;
DROP TABLE IF EXISTS 损失指数R;
CREATE TABLE 损失指数R (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 损失指数R VALUES
(1,'损失等级','表头字段','NULL','{"1":"特征","2":"R","3":"r1"}',0),
(2,'II','数据字段','NULL','{"1":"黏土；地下水位较高（0.3m~0.5m）盐碱土地面；土层较薄的岩石地区；植被差、风化轻微的岩石地区","2":"0.93","3":"0.63"}',0),
(3,'III','数据字段','NULL','{"1":"植被差的砂黏土；戈壁滩；土层较厚的岩石山区；植被中等、风化中等的岩石地区；北方地区坡度不大的山间草地；黄土（Q₂）区","2":"1.02","3":"0.69"}',0),
(4,'IV','数据字段','NULL','{"1":"植被差的黏砂土；风化严重、土层厚的土石山区；杂草灌木较密的山丘区或草地；人工幼林或土层较薄中等密度的林区；黄土（Q₃、Q₄）区","2":"1.10","3":"0.76"}',0),
(5,'V','数据字段','NULL','{"1":"植被差的一般砂土地面；土层较厚森林较密的地区；有大面积水土保持措施、治理较好的土层山区","2":"1.18","3":"0.83"}',0),
(6,'VI','数据字段','NULL','{"1":"无植被的松散的砂土地面；茂密的并有枯枝落叶层的原始森林区","2":"1.25","3":"0.90"}',0)
;

DROP TABLE IF EXISTS 降雨历时转换系数Ct;
CREATE TABLE 降雨历时转换系数Ct (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 降雨历时转换系数Ct VALUES
(1,'C₆₀','表头字段','NULL','{"1":"3","2":"5","3":"10","4":"15","5":"20","6":"30","7":"40","8":"50","9":"60","10":"90","11":"120"}',0),
(2,'0.25','数据字段','NULL','{"1":"1.40","2":"1.25","3":"1.00","4":"0.75","5":"0.60","6":"0.46","7":"0.35","8":"0.30","9":"0.25","10":"0.18","11":"0.15"}',0),
(3,'0.30','数据字段','NULL','{"1":"1.40","2":"1.25","3":"1.00","4":"0.77","5":"0.64","6":"0.50","7":"0.40","8":"0.34","9":"0.30","10":"0.22","11":"0.18"}',0),
(4,'0.25','数据字段','NULL','{"1":"1.40","2":"1.25","3":"1.00","4":"0.80","5":"0.68","6":"0.55","7":"0.45","8":"0.39","9":"0.35","10":"0.26","11":"0.21"}',0),
(5,'0.40','数据字段','NULL','{"1":"1.40","2":"1.25","3":"1.00","4":"0.82","5":"0.72","6":"0.59","7":"0.50","8":"0.44","9":"0.40","10":"0.30","11":"0.25"}',0),
(6,'0.45','数据字段','NULL','{"1":"1.40","2":"1.25","3":"1.00","4":"0.84","5":"0.76","6":"0.63","7":"0.55","8":"0.50","9":"0.45","10":"0.34","11":"0.29"}',0),
(7,'0.50','数据字段','NULL','{"1":"1.40","2":"1.25","3":"1.00","4":"0.87","5":"0.80","6":"0.68","7":"0.60","8":"0.55","9":"0.50","10":"0.39","11":"0.33"}',0)
;

DROP TABLE IF EXISTS 重现期转换系数Cp;
CREATE TABLE 重现期转换系数Cp (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 重现期转换系数Cp VALUES
(1,'地区','表头字段','NULL','{"1":"3","2":"5","3":"10","4":"15","5":"25","6":"50","7":"100"}',0),
(2,'安徽、山东、浙江、江苏、福建、江西、上海、台湾','数据字段','NULL','{"1":"0.90","2":"1.00","3":"1.14","4":"1.23","5":"1.33","6":"1.44","7":"1.56"}',0),
(3,'广西、广东、海南、澳门、香港','数据字段','NULL','{"1":"0.90","2":"1.00","3":"1.14","4":"1.23","5":"1.33","6":"1.44","7":"1.56"}',0),
(4,'湖南、湖北、河南','数据字段','NULL','{"1":"0.87","2":"1.00","3":"1.20","4":"1.33","5":"1.47","6":"1.63","7":"1.80"}',0),
(5,'四川、重庆、贵州、云南','数据字段','NULL','{"1":"0.87","2":"1.00","3":"1.20","4":"1.33","5":"1.47","6":"1.63","7":"1.80"}',0),
(6,'天津、河北、北京、内蒙古、山西','数据字段','NULL','{"1":"0.85","2":"1.00","3":"1.25","4":"1.41","5":"1.60","6":"1.82","7":"2.06"}',0),
(7,'黑龙江、吉林、辽宁','数据字段','NULL','{"1":"0.85","2":"1.00","3":"1.25","4":"1.41","5":"1.60","6":"1.82","7":"2.06"}',0),
(8,'陕西、甘肃、宁夏、青海、新疆、西藏（干旱）','数据字段','NULL','{"1":"0.82","2":"1.00","3":"1.31","4":"1.51","5":"1.76","6":"2.04","7":"2.34"}',0),
(9,'陕西、甘肃、宁夏、青海、新疆、西藏（潮湿）','数据字段','NULL','{"1":"0.76","2":"1.00","3":"1.59","4":"2.03","5":"2.57","6":"3.20","7":"3.95"}',0)
;
DROP TABLE IF EXISTS 地表粗度系数m1;
CREATE TABLE 地表粗度系数m1 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 地表粗度系数m1 VALUES
(1,'地表状况','表头字段','NULL','{"1":"粗度系数（m₁）"}',0),
(2,'沥青路面、水泥混凝土路面','数据字段','NULL','{"1":"0.013"}',0),
(3,'光滑的不透水地面','数据字段','NULL','{"1":"0.020"}',0),
(4,'光滑的压实土地面','数据字段','NULL','{"1":"0.100"}',0),
(5,'稀疏草地、耕地','数据字段','NULL','{"1":"0.200"}',0),
(6,'牧草地、草地','数据字段','NULL','{"1":"0.400"}',0),
(7,'落叶树林','数据字段','NULL','{"1":"0.600"}',0),
(8,'针叶树林','数据字段','NULL','{"1":"0.800"}',0)
;
DROP TABLE IF EXISTS 地表径流系数;
CREATE TABLE 地表径流系数 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 地表径流系数 VALUES
(1,'地表种类','表头字段','NULL','{"1":"粗度系数（ψ）"}',0),
(2,'粗粒土坡面','数据字段','NULL','{"1":"0.10~0.30"}',0),
(3,'细粒土坡面','数据字段','NULL','{"1":"0.40~0.65"}',0),
(4,'硬质岩石坡面','数据字段','NULL','{"1":"0.70~0.85"}',0),
(5,'软质岩石坡面','数据字段','NULL','{"1":"0.50~0.75"}',0),
(6,'陡峻的山地','数据字段','NULL','{"1":"0.75~0.90"}',0),
(7,'起伏的山地','数据字段','NULL','{"1":"0.60~0.80"}',0),
(8,'起伏的草地','数据字段','NULL','{"1":"0.40~0.65"}',0),
(9,'平坦的耕地','数据字段','NULL','{"1":"0.45~0.60"}',0),
(10,'落叶林地','数据字段','NULL','{"1":"0.35~0.60"}',0),
(11,'针叶林地','数据字段','NULL','{"1":"0.25~0.50"}',0),
(12,'水田、水面','数据字段','NULL','{"1":"0.70~0.80"}',0)
;

DROP TABLE IF EXISTS 主河床糙率系数m1;
CREATE TABLE 主河床糙率系数m1 (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    unit TEXT,
    value TEXT,
    need_help INTEGER NOT NULL DEFAULT 0
);
INSERT INTO 主河床糙率系数m1 VALUES
(1,'m1','表头字段','NULL','{"1":"1","2":"2","3":"3","4":"4","5":"5","6":"7","7":"10","8":"15","9":"20","10":"30","11":"50","12":"主河槽形态特征"}',0),
(2,'5','数据字段','NULL','{"1":"0.095","2":"0.084","3":"0.077","4":"0.071","5":"0.068","6":"0.062","7":"0.057","8":"0.050","9":"0.047","10":"0.041","11":"0.036","12":"从林郁闭度占75%以上的海购"}',0),
(3,'细粒土坡面','数据字段','NULL','{"1":"0.40~0.65"}',0),
(4,'硬质岩石坡面','数据字段','NULL','{"1":"0.70~0.85"}',0),
(5,'软质岩石坡面','数据字段','NULL','{"1":"0.50~0.75"}',0),
(6,'陡峻的山地','数据字段','NULL','{"1":"0.75~0.90"}',0),
(7,'起伏的山地','数据字段','NULL','{"1":"0.60~0.80"}',0),
(8,'起伏的草地','数据字段','NULL','{"1":"0.40~0.65"}',0),
(9,'平坦的耕地','数据字段','NULL','{"1":"0.45~0.60"}',0),
(10,'落叶林地','数据字段','NULL','{"1":"0.35~0.60"}',0),
(11,'针叶林地','数据字段','NULL','{"1":"0.25~0.50"}',0),
(12,'水田、水面','数据字段','NULL','{"1":"0.70~0.80"}',0)
;