import pytest
import allure
from api_testcases.web_user.action_re_body import *
from api_testcases.web_user.fieldlib.admin_fieldlib_edit_a.AddAction.api import *
from base.common import send_request, success_assert, base64_encode_value


@allure.severity('normal')
@allure.step('提交编辑级联字段')
def get_tree_cascader_change(ObjectType, FieldName, SelectOptions, ID, form_id, add_body):
    """
    提交编辑自定义字段

    :param ObjectType: 系统字段对象
    :param FieldName: 系统字段和字段名称
    :param SelectOptions: 选项标号
    :param ID: 字段ID，默认为空
    :param form_id: 上传文件的form_id
    :param add_body: 额外添加的body部分，具体为CascaderField属性
    """
    data_body = common_data(ObjectType, 'TreeCascader', FieldName)
    data_body['SelectOptions'] = SelectOptions
    data_body['ID'] = ID
    data_body.update(add_body)
    re_body = {"data": base64_encode_value(data_body), "FormID": form_id}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])
    assert re_json['data']['DynamicField_'+FieldName]['ID'] == ID, "ID"
    assert re_json['data']['DynamicField_'+FieldName]['FieldType'] == 'TreeCascader', "字段类型"
    assert re_json['data']['DynamicField_' + FieldName]['ObjectType'] == ObjectType, "系统字段对象"
    assert re_json['data']['DynamicField_' + FieldName]['Config']['CascaderField'] == add_body['CascaderField'], "级联字段值"
