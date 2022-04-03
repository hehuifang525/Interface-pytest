
from base.common import send_request, success_assert, get_datetime, config_get_section_value, mysql
from api_testcases.web_user.action_re_body import *

#
# def assert_commom(re_json, valid):
#     """
#     创建取数据后，对数据库字段进行校验
#
#     :param re_json: 请求返回值
#     :param valid: 有效性
#     """
#     service_info = mysql.get_value("service", "id ,name,short_name,valid_id,change_time,create_time,is_leaf ,comments",
#                                    "name", name_db)
#     service_id, name, short_name, valid_id, change_time, create_time, is_leaf, comments = service_info[0]  # 解包
#
#     if valid["valid_id"] == "1":
#         valid_name = "valid"
#     else:
#         valid_name = "invalid"
#
#         # 返回数据中有效性以及名称对比
#     for i in re_json["data"][valid["list"]]:
#         assert i["Name"] == name_db, "名称校验"
#         assert i["ValidID"] == str(valid["valid_id"]), "有效性id校验"
#         assert i["Valid"] == valid_name, "有效性名称校验"
#         assert i["ChangeTime"] == str(change_time), "更新时间"
#         assert i["CreateTime"] == str(create_time), "创建时间"
#         assert i["ServiceID"] == str(service_id), "服务id"
#         assert i["ShortName"] == short_name, "短名称"
#         assert i["isLeaf"] == str(is_leaf)
#         if i["Comments"]:  # 备注不为空则校验
#             assert i["Comments"] in comments, "备注校验"
#
#
