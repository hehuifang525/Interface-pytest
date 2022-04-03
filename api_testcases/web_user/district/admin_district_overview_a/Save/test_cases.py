import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_all,config_read
from .api import *
from base.Mysql import Mysql
from time import sleep


@pytest.mark.run(order=2)
@allure.severity('Blocker')
def test_init_add_district():
    """
    进入区域-填写必填增加区域
    """

    district_name = "%s-%s" % ('dis', get_datetime())  # 随机生成区域名称
    data_body = common_data(district_name)

    re_body = {"DistrictID":"","data": data_body}

    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    assert re_json["data"]["message"] == "Successfuly Add", "添加成功提示"
    # 添加成功后，查询区域id，向config中写入区域id
    districtid = mysql_get_value("district", "id", "NAME", district_name, "")
    config_write("district", "districtid", districtid)
    config_write("district", "districtname", district_name)


@allure.severity('Critical')
def test_add_full_district():
    """
    进入区域-填写全增加区域
    """

    district_name = "%s-%s" % ('dis', get_datetime())  # 随机生成区域名称
    parent_district_id = config_read("district", "districtid")
    parent_district_name = config_read("district", "districtname")
    data_body = common_data(district_name, parent_district_id, "1", "区域备注2021通过pytest")
    re_body = {"DistrictID": parent_district_id,"data": data_body}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    assert re_json["data"]["message"] == "Successfuly Add", "添加成功提示"

    district_name_db = parent_district_name+"::" + district_name
    district_id = mysql_get_value("district", "id", "NAME", district_name_db)
    valid_id = mysql_get_value("district", "valid_id", "id", district_id)
    comments = mysql_get_value("district", "comments", "id", district_id)
    assert valid_id == "1", "有效性校验"
    assert comments == "区域备注2021通过pytest", "备注信息校验"


@allure.severity('Normal')
def test_edit_district():
    """
    进入区域-编辑除父区域外的所以字段，再编辑清空非必填字段(预置的区域无父区域)
    """

    district_id = config_read("district", "districtid")
    district_name = config_read("district", "districtname")

    # 编辑1-编辑除父区域外的所有字段
    data_body = common_data(district_name+'edit', None, "2", "修改无效备注", district_id)
    re_body = {"DistrictID": district_id, "data": data_body}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    success_assert(result.status_code, re_json["result"])
    assert re_json["data"]["message"] == "Successfuly Add", "添加成功提示"
    district_id = mysql_get_value("district", "id", "NAME", district_name+'edit')
    valid_id = mysql_get_value("district", "valid_id", "id", district_id)
    comments = mysql_get_value("district", "comments", "id", district_id)
    assert valid_id == "2", "有效性校验"
    assert comments == "修改无效备注", "备注信息校验"

    # 编辑2-清空非必填
    data_body_null = common_data(district_name, None, 1, None, district_id)
    re_body_null = {"DistrictID": district_id, "data": data_body_null}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body_null))
    re_json_null = result.json()
    success_assert(result.status_code, re_json_null["result"])
    assert re_json_null["data"]["message"] == "Successfuly Add", "添加成功提示"

    district_id_null = mysql_get_value("district", "id", "NAME", district_name)
    valid_id_null = mysql_get_value("district", "valid_id", "id", district_id_null)
    comments_null = mysql_get_value("district", "comments", "id", district_id_null)
    assert valid_id_null == "1", "有有效性校验"
    assert comments_null == "", "备注信息校验"


def add_district_commom():
    """
    进入区域-填写必填增加区域
    return  以字典形式返回区域名称：districtname,区域id：districtid
    """
    districtname = "%s-%s" % ('dis', get_datetime())  # 随机生成区域名称
    data_body = common_data(districtname)
    re_body = {"DistrictID":"","data": data_body}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    assert result.status_code == 200, "接口请求成功标识"
    assert re_json["result"] == 1, "数据添加成功标识"
    assert re_json["data"]["message"] == "Successfuly Add", "添加成功提示"
    # 返回区域id
    districtid = mysql_get_value("district", "id", "NAME", districtname, "")
    district_info = {"districtname": districtname,"districtid": districtid}
    return district_info








