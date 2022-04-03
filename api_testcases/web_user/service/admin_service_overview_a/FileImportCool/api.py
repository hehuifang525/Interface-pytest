
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


def common_data(form_id, import_data: list, import_analysis: str):
    """
    创建服务导入分析请求body

    :param form_id: 导入的文件id
    :param import_data: 导入的数据列表
    :param import_analysis: 1:导入分析  2：导入数据

    """
    # form_id = get_form_id()
    data_body =  {"ObjectBackend": "ServiceCool",
                  "ImportAnalysis": import_analysis,
                  "FileType": "Excel",
                  "Headline": ["Name", "Valid", "InternalComments", "ExternalComments"],
                  "ImportData": import_data,
                  "FormID": form_id, "RowCount": str(len(import_data)), "data": {}}
    return data_body


def common_data_sec(form_id):
    """
    封装分析，导入执行后的二次请求body
    :param form_id: 导入的文件id
    """
    data_body = {
        "Subaction": "ImportResultGetCool",
        "data": '{"FormID":"'+str(form_id)+'","ObjectBackend":"ServiceCool"}',
        "Action": "admin_service_overview_a"}
    return data_body