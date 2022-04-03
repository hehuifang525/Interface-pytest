import os
import json
from base.common import conf


url = conf["ServiceCool"]["url_host"]+r"/otrs/indexNew.pl?"
method = "POST"


def headers():
    return {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "cookie": "OTRSAgentInterface=%s" % conf["ServiceCool"]['OTRSAgentInterface']
                }


def action_body(path, data_body):
    """
    含有action和subaction请求body的常规格式

    :param path: eg:__file__ 文件执行路径，用于自动获取action和subaction的值
    :param data_body: data参数的值
    """
    path_list = os.path.abspath(path).split('\\')
    re_body = {
                "Action": path_list[-3],
                "Subaction": path_list[-2]
                }
    if data_body:
        re_body["data"] = json.dumps(data_body)
    return re_body
