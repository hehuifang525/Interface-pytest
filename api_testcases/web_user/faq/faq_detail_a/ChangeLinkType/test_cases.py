import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import *
from base.Mysql import Mysql
from api_testcases.web_user.faq.faq_edit_a.Save.test_cases import add_faq_commom
from time import sleep
from .function import get_link_id,get_cmdb_class_id,get_link_list
from .api import *


@pytest.mark.parametrize("link_type", ["Ticket", "ITSMConfigItem", "FAQ"])
# @pytest.mark.parametrize("link_type", ["Ticket"])
@allure.severity('Critical')
def test_add_link(link_type):

    """
        知识库，链接一篇知识库文章，链接一个工单，链接一个cmdb资产
    """

    # 搜索目前系统中存在的第一篇知识库文章
    faq_id = mysql_get_value("faq_item", "id", "valid_id", "1")
    # 如果系统中没有任何一篇文章，则先现加一篇文档
    # if not faq_id:
    #     # print("不存在，需要新增")
    #     faq_info = add_faq_commom()
    #     faq_id = faq_info["faq_id"]
    link_target_keys = get_link_id(link_type, 1)

    cmdb_class_id = 0
    if link_type == "ITSMConfigItem":
        cmdb_class_id = get_cmdb_class_id(link_target_keys)

    re_body = common_add_link_data(faq_id, link_type, link_target_keys)
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    assert re_json["data"]["message"] == "成功添加1个链接。", "添加成功提示"

    # 进入知识库详情页面链接的工单
    re_body_detail = {"SourceObject": "FAQ", "SourceKey": faq_id}
    result_detail = send_request(method, url, headers=headers(), data=action_body(__file__, re_body_detail))
    re_json_detail = result_detail.json()
    success_assert(result_detail.status_code, re_json_detail["result"])
    link_target_keys_list_num = get_link_list(link_type, re_json_detail,cmdb_class_id)
    assert str(link_target_keys) in link_target_keys_list_num, "检查知识库详情中是否存在链接的id"


@allure.severity('Critical')
def test_del_link_ticket():
    """
    知识库，删除链接的一个工单,删除链接的知识库，删除链接的cmdb
    """
    # 从系统中搜索一篇有知识库的文章，将其链接的一工单进行删除
    ticket_id = mysql_get_value("link_relation", "source_key,target_key", "target_object_id", 3, "")
    faq_id = mysql_get_value("link_relation", "target_key", "target_object_id", 3, "")
    re_body = common_del_link_data(faq_id,"Ticket",ticket_id)
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    assert re_json["data"]["message"] == "成功删除1个链接。", "添加成功提示"

    # 进入详情页检查链接的工单
    re_body_detail = {"SourceObject": "FAQ", "SourceKey": faq_id}
    result_detail = send_request(method, url, headers=headers(), data=action_body(__file__, re_body_detail))
    re_json_detail = result_detail.json()
    ticket_list_num = get_link_list("Ticket", re_json_detail)
    success_assert(result_detail.status_code, re_json_detail["result"])
    assert str(ticket_id) not in ticket_list_num, "删除链接工单后进入知识库详情检查"


# # @pytest.mark.parametrize("link_info",
# #                          [{"link_type":"Ticket","source_object_id":2},
# #                           {"link_type":"FAQ","source_object_id": 1},
# #                           {"link_type":"ITSMConfigItem","source_object_id": 3}])
#
#
# @pytest.mark.parametrize("link_info",
#                          [{"link_type":"FAQ","source_object_id": 1}])
# @allure.severity('Critical')
# def test_del_link(link_info):
#     """
#     知识库，删除链接的一个工单,删除链接的知识库，删除链接的cmdb
#     """
#     link_type = link_info.get("link_type") # 链接类型
#     # 链接的对象id target_object_id/source_object_id 1=> 知识库，2=> 工单 ，3=> cmdb
#     source_object_id = link_info.get("source_object_id")
#     # 备注： target_object_id/source_object_id 1=> 知识库，2=> 工单 ，3=> cmdb
#
#     # 查询出来的数据中必须是有有效数据，否则删除失败
#     link_info_id = list(Mysql().get_value("link_relation", "source_key, target_key", "", "",
#                                 "target_object_id = 1 AND source_object_id = " + str(source_object_id))[0])
#     # link_info_id = list(link_info_id)
#     print(link_info_id)
#
#     # 需要删除的数据id
#     # for i in link_info_id:
#     #     print(i)
#     faq_id = link_info_id[1]
#     del_id = link_info_id[0]
#     print(faq_id,del_id)
#
#     # 从系统中搜索一个链接了工单的知识库，并将其删除链接
#     # 注意这里的SourceKey在数据库中的字段是target_key
#     re_body = {"SourceObject": "FAQ", "SourceKey": faq_id,
#                "LinkDeleteIdentifier": [link_type +"::" + del_id + "::Normal"], "Method": "LinkDelete"}
#     result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
#     re_json = result.json()
#
#     success_assert(result.status_code, re_json["result"])
#     assert re_json["data"]["message"] == "成功删除1个链接。", "添加成功提示"
#
#     # # 进入知识库详情查看记录是否删除
#     # re_body_detail = {"SourceObject": "FAQ", "SourceKey": faq_id}
#     # result_detail = send_request(method, url, headers=headers(), data=action_body(__file__, re_body_detail))
#     # re_json_detail = result_detail.json()
#     # success_assert(result_detail.status_code, re_json_detail["result"])
#     # link_target_keys_list = re_json_detail["data"]["TableData"][link_type]["OverviewList"]
#     # link_target_keys_list_num = []
#     # for i in link_target_keys_list:
#     #     if link_type == "Ticket":
#     #         link_target_keys_list_num.append(i["TicketID"])
#     #     # elif link_type == "ITSMConfigItem":
#     #     #     link_target_keys_list_num.append(i["ConfigItemID"])
#     #     else:
#     #         link_target_keys_list_num.append(i["FAQID"])
#     # link_target_is_in_list_flag = 0
#     #
#     # if str(del_id) not in link_target_keys_list_num:
#     #     link_target_is_in_list_flag = 1
#     # assert link_target_is_in_list_flag == 1, "知识库详情中错误显示删除后的数据"







