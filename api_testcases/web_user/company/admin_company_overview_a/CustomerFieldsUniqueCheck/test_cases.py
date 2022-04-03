import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_value,config_read,get_moblie_number
from api_testcases.web_user.company.admin_company_overview_a.StoreOrUpdateCustomerUser.test_cases import add_full_customer_user_commom

#
# @allure.severity('Normal')
# @pytest.mark.parametrize('check', [{"filter":"UserLogin","filter_value":config_read("customer", "userlogin"),"describe":"账号"},
#                                     {"filter":"UserEmail","filter_value":config_read("customer", "useremail"),"describe":"邮箱号"},
#                                     {"filter":"UserMobile","filter_value":config_read("customer", "usermobile"),"describe":"手机号"}])
# def test_check_repeat(check):
#     """
#         前置：需要执行创建全填用户
#         进入客户用户管理-检查客户用户正确手机号格式、手机号重复；正确邮箱格式、邮箱重复校验
#     """
#     re_body = {"Filter": check.get("filter"), "FilterValue": check.get("filter_value")}
#     result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
#     re_json = result.json()
#     assert re_json["result"] == 1, "接口请求成功标识"
#     assert re_json["data"]["message"] == "The field value already exists in DB. Please retype it!", "用户"+check.get("describe")+"唯一性校验提示"

# 参数读取的方式parametrize会先于test_init_add_full_customeruser执行，使用在用例内创建用户


@allure.severity('Normal')
def test_check_repeat():
    """
        前置：需要执行创建全填用户
        进入客户用户管理-检查客户用户正确手机号格式、手机号重复；正确邮箱格式、邮箱重复校验
    """
    # 创建一个全填用户
    customer_info = add_full_customer_user_commom()
    check_repeat_info = [{"filter":"UserLogin","filter_val":customer_info.get("UserLogin"),"describe":"账号"},
                        {"filter":"UserEmail","filter_val":customer_info.get("UserMmail"),"describe":"邮箱号"},
                         {"filter":"UserMobile","filter_val":customer_info.get("UserMobile"),"describe":"手机号"}]
    for each_check_repeat_info in check_repeat_info:
        re_body = {"Filter": each_check_repeat_info.get("filter"), "FilterValue":each_check_repeat_info.get("filter_val")}
        result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
        re_json = result.json()
        assert re_json["result"] == 1, "接口请求成功标识"
        assert re_json["data"]["message"] == "The field value already exists in DB. Please retype it!", "用户"+each_check_repeat_info.get("describe")+"唯一性校验提示"