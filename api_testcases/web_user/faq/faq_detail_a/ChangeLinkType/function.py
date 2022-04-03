import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import *
from base.Mysql import Mysql
from api_testcases.web_user.faq.faq_edit_a.Save.test_cases import add_faq_commom
from time import sleep


def get_link_id(link_type, location=0):
    """
    查找数据库中工单，知识库概览，cmdb概览中数据id
    默认取第一条数据

    :param link_type: 链接的类型 （Ticket-工单 ,ITSMConfigItem-cmdb概览 ,FAQ-知识库）
    :param location: 查询第几个数据

    返回工单id/知识库概览id/cmdb概览id
    """

    if link_type == "Ticket":

        link_target_keys = mysql_get_list("ticket", "id", "", "", "1=1")[location]

    elif link_type == "ITSMConfigItem":
        # 查找资产
        link_target_keys =mysql_get_list("ci_base", "id", "", "", "1=1")[location]

    else:
        # 找知识库
        link_target_keys = mysql_get_list("faq_item", "id", "", "", "valid_id=1")[location]

    return link_target_keys


def get_cmdb_class_id(cmdb_id):
    """
    取cmdb概览对应的id
    :param cmdb_id: cmdbid
    """

    class_id = mysql_get_value("ci_base", "class_id", "id", cmdb_id, "")
    return class_id


def get_link_list(link_type, re_json ,cmdb_class_id=0):
    """
    返回当前知识库文章，对应类别的链接列表

    :param link_type: 链接的类型 （Ticket-工单 ,ITSMConfigItem-cmdb概览 ,FAQ-知识库）
    :param location: 响应json
    :param cmdb_class_id: 如果分类为cmbd，则需要传入cmdb的分类id

    """
    if link_type == "ITSMConfigItem":
        link_target_keys_list = re_json["data"]["TableData"][link_type][str(cmdb_class_id)]["OverviewList"]
    else:
        link_target_keys_list = re_json["data"]["TableData"][link_type]["OverviewList"]
    link_target_keys_list_num = []
    for i in link_target_keys_list:
        if link_type == "Ticket":
            link_target_keys_list_num.append(i["TicketID"])
        elif link_type == "ITSMConfigItem":
            link_target_keys_list_num.append(i["ConfigItemID"])
        else:
            link_target_keys_list_num.append(i["FAQID"])
    return link_target_keys_list_num