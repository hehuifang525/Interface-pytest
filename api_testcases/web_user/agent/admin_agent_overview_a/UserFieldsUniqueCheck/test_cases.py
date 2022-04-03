import pytest
import allure
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert
from base.common import send_request, success_assert, get_datetime, config_get_section_value, base64_encode_all,config_read
from api_testcases.web_user.agent.admin_agent_overview_a.Save.test_cases import add_full_user_commom


@allure.severity('Normal')
# @pytest.mark.parametrize('check', [{"filter":"UserLogin","filter_value": config_read("user_normal_init", "userlogin"),"describe":"账号"},
#                                     {"filter":"UserEmail","filter_value":config_read("user_normal_init", "useremail"),"describe":"邮箱号"},
#                                     {"filter":"UserMobile","filter_value":config_read("user_normal_init", "usermobile"),"describe":"手机号"},
#                                     {"filter":"JobNumber","filter_value":config_read("user_normal_init", "job_number"),"describe":"工号"}])
def test_check_repeat():
    """
        前提：需要读取全填的服务人员信息
        服务人员：账号、邮箱、工号、手机号唯一性校验
    """
    user_info = add_full_user_commom()
    # user_info = {"login": user_login, "mobile": user_mobile, "email": user_email, "jobnumber": job_number}
    check_repeat_info= [{"filter":"UserLogin","filter_val": user_info.get("login"),"describe":"账号"},
                         {"filter":"UserEmail","filter_val":user_info.get("email"),"describe":"邮箱号"},
                         {"filter":"UserMobile","filter_val":user_info.get("mobile"),"describe":"手机号"},
                          {"filter":"JobNumber","filter_val":user_info.get("jobnumber"),"describe":"工号"}]
    for each_check_repeat_info in check_repeat_info:
        re_body = {"Filter": each_check_repeat_info.get("filter"), "FilterValue": each_check_repeat_info.get("filter_val")}
        result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
        re_json = result.json()
        assert re_json["result"] == 1, "接口请求成功标识"
        assert re_json["data"]["message"] == "The field value already exists in DB. Please retype it!", "用户"+each_check_repeat_info.get("describe")+"唯一性校验提示"












