import pytest
import allure
from api_testcases.web_customer.action_re_body import *
from .fuction import *
from base.common import conf, send_request, success_assert, fail_assert
from api_testcases.web_customer.ticket.ticket_detail_c.ShowJSONDataCustomer.fuction import *
from api_testcases.web_customer.ticket.ticket_detail_c.UpdateFlowCardCustomer.fuction import customer_ticket_flow_card_default
from api_testcases.web_user.ticket.ticket_detail_a.ShowJSONData.fuction import ticket_customer_check, ticket_mysql_expand_inner


def data(TicketID):
    """
    查看工单详情接口固定请求body

    :param TicketID: 工单ID
    """
    data_body = {"TicketID": TicketID}
    return action_body(__file__, data_body)


@allure.severity('blocker')
@pytest.mark.parametrize("TicketID", get_customer_random_ticket_id())
def test_2020111210000034_check(TicketID):
    """
    rd工单2020111210000034版本-查看工单详情接口-正向验证

    :param TicketID: 工单ID
    """
    result = send_request(method, url, headers=headers(), data=data(TicketID))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])
    assert re_json['data']['Content']['TicketZoomFlowCardDefault'] == \
           customer_ticket_flow_card_default(conf['ServiceCool']['url_customer']), "当前账号默认工单信件展开方式"
    customer_articles_check(re_json['data']['Content']['TicketZoomFlowInformation'], TicketID)  # 随机抽取random_size个信件检查信件的主题、操作时间、模板名称、节点名称、操作人类型、操作人名称、操作人所在单位信息、用户是否可见、(信件数据基本信息)
    assert re_json['data']['TicketInformation']['Order'] == ["CustomerUserData", "BaseData"], "右侧卡片顺序(目前为固定顺序）"
    assert re_json['data']['TicketInformation']['CustomerUserID'] == \
           mysql_get_value('ticket', 'customer_user_id', 'id', TicketID), "右侧客户用户ID"

    assert re_json['data']['TicketInformation']['CustomerUserDataOrder'] == \
           ["CustomerCompany", "CustomerUser", "CustomerUserDataLink"], "右侧客户信息栏顺序(目前为固定顺序）"
    ticket_customer_check(4, re_json['data']['TicketInformation'], TicketID)  # 右侧客户信息栏

    assert re_json['data']['TicketInformation']['BaseDataOrder'] == \
           ["Queue", "State", "TicketCreatorUser", "TicketCustomerUser", "Type", "Priority", "Owner"], "右侧基本信息栏顺序(目前为固定顺序）"
    assert re_json['data']['TicketInformation']['BaseData']['Queue']['value'] == \
           ticket_mysql_expand_inner('b.name', 'queue', 'queue_id', 'id', TicketID), "右侧基本信息栏-角色"
    assert re_json['data']['TicketInformation']['BaseData']['State']['value'] == \
           ticket_mysql_expand_inner('b.name', 'ticket_state', 'ticket_state_id', 'id', TicketID), "右侧基本信息栏-状态"
    assert re_json['data']['TicketInformation']['BaseData']['TicketCreatorUser']['value'] == \
           customer_ticket_creator(TicketID), "右侧基本信息栏-创建人"
    assert re_json['data']['TicketInformation']['BaseData']['TicketCustomerUser']['value'] == \
           ticket_mysql_expand_inner('b.full_name', 'customer_user', 'customer_user_id', 'login', TicketID), "右侧基本信息栏-用户"
    assert re_json['data']['TicketInformation']['BaseData']['Type']['value'] == \
           ticket_mysql_expand_inner('b.name', 'ticket_type', 'type_id', 'id', TicketID), "右侧基本信息栏-类型"


def fail_check(TicketID, message):
    """
    查看错误工单

    :param TicketID:工单ID
    :param message: 报错信息
    """
    result = send_request(method, url, headers=headers(), data=data(TicketID))
    re_json = result.json()

    if TicketID in ["0", ""]:
        assert result.status_code == 200, "请求状态码"
        assert re_json['result'] == 0, "接口状态码"
        assert re_json['data']['errorInfo'] == message, "接口信息"
    else:
        fail_assert(result.status_code, re_json, message)  # 负向请求返回的固定校验


@allure.severity('blocker')
@pytest.mark.parametrize("TicketID", get_customer_random_no_permissions_ticket_id())
def test_2020111210000034_fail_check(TicketID):
    """
    rd工单2020111210000034版本-查看工单详情接口-无权限查看工单

    :param TicketID:工单ID
    """
    message = "This ticket does not exist, or you don't have permissions to access it in its current state."
    fail_check(TicketID, message)


@allure.severity('Normal')
@pytest.mark.parametrize('TicketID,message',
                         [pytest.param("0", "The ticket is not exists, please check you permission or ticket "
                                            "number/ID is exists", id='工单ID为0'),
                          pytest.param("", "The ticket is not exists, please check you permission or ticket number/ID "
                                           "is exists", id='工单ID为空'),
                          pytest.param("-1", "This ticket does not exist, or you don't have permissions to access it "
                                             "in its current state.", id='工单ID为-1'),
                          pytest.param("100000000", "This ticket does not exist, or you don't have permissions to "
                                                    "access it in its current state.", id='工单ID不存在')])
def test_2020111210000034_fail2_check(TicketID, message):
    """
    rd工单2020111210000034版本-查看工单详情接口-查看错误工单

    :param TicketID:工单ID
    :param message: 报错信息
    """
    fail_check(TicketID, message)
