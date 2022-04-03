import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert, get_regex_value


@allure.step('检查模板的显示')
def page_check_icon_color(TicketColor, TemplateIcon, template_id):
    """
    web-user创建工单页面检查模板的显示
    SC_Template_11&13-修改颜色，修改图片，二次进入查看，创单页面查看-第四步

    :param TicketColor: 模板颜色
    :param TemplateIcon: 模板图片
    :param template_id: 工单模板ID
    """
    result = send_request(method, url, headers=headers(), data=action_body(__file__, None))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])
    check_body = re_json['data']['ProcessTicketCreate']['Info']['TemplateData']
    assert get_regex_value(check_body, "(?=\"TemplateID\": \"%%%\")[\\s\\S]+?\"TemplateColor\": \"(.*?)\"",
                           template_id) == TicketColor, "页面中的模板颜色"
    assert get_regex_value(check_body, "(?=\"TemplateID\": \"%%%\")[\\s\\S]+?\"TemplateIcon\": \"(.*?)\"",
                           template_id) == TemplateIcon, "页面中的模板图片"
