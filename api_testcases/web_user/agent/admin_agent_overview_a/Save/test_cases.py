import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_all,get_moblie_number
from .api import *


@allure.severity('Blocker')
def test_add_user():
    """
    进入服务人员-必填添加服务人员
    """
    user_login = "%s-%s" % ('user', get_datetime())
    re_body = {"UserID":"","data":common_data(user_login)}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    assert re_json["data"]["message"] == "Successfuly add", "添加成功提示"
    assert re_json["data"]["data"]["UserID"] == mysql_get_value("users", "id", "login", user_login), "返回的userid与数据库id校验"


@pytest.mark.run(order=1)
@allure.severity('Critical')
def test_init_add_full_user():
    """
    初始化用例
    进入服务人员界面-填写全填增加服务人员
    同时作为初始化用例，执行后写入用户账号、手机号、邮箱号、工号
    """
    user_login = "%s-%s" % ('user', get_datetime())
    user_mobile = get_moblie_number("137")
    user_email = user_mobile + "@qq.com"
    job_number = user_mobile + "gh"
    re_body = {"UserID":"","data":common_data(user_login,"",user_email,user_mobile,"1","123",job_number)}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    assert re_json["data"]["message"] == "Successfuly add", "添加成功提示"
    assert re_json["data"]["data"]["UserID"] == mysql_get_value("users", "id", "login", user_login), "返回的userid与数据库id校验"

    # 全填成功后将创建的服务人员写入config
    user_id = re_json["data"]["data"]["UserID"]
    config_write("user_normal_init", "userlogin", user_login)
    config_write("user_normal_init", "useremail", user_email)
    config_write("user_normal_init", "usermobile", user_mobile)
    config_write("user_normal_init", "job_number", job_number)
    config_write("user_normal_init", "user_id", user_id)


@allure.severity('Critical')
def test_edit_user():
    """
    编辑服务人员
    """
    # 必填创建一个服务人员
    user_login = "%s-%s" % ('user', get_datetime())
    re_body = {"UserID": "", "data": common_data(user_login)}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    assert re_json["data"]["message"] == "Successfuly add", "添加成功提示"
    assert re_json["data"]["data"]["UserID"] == mysql_get_value("users", "id", "login", user_login), "返回的userid与数据库id校验"

    # 编辑填写非必填信息（除密码）
    user_id = re_json["data"]["data"]["UserID"]
    user_mobile = get_moblie_number("139")
    user_email = user_mobile + "@qq.com"
    job_number = user_mobile + "gh"
    re_body = {"UserID": user_id,
               "data": common_data(user_login, user_id, user_email, user_mobile, job_number=job_number, user_city="上海", user_title="填写非必填字段")}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    #   取数据库数据校验（除密码）
    assert_input_value(user_id, "job_number", job_number, "工号编辑校验")
    assert_input_value(user_id, "mobile", user_mobile, "手机号校验")
    assert_input_value(user_id, "email", user_email, "邮件地址校验")
    assert_input_value(user_id, "city", "上海", "城市校验")
    assert_input_value(user_id, "title", "填写非必填字段", "标题或问候语校验")

    # 编辑必填信息(除有效性)
    user_login_edit = "%s%s" % ('user', get_datetime())
    re_body = {"UserID": user_id,
               "data": common_data(user_login_edit, user_id, user_firstname="自动",user_lastname="赵",user_fullname="赵自动")}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    #   取数据库数据校验(除有效性)
    assert_input_value(user_id, "login", user_login_edit, "账号编辑校验")
    assert_input_value(user_id, "first_name", "自动", "名校验")
    assert_input_value(user_id, "last_name", "赵", "姓校验")
    assert_input_value(user_id, "full_name", "赵自动", "全名校验")


def add_full_user_commom():
    """
    进入服务人员界面-填写全填增加服务人员
    return 返回账号、邮箱、手机号、工号
    """
    user_login = "%s-%s" % ('user', get_datetime())
    # print(user_login)
    user_mobile = get_moblie_number("137")
    user_email = user_mobile + "@qq.com"
    job_number = user_mobile + "gh"
    re_body = {"UserID":"","data":common_data(user_login,"",user_email,user_mobile,"1","123",job_number)}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    success_assert(result.status_code, re_json["result"])
    assert re_json["data"]["message"] == "Successfuly add", "添加成功提示"
    assert re_json["data"]["data"]["UserID"] == mysql_get_value("users", "id", "login", user_login), "返回的userid与数据库id校验"
    user_info = {"login":user_login,"mobile":user_mobile,"email":user_email, "jobnumber": job_number}
    return user_info


# def add_user_commom():
#     """
#     进入服务人员界面-填写必填增加服务人员,公共用例
#     return 返回账号
#     """
#     user_login = "%s-%s" % ('user', get_datetime())
#     re_body = {"UserID":"","data":common_data(user_login,"")}
#     result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
#     re_json = result.json()
#     success_assert(result.status_code, re_json["result"])
#     success_assert(result.status_code, re_json["result"])
#     assert re_json["data"]["message"] == "Successfuly add", "添加成功提示"
#     assert re_json["data"]["data"]["UserID"] == mysql_get_value("users", "id", "login", user_login), "返回的userid与数据库id校验"
#     user_info = {"login_id":re_json["data"]["data"]["UserID"],"login":user_login}
#     return user_info


# @allure.severity('Critical')
# def test_search_user():
#     """
#     进入服务人员-右侧搜索服务人员,未完成，需要补充，搜索后未能返回正确的搜索数据，需检查
#     """
#     re_body = {"Subaction":"", "data":{"SearchName": "特殊色所所所所", "Filter":"Invalid"}, "Action":"admin_agent_overview_a"}
#     result = send_request(method, url, headers=headers(), data=re_body)
#     re_json = result.json()
#     success_assert(result.status_code, re_json["result"])
#     TEST001 = len(re_json["data"]["OverviewList"])
#     print(re_json["data"]["OverviewList"])
#     # # print(len(re_json["data"]["OverviewList"]))
#     # assert re_json["data"]["OverviewList"][0]["UserLogin"] == "root@localhost", "搜索返回结果校验"

