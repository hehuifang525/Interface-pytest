
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_all
import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert


def get_form_id():
    """
    进入服务界面
    return FormID
    """

    re_body = {"Subaction": "ImportExportOverview",
               "Action": "admin_service_overview_a"}
    result = send_request(method, url, headers=headers(), data=re_body)
    re_json = result.json()
    form_id = re_json["data"]["ImportExport"]["Import"]["FormID"]   # 取FormID
    success_assert(result.status_code, re_json["result"])
    return form_id


def common_data(valid="1", export_filter=None):
    """
    创建客户用户请求body

    :param valid: 有效性
    :param export_filter: 过滤项
    """
    form_id = get_form_id()
    data_body = {
                    "ObjectBackend": "ServiceCool",
                    "FormID": form_id,
                    "data": {"FileType": "Excel", "ExportFilter": export_filter, "Valid": valid}}

    return data_body


