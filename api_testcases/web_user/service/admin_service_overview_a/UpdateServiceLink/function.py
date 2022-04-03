from base.common import es, mysql, config_read, mysql_get_value, mysql_format_trans2, es_search_list, mysql_get_list,mysql
from api_testcases.web_user.service.admin_service_overview_a.Save.test_cases import add_service_commom
import re


def get_service():
    """
    取一条有效的服务
    """
    service_id = mysql_get_list("service", "id", "", "", "valid_id =1  AND NAME LIKE'ser%' ")
    if not service_id:
        service_info = add_service_commom()
        service_id = service_info["id"]
    return service_id


def get_sla():
    """
    取一条有效的协议
    """
    sla_id = mysql_get_list("sla", "id", "","","valid_id =1")
    return sla_id


def get_tag():
    """
    取一条有效的标签
    """
    pass


def get_process():
    """
    取一条有效的流程
    """
    process_id = mysql_get_list("pm_process_c  a , pm_process_type_c b", "a.id", "", "",
                   " a.process_type = b.id AND b.valid_id =1 AND a.state_entity_id = 'S1'")
    return process_id


def get_company():
    """
    取一条有效的客户
    """
    company_id = mysql_get_list("customer_company", "customer_id", "", "", "valid_id ='1'")
    return company_id