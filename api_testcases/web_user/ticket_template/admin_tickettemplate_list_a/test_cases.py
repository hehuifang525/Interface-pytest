import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert


re_body = {
            "Subaction": "",
            "data": "{\"startHit\": \"1\"}",
            "Action": "admin_tickettemplate_list_a"
            }


@pytest.mark.run(order=1)
@pytest.mark.xfail
@allure.severity('Blocker')
def test_init_SC_Template_6_8_check():
    """
    SC_Template_6-8-新系统，模板列表页面显示
    """
    result = send_request(method, url, headers=headers(), data=re_body)
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])
    assert re_json['data']['TabCardList']['Tab01-FreeStyleAdminTicketTemplate']['Count'] == 0
    assert re_json['data']['PageSize'] is None
    assert re_json['data']['PreferenceFields'] == ["Name", "Frontend", "ShowMobile", "ShowWeb", "TemplateType",
                                                   "ShowWindows", "Describe", "ValidID", "ChangeBy", "ChangeTime",
                                                   "CreateBy", "CreateTime"]
