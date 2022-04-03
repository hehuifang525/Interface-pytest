import random
import pytest
import allure
from api_testcases.web_customer.action_re_body import *
from base.common import conf, send_request, success_assert, fail_assert
from .fuction import *
from api_testcases.web_customer.ticket.ticket_detail_c.ShowJSONDataCustomer.fuction import get_customer_random_ticket_id

data_body = {}


@allure.severity('normal')
@pytest.mark.parametrize('TicketID,message',
                         [pytest.param("0", "The ticket is not exists, please check you permission or ticket "
                                            "number/ID is exists", id='工单ID为0'),
                          pytest.param("", "The ticket is not exists, please check you permission or ticket number/ID "
                                           "is exists", id='工单ID为空'),
                          pytest.param("-1", "This ticket does not exist, or you don't have permissions to access it "
                                             "in its current state.", id='工单ID为-1'),
                          pytest.param("100000000", "This ticket does not exist, or you don't have permissions to "
                                                    "access it in its current state.", id='工单ID不存在')])
@pytest.mark.parametrize('FlowCardData', [random.choice(range(2))])
def test_set_FlowCard_fail(TicketID, FlowCardData, message):
    """
    web-customer失败设置信件展开方式偏好设置

    :param TicketID: 工单ID
    :param FlowCardData: 信件展开方式
    :param message: 期望的报错提示信息
    """
    data_body['TicketID'] = TicketID
    data_body['FlowCardData'] = FlowCardData
    old_FlowCardData = customer_ticket_flow_card_default(conf['ServiceCool']['url_customer'])  # 旧的信件展开方式值
    result = send_request(method, url, headers=headers(), data=action_body(__file__, data_body))
    re_json = result.json()

    if TicketID in ["0", ""]:
        assert result.status_code == 200, "请求状态码"
        assert re_json['result'] == 0, "接口状态码"
        assert re_json['data']['errorInfo'] == message, "接口信息"
    else:
        fail_assert(result.status_code, re_json, message)  # 负向请求返回的固定校验
    assert customer_ticket_flow_card_default(conf['ServiceCool']['url_customer']) == old_FlowCardData, "数据库里信件展开方式值未更改"


@allure.severity('normal')
@pytest.mark.parametrize('TicketID', [get_customer_random_ticket_id()[0]])
@pytest.mark.parametrize('FlowCardData', [pytest.param('0', id='展开第一封'),
                                          pytest.param('1', id='展开全部'),
                                          pytest.param('2', id='不展开')])
def test_set_FlowCard_success(TicketID, FlowCardData):
    """
    web-customer成功设置信件展开方式偏好设置

    :param TicketID: 工单ID
    :param FlowCardData: 信件展开方式
    """
    data_body['TicketID'] = TicketID
    data_body['FlowCardData'] = FlowCardData
    result = send_request(method, url, headers=headers(), data=action_body(__file__, data_body))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])  # 正向请求返回的固定校验
    assert re_json['data']['message'] == "Successfuly updated", "操作返回信息"
    assert customer_ticket_flow_card_default(conf['ServiceCool']['url_customer']) == FlowCardData, "数据库里信件展开方式值"
