import pytest
import os


if __name__ == '__main__':
    pytest.main(["-vs", "api_testcases/web_user/agent/admin_agent_overview_a/Save/test_cases.py::test_case1", '--alluredir', './report_temp', '--clean-alluredir'])
    # pytest.main(["-vs", "api_testcases", '--alluredir', './report_temp', '--clean-alluredir'])
    # pytest.main(["-vs", "api_testcases/web_user", "--reruns", '3', "--reruns-delay", '1', '--alluredir', './report_temp', '--clean-alluredir'])  # 失败重试3次执行
    # os.system('allure generate ./report_temp -o ./report --clean')  # 保存报告
    # os.system('allure open report')  # 打开报告
    os.system('allure serve ./report_temp')  # 立即打开报告（程序会持续执行）
