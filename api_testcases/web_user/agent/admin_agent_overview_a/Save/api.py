from base.common import mysql_get_value, config_write


def common_data(user_login,
                user_id="",
                user_email="",
                user_mobile="",
                validid="1",
                user_pw ="123",
                job_number="",
                user_firstname="测试",
                user_lastname="张",
                user_fullname="张测试",
                user_city="新疆",
                user_title=""):
    """
    创建服务人员请求body
    :param user_login: user账号
    :param user_id: user ID
    :param user_email: 邮件
    :param user_mobile:手机号
    :param validid:有效性
    :param user_pw:密码
    :param job_number 工号
    :param user_firstname:名
    :param user_lastname:姓
    :param user_fullname:姓名
    :param user_city：城市
    :param user_title:标题
    """
    data_body = {
            "UserID":user_id,
            "ValidID": validid,
            "UserEmail": user_email,
            "UserLogin": user_login,
            "UserFirstname": user_firstname,
            "UserLastname": user_lastname,
            "JobNumber": job_number,
            "UserFullname": user_fullname,
            "UserMobile": user_mobile,
            "UserCity": user_city,
            "UserPw": user_pw,
            "UserDistrict": "",
            "UserTitle":user_title
    }
    return data_body


def assert_input_value(user_id, field, expected_value, describe=""):
    """
    对表的各个字段输入值与数据库最终值进行校验
    :param company_id: 查询的字段
    :param field: 需要查询的字段值
    :param expected_value:预期值
    :param describe:描述
    """
    actual_value = mysql_get_value("users", field, "id", user_id)
    assert actual_value == expected_value, describe
