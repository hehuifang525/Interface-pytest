from api_testcases.web_user.action_re_body import action_body
from base.common import mysql_get_value, config_write


def common_data(processType_name, valid):
    """
    创建流程类型固定请求body

    :param processType_name: 流程类型名称
    :param valid: 有效无效
    """
    data_body = {
        "name": processType_name,
        "valid": valid,
        "id": ""
    }
    return action_body(__file__, data_body)


def common_assert(processType_name, valid, re_json):
    """
    创建流程类型固定校验

    :param processType_name: 流程类型名称
    :param valid: 有效无效
    :param re_json: 请求返回的json格式
    :return: 流程类型ID
    """
    processType_id = re_json['data']['processTypeID']
    assert mysql_get_value('pm_process_type_c', 'name', 'id', processType_id) == processType_name, "数据库中保存的流程类型名称"
    assert mysql_get_value('pm_process_type_c', 'valid_id', 'id', processType_id) == valid, "数据库中保存的流程类型的有无效"
    config_write('ticket_init', "processTypeID", processType_id)
    return processType_id
