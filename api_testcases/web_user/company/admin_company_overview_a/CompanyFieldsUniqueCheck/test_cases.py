import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_value,config_read
# from .api import *


@allure.severity('Normal')
def test_check_repeat():
    """
        进入客户用户管理-检查客户编号、客户名称重复
    """
    CompanyName = config_read("company", "companyname")
    re_body = {"Filter":"CustomerCompanyName","FilterValue":CompanyName}

    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()

    # 检查客户名称重复
    assert re_json["result"] == 1, "接口请求成功标识"
    assert re_json["data"]["message"] == "The field value already exists in DB. Please retype it!", "客户名称重复提示"

    # 检查客户编号重复
    CompanyID = config_read("company", "customerid")
    re_body = {"Filter": "CustomerID", "FilterValue": CompanyID}

    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    assert re_json["result"] == 1, "接口请求成功标识"
    assert re_json["data"]["message"] == "The field value already exists in DB. Please retype it!", "客户编号重复提示"


