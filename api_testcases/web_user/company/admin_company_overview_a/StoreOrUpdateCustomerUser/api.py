from base.common import mysql_get_value, config_write


def common_data(user_login, company_id):
    """
    创建客户用户请求body

    :param company_id: 客户ID
    :param user_login: 用户登录名
    """
    data_body = {
        "ValidID": "1",
        "UserCustomerID":company_id,
        "UserLogin": user_login,
        "UserFirstname":"测试",
        "UserLastname":"宋",
        "UserFullname":"宋测试"
    }
    return data_body


def common_full_data(user_login,
                     company_id,
                     user_email,
                     user_mobile,
                     user_firstname="测试",
                     user_lastname="宋",
                     user_fullname="宋测试",
                     user_comment="测试备注、这是区域经理",
                     user_phone="4569663",
                     user_fax="563332",
                     user_password="321",
                     user_title="这是标题问候",
                     user_street="街道-南湖",
                     user_city="苏州",
                     user_country="中国",
                     user_zip="53000"):
    """
    创建客户用户请求body
    :param company_id: 客户ID
    :param user_login: 用户登录名
    :param user_email: 邮箱地址
    :param user_mobile: 手机号
    :param user_firstname: 用户名
    :param user_lastname: 用户姓
    :param user_fullname: 用户全名
    :param user_comment: 备注
    :param user_phone: 电话
    :param user_fax: 传真
    :param user_password: 密码
    :param user_title: 标题
    :param user_street: 街道
    :param user_city: 城市
    :param user_country: 国家
    :param user_zip: 邮编


    """
    data_body = {
        "ValidID": "1",
        "UserCustomerID": company_id,
        "UserLogin": user_login,
        "UserEmail": user_email,
        "UserMobile": user_mobile,
        "UserFirstname":user_firstname,
        "UserLastname": user_lastname,
        "UserFullname": user_fullname,
        "UserDistrict": None,
        "UserComment": user_comment,
        "UserFax": user_fax,
        "UserTitle":user_title,
        "UserStreet": user_street,
        "UserPhone": user_phone,
        "UserCity": user_city,
        "UserCountry": user_country,
        "UserPassword": user_password,
        "UserZip":user_zip
    }
    return data_body
