from base.common import es, mysql, config_read, mysql_get_value,mysql_get_list, mysql, get_datetime
import re


def get_import_data(amount: int, valid="valid"):
    """
    生成有效导入的数据  Name  Valid  InternalComments  ExternalComments
    :param amount: 生成的记录数
    :param valid: 有效性

    return  id  名称 有效性 内部备注 外部备注
    """
    service_name = "%s%s" % ('import_ser', get_datetime())  # 随机生成服务名称
    import_data_list = []
    for i in range(amount):
        import_data_list.append([service_name + str(i+1),valid,"导入的内部备注{}".format(str(i+1)),
                                 "导入的外部备注{}".format(str(i+1))])

    return import_data_list


def assert_analysis_data(re_json, count: int):
    """
    对分析的数据、导入数据进行校验
    :param re_json: 响应数据
    :param count: 数据总量

    """
    assert re_json["data"]["Count"] == count, "导入总记录校验"
    assert re_json["data"]["New"] == count, "导入新增记录数校验"
    for i in re_json["data"]["FieldRowInfo"]:
        assert i["errorinfo"] == "It is OK", "新增导入数据的分析正确提示"





