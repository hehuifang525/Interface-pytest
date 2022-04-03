import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_all,config_read,fail_assert,base64_encode_value, mysql_get_value,mysql_get_list
from base.Mysql import Mysql
from time import sleep
from api_testcases.web_user.faq.faq_edit_a.Save.test_cases import add_faq_commom


@allure.severity('Normal')
def test_all_num():
    """
    数据差校验
    """
    # faq_category_num = mysql_get_value("ticket", "COUNT(id) as num", "", "", "title LIKE'%测试%'")
    num_list = mysql_get_list("ticket", "tn", "", "", "title LIKE'%测试%'")

    # re_data = {"ResultForm":"Print","ShownAttributes":["Fulltext"],"SearchField":{"Fulltext":"测试"},"Dynamic":{},"Profile":"","ProfileID":""}
    # re_body = {
    #     "Subaction":"Search",
    #     "data":re_data,
    #     "Action": "ticket_search_a"
    # }
    ""
    re_body ="Subaction=Search&data=%7B%22ResultForm%22:%22Print%22,%22ShownAttributes%22:%5B%22Fulltext%22%5D,%22SearchField%22:%7B%22Fulltext%22:%22%E6%B5%8B%E8%AF%95%22%7D,%22Dynamic%22:%7B%7D,%22Profile%22:%22%22,%22ProfileID%22:%22%22%7D&Action=ticket_search_a"
    result = send_request(method, url, headers=headers(), data=re_body)
    re_json = result.json()
    # print(re_json)
    result_list = re_json["data"]["OverviewList"]
    for i in result_list:
        # print(type(i["TicketNumber"]),'111')
        # print(type(num_list[0]),'222')
        if i["TicketNumber"] in num_list:
            num_list.remove(i["TicketNumber"])
        print(i["TicketNumber"])
    print(num_list)
    # print(num_list,"相差的数据")


