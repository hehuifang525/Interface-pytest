
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_all
import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert


def common_data(service_link_company, sla, process, tag_data):
    """
    服务链接数据body

    :param service_link_company: 链接客户
    :param sla: 服务水平协议
    :param process: 过程
    :param tag_data: 标签
    """
    data_body = {'ServiceLinkCompany': service_link_company,
                 'SLA': sla,
                 'Process': process,
                 'TagData': tag_data}

    return data_body


def common_assert(re_json, link_type: list):
    """
    管理成功的提示信息校验
     :param re_json: 返回的响应
     :param link_type: 链接的类型(sla/process/company)
    """
    # 'data': {'TagData': 'success', 'slamsg': 'success'}
    if "sla" in link_type:
        assert re_json["data"]["slamsg"] == 'success','关联sla成功校验'
        print(1)
    if "process" in link_type:
        assert re_json["data"]["processmsg"] == 'success','关联流程成功校验'
        print(2)
    if "company" in link_type:
        assert re_json["data"]["companymsg"] == 'success','关联客户成功校验'
        print(3)

    assert re_json["data"]["TagData"] == 'success'
    print(4)
