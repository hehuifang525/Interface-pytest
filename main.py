import argparse
import configparser

import pytest

parser = argparse.ArgumentParser()
parser.add_argument("--url_host", default="https://re1.otrs365.cn", help="接口的host.")  # 添加命令行参数
parser.add_argument("--url_user", default="root@localhost", help="服务人员登录名.")
parser.add_argument("--url_customer", default="cool", help="客户用户登录名.")
parser.add_argument("--url_password", default="123456", help="用户密码.")
parser.add_argument("--mysql_host", default="10.8.0.21", help="数据库的host.")
parser.add_argument("--mysql_port", default="3306", help="数据库的port.")
parser.add_argument("--mysql_user", default="root", help="数据库登录的用户名.")
parser.add_argument("--mysql_password", default="Y8G_CWlhp__", help="数据库登录的密码.")
parser.add_argument("--mysql_db", default="release_sc_10082", help="连接的数据库db名.")
parser.add_argument("--es_ticket_data", default="release-sc-10082_ticket_data", help="连接的es库的工单数据库名.")
parser.add_argument("--test_path", default="testsuites", help="指定执行的文件的路径. eg.testsuites/web_user")
args = parser.parse_args()

# 把命令行中的参数，记录到config文件里
conf = configparser.ConfigParser()
conf.read("config.ini")
conf.set('ServiceCool', 'url_host', args.url_host)
conf.set('ServiceCool', 'url_user', args.url_user)
conf.set('ServiceCool', 'url_customer', args.url_customer)
conf.set('ServiceCool', 'url_password', args.url_password)
conf.set('ServiceCool', 'mysql_host', args.mysql_host)
conf.set('ServiceCool', 'mysql_port', args.mysql_port)
conf.set('ServiceCool', 'mysql_user', args.mysql_user)
conf.set('ServiceCool', 'mysql_password', args.mysql_password)
conf.set('ServiceCool', 'mysql_db', args.mysql_db)
conf.set('Elasticsearch', 'ticket_data', args.es_ticket_data)
conf.write(open("config.ini", "w"))

# 运行pytest
pytest.main(["-vs", args.test_path,
             "--reruns", "3", "--reruns-delay", "1",
             "--alluredir", "./report_temp", "--clean-alluredir"])
