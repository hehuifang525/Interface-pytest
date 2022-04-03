import pytest
import allure
from base.common import send_request, success_assert
from api_testcases.web_user.action_re_body import *
from .api import *
from .function import *


@pytest.mark.parametrize('valid', ['1', '2', '5'])
@allure.severity('Normal')
def test_export_service(valid):
    """
        服务导出/全部/有效/无效
    """
    re_body = common_data(valid)

    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json['result'])
    check_export_data(valid, re_json)           # 取导出的数据进行校验


@allure.severity('Normal')
@pytest.mark.parametrize('export_filter', [{"1": "Name", "2": "InternalComments", "3": "ExternalComments"},
                                            {"1": "Name", "2": "InternalComments", "3": "ExternalComments","4":"valid"}])
def test_export_service_col(export_filter):
    """
        带过滤项导出
        已知错误，未屏蔽:当导出的备注信息值为空，excel显示会错位
    """
    # print(export_filter.values())
    re_body = common_data(export_filter=list(export_filter.values()))
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])
    check_export_col_data(re_json, export_filter=export_filter.values())    # 取导出的数据进行校验


