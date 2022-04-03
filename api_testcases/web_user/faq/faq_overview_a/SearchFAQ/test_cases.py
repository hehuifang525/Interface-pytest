import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_all,config_read,fail_assert,base64_encode_value, mysql_get_value,mysql_get_list
from base.Mysql import Mysql
from time import sleep
from api_testcases.web_user.faq.faq_edit_a.Save.test_cases import add_faq_commom


@allure.severity('Normal')
def test_category_all_num():
    """
    知识库类别管理-检查键入知识库类别管理，加载的数据总量
    """
    faq_category_num = mysql_get_value("faq_category", "COUNT(id) as category_num", "", "", "1=1")

    re_body = {"Action": "admin_faq_overview_a"}
    result = send_request(method, url, headers=headers(), data=re_body)
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    assert re_json["data"]["TableData"]["Count"] == int(faq_category_num), "知识库类别管理-数量总量校验"


@allure.severity('Normal')
def test_search_faq():
    """
    知识库概览-右侧精确搜索一篇文章
    """
    # 创建一篇文章
    faq_info = add_faq_commom()
    re_body ={"FilterFAQSearch":faq_info["name"],"CategoryID":""}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    faq_list = re_json["data"]["FAQDetailInfo"]
    success_assert(result.status_code, re_json["result"])
    assert re_json["data"]["FAQItemCount"] == 1, "数量校验"
    assert faq_list[0]["FAQID"] == faq_info["faq_id"], "接口返回的知识库文章id校验"
    assert faq_list[0]["CategoryID"] == faq_info["parent_id"], "接口返回的知识库文章分类id校验"
    assert faq_list[0]["Title"] == faq_info["name"], "接口返回的名称"


@allure.severity('Normal')
@pytest.mark.xfail
def test_check_all_num():
    """
        知识库概览-检查进入知识库概览页面，展示的所有工单数量
        加载的界面，无效数据则不显示，数据库查询需要校验分类数据是否有效

        预期失败，已知bug，进入知识库概览，只能加载50条数据
    """
    # 查询有效的知识库文章数量
    faq_count = Mysql().get_value(" faq_item a , faq_category b", " COUNT(a.id) as times", "", "",
                                        "a.category_id = b.id AND b.valid_id = 1 AND a.valid_id = 1")
    faq_db_count = faq_count[0][0]
    # 当无"total": "10000" 参数的时候（"data": '{"InitMode": "1","total": "10000"}'），预期应该返回全部有些数据
    re_body = {"Subaction": "", "data": '{"InitMode": "1"}', "Action": "faq_overview_a"}
    result = send_request(method, url, headers=headers(), data=re_body)
    re_json = result.json()
    # print(re_json)
    result_num = re_json["data"]["FAQItemCount"]
    assert faq_db_count == result_num,"知识库概览进入界面加载数量校验"
    #
    # if faq_db_count > 50:
    #     for total_num in [50, 30]:
    #         re_body = {'Action': 'faq_overview_a', 'Subaction': 'TreeAction',
    #                    'data': '{"startHit": "1", "total": '+ str(total_num) +'}'}
    #         result = send_request(method, url, headers=headers(), data=re_body)
    #         re_json = result.json()
    #         result_count = re_json["data"]["FAQItemCount"]
    #         assert int(result_count) == total_num, "知识库概览指定分类-指定总量返回校验"


@allure.severity('Normal')
def test_appoint_category_faq():
    """
        知识库概览：
        加载指定分类的知识库文章
        对返回的数量以及展示的分类进行检查（找翻页数据）
        对返回数据条数校验：数据超50条（1）检查去参数限制后，默认的50条显示  （2）检查返回30条测试 ；
    """
    faq_count_tuple = Mysql().get_value("faq_item", "category_id ,COUNT(id) as times", "", "", "valid_id = 1 GROUP BY category_id order by times ")
    category_id = faq_count_tuple[0][0]

    # category_id = 106
    # faq_times = 59
    faq_times = faq_count_tuple[0][1]
    # 检查分类总数显示，控制数量
    re_body = {'Action': 'faq_overview_a', 'Subaction': 'TreeAction', 'data': '{"startHit": "1", "CategoryID": '+ str(category_id)+', "total": "10000"}'}

    result = send_request(method, url, headers=headers(), data=re_body)
    re_json = result.json()
    result_count = re_json["data"]["FAQItemCount"]
    faq_detail_info = re_json["data"]["FAQDetailInfo"]

    for detail_info_item in faq_detail_info:
        assert detail_info_item["CategoryID"] == str(category_id), "返回的记录中，分类id的校验"

    assert int(result_count) == faq_times, "知识库概览指定分类-数量总量校验"

    if faq_times > 50:
        for total_num in [50, 30]:
            re_body = {'Action': 'faq_overview_a', 'Subaction': 'TreeAction',
                       'data': '{"startHit": "1", "CategoryID": ' + str(category_id) + ', "total": '+ str(total_num) +'}'}
            result = send_request(method, url, headers=headers(), data=re_body)
            re_json = result.json()
            result_count = re_json["data"]["FAQItemCount"]
            assert int(result_count) == total_num, "知识库概览指定分类-指定总量返回校验"


