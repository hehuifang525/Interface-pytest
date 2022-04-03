import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_all,config_read,fail_assert
from base.Mysql import Mysql
from .api import *
from time import sleep


@pytest.mark.run(order=1)
@allure.severity('Blocker')
def test_init_add_faq_category():
    """
    填写必填增加知识库类别
    """

    faq_category_name = "%s-%s" % ('faqc', get_datetime())  # 随机生成名称
    data_body = common_data(faq_category_name)

    re_body = {"CategoryID":"","data": base64_encode_all(data_body)}

    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    category_id = mysql_get_value("faq_category", "id", "NAME", faq_category_name, "")
    success_assert(result.status_code, re_json["result"])
    common_assert(faq_category_name, re_json)

    # 添加成功后，查询区域id，向config中写入分类id、名称
    config_write("faq_category", "CategoryID", category_id)
    config_write("faq_category", "name", faq_category_name)


@allure.severity('Normal')
@pytest.mark.parametrize('faq_category_name', [''])
@pytest.mark.parametrize('valid_id', ['1', ''])
def test_required(faq_category_name,valid_id):
    """
    知识库类别必填校验:名称、有效性
    """

    data_body = common_data(faq_category_name, valid_id=valid_id)
    re_body = {"CategoryID": "", "data": base64_encode_all(data_body)}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    fail_assert(result.status_code, re_json, 'Add Failed')


@allure.severity('Normal')
def test_check_repeat():
    """
    知识库类别同名校验
    """
    # 取当前config预置数据
    faq_category_name = config_read("faq_category", "name")
    # 判断当前系统中是不是有这个数据，有则直接校验重复，无责新增一个
    faq_category_name_db_num = mysql_get_value("faq_category", "id", "NAME", faq_category_name, "")
    if not faq_category_name_db_num:
        faq_category_info = add_faq_category_commom()
        faq_category_name = faq_category_info["name"]
    data_body = common_data(faq_category_name)
    re_body = {"CategoryID": "", "data": base64_encode_all(data_body)}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    fail_assert(result.status_code, re_json, 'This category already exists')


def add_faq_category_commom():
    """
    填写必填增加知识库类别,公共用例
    """

    faq_category_name = "%s-%s" % ('faqc', get_datetime())  # 随机生成名称
    data_body = common_data(faq_category_name)

    re_body = {"CategoryID":"","data": base64_encode_all(data_body)}

    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    category_id = mysql_get_value("faq_category", "id", "NAME", faq_category_name, "")
    success_assert(result.status_code, re_json["result"])

    # 添加成功后，查询区域id，向config中写入分类id、名称
    config_write("faq_category", "CategoryID", category_id)
    config_write("faq_category", "name", faq_category_name)
    faq_category_info = {"CategoryID": category_id, "name":faq_category_name}
    return faq_category_info
