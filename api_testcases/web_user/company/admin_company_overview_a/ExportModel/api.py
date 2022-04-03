
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_all
import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert


def get_form_id():
    """
    进入客户用户导入导出页面
    return FormID
    """

    re_body={"Subaction":"ImportExportOverview",
             "Action":"admin_company_overview_a"}
    result = send_request(method, url, headers=headers(), data=re_body)
    re_json = result.json()
    # 取FormID
    form_id = re_json["data"]["ImportExport"]["FormID"]
    success_assert(result.status_code, re_json["result"])
    return form_id