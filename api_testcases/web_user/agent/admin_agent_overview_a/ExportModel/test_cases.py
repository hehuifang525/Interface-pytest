import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_all
from .api import get_form_id


@allure.severity('Critical')
@pytest.mark.parametrize('valid', ['1', '2', '5'])
def test_export_user(valid):
    """
    进入服务人员页面，导出user（全部、无效、有效）
    :param valid: 导出有效性


    """
    form_id = get_form_id()

    re_body ={"ObjectBackend": "Agent","data": {"FileType": "Excel","ExportAttribute": None,"Valid": valid},
              "FormID":form_id}
    result = send_request(method, url, headers=headers(), data=action_body(__file__,re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    # 导出的所有记录
    export_list = re_json["data"]["data"]
    # 初始化，有效性标记位
    valid_sign = 0
    # 取出有效性在第几位
    for i in range(len(export_list[0])):
        if export_list[0][i].get("key") == "Valid":
            valid_sign = i
            # print(valid_sign)
            break
    if valid == "1":
        # 遍历所有数据，取出有效性，对有效性进行断言
        for i in range(1, len(export_list)):
            # print(export_list[i][valid_sign])
            assert export_list[i][valid_sign] == "valid","导出有效数据出错"
    elif valid == "2":
        # 遍历所有数据，取出有效性，对有效性进行断言
        for i in range(1, len(export_list)):
            assert export_list[i][valid_sign] == "invalid", "导出无效数据出错"


@allure.severity('Normal')
def test_export_user_col():
    """
    指定导出字段，导出服务人员

    """
    form_id = get_form_id()
    re_body = {"ObjectBackend": "Agent", "data": {"FileType": "Excel","ExportFilter":["UserLogin","UserFullname","UserEmail"],
                                                  "ExportAttribute": None, "Valid": "2"},"FormID": form_id}
    result = send_request(method, url, headers=headers(), data=action_body(__file__,re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    export_list =re_json["data"]["data"][0]
    # 变量-实际导出的记录列
    actual_list = []
    # 对返回的数据取出返回的数据列，并赋值actual_list
    for i in range(len(export_list)):
        actual_list.append(export_list[i].get("key"))
    assert actual_list == ["UserLogin","UserFullname","UserEmail"],"选择输出的字段错误"







