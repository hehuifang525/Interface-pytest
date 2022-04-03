from urllib import parse
import os


def fetch(url, dic):
    # 请求的一些信息
    data_dic = parse.parse_qs(dic['body'], keep_blank_values=True)
    title_list = '''import pytest
import allure
from base.common import send_request, success_assert'''.split('\n')
    text_list = '''

@allure.severity('Normal')
def test_case():
    result = send_request(method, url, headers=headers(), data=action_body(__file__, re_body))
    re_json = result.json()
'''.split('\n')
    common_dic = {}
    for i in data_dic:
        common_dic[i] = data_dic[i][0]

    # 判断测试用例的路径和脚本内容
    if 'Action' in data_dic:
        if 'indexNew' in url:
            sign = 'web_user'
        else:
            sign = 'web_customer'
        text_list.append("    success_assert(result.status_code, re_json['result'])\n")
        title_list.insert(4, "from api_testcases.%s.action_re_body import *" % sign)
        path = 'api_testcases/%s' % sign

        for i in os.listdir(path):
            path_temp = '/'.join((path, i, data_dic['Action'][0]))
            if os.path.isdir('/'.join((path, i))) and os.path.exists(path_temp):
                path = path_temp
                break
            elif i == '__init__.py':
                path = '/'.join((path, data_dic['Action'][0]))
        if 'Subaction' in data_dic:
            path = '/'.join((path, data_dic['Subaction'][0]))
            text_list.insert(4, "    re_body = %s\n" % data_dic['data'][0])
        else:
            text_list[4] = "    re_body = %s\n\n" \
                           "    result = send_request(method, url, headers=headers(), data=re_body)" % common_dic
    else:
        path = 'test_cases'
        text_list[4] = '''    url = '%s'
    method = '%s'
    headers = %s
    re_body = %s

    result = send_request(method, url, headers=headers, data=re_body)''' % (url, dic['method'], dic['headers'], common_dic)

    # 判断文件是否存在以及写入
    if not os.path.exists(path):
        os.makedirs(path)
        open(path + '/__init__.py', 'w')
        text = '\n'.join(title_list + text_list)
    else:
        if not os.path.exists(path + '/test_cases.py'):
            text = '\n'.join(title_list + text_list)
        else:
            text = '\n'.join(text_list)
    with open(path + '/test_cases.py', 'a') as test_cases:
        test_cases.write(text)
    print(path + '  的用例脚本已新增')


if __name__ == '__main__':
    f = open("base/request_copy", encoding="utf-8")
    exec(f.read()[:-1].replace("); ;", ")"))
