import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_value,config_read ,get_moblie_number
from .api import *


@allure.severity('Blocker')
def test_add_customeruser():
    """
    进入客户用户管理-填写必填添加用户
    """
    # CompanyName = config_read("company", "companyname")
    company_id = config_read("company", "customerid")
    user_login = "%s-%s" % ('user', get_datetime())  # 随机生成获取客户用户账号
    data_body = common_data(user_login,company_id)

    re_body = {"DetailAction": "AddCustomerUser","SelectedParentCustomeID": company_id, "data": base64_encode_value(data_body)}

    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    assert result.status_code == 200, "接口请求成功标识"
    assert re_json["result"] == 1, "数据添加成功标识"
    assert re_json["data"]["data"]["id"] == user_login, "接口返回的客户id"


@pytest.mark.run(order=2)
@allure.severity('Blocker')
def test_init_add_full_customeruser():
    """
    进入客户用户管理-填写全填添加用户
    """
    company_id = config_read("company", "customerid")
    user_login = "%s-%s" % ('cus', get_datetime())  # 随机生成获取客户用户账号
    user_mobile = get_moblie_number("137")
    user_email = user_mobile + "@qq.com"
    data_body = common_full_data(user_login,company_id,user_email, user_mobile)
    re_body = {"DetailAction": "AddCustomerUser","SelectedParentCustomeID": company_id, "data": base64_encode_value(data_body)}

    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    assert result.status_code == 200, "接口请求成功标识"
    assert re_json["result"] == 1, "数据添加成功标识"
    assert re_json["data"]["data"]["id"] == user_login, "接口返回的客户id"
    # 创建客户成功后，将客户编号、名称写入config
    config_write("customer", "userlogin", user_login)
    config_write("customer", "useremail", user_email)
    config_write("customer", "usermobile", user_mobile)


def add_customer_user_commom():
    """
    进入客户用户管理-填写必填添加用户,公共用例
    """
    CompanyID = config_read("company", "customerid")
    UserLogin = "%s-%s" % ('cus', get_datetime())  # 随机生成获取客户用户账号
    data_body = common_data(UserLogin,CompanyID)

    re_body = {"DetailAction": "AddCustomerUser","SelectedParentCustomeID": CompanyID, "data": base64_encode_value(data_body)}

    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    assert re_json["data"]["data"]["id"] == UserLogin, "接口返回的客户用户id"
    customer_user_info = {"UserLogin": UserLogin, "CompanyID": CompanyID}
    return customer_user_info


def add_full_customer_user_commom():
    """
    进入客户用户管理-填写全填添加用户,公共用例
    """
    company_id = config_read("company", "customerid")
    user_login = "%s-%s" % ('cus', get_datetime())  # 随机生成获取客户用户账号
    user_mobile = get_moblie_number("137")
    user_email = user_mobile + "@qq.com"
    data_body = common_full_data(user_login,company_id,user_email, user_mobile)
    re_body = {"DetailAction": "AddCustomerUser","SelectedParentCustomeID": company_id, "data": base64_encode_value(data_body)}

    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    assert result.status_code == 200, "接口请求成功标识"
    assert re_json["result"] == 1, "数据添加成功标识"
    assert re_json["data"]["data"]["id"] == user_login, "接口返回的客户id"

    customer_user_info = {"UserLogin": user_login, "CompanyID": company_id,"UserMobile":user_mobile,"UserMmail":user_email}
    return customer_user_info



