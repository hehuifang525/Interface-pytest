import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert,get_datetime,mysql_get_value
from .api import *
from .function import *


@allure.severity('Normal')
def test_add_service():
    """
        必填增加服务校验
    """
    service_name = "%s%s" % ('ser', get_datetime())  # 随机生成服务名称
    re_body = common_data(service_name)
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json['result'])
    assert_db(re_json,service_name)


def add_service_commom():
    """
         必填增加服务校验,公共
     """
    service_name = "%s%s" % ('ser', get_datetime())  # 随机生成服务名称
    re_body = common_data(service_name)
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])
    assert re_json["data"]["data"]["id"] == mysql_get_value("service", "id", "name", service_name, ""), "添加成功后返回的服务id校验"
    service_info = {"service_name":service_name,"ID":re_json["data"]["data"]["id"]}
    return service_info



