from base.common import mysql_get_value, config_write,mysql
import re


def assert_db(re_json, service_name, externalComments=None, internalComments=None):
    """
        校验数据库值
        :param re_json: 返回的json
        :param service_name: 服务名称
        :param externalComments: 外部备注
        :param internalComments: 内部备注
    """
    service_db = mysql.get_value("service", "id,short_name,type_id,criticality,valid_id,comments", "name", service_name, "")
    assert len(service_db) == 1, "添加成功的数据库个数校验"
    service_id,short_name,type_id,criticality,valid_id ,comments = service_db[0]  # 解包
    assert str(re_json["data"]["data"]["id"]) == str(service_id), "添加成功后返回的服务id校验"
    assert str(re_json["data"]["JustaddServiceID"]) == str(service_id),  "添加成功后返回的服务id校验"
    assert service_name == short_name,  "校验数据库中short_name"
    assert type_id == 4,  "校验数据库中type_id"
    assert criticality == "3 normal",  "校验数据库中criticality"
    assert valid_id == 1,  "校验数据库中valid_id"

    internal_comments_re = re.compile(r'"InternalComments":"(?P<internal_comments>.*?)"}', re.S)  # 正则取内部备注
    external_comments_re = re.compile(r'"ExternalComments":"(?P<ExternalComments>.*?)",', re.S)  # 正则取外部备注

    if externalComments:
        for y in external_comments_re.finditer(comments):
            external_comments_db = y.groups("ExternalComments")[0]
            assert externalComments == external_comments_db
    if internalComments:
        for x in internal_comments_re.finditer(comments):
            internal_comments_db = x.groups("InternalComments")[0]
            assert internalComments == internal_comments_db

