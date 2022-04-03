import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_all
from .api import *


@allure.severity('Critical')
@pytest.mark.parametrize('export_object', ['CustomerCompany', 'CustomerUser'])
@pytest.mark.parametrize('valid', ['1', '2', '5'])
def test_export_company(export_object, valid):
    """
    进入客户用户页面,导出客户、用户,有效性（全部、无效、有效）
    :param export_object: 导出过滤客户/用户
    :param valid: 导出有效性

    """
    form_id = get_form_id()

    if export_object == 'CustomerCompany':
        export_type = "Company"
    else:
        export_type = "Customer"
    re_body ={"ObjectBackend": export_object,"data": {"FileType": "Excel","ExportAttribute": None,"ExportType": export_type,"Valid": valid},
              "FormID": form_id}
    result = send_request(method, url, headers=headers(), data=action_body(__file__,re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])


@allure.severity('Normal')
def test_export_company_col():
    """
    指定导出字段，导出客户

    """
    form_id = get_form_id()

    re_body ={"ObjectBackend": 'CustomerCompany',"data": {"FileType": "Excel","ExportAttribute":
             ["CustomerID","CustomerCompanyName", "CustomerCompanyCity","CustomerCompanyURL","ParentCustomerCompanyName"],
                                                          "ExportType": "Company","Valid": "1"},"FormID": form_id}
    result = send_request(method, url, headers=headers(), data=action_body(__file__,re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])


@allure.severity('Normal')
def test_export_customer_col():
    """
    指定导出字段，导出客户用户

    """
    form_id = get_form_id()
    re_body ={"ObjectBackend": "CustomerUser", "data": {"FileType": "Excel","ExportAttribute":
             ["UserCustomerID","CustomerCompany","UserFullname","UserLastname"],"ExportType": "Customer", "Valid": "1"},
              "FormID": form_id}
    result = send_request(method, url, headers=headers(), data=action_body(__file__,re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])







