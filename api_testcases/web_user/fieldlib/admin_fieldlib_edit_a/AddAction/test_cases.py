import json
import pytest
import allure
from api_testcases.web_user.action_re_body import *
from .api import *
from .fuction import *
from base.common import send_request, success_assert, config_write_random, config_get_section_value, base64_encode_value


@allure.step('创建文字类字段')
def init_text(ObjectType, FieldType):
    """
    创建自定义字段-文字类字段初始化函数

    :param ObjectType: 系统字段对象
    :param FieldType: 字段类型
    :return: 字段ID
    """
    FieldName = config_write_random('ticket_init_fieldlib', FieldType, FieldType)
    re_body = {"data": base64_encode_value(common_data(ObjectType, FieldType, FieldName))}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])  # 正向请求返回的固定校验
    return common_assert(ObjectType, FieldType, FieldName, re_json), FieldName  # 创建自定义字段固定校验并返回字段ID


@pytest.mark.run(order=2)
@allure.severity('Blocker')
@pytest.mark.parametrize('FieldType', [pytest.param('Date', id='日期（年月日）'),
                                       pytest.param('DateTime', id='日期'),
                                       pytest.param('Text', id='文本'),
                                       pytest.param('TextArea', id='多文本')])
@pytest.mark.parametrize('ObjectType', ['Ticket'])
def test_init_text(ObjectType, FieldType):
    """
    创建自定义字段-文字类字段初始化用例

    :param ObjectType: 系统字段对象
    :param FieldType: 字段类型
    """
    init_text(ObjectType, FieldType)


@pytest.mark.run(order=2)
@allure.severity('Blocker')
@pytest.mark.parametrize('FieldType', [pytest.param('Checkbox', id='复选框'),
                                       pytest.param('Dropdown', id='下拉选择框'),
                                       pytest.param('Multiselect', id='下拉多选框')])
@pytest.mark.parametrize('ObjectType', ['Ticket'])
def test_init_select(ObjectType, FieldType):
    """
    创建自定义字段-选择类字段初始化

    :param ObjectType: 系统字段对象
    :param FieldType: 字段类型
    """
    FieldName = config_write_random('ticket_init_fieldlib', FieldType, FieldType)
    data_body = common_data(ObjectType, FieldType, FieldName)
    data_body['SelectOptions'] = ["0", "1", "2"]  # 选项标号
    select_body = {"FileTypeValue0": "选项一",  # 选项内容
                   "FileTypeKey0": "key1",
                   "FileTypeValue1": "选项二",
                   "FileTypeKey1": "key2",
                   "FileTypeValue2": "选项三",
                   "FileTypeKey2": "key3"}
    data_body.update(select_body)
    re_body = {"data": base64_encode_value(data_body)}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])  # 正向请求返回的固定校验
    common_assert(ObjectType, FieldType, FieldName, re_json)  # 创建自定义字段固定校验


@pytest.mark.run(order=3)
@allure.severity('Blocker')
@pytest.mark.parametrize('FieldType', [pytest.param('FieldGroup', id='字段组')])
@pytest.mark.parametrize('ObjectType', ['Ticket'])
def test_init_fieldgroup(ObjectType, FieldType):
    """
    创建自定义字段-字段组初始化

    :param ObjectType: 系统字段对象
    :param FieldType: 字段类型
    """
    FieldGroupOrder = config_get_section_value('ticket_init_fieldlib', ["fieldgroup", "treecascader"])  # 获取所有自定义字段
    fieldgroup_body = fieldgroup_structure_add({}, FieldGroupOrder)  # 根据FieldGroupOrder中的字段id来添加对应的字段组结构
    FieldName = config_write_random('ticket_init_fieldlib', FieldType, FieldType)
    data_body = common_data(ObjectType, FieldType, FieldName)
    data_body['FieldGroupOrder'] = FieldGroupOrder
    data_body.update(fieldgroup_body)
    re_body = {"data": base64_encode_value(data_body)}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])  # 正向请求返回的固定校验
    common_assert(ObjectType, FieldType, FieldName, re_json)  # 创建自定义字段固定校验
