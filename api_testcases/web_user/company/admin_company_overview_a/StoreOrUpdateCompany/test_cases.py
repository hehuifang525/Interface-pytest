import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_value,config_read
from .api import *
from .function import *
from api_testcases.web_user.district.admin_district_overview_a.Save.test_cases import add_district_commom


@pytest.mark.run(order=1)
@allure.severity('Blocker')
def test_init_add_company():
    """
    进入客户用户管理-填写必填添加客户
    """
    company_name = "%s-%s" % ('name', get_datetime())
    company_id = "%s-%s" % ('ID', get_datetime())
    data_body = common_data(company_id, company_name)

    re_body = {"CustomerID":"All", "DetailAction": "AddSubCompany", "data": base64_encode_value(data_body)}

    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    assert re_json["data"]["data"]["id"] == company_id, "接口返回的客户id"
    # 创建客户成功后，将客户编号、名称写入config
    config_write("company", "customerid", company_id)
    config_write("company", "companyname", company_name)

    # 调用区域，增加一个区域
    add_district_commom()


@allure.severity('Normal')
def test_add_full_company():
    """
    进入客户用户管理-填写全填添加客户
    """
    company_name = "%s-%s" % ('name', get_datetime())
    company_id = "%s-%s" % ('ID', get_datetime())

    # 取父客户、区域
    parent_customer_id = config_read("company","customerid")
    company_district = config_read("district","districtid")
    data_body = common_data(company_id, company_name, "1", parent_customer_id, company_district, "China")

    re_body = {"CustomerID": "All", "DetailAction": "AddSubCompany", "data": base64_encode_value(data_body)}

    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    assert re_json["data"]["data"]["id"] == company_id, "接口返回的客户id"

    # 对填入的数据进行校验
    parent_customer_name = mysql_get_value("customer_company", "name", "customer_id", parent_customer_id)

    assert_input_value(company_id, "street", "南湖", "街道校验")
    assert_input_value(company_id, "parent_customer_id", parent_customer_name+"::"+company_name, "父部门校验")
    assert_input_value(company_id, "district", company_district, "区域校验")
    assert_input_value(company_id, "zip", "532201", "邮编校验")
    assert_input_value(company_id, "city", "新疆", "城市校验")
    assert_input_value(company_id, "country","China", "国家校验")
    assert_input_value(company_id, "url", "http://www.ceshi.com", "网址校验")
    assert_input_value(company_id, "comments",  "设置备注", "备注校验")
    assert_input_value(company_id, "valid_id",  "1", "有效性校验")


@allure.severity('Normal')
def test_edit_company():
    """
    进入客户用户管理-编辑客户除父客户、区域外的所有字段，再清空所有非必填
    """
    company_id = config_read("company", "customerid")
    company_name = config_read("company", "companyname")
    data_body = common_data(company_id, company_name, "1", None, None, "Colombia",
                            "南宁", "http://re1.com", "街道", "备注edit", "530000")

    re_body = {"CustomerID": company_id, "DetailAction": "EditCompany", "data": base64_encode_value(data_body),
               "CustomerCompanyID": company_id}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    # print(re_json)
    success_assert(result.status_code,re_json["result"])
    # 错误返回id=1
    # assert re_json["data"]["data"]["id"] == company_id + "ces", "接口返回的客户id"
    assert_input_value(company_id, "street", "街道", "街道校验")
    assert_input_value(company_id, "zip", "530000", "邮编校验")
    assert_input_value(company_id, "city", "南宁", "城市校验")
    assert_input_value(company_id, "country","Colombia", "国家校验")
    assert_input_value(company_id, "url", "http://re1.com", "网址校验")
    assert_input_value(company_id, "comments",  "备注edit", "备注校验")
    # assert_input_value(company_id, "valid_id",  "1", "有效性校验")

    # 编辑-将非必填清空
    data_body = common_data(company_id, company_name, "1", None, None, None, None,
                            None, None, None, None)
    re_body = {"CustomerID": company_id, "DetailAction": "EditCompany", "data": base64_encode_value(data_body),
               "CustomerCompanyID": company_id}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    # assert re_json["data"]["data"]["id"] == company_id, "接口返回的客户id"
    assert_input_value(company_id, "street", "", "街道校验")
    assert_input_value(company_id, "zip", "", "邮编校验")
    assert_input_value(company_id, "city", "", "城市校验")
    assert_input_value(company_id, "country", "", "国家校验")
    assert_input_value(company_id, "url", "", "网址校验")
    assert_input_value(company_id, "comments", "", "备注校验")


def add_company_common():
    """
    添加客户公共用例
    """
    company_name = "%s-%s" % ('name', get_datetime())
    company_id = "%s-%s" % ('ID', get_datetime())
    data_body = common_data(company_id, company_name)

    re_body = {"CustomerID":"All", "DetailAction": "AddSubCompany", "data": base64_encode_value(data_body)}

    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    assert re_json["data"]["data"]["id"] == company_id, "接口返回的客户id"
    company_info = {"CompanyName": company_name, "CompanyID": company_id}
    return company_info








