import pytest
import allure
from base.common import send_request, success_assert
from api_testcases.web_user.action_re_body import *
from .function import *
from .api import *


@allure.severity('Normal')
def test_case11():
    """
        服务导入新增
    """
    count_data = 2
    import_data = get_import_data(count_data)
    form_id = get_form_id()

    re_body_analysis = common_data(form_id, import_data, "1")
    result_analysis = send_request(method, url, headers=headers(), data=action_body(__file__, re_body_analysis))  # 分析数据第一次请求
    re_json_analysis = result_analysis.json()
    success_assert(result_analysis.status_code, re_json_analysis['result'])

    re_body_analysis_2 = common_data_sec(form_id)
    result_analysis_2 = send_request(method, url, headers=headers(), data=re_body_analysis_2)  # 分析数据第二次请求
    re_json_analysis_2 = result_analysis_2.json()
    success_assert(result_analysis_2.status_code, re_json_analysis_2['result'])
    assert_analysis_data(re_json_analysis_2, count_data)  # 对分析结果进行校验

    re_body_im = common_data(form_id, import_data, "2")
    result_im = send_request(method, url, headers=headers(), data=action_body(__file__, re_body_im))  # 导入数据第一次请求
    re_json_im = result_im.json()
    success_assert(result_im.status_code, re_json_im['result'])

    re_body_im2 = common_data_sec(form_id)
    result_im2 = send_request(method, url, headers=headers(), data=re_body_im2) # 导入数据第二次请求
    re_json_im2 = result_im2.json()
    success_assert(result_im2.status_code, re_json_im2['result'])
    assert_analysis_data(re_json_analysis_2, count_data)  # 对导入结果进行校验




