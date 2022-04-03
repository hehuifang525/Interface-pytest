from base.common import es, mysql, config_read, mysql_get_value, mysql_format_trans2, es_search_list, mysql_get_list,mysql
import re


def split_db_comments(db_export_list, location: int = 3):
    """
    拆分数据中comments，字段为内部备注，外部备注
    :param db_export_list: 查询sql
    :param location: 备注所在位置

    return  id  名称 有效性 内部备注 外部备注
    """
    internal_comments_re = re.compile(r'"InternalComments":"(?P<internal_comments>.*?)"}', re.S)  # 正则取内部备注
    external_comments_re = re.compile(r'"ExternalComments":"(?P<ExternalComments>.*?)",', re.S)  # 正则取外部备注
    for index, item in enumerate(db_export_list):  # 遍历每一条服务记录
        each_service = list(item)
        internal_comments = ""
        external_comments = ""
        for j_index, j_item in enumerate(each_service):  # 遍历记录中的每一个数据
            each_service[j_index] = str(j_item)
            if j_index == location:
                if j_item:  # j: str 备注{},备注不为空，则将备注进行拆分为内部备注外部备注
                    for x in internal_comments_re.finditer(j_item):
                        internal_comments = x.groups("InternalComments")[0]
                    for y in external_comments_re.finditer(j_item):
                        external_comments = y.groups("ExternalComments")[0]

        del each_service[location]  # 列表中删除数据库中查询出来的备注信息
        each_service.append(internal_comments)
        each_service.append(external_comments)
        db_export_list[index] = each_service

    return db_export_list


def get_table_head(re_json):
    """
    根据响应返回，取出表头数据
    """
    header_list = []
    for i in re_json["data"]["data"][0]:
        header_list.append(i['key'])

    return header_list


def check_export_data(valid: str, re_json):
    """
        对导出的数据艰进行检查：检查导出数据总数，导出的表头，导出的每一条记录

        :param valid: 有效性
        :param re_json: 请求返回


    """
    if valid == "5":
        valid_id = "(1,2)"
    else:
        valid_id = "("+valid+")"
    sql_s = "select id,NAME,case valid_id when '1' then 'valid' ELSE 'invalid' END  AS valid ,comments from service " \
            "where valid_id in {}".format(valid_id)
    db_export_list = split_db_comments(list(mysql.cursor_conn(sql_s)))
    re_list = list(re_json["data"]["data"])    # 取请求返回的记录
    del re_list[0]  # 删除第一条记录
    for index, item in enumerate(re_list):
        item = list(item)
        if len(item) == 3:
            item.append("")
            item.append("")
            re_list[index] = item

    assert len(db_export_list) == len(re_json["data"]["data"])-1, "导入记录总数与数据库数据对比"  # 断言总数

    # 断言导出的表头
    header_list = get_table_head(re_json)
    assert header_list == ["ServiceID","Name","Valid","InternalComments","ExternalComments"], '导出的表头断言'
    for each_db in db_export_list:        # db_export_list 为db中查询的数据 re_list 为请求中返回的数据
        assert each_db in re_list, " 遍历判断数据库中查询到的数据在请求返回中是否存在"


def check_export_col_data(re_json, export_filter, valid: str = "1"):
    """
        对指定字段导出的数据进行检查：
        已知错误，未屏蔽:当导出的备注信息值为空，excel显示会错位

        :param valid: 有效性
        :param export_filter: list 导出的具体字段
        :param re_json: 请求返回

    """
    if valid == "5":
        valid_id = "(1,2)"
    else:
        valid_id = "("+valid+")"
    sql_s = "select id, NAME,case valid_id when '1' then 'valid' ELSE 'invalid' END  AS valid ,comments from service " \
            "where valid_id in {}".format(valid_id)

    # 拆分备注
    db_export_list = split_db_comments(list(mysql.cursor_conn(sql_s)))
    # 对处理的数据进行处理，取出当前导出的列
    db_export_list02 = []

    for i in db_export_list:  # i:每一条服务值  id  名称 有效性 内部备注 外部备注
        db_export_list02_child = []
        if "Name" in export_filter:
            db_export_list02_child.append(i[1])
        if "InternalComments" in export_filter:
            db_export_list02_child.append(i[3])
        if "ExternalComments" in export_filter:
            db_export_list02_child.append(i[4])
        if "Valid" in export_filter:
            db_export_list02_child.append(i[2])
        db_export_list02.append(db_export_list02_child)

    # 处理请求
    re_list = list(re_json["data"]["data"])  # 取请求返回的记录
    del re_list[0]  # 删除第一条记录

    if len(export_filter) == 3:
        for index, item in enumerate(re_list):
            item = list(item)
            if len(item) == 1:
                item.append("")
                item.append("")
                re_list[index] = item

    assert len(db_export_list) == len(re_json["data"]["data"]) - 1, "导入记录总数与数据库数据对比"  # 断言总数

    # # 断言导出的表头 get_table_head
    header_list = get_table_head(re_json)
    assert header_list == list(export_filter), '导出的表头断言'

    for each_db in db_export_list02:  # db_export_list 为db中查询的数据 re_list 为请求中返回的数据
        assert each_db in re_list, " 遍历判断数据库中查询到的数据在请求返回中是否存在"



