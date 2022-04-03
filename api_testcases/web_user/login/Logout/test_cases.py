from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert, config_write


def common_logout():
    """
    常规登出接口，用于conftest.py
    """
    result = send_request(method, url, headers=headers(), data={"Action": "Logout"})
    re_json = result.json()
    success_assert(result.status_code, re_json['result'])  # 正向请求返回的固定校验
    config_write('ServiceCool', 'otrsagentinterface', '')
    print('web-user登出')
