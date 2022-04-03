def fieldgroup_structure_add(primary_data, add_list):
    """
    根据add_list中的字段id来添加对应的字段组结构
    用于添加字段组接口
    """
    for i in add_list:
        primary_data[i] = None
        primary_data[i + "_configFieldOptionsType"] = None
        primary_data[i + "_configFieldOptions"] = None
        primary_data[i + "_display"] = "1"
    return primary_data
