import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_all, mysql_get_list,mysql_get_value


@allure.severity('normal')
# 已知bug
@pytest.mark.xfail
def test_all_user():
    """
     按角色查询数据-左侧角色列表点击全部
    """
    re_body ={"Filter":"Valid","QueueID":"All"}
    result = send_request(method, url, headers=headers(), data=action_body(__file__,re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    # 取请求返回的有效，无效记录数
    invalid_list = len(re_json["data"]["TableData"]["InvalidList"])
    overview_list = len(re_json["data"]["TableData"]["OverviewList"])
    # 查询数据库有效记录数
    valid_users_db = len(mysql_get_list("users", "id", "valid_id", "1"))
    # 查询数据库无效记录数
    invalid_users_db = len(mysql_get_list("users", "id", "valid_id", "1"))
    assert overview_list == valid_users_db, "点击全部角色，有效tab显示错误"
    assert invalid_list == invalid_users_db, "点击全部角色，无效tab显示错误"


@allure.severity('normal')
def test_appoint_queue():
    """
     按角色查询数据-左侧角色列表点击指定角色显示
    """
    # 查询数据库，找出一条角色记录
    # 查询有效/无效tab
    valid_users_db = mysql_get_list("users", "id", "valid_id", "1")
    invalid_users_db = mysql_get_list("users", "id", "valid_id", "2")
    queue_id = ""
    for i in range(0, len(valid_users_db)):
        valid_users_db_list = mysql_get_list("queue_user", "queue_id", "user_id", valid_users_db[i])
        if valid_users_db_list != None:
            queue_id = valid_users_db[0]
            break
    # queue_id 数据库查询指定角色对应的有效user列表，无效user列表
    appoint_invalid_users_db = []    # 指定角色无效user，列表初始化
    appoint_valid_users_db = []    # 指定角色有效user，列表初始化
    # 指定queue_id，查询queue_user，返回usersid
    appoint_queue_user_list_db = mysql_get_list("queue_user", "user_id", "queue_id", queue_id)
    for i in range(0, len(appoint_queue_user_list_db)):
        if appoint_queue_user_list_db[i] in valid_users_db:
            appoint_valid_users_db.append(str(appoint_queue_user_list_db[i]))
        elif appoint_queue_user_list_db[i] in invalid_users_db:
            appoint_invalid_users_db.append(str(appoint_queue_user_list_db[i]))

    re_body ={"Filter":"Valid","QueueID": queue_id}
    # print(queue_id, "查询的角色id")
    result = send_request(method, url, headers=headers(), data=action_body(__file__,re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    # 无效记录初始化
    invalid_list=[]
    # 有效记录初始化
    overview_list=[]
    for i in range(0,len(re_json["data"]["TableData"]["OverviewList"])):
        overview_list.append(re_json["data"]["TableData"]["OverviewList"][i].get("UserID"))

    for i in range(0,len(re_json["data"]["TableData"]["InvalidList"])):
        invalid_list.append(re_json["data"]["TableData"]["InvalidList"][i].get("UserID"))

    # print(invalid_list,overview_list)
    # print("cesjo ",appoint_invalid_users_db,appoint_valid_users_db)
    for i in range(0, len(overview_list)):
        assert overview_list[i] in appoint_valid_users_db ,"左侧指定角色点击，有效列表显示错误"

    for i in range(0, len(invalid_list)):
        assert invalid_list[i] in appoint_invalid_users_db ,"左侧指定角色点击，无效列表显示错误"











