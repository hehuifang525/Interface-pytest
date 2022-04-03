import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_all,config_read
# from api_testcases.web_user.agent.admin_agent_overview_a.Save.test_cases import add_user_commom
from base.common import mysql_get_value,mysql_get_list


@allure.severity('Normal')
def test_link_one_queue():
    """
    关联角色-单个角色
    """
    user_id = config_read("user_normal_init", "user_id")
    # 数据库中查询第一条有效的角色记录
    queue_id = mysql_get_value("queue", "id", "valid_id", "1")
    re_body = {"UserID":user_id,"data":{"UserQueue":[queue_id]}}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    assert re_json["data"]["message"] == "Successfuly add", "服务人员关联角色成功提示"

    # 查询数据库
    actual_queue_id = mysql_get_value("queue_user", "queue_id", "user_id", user_id)
    assert actual_queue_id == queue_id, "服务人员关联角色数据库校验"


@allure.severity('Normal')
def test_link_more_queue():
    """
    关联角色-多个角色
    """
    user_id = config_read("user_normal_init", "user_id")
    # 数据库中查询有效的角色记录
    queue_id = mysql_get_list("queue", "id", "valid_id", "1")
    re_body = {"UserID":user_id,"data":{"UserQueue":[queue_id[0],queue_id[1],queue_id[3]]}}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    assert re_json["data"]["message"] == "Successfuly add", "服务人员关联角色成功提示"

    # 查询数据库
    actual_queue_id = mysql_get_list("queue_user", "queue_id", "user_id", user_id)
    assert actual_queue_id == [queue_id[0],queue_id[1],queue_id[3]], "服务人员关联角色数据库校验"













