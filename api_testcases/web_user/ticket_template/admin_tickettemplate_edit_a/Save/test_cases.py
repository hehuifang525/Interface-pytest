import pytest
import allure
from api_testcases.web_user.action_re_body import *
from .api import *
from .fuction import *
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_all


@pytest.mark.run(order=4)
@allure.severity('Blocker')
@pytest.mark.parametrize('TemplateType', [pytest.param('CreateNormal', id='创建'),
                                          pytest.param('Deal', id='处理')])
@pytest.mark.parametrize('Frontend', [pytest.param('Agent', id='服务人员'),
                                      pytest.param('Customer', id='客户用户')])
def test_init_create_template(Frontend, TemplateType):
    """
    web-user创建工单模板-初始化

    :param Frontend: 使用对象，Agent服务人员，Customer客户用户
    :param TemplateType: 工单模板类型，CreateNormal创建，Deal处理
    """
    TemplateName = "%s-%s%s" % (Frontend, TemplateType, get_datetime())
    data_body = common_data(Frontend, TemplateType, TemplateName)
    data_body = tickettemplate_structure_add_sim(data_body, config_get_section_value('ticket_init_fieldlib'))
    re_body = {"data": base64_encode_all(data_body)}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])  # 正向请求返回的固定校验
    common_assert(Frontend, TemplateType, TemplateName, re_json)  # 创建工单模板固定校验


@allure.severity('Minor')
@pytest.mark.parametrize('TemplateType', [pytest.param('CreateNormal', id='创建'),
                                          pytest.param('Deal', id='处理')])
@pytest.mark.parametrize('Frontend', [pytest.param('Agent', id='服务人员'),
                                      pytest.param('Customer', id='客户用户')])
@pytest.mark.parametrize('letter', ["test11", "TEST11"])
def test_SC_Template_24(Frontend, TemplateType, letter):
    """
    SC_Template_24-“名称”大小写会校验为俩值

    :param Frontend: 使用对象，Agent服务人员，Customer客户用户
    :param TemplateType: 工单模板类型，CreateNormal创建，Deal处理
    """
    TemplateName = "%s%s-%s%s" % (letter, Frontend, TemplateType, get_datetime())
    data_body = common_data(Frontend, TemplateType, TemplateName)
    re_body = {"data": base64_encode_all(data_body)}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])  # 正向请求返回的固定校验
    common_assert(Frontend, TemplateType, TemplateName, re_json)  # 创建工单模板固定校验


@allure.step("创建/编辑工单模板-默认版")
def create_common_template(Frontend, TemplateType, ValidID, TemplateID=None):
    """
    web-user创建工单模板-常用版

    :param Frontend: 使用对象，Agent服务人员，Customer客户用户
    :param TemplateType: 工单模板类型，CreateNormal创建，Deal处理
    :param ValidID: 工单模板有无效
    :param TemplateID: 工单模板ID,不填为新增，填为鞭酒
    :return: [模板ID，模板名称]
    """
    TemplateName = "COM-%s-%s%s" % (Frontend, TemplateType, get_datetime())
    data_body = common_data(Frontend, TemplateType, TemplateName)
    data_body['ValidID'] = ValidID
    if TemplateName is not None:
        data_body['TemplateID'] = TemplateID
    re_body = {"data": base64_encode_all(data_body)}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])  # 正向请求返回的固定校验
    return common_assert(Frontend, TemplateType, TemplateName, re_json), TemplateName  # 创建工单模板固定校验


@allure.step("创建工单模板-检查颜色、图片")
def check_icon_color(TicketColor, TemplateIcon):
    """
    web-user创建工单模板-检查颜色、图片
    SC_Template_11&13-修改颜色，修改图片，二次进入查看，创单页面查看-第一步

    :param TicketColor: 模板颜色
    :param TemplateIcon: 模板图片
    :return: 模板ID
    """
    TemplateName = "检查颜色图片%s" % get_datetime()
    data_body = common_data('Agent', 'CreateNormal', TemplateName)
    data_body['TicketColor'] = TicketColor
    data_body['TemplateIcon'] = TemplateIcon
    re_body = {"data": base64_encode_all(data_body)}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])  # 正向请求返回的固定校验
    template_id = common_assert('Agent', 'CreateNormal', TemplateName, re_json)  # 创建工单模板固定校验
    assert mysql_get_value('ticket_template_c', 'template_color', 'id', template_id) == TicketColor, "数据库中的模板颜色"
    assert mysql_get_value('ticket_template_c', 'template_icon', 'id', template_id) == TemplateIcon, "数据库中的模板图片"
    return template_id

