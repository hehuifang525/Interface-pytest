import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_all


@allure.severity('Normal')
@pytest.mark.parametrize('SearchName', ["小酷cool", ""])
def test_search_user(SearchName):
    """
    搜索用户
    """
    re_body = {"SearchName":SearchName, "Filter": "Valid", "CompanyID": ""}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    # print(re_json)


