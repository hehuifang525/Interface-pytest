import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_all


@allure.severity('Critical')
def test_select_valid_tab():
    """
    进入服务人员管理-切换有效tab
    """
    re_body = {"Filter": "Valid", "searchMode": "1", "startHit": "1", "name":"", "SearchName": "",
                 "OtherParams":"", "total":"250"}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    assert re_json["data"]["OverviewList"][0]["Valid"] == "valid", "第一条记录有效值校验"
    assert re_json["data"]["OverviewList"][0]["ValidID"] == "1", "第一条记录有效性ID校验"


@allure.severity('Critical')
def test_select_invalid_tab():
    """
    进入服务人员-切换无效tab
    """
    re_body = {"Filter": "Invalid", "searchMode": "1", "startHit": "1", "name": "", "SearchName": "",
                 "OtherParams": "", "total": "250"}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    assert re_json["data"]["OverviewList"][0]["Valid"] == "invalid","第一条记录无效值校验"
    assert re_json["data"]["OverviewList"][0]["ValidID"] == "2","第一条记录无效性ID校验"





