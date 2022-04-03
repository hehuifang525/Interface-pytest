import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert, mysql_get_value, mysql_get_list,mysql


@allure.severity('Normal')
def test_all_num():
    """
        获取全部数据服务，检查有效数据与无效数据
    """
    re_body = {"Filter": ""}

    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    # 查询数据库有效数据
    invalid_count_db = mysql_get_value("service","COUNT(*) AS num","valid_id","2")
    valid_count_db = mysql_get_value("service","COUNT(*) AS num","valid_id","1")
    # 取返回的请求数据对比 InvalidCount
    InvalidCount = re_json["data"]["InvalidCount"]
    ValidCount = re_json["data"]["ValidCount"]
    success_assert(result.status_code, re_json['result'])
    assert int(invalid_count_db) == InvalidCount, '无效数据校验'
    assert int(valid_count_db) == ValidCount, "有效数据校验"

    # 循环解包
    service_info = mysql.get_value("service", "id ,name,short_name,valid_id,change_time,create_time,is_leaf ,comments",
                                 "","", "valid_id is not null")

    for j in service_info:
        service_id, name, short_name, valid_id, change_time, create_time, is_leaf, comments = j  # 解包-查询数据库
        # 返回数据中有效性以及名称对比
        if valid_id == "1":  # 有效
            for i in re_json["data"]["ValidList"]:
                if i["ServiceID"] == str(service_id):
                    assert i["Name"] == name, "名称校验"
                    assert i["Valid"] == "valid", "有效性名称校验"
                    assert i["ServiceID"] == str(service_id), "服务id"
                    assert i["ChangeTime"] == str(change_time), "更新时间"
                    assert i["CreateTime"] == str(create_time), "创建时间"
                    # assert i["ServiceID"] == str(service_id), "服务id"
                    assert i["ShortName"] == short_name, "短名称"
                    assert i["isLeaf"] == str(is_leaf)
                    if i["Comments"]:  # 备注不为空则校验
                        assert i["Comments"] in comments, "备注校验"
        else:  # 无效
            for i in re_json["data"]["InvalidList"]:   # i 遍历请求返回的数据  --字典
                if i["ServiceID"] == str(service_id):
                    assert i["Name"] == name, "名称校验"
                    assert i["Valid"] == "invalid", "有效性名称校验"
                    assert i["ChangeTime"] == str(change_time), "更新时间"
                    assert i["CreateTime"] == str(create_time), "创建时间"
                    # assert i["ServiceID"] == str(service_id), "服务id"
                    assert i["ShortName"] == short_name, "短名称"
                    assert i["isLeaf"] == str(is_leaf)
                    if i["Comments"]:  # 备注不为空则校验
                        assert i["Comments"] in comments, "备注校验"


@allure.severity('Normal')
@pytest.mark.parametrize("valid", [{"valid_id": "1","count":"ValidCount","list":"ValidList","opposite_count":"InvalidCount"},
                                    {"valid_id": "2","count":"InvalidCount","list":"InvalidList","opposite_count":"ValidCount"}])
def test_search_appoint(valid):
    """
            查询指定一条有效/无效数据
    """
    # 查询一条有效/无效数据
    name_db = mysql_get_value("service", "name", "valid_id", valid["valid_id"])
    service_info =  mysql.get_value("service", "id ,name,short_name,valid_id,change_time,create_time,is_leaf ,comments", "name", name_db)
    service_id, name, short_name, valid_id, change_time, create_time,is_leaf, comments = service_info[0]  # 解包

    re_body = {"Filter": name_db}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    # 取返回的请求有效无效数量
    success_assert(result.status_code, re_json['result'])
    assert re_json["data"][valid["count"]] == 1, '数量校验'
    assert re_json["data"][valid["opposite_count"]] == 0, '数量校验'

    if valid["valid_id"]=="1":
        valid_name = "valid"
    else:
        valid_name = "invalid"

    # 返回数据中有效性以及名称对比
    for i in re_json["data"][valid["list"]]:
        assert i["Name"] == name_db, "名称校验"
        assert i["ValidID"] == str(valid["valid_id"]), "有效性id校验"
        assert i["Valid"] == valid_name, "有效性名称校验"
        assert i["ChangeTime"] == str(change_time), "更新时间"
        assert i["CreateTime"] == str(create_time), "创建时间"
        assert i["ServiceID"] == str(service_id), "服务id"
        assert i["ShortName"] == short_name, "短名称"
        assert i["isLeaf"] == str(is_leaf)
        if i["Comments"]:  # 备注不为空则校验
            assert i["Comments"] in comments, "备注校验"






