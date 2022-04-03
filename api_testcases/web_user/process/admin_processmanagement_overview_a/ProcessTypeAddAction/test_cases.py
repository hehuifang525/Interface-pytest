import pytest
import allure
from api_testcases.web_user.action_re_body import *
from .api import *
from base.common import send_request, success_assert, get_datetime


@allure.step('创建流程类型')
def init_create_processType():
    """
    web-user创建流程类型
    """
    processType_name = "%s%s" % ('processType', get_datetime())
    valid = "1"
    result = send_request(method, url, headers=headers(), data=common_data(processType_name, valid))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])  # 正向请求返回的固定校验
    return common_assert(processType_name, valid, re_json)  # 创建流程类型固定校验
