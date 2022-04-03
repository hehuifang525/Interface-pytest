import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert, mysql_get_value


def data(field_id):
    """
    进入添加字段页面固定请求body
    """
    data_body = {"ID": str(field_id)}
    return action_body(__file__, data_body)


@allure.severity('normal')
@allure.step('查看字段的FormID')
def get_form_id(field_id):
    """
    查看字段的FormID

    :param field_id: 字段ID
    :return: 字段的FormID
    """
    result = send_request(method, url, headers=headers(), data=data(field_id))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])
    assert re_json['data']['FieldType'] == mysql_get_value('dynamic_field', 'field_type', 'id', field_id), "字段类型"
    assert mysql_get_value('dynamic_field', 'name', 'id', field_id) in re_json['data']['FieldInfo'], "字段名称"
    return re_json['data']['FormID']
