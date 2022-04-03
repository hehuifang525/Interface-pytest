import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert


@allure.step("进入工单模板编辑页面检查填入值")
def check_normal(TemplateID, TemplateName, Frontend, TemplateType, ValidID):
    """
    进入工单模板编辑页面检查填入值

    :param TemplateID: 工单模板ID
    :param TemplateName: 工单模板名字
    :param Frontend: 使用对象，Agent服务人员，Customer客户用户
    :param TemplateType: 工单模板类型，CreateNormal创建，Deal处理
    :param ValidID: 工单模板有无效
    """
    data_body = {"TemplateID": TemplateID}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, data_body))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])
    assert re_json['data']['data']['adminTicketTemplateBaseData']['Name']['default'] == TemplateName, "模板名字"
    assert re_json['data']['data']['adminTicketTemplateBaseData']['Frontend']['default'] == Frontend, "模板使用对象"
    assert re_json['data']['data']['adminTicketTemplateBaseData']['TemplateType']['default'] == TemplateType, "模板类型"
    assert re_json['data']['data']['adminTicketTemplateBaseData']['ValidID']['default'] == ValidID, "模板有无效"

