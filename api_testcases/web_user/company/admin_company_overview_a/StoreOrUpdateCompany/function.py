from base.common import mysql_get_value, config_write


def assert_input_value(company_id, field,  expected_value, describe=""):
    """
    对客户的各个字段取数据库值与输入值进行校验
    :param company_id: 客户ID
    :param field: 需要查询的字段值
    :param expected_value:预期值
    :param describe:描述
    """
    actual_value = mysql_get_value("customer_company", field, "customer_id", company_id)
    assert actual_value == expected_value, describe


