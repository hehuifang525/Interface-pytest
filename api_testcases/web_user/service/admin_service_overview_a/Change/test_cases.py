import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert, mysql_get_value, mysql_get_list


@allure.severity('Normal')
@pytest.mark.parametrize("field_type",[{"type":"service","table":"service","select_field":"id"},
                                       {"type":"SLA","table":"sla","select_field":"id"},
                                       {"type":"ServiceLinkCompany","table":"customer_company","select_field":"customer_id"}
                                      ])
def test_drop_down(field_type):
    """
        检查新增界面中，父级服务，服务水平协议、客户下拉数据值,预期应显示有效性
    """
    re_body = {"IsLeaf":"AddService"}
    
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
    
    success_assert(result.status_code, re_json['result'])

    list_db = mysql_get_list(field_type["table"], field_type["select_field"], "valid_id", "1")
    re_ser_list=[]
    if field_type["type"] != "service":
        re_ser_list = list(dict(re_json['data']['serviceLinkObject']['fieldData'][field_type["type"]]['options']).keys())
    if field_type["type"] == "service":
        re_ser_list.clear()
        re_ser_list = list(dict(re_json['data']['ServiceInfo']['ChildrenService']['options']).keys())
        assert re_json['data']['ServiceInfo']['ChildrenService']['default'] == "", "默认值校验"
        assert re_json['data']['ServiceInfo']['ChildrenService']['display'] == "1", "显示校验"
        assert re_json['data']['ServiceInfo']['ChildrenService']['label'] == "Belongs to", "标签校验"
        assert re_json['data']['ServiceInfo']['ChildrenService']['name'] == "ChildrenService", "名称"
        assert re_json['data']['ServiceInfo']['ChildrenService']['promptCode'] == 2, "提示码校验"
        assert re_json['data']['ServiceInfo']['ChildrenService']['promptMessage'] == \
               "The service belong to which parent service", "提示信息校验"
        assert re_json['data']['ServiceInfo']['ChildrenService']['type'] == "TreeSelect", "字段类型校验"

    if field_type["type"] == "SLA":
        assert re_json['data']['serviceLinkObject']['fieldData']["SLA"]['default'] == "", "默认值校验"
        assert re_json['data']['serviceLinkObject']['fieldData']["SLA"]['display'] == "1", "显示标记校验"
        assert re_json['data']['serviceLinkObject']['fieldData']["SLA"]['label'] == "SLA", "标签名称校验"
        assert re_json['data']['serviceLinkObject']['fieldData']["SLA"]['multiple'] == 1, "多选标记校验"
        assert re_json['data']['serviceLinkObject']['fieldData']["SLA"]['name'] == "SLA", "名称校验"
        assert re_json['data']['serviceLinkObject']['fieldData']["SLA"]['type'] == "Dropdown", "类型校验"
        assert re_json['data']['serviceLinkObject']['fieldData']["SLA"]['promptCode'] == 2, "提示码"
        assert re_json['data']['serviceLinkObject']['fieldData']["SLA"]['promptMessage'] == \
               "If no parent service choose, It's parent service.", "提示信息"

    if field_type["type"] == "ServiceLinkCompany":
        # 客户用户校验
        assert re_json['data']['serviceLinkObject']['fieldData']["ServiceLinkCompany"]['default'] == "", "，默认值校验"
        assert re_json['data']['serviceLinkObject']['fieldData']["ServiceLinkCompany"]['display'] == "1", "显示标记校验"
        assert re_json['data']['serviceLinkObject']['fieldData']["ServiceLinkCompany"]['label'] == "Customer Company", "标签名称校验"
        assert re_json['data']['serviceLinkObject']['fieldData']["ServiceLinkCompany"]['multiple'] == 1, "多选标记校验"
        assert re_json['data']['serviceLinkObject']['fieldData']["ServiceLinkCompany"]['name'] == "ServiceLinkCompany", "名称校验"
        assert re_json['data']['serviceLinkObject']['fieldData']["ServiceLinkCompany"]['type'] == "TreeSelect", "类型校验"
        assert re_json['data']['serviceLinkObject']['fieldData']["ServiceLinkCompany"]['placeholder'] == "", "占位符"
        assert re_json['data']['serviceLinkObject']['fieldData']["ServiceLinkCompany"]['promptCode'] == 2, "提示码"
        assert re_json['data']['serviceLinkObject']['fieldData']["ServiceLinkCompany"]['promptMessage'] == \
               "Set which company can use the service" ,"提示信息"
    assert sorted(re_ser_list) == sorted([str(i) for i in list_db]), "每一条数据id详细对比"


@allure.severity('Normal')
def test_drop_down_process():
    """
        检查服务管理界面中流程字段下拉显示，预期应显示有效性
    """
    re_body = {"IsLeaf": "AddService"}

    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])
    list_db = mysql_get_list("pm_process_c  a , pm_process_type_c b", "a.id", "","",
                             " a.process_type = b.id AND b.valid_id =1 AND a.state_entity_id = 'S1'")
    re_ser_list = list(dict(re_json['data']['serviceLinkObject']['fieldData']["Process"]['options']).keys())
    assert sorted(re_ser_list) == sorted([str(i) for i in list_db]), "每一条数据id详细对比"

    # 校验流程返回json的其他数据
    assert re_json['data']['serviceLinkObject']['fieldData']["Process"]['default'] == [],"，默认值校验"
    assert re_json['data']['serviceLinkObject']['fieldData']["Process"]['display'] == "1","显示标记校验"
    assert re_json['data']['serviceLinkObject']['fieldData']["Process"]['label'] == "Process", "标签名称校验"
    assert re_json['data']['serviceLinkObject']['fieldData']["Process"]['multiple'] == 1, "多选标记校验"
    assert re_json['data']['serviceLinkObject']['fieldData']["Process"]['name'] == "Process", "名称校验"
    assert re_json['data']['serviceLinkObject']['fieldData']["Process"]['type'] == "Dropdown", "类型校验"












