import pytest
import allure
import random
from api_testcases.web_user.action_re_body import *
from base.common import conf, send_request, success_assert, fail_assert
from .fuction import *
from api_testcases.web_user.ticket.ticket_detail_a.ShowJSONData.fuction import get_random_ticketid

data_body = {}


@allure.severity('normal')
@pytest.mark.parametrize('TicketID,message',
                         [pytest.param("0", "No TicketID is given!", id='工单ID为0'),
                          pytest.param("", "No TicketID is given!", id='工单ID为空'),
                          pytest.param("-1", "This ticket does not exist, or you don't have permissions to access it "
                                             "in its current state.", id='工单ID为-1',
                                       marks=pytest.mark.skipif(conf['ServiceCool']['url_user'] == 'root@localhost',
                                                                reason='root账存在BUG，能查看所有不存在的工单')),
                          pytest.param("10000000", "This ticket does not exist, or you don't have permissions to "
                                                   "access it in its current state.", id='工单ID不存在',
                                       marks=pytest.mark.skipif(conf['ServiceCool']['url_user'] == 'root@localhost',
                                                                reason='root账存在BUG，能查看所有不存在的工单'))])
@pytest.mark.parametrize('FlowCardData', [random.choice(range(2))])
def test_set_FlowCard_fail(TicketID, FlowCardData, message):
    """
    web-user失败设置信件展开方式偏好设置

    :param TicketID: 工单ID
    :param FlowCardData: 信件展开方式
    :param message: 期望的报错提示信息
    """
    data_body['TicketID'] = TicketID
    data_body['FlowCardData'] = FlowCardData
    old_FlowCardData = ticket_flow_card_default(conf['user_info']['user_id'])  # 旧的信件展开方式值
    result = send_request(method, url, headers=headers(), data=action_body(__file__, data_body))
    re_json = result.json()

    fail_assert(result.status_code, re_json, message)  # 负向请求返回的固定校验
    assert ticket_flow_card_default(conf['user_info']['user_id']) == old_FlowCardData, "数据库里信件展开方式值未更改"


@allure.severity('normal')
@pytest.mark.parametrize('TicketID', [get_random_ticketid()[0]])
@pytest.mark.parametrize('FlowCardData', [pytest.param('0', id='展开第一封'),
                                          pytest.param('1', id='展开全部'),
                                          pytest.param('2', id='不展开')])
def test_set_FlowCard_success(TicketID, FlowCardData):
    """
    web-user成功设置信件展开方式偏好设置

    :param TicketID: 工单ID
    :param FlowCardData: 信件展开方式
    """
    data_body['TicketID'] = TicketID
    data_body['FlowCardData'] = FlowCardData
    result = send_request(method, url, headers=headers(), data=action_body(__file__, data_body))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])  # 正向请求返回的固定校验
    assert re_json['data']['message'] == "Successfuly updated", "操作返回信息"
    assert ticket_flow_card_default(conf['user_info']['user_id']) == FlowCardData, "数据库里信件展开方式值"
