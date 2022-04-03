import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert,mysql_get_value, mysql_get_list


@allure.severity('Normal')
def test_repeat_name():
    """
        服务同名校验
    """
    # 从数据库中去一个服务
    name_db = mysql_get_value("service", "name", "valid_id", "1")
    re_body = {"Filter":"Name","FilterValue": name_db}

    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])
    assert re_json["data"]["message"] == "The field value already exists in DB. Please retype it!", "服务同名校验，提示信息"

