import pytest
import allure
from api_testcases.web_user.action_re_body import *
from .api import *
from .fuction import *
from base.common import send_request, success_assert, config_write_random, url_encode


@allure.step('创建初始化流程')
def init_create_process(processType_id):
    """
    web-user创建流程

    :param processType_id: 流程类型ID
    """
    process_name = config_write_random('ticket_init', 'process', 'process')
    body_data, node_list, transition_list = init_data(process_name, processType_id)
    re_body = {"data": url_encode(body_data)}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])  # 正向请求返回的固定校验
    process_id = re_json['data']['processID']
    common_assert(processType_id, process_id, process_name)
    assert "EndNode: %s\nFirstNode: %s" % (node_list[1], node_list[2]) in \
           mysql_get_value('pm_process_c', 'config', 'id', process_id), "流程数据库中的流程配置1"
    assert "StartNode: %s" % node_list[0] in \
           mysql_get_value('pm_process_c', 'config', 'id', process_id), "流程数据库中的流程配置2"
    assert "%s:\n    %s:\n      NextNode: %s" % (node_list[0], transition_list[0], node_list[2]) in \
           mysql_get_value('pm_process_c', 'config', 'id', process_id), "流程数据库中的流程配置3"
    assert "%s:\n    %s:\n      NextNode: %s" % (node_list[2], transition_list[1], node_list[3]) in \
           mysql_get_value('pm_process_c', 'config', 'id', process_id), "流程数据库中的流程配置4"
    assert "%s:\n    %s:\n      NextNode: %s" % (node_list[3], transition_list[2], node_list[1]) in \
           mysql_get_value('pm_process_c', 'config', 'id', process_id), "流程数据库中的流程配置5"
    assert mysql_get_value('pm_activity_c', 'name', 'entity_id', node_list[2]) == "Process node1", "节点数据库中的节点1名字"
    assert mysql_get_value('pm_activity_c', 'name', 'entity_id', node_list[3]) == "Process node2", "节点数据库中的节点2名字"
    assert process_node_validate('ticket_init', ["Agent-CreateNormal", "Customer-CreateNormal"]) in \
           mysql_get_value('pm_activity_c', 'config', 'entity_id', node_list[2]),  "节点数据库中的节点1配置"
    assert process_node_validate('ticket_init', ["Agent-Deal","Customer-Deal"]) in \
           mysql_get_value('pm_activity_c', 'config', 'entity_id', node_list[3]),  "节点数据库中的节点2配置"
    assert "FieldName: TypeID" \
           "\n        FieldType: Dropdown" \
           "\n        FieldValue:\n        - '1'\n        - '2'\n        - '3'\n        - '4'\n        - '5'" \
           in mysql_get_value('pm_transition_c', 'config', 'entity_id', transition_list[1]),  "转换数据库中的转换2配置"
    # assert mysql_get_value('pm_transition_c', 'name', 'entity_id', transition_list[0]),   "转换数据库中的转换1名字"
    # assert mysql_get_value('pm_transition_c', 'name', 'entity_id', transition_list[1]), "转换数据库中的转换2名字"
    # assert mysql_get_value('pm_transition_c', 'name', 'entity_id', transition_list[2]), "转换数据库中的转换3名字"


@allure.step('创建流程-添加指定工单模板到流程中')
def init_create_process(TemplateID):
    """
    web-user创建流程-添加指定工单模板到流程中
    SC_Template_11&13-修改颜色，修改图片，二次进入查看，创单页面查看-第二步

    :param TemplateID: 工单模板ID
    """
    processType_id = conf['ticket_init']['processtypeid']
    process_name = config_write_random('ticket_init', 'process', 'process')
    body_data, node_list, transition_list = init_data(process_name, processType_id)
    body_data['nodeValue'][node_list[2]]['templateList'] = [TemplateID]
    re_body = {"data": url_encode(body_data)}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])  # 正向请求返回的固定校验
    process_id = re_json['data']['processID']
    common_assert(processType_id, process_id, process_name)
