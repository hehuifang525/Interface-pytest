from base.common import mysql_get_value, config_write


def common_data(customer_id,
                company_name,
                validid="1",
                parent_customer_id=None,
                customer_company_district=None,
                company_country=None,
                customer_company_city="新疆",
                company_url="http://www.ceshi.com",
                company_street="南湖",
                company_comment="设置备注",
                company_zip="532201"):
    """
    创建客户请求body
    :param customer_id: 客户ID
    :param company_name: 客户名称
    :param validid:有效性
    :param parent_customer_id:父客户id
    :param customer_company_district:区域id
    :param customer_company_city:城市
    :param company_url:网址
    :param company_country:国家
    :param company_street:街道
    :param company_comment:备注
    :param company_zip:邮编

    """
    data_body = {
            "ValidID": validid,
            "CustomerID": customer_id,
            "CustomerCompanyName": company_name,
            "ParentCustomerID": parent_customer_id,
            "CustomerCompanyCity": customer_company_city,
            "CustomerCompanyURL": company_url,
            "CustomerCompanyDistrict": customer_company_district,
            "CustomerCompanyCountry": company_country,
            "CustomerCompanyStreet": company_street,
            "CustomerCompanyComment": company_comment,
            "CustomerCompanyZIP": company_zip
    }
    return data_body
