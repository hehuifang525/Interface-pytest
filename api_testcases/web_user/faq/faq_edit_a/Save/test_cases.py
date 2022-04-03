import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_all,config_read,fail_assert,base64_encode_value
from base.Mysql import Mysql
from .api import *
from time import sleep
from  api_testcases.web_user.faq.admin_faq_overview_a.Save.test_cases import add_faq_category_commom


@allure.severity('Blocker')
def test_add_faq():
    """
    填写必填增加知识库文章-无附件
    """

    faq_name = "%s-%s" % ('pytest-faq', get_datetime())  # 随机生成名称
    # 取分类
    parent_id = config_read("faq_category","categoryid")
    faq_category_name_db_num = mysql_get_value("faq_category", "NAME", "ID", parent_id, "")
    if not faq_category_name_db_num:  # 不存在则创建
        faq_category_info = add_faq_category_commom()
        parent_id = faq_category_info["CategoryID"]
    body = "ceshi wenb"
    data_body = common_data(faq_name, body, category_id_parent=parent_id)
    re_body = {"data": base64_encode_value(data_body)}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    # print(re_json)
    # 校验返回的id
    success_assert(result.status_code, re_json["result"])
    common_assert(faq_name, re_json)


def add_faq_commom():
    """
    填写必填增加知识库文章-无附件-公共用例
    """

    faq_name = "%s-%s" % ('pytest-faq', get_datetime())  # 随机生成名称
    # 取分类
    parent_id = config_read("faq_category","categoryid")
    # 判断当前分类系统中是否存在，不存在则新建一个分类
    faq_category_name_db_num = mysql_get_value("faq_category", "NAME", "ID", parent_id, "")
    if not faq_category_name_db_num:  # 不存在则创建
        faq_category_info = add_faq_category_commom()
        parent_id = faq_category_info["CategoryID"]
    body = "ceshi wenb"
    data_body = common_data(faq_name, body, category_id_parent=parent_id)

    re_body = {"data": base64_encode_value(data_body)}

    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    faq_id = mysql_get_value("faq_item", "id", "f_subject", faq_name, "")
    success_assert(result.status_code, re_json["result"])
    common_assert(faq_name, re_json)
    faq_info = {"faq_id": faq_id,"name": faq_name, "parent_id":parent_id}
    return faq_info



# def test_add_faq_xunhuan():
#     """
#     填写必填增加知识库文章-无附件，批量增加数据
#     """
#     add_num_start = 1   # 开始号段
#     add_num_end = 60   # 结束号段
#
#     for i in range(add_num_start, add_num_end):
#
#         # faq_category_name = "%s-%s" % ('pytest-faq', get_datetime())  # 随机生成名称
#         faq_category_name = "批量" + str(i) # 随机生成名称
#         # 取分类
#         parent_id = config_read("faq_category","categoryid")
#         faq_category_name_db_num = mysql_get_value("faq_category", "NAME", "ID", parent_id, "")
#         if not faq_category_name_db_num:  # 不存在则创建
#             faq_category_info = add_faq_category_commom()
#             parent_id = faq_category_info["CategoryID"]
#         # body = "ceshi wenb"
#         body = "批量内容" + str(i)
#         data_body = common_data(faq_category_name, body, category_id_parent=parent_id)
#
#         re_body = {"data": base64_encode_value(data_body)}
#
#         result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
#         re_json = result.json()
#         # print(re_json)
#         # 校验返回的id
#         faq_id = mysql_get_value("faq_item", "id", "f_subject", faq_category_name, "")
#         success_assert(result.status_code, re_json["result"])
#         assert re_json["data"]["message"] == "Added successfully!", "添加成功提示"
#         assert re_json["data"]["data"]["ItemID"] == faq_id, "接口返回的知识库文章id校验"
#         print("成功", i)
#
