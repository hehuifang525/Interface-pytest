import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_all


@allure.severity('Blocker')
def test_customer_user_list():
    """
    进入客户用户管理-获取根据客户获取客户用户列表数据
    """
    data_body = {"InitMode": "1", "TreeInitMode": "1"}
    re_body = {"data": base64_encode_all(data_body)}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    # print(re_json, '3')
    success_assert(result.status_code, re_json["result"])



