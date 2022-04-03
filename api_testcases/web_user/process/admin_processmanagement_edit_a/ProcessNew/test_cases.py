import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert, get_regex_value

data_body = {"processID": ""}


@allure.step('进入创建流程页面查看工单模板属性')
def check_template_attribute(TemplateID, field_name, field_value):
    """
    打开流程配置页面，检查相应的正则语句
    SC_Template_31-无效模板（创建/处理模板）不能显示在流程配置页面以供使用-第二步

    :param TemplateID: 工单模板ID
    :param field_name: 属性名
    :param field_value: 属性期望值
    """
    result = send_request(method, url, headers=headers(), data=action_body(__file__, data_body))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])
    assert re_json['data']['ticketTemplateList'][TemplateID][field_name] == field_value
