import pytest
import allure

from api_testcases.web_customer.action_re_body import *
from base.common import conf, send_request, success_assert, config_write


def data(user, pwd):
    """
    登录接口固定请求body

    :param user: user用户名
    :param pwd: 密码
    """
    data_body = {
                    "Action": "Login",
                    "data": "{\"Lang\":\"zh_CN\",\"TimeZoneOffset\":\"-480\",\"User\":\"%s\",\"Password\":\"%s\"}"
                            % (user, pwd)
                }
    return data_body


def common_login():
    """
    常规登录接口，用于conftest.py
    """
    user_login = conf['ServiceCool']['url_customer']
    result = send_request(method, url, headers=headers(),
                          data=data(user_login, conf['ServiceCool']['url_password']))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])  # 正向请求返回的固定校验
    # 把OTRSCustomerInterface、userID和user角色列表写入config
    config_write('ServiceCool', 'OTRSCustomerInterface', re_json['data']['sessionData']['sessionDataValue'])
    print('web-customer登录')
