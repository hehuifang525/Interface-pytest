import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_value,config_read
from api_testcases.web_user.company.admin_company_overview_a.StoreOrUpdateCustomerUser.test_cases import add_customer_user_commom


@allure.severity('Critical')
def test_set_responsible():
    """
    设置客户主管
    """
    # 在客户下创建一个用户，将这个用户设置成客户主管
    customer_user_info = add_customer_user_commom()
    customer_user = customer_user_info.get("UserLogin")
    company_id = customer_user_info.get("CompanyID")
    re_body = {"CustomerID": company_id, "Responsible": [customer_user]}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    assert re_json["data"]["Info"] == "Set Successfully!", "添加成功提示"
    # print(re_json)



