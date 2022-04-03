import pytest
import allure
from base.common import send_request, success_assert, base64_encode_value
from api_testcases.web_user.action_re_body import *
from .api import *
from .function import *


@allure.severity('Normal')
def test_link_sla():
    """
        服务关联客户、sla、流程

    """

    service_id = str(get_service()[0])
    sla_id = [str(get_sla()[0])]
    company_id = [str(get_company()[0])]
    process_id = [str(get_process()[0])]
    data_body = common_data(company_id,sla_id, process=process_id, tag_data=None)
    re_body = {"ServiceID": service_id, "justaddServiceID": service_id, "data": base64_encode_value(data_body)}
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()

    success_assert(result.status_code, re_json['result'])
    common_assert(re_json, ["sla","company","process"])
