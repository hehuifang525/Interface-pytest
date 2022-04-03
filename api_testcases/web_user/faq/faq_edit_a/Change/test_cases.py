import pytest
import allure
from base.common import send_request, success_assert
from api_testcases.web_user.action_re_body import *


@allure.severity('Normal')
def get_form_id():
    re_body = {"ItemID":""}

    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json['result'])
    return re_json["data"]["FormID"]





