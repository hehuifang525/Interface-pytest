def tickettemplate_structure_add(primary_data, add_list):
    """
    根据add_list中的字段id来添加对应的字段
    用于添加工单模板接口
    ps.无数据的值暂时不加也可
    """
    for i in add_list:
        primary_data["DynamicField_" + i] = ""
        primary_data["DynamicField_" + i + "_optionsShowType"] = None
        primary_data["DynamicField_" + i + "_optionsShowValue"] = None
        primary_data["DynamicField_" + i + "_regex"] = None
        primary_data["DynamicField_" + i + "_regexError"] = None
        primary_data["DynamicField_" + i + "_promptCode"] = None
        primary_data["DynamicField_" + i + "_promptMessage"] = None
        primary_data["DynamicField_" + i + "_formula"] = None
        primary_data["DynamicField_" + i + "_display"] = "1"
        primary_data["DefalutFieldOrder"].append("DynamicField_" + i)
    return primary_data


def tickettemplate_structure_add_sim(primary_data, add_list):
    """
    根据add_list中的字段id来添加对应的字段(简化版）
    用于添加工单模板接口
    ps.无数据的值暂时不加也可
    """
    for i in add_list:
        primary_data["DynamicField_" + i + "_display"] = "1"
        primary_data["DefalutFieldOrder"].append("DynamicField_" + i)
    return primary_data