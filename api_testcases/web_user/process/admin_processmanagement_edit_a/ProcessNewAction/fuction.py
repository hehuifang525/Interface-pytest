from base.common import mysql, config_get_list_value, mysql_get_value, config_write


def process_node_validate(section: str, key_list: list is None):
    """
    用于创建流程接口校验
    """
    if key_list is None:
        key_list = []
    result = config_get_list_value(section, key_list)
    return ''.join("\n- '" + i + "'" for i in result)


def save_mysql_value(table: str, key: str, field: str, field_value):
    """
    将从数据库中获取到的 ProcessEntityID 保存至 config 文件
    方便创单时调用
    """
    result = mysql_get_value(table, key, field, field_value)
    config_write("process", "ProcessEntityID", result)
    return 1


def get_entityid(data_node, value_str):
    """
    从返回值中找到 name Ϊ为 Process node 的 entityID

    """
    for list_key in data_node:
        try:
            json_value = data_node[list_key]
            value = json_value['name']
            if value == value_str:
                config_write("process", "entityID", json_value['entityID'])
                return 1
        except:
            print('未找到')
            return 0
