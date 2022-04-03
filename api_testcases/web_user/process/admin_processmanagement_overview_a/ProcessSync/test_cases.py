import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert


@allure.step('部署所有流程')
def process_sync():
    """
    web-user部署所有流程
    """
    result = send_request(method, url, headers=headers(), data=action_body(__file__, None))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])

