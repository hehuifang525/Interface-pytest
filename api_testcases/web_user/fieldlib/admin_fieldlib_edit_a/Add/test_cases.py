import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert


data_body = {"ID": "new"}


@allure.severity('normal')
def test_qq_check():
    """
    进入添加字段页面—检查QQ类型字段配置
    """
    result = send_request(method, url, headers=headers(), data=action_body(__file__, data_body))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])  # 正向请求返回的固定校验
    assert 'QQ' in re_json['data']['FieldInfo']['FieldType']['options'], "字段类型是否包含QQ的选项"
    assert re_json['data']['FieldInfo']['FieldTypeDefaultData']['QQ']['regex'] == "^[1-9][0-9]{4,11}$", "QQ类型字段的默认正则表达式"
    assert re_json['data']['FieldInfo']['FieldTypeDefaultData']['QQ']['regexError'] \
           == "The QQ format is wrong. Please check it!", "QQ类型字段的默认正则错误提示"

