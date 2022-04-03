import pytest
import allure
from api_testcases.web_user.action_re_body import *
from .fuction import *
from base.common import conf, send_request, success_assert, fail_assert
from api_testcases.web_user.ticket.ticket_detail_a.UpdateFlowCard.fuction import ticket_flow_card_default


def data(TicketID):
    """
    查看工单详情接口固定请求body

    :param TicketID: 工单ID
    """
    data_body = {"TicketID": TicketID}
    return action_body(__file__, data_body)


@allure.severity('blocker')
@pytest.mark.parametrize("TicketID", get_random_ticketid())
def test_2020111210000034_check(TicketID):
    """
    rd工单2020111210000034版本-查看工单详情接口-正向验证

    :param TicketID: 工单ID
    """
    result = send_request(method, url, headers=headers(), data=data(TicketID))
    re_json = result.json()
    user_id = conf['user_info']['user_id']

    success_assert(result.status_code, re_json['result'])
    assert re_json['data']['Content']['TicketZoomFlowCardDefault'] == \
           ticket_flow_card_default(user_id), "当前账号默认工单信件展开方式"
    articles_check(re_json['data']['Content']['TicketZoomFlowInformation'], TicketID)  # 随机抽取random_size个信件检查信件的主题、操作时间、模板名称、节点名称、操作人类型、操作人名称、操作人所在单位信息、用户是否可见、(信件数据基本信息)
    assert re_json['data']['TicketInformation']['Order'] == \
           ["CustomerUserData", "OperatorInfo", "BaseData"], "右侧卡片顺序(目前为固定顺序）"
    assert re_json['data']['TicketInformation']['CustomerUserID'] == \
           mysql_get_value('ticket', 'customer_user_id', 'id', TicketID), "右侧客户用户ID"
    ticket_SLA_check(re_json['data']['TicketInformation'], TicketID)  # 工单SLA相关信息

    assert re_json['data']['TicketInformation']['CustomerUserDataOrder'] == \
           ["CustomerCompany", "CustomerUser", "CustomerUserDataLink"], "右侧客户信息栏顺序(目前为固定顺序）"
    ticket_customer_check(3, re_json['data']['TicketInformation'], TicketID)  # 右侧客户信息栏

    owner = re_json['data']['TicketInformation']['OperatorInfo']['Owner']['value']
    assert re_json['data']['TicketInformation']['OperatorInfoOrder'] == \
           ["Queue", "CreatedBy", "Owner", "UserMobile", "Responsible", "OldOwner", "LastChangedByUser"], "右侧处理人员信息栏顺序(目前为固定顺序）"
    assert re_json['data']['TicketInformation']['OperatorInfo']['Queue']['value'] == \
           ticket_mysql_expand_inner('b.name', 'queue', 'queue_id', 'id', TicketID), "右侧处理人员信息栏-角色"
    assert re_json['data']['TicketInformation']['OperatorInfo']['CreatedBy']['value'] == \
           ticket_mysql_expand_inner('b.full_name', 'users', 'create_by', 'id', TicketID)+' ( User )', "右侧处理人员信息栏-创建人"
    assert owner == ticket_mysql_expand_inner('b.full_name', 'users', 'user_id', 'id', TicketID), "右侧处理人员信息栏-指定处理人"
    assert re_json['data']['TicketInformation']['OperatorInfo']['UserMobile']['value'] == \
           ticket_mysql_expand_inner('b.mobile', 'users', 'user_id', 'id', TicketID), "右侧处理人员信息栏-手机"
    assert re_json['data']['TicketInformation']['OperatorInfo']['Responsible']['value'] == \
           ticket_mysql_expand_inner('b.full_name', 'users', 'responsible_user_id', 'id', TicketID), "右侧处理人员信息栏-负责人"
    assert re_json['data']['TicketInformation']['OperatorInfo']['OldOwner']['value'] in \
           ticket_mysql_old_owner(TicketID, owner), "右侧处理人员信息栏-上次所有者"
    assert re_json['data']['TicketInformation']['OperatorInfo']['LastChangedByUser']['value'] == \
           ticket_mysql_expand_inner('b.full_name', 'users', 'change_by', 'id', TicketID), "右侧处理人员信息栏-上次修改人"

    assert re_json['data']['TicketInformation']['BaseDataOrder'] == get_base_data_order(TicketID), "右侧基本信息栏顺序(目前为固定顺序）"
    assert re_json['data']['TicketInformation']['BaseData']['TypeID']['value'] == \
           ticket_mysql_expand_inner('b.name', 'ticket_type', 'type_id', 'id', TicketID), "右侧基本信息栏-类型"
    assert re_json['data']['TicketInformation']['BaseData']['Age']['value'] == ticket_age(TicketID), "右侧基本信息栏-总时长"
    assert re_json['data']['TicketInformation']['BaseData']['Created']['value'] == \
           mysql_get_value('ticket', 'create_time', 'id', TicketID), "右侧基本信息栏-创建时间"
    assert re_json['data']['TicketInformation']['BaseData']['State']['value'] == \
           ticket_mysql_expand_inner('b.name', 'ticket_state', 'ticket_state_id', 'id', TicketID), "右侧基本信息栏-状态"
    assert re_json['data']['TicketInformation']['BaseData']['Priority']['value'] == \
           ticket_mysql_expand_inner('b.name', 'ticket_priority', 'ticket_priority_id', 'id', TicketID), "右侧基本信息栏-优先级"
    assert re_json['data']['TicketInformation']['BaseData']['ServiceID']['value'] == \
           ticket_mysql_expand_inner('b.name', 'service', 'service_id', 'id', TicketID), "右侧基本信息栏-服务"


def fail_check(TicketID, message):
    """
    查看错误工单

    :param TicketID:工单ID
    :param message: 报错信息
    """
    result = send_request(method, url, headers=headers(), data=data(TicketID))
    re_json = result.json()

    fail_assert(result.status_code, re_json, message)  # 负向请求返回的固定校验


@allure.severity('blocker')
@pytest.mark.parametrize("TicketID", get_random_no_permissions_ticketid())
def test_2020111210000034_fail_check(TicketID):
    """
    rd工单2020111210000034版本-查看工单详情接口-无权限查看工单

    :param TicketID:工单ID
    """
    message = "This ticket does not exist, or you don't have permissions to access it in its current state."
    fail_check(TicketID, message)


@allure.severity('Normal')
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
def test_2020111210000034_fail2_check(TicketID, message):
    """
    rd工单2020111210000034版本-查看工单详情接口-查看错误工单

    :param TicketID:工单ID
    :param message: 报错信息
    """
    fail_check(TicketID, message)
