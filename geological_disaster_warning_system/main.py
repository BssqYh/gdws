import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from pages.home_page import HomePage
from pages.load_page import LoadPage
from pages.survey_data_page import SurveyDataPage
from pages.survey_data_work_point_base_info_page import SurveyDataWorkPointBaseInfoPage
from pages.survey_data_work_point_collapse_page import SurveyDataWorkPointCollapsePage
from pages.survey_data_work_point_di_zhi_tiao_jian_page import SurveyDataWorkPointDiZhiTiaoJianPage
from pages.survey_data_work_point_grand_fissure_page import SurveyDataWorkPointGrandFissurePage
from pages.survey_data_work_point_debrisflow_page import  SurveyDataWorkPointDebrisFlowPage
from pages.survey_data_work_point_mudslide_page import SurveyDataWorkPointMudslidePage
from pages.survey_data_work_point_qi_xiang_tiao_jian_page import SurveyDataWorkPointQiXiangTiaoJianPage
import compiled_resources
from pages.testpage2 import TestPage2

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 创建主窗口
    main_window = MainWindow()
    load_page = LoadPage()
    load_page.set_main_window(main_window)
    main_window.set_load_page(load_page)


    # 获取页面管理器
    page_manager = main_window.get_page_manager()
    """所有的页面都要在这里注册,为什么不放在各自需要的页面里面注册呢？
    因为如果自己注册，那么可能造成文件互相依赖"""
    page_manager.register_page("homepage",HomePage)
    # page_manager.register_page("testpage2",TestPage2)
    page_manager.register_page("survey_data_page", SurveyDataPage)
    page_manager.register_page("survey_data_work_point_mudslide_page", SurveyDataWorkPointMudslidePage)
    page_manager.register_page("survey_data_work_point_base_info_page", SurveyDataWorkPointBaseInfoPage)
    page_manager.register_page("survey_data_work_point_di_zhi_tiao_jian_page",SurveyDataWorkPointDiZhiTiaoJianPage)
    page_manager.register_page("survey_data_work_point_qi_xiang_tiao_jian_page",SurveyDataWorkPointQiXiangTiaoJianPage)
    page_manager.register_page("survey_data_work_point_collapse_page", SurveyDataWorkPointCollapsePage)
    page_manager.register_page("survey_data_work_point_debris_flow_page", SurveyDataWorkPointDebrisFlowPage)
    page_manager.register_page("survey_data_work_point_grand_fissure_page", SurveyDataWorkPointGrandFissurePage)


    # # 默认打开测试页面1
    # page_manager.switch_page("testpage1")

    # 显示窗口
    load_page.show()

    sys.exit(app.exec())