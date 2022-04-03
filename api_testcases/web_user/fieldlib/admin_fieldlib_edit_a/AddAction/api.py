from api_testcases.web_user.action_re_body import *
from base.common import mysql_get_value


def common_data(ObjectType, FieldType, FieldName):
    """
    创建自定义字段固定请求body

    :param ObjectType: 系统字段对象
    :param FieldType: 字段类型
    :param FieldName: 系统字段和字段名称
    """
    data_body = {
        "FieldGroupCopy": "No",
        "FieldGroupAmount": "",
        "FieldGroupFormula": "",
        "HintType": "",
        "Valid": "1",
        "Cols": "",
        "CustomerVisible": "1",
        "FieldID": FieldName,
        "Regex": "",
        "FieldName": FieldName,
        "HintContent": "",
        "ObjectType": ObjectType,
        "RegexHint": "",
        "Rows": "3",
        "Formula": "",
        "FieldType": FieldType,
        "SelectOptions": "",
        "TreeView": "0",
        "FieldLibraryList": "undefined",
        "Unique": "0",
        "ID": "new",
        "FieldGroupOrder": [],
        "AddFieldType": ""
    }
    return data_body


def common_assert(ObjectType, FieldType, FieldName, re_json):
    """
    创建自定义字段固定校验

    :param ObjectType: 系统字段对象
    :param FieldType: 字段类型
    :param FieldName: 系统字段和字段名称
    :param re_json: 请求返回的json格式
    :return: 字段ID
    """
    field_id = re_json['data']['DynamicField_'+FieldName]['id']
    assert mysql_get_value('dynamic_field', 'name', 'id', field_id) == FieldName, "数据库中保存的系统字段"
    assert mysql_get_value('dynamic_field', 'label', 'id', field_id) == FieldName, "数据库中保存的字段名称"
    assert mysql_get_value('dynamic_field', 'object_type', 'id', field_id) == ObjectType, "数据库中保存的系统字段对象"
    assert mysql_get_value('dynamic_field', 'field_type', 'id', field_id) == FieldType, "数据库中保存的字段类型"
    return field_id
