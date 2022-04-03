import random
import datetime

import allure
import yaml

from base.common import es, mysql, config_read, mysql_get_value, mysql_format_trans2, es_search_list, mysql_get_list


def get_user_role(user_id):
    """
    根据user_id来获取服务人员对应的角色列表

    :return result:角色列表
    """
    if user_id == "0":
        return 0
    result = mysql_get_list("queue_user", "queue_id", "user_id", user_id)
    return result


@allure.step("随机抽取random_size个信件检查信件的主题、操作时间、模板名称、节点名称、操作人类型、操作人名称、操作人所在单位信息、用户是否可见、(信件数据基本信息)")
def articles_check(articles, ticket_id):
    """
    随机抽取random_size个工单ticket_id的信件articles
    检查信件的主题、操作时间、模板名称、节点名称、操作人类型、操作人名称、操作人所在单位信息

    :param articles: 信件集合的json，一般为re_json['data']['Content']['TicketZoomFlowInformation']
    :param ticket_id: 工单ID
    """
    random_size = int(config_read('ServiceCool', 'random_size'))
    time_difference = int(config_read('ServiceCool', 'time_difference'))
    create_transition_id = mysql_get_value('ticket_history', 'transition_id', '', '',
                                           "ticket_id = {} AND history_type_id = 1 "
                                           "AND name NOT LIKE 'New interactive ticket:%'".format(ticket_id))  # 创建信件的transition_id
    for article in random.sample(articles, min(random_size, len(articles))):
        article_id = article['ArticleID']
        with allure.step("检查ID为%s的article" % article_id):
            assert mysql_get_value('article', 'ticket_id', 'id', article_id) == str(ticket_id), "信件是否是该工单的信件"
            # 检查信件的主题、操作时间、模板名称、用户是否可见
            transition_id = mysql_get_value('ticket_history', 'transition_id', 'article_id', article_id)  # 转换id
            is_interactive = mysql_get_value('ticket_history', '*', '', '',
                                             "article_id = {} AND history_type_id = 1 "
                                             "AND name LIKE 'New interactive ticket:%'".format(article_id))
            if is_interactive:  # 若信件为交互单合并信件，则信件的主题名和模板名为固定的值
                a_subject = 'Session merge'
                action_name = ''
            else:
                a_subject = mysql_get_value('article_data_mime', 'a_subject', 'article_id', article_id)
                action_name = mysql.cursor_conn('SELECT case when b.name is null then a.detail_action else b.name end '
                                                'FROM ticket_history a '
                                                'LEFT JOIN ticket_template_c b ON detail_action = b.id '
                                                'WHERE article_id = %s' % article_id)[0][0]
            create_time = datetime.datetime.strptime(mysql_get_value('article', 'create_time', 'id', article_id),
                                                     "%Y-%m-%d %H:%M:%S")
            assert article['Subject']['value']['Value'] == a_subject.lstrip(), "信件的主题"
            assert abs(create_time-datetime.datetime.strptime(article['ActionOperationTime'], "%Y-%m-%d %H:%M:%S")).seconds <= time_difference, "信件的操作时间"
            assert action_name == article['ActionName'], "信件的模板名称"
            assert article['IsVisibleForCustomer'] == mysql_get_value('article', 'is_visible_for_customer', 'id', article_id), "信件的用户是否可见"
            # 检查信件的节点名称
            activity_id = mysql.cursor_conn("SELECT b.name FROM ticket_history a INNER JOIN pm_activity_c b "
                                            "ON SUBSTRING_INDEX(SUBSTRING_INDEX(a.name,'%%',-3),'%%',1) = entity_id "
                                            "WHERE ticket_id = {} AND a.name like '%ProcessManagementActivityID%' "
                                            "AND transition_id <= '{}' ORDER BY a.id DESC"
                                            .format(ticket_id, transition_id))
            if action_name.startswith('AdminMail'):
                assert article['ProcessManagementActivityName'] is None, "若为邮件创单，则无流程也无流程节点名称"
            elif transition_id == create_transition_id:
                assert activity_id[-1][0] == article['ProcessManagementActivityName'],\
                    "若当前信件transition_id等于创建信件的transition_id则取创建节点名称"
            elif is_interactive:
                assert article['ProcessManagementActivityName'] == '', "若为交互单合并信件，则节点名为空"
            else:
                assert activity_id[0][0] == article['ProcessManagementActivityName'], "正常信件检查节点名称"
            # 检查信件的操作人类型、操作人名称、操作人所在单位信息
            article_sender_type_id = mysql_get_value('article', 'article_sender_type_id', 'id', article_id)
            if action_name.startswith('AdminMail'): pass  # 若为邮件创单，不检查
            elif article_sender_type_id == '1':  # 若为服务人员创单
                assert article['ActionOperatorFlag'] == 'User', "信件操作人类型图标显示"
                assert mysql.cursor_conn('SELECT b.full_name FROM ticket_history a '
                                         'INNER JOIN users b on a.create_by = b.id '
                                         'WHERE article_id = %s' % article_id)[0][0] \
                       == article['ActionOperatorName'], "信件操作人名称"
            elif article_sender_type_id == '3':  # 若为客户用户创单
                assert article['ActionOperatorFlag'] == 'Customer', "信件操作人类型图标显示"
                assert mysql.cursor_conn('SELECT b.full_name,c.name FROM ticket_history a '
                                         'INNER JOIN customer_user b on a.customer = b.login '
                                         'INNER JOIN customer_company c on b.customer_id = c.customer_id '
                                         'WHERE article_id = %s' % article_id)[0] \
                       == (article['ActionOperatorName'], article['CompanyName']), "信件操作人名称"
            elif article_sender_type_id == '2': pass  # 若为其他创单，不检查
            # 检查信件右上方图标信息和顺序以及附件信息
            bar_standard_order = ['Attachment', 'Voice', 'Video', 'ActionAttribute', 'Source', 'SignatureContent']
            bar_order = []
            for order in bar_standard_order:
                if order in article:
                    # 检查附件信息
                    if order == 'Attachment':
                        assert article['ToolBarData']['Attachment']['Count'] != len(article['Attachment']), "附件数量"
                        attachment = mysql.cursor_conn("SELECT filename,content_size,content_type "
                                                       "FROM article_data_mime_attachment "
                                                       "WHERE article_id = {} "
                                                       "AND content_type not like '%=%' ".format(article_id))
                        if len(attachment) == len(article['Attachment']):
                            for i in range(len(attachment)):
                                assert (article['Attachment'][i]['Filename'],
                                        article['Attachment'][i]['FilesizeRaw'],
                                        article['Attachment'][i]['ContentType']) in attachment, "附件名、大小、类型"
                    # 检查视频和语音信息的数量显示（因文件放在服务端，暂时无法查询到）
                    elif order in ['Voice', 'Video']:
                        assert article['ToolBarData'][order]['Count'] != len(article[order]['value']), "视频或语音数量"
                    elif order == 'ActionAttribute':  # 检查基础信息
                        if article[order] is None or len(article[order]) == 0: continue  # 若无基础信息，则无基础信息图标
                        else: order = 'BaseInfo'
                    bar_order.append(order)
            assert article['ToolBarOrder'] == bar_order, "图标列表"


def ticket_mysql_expand_inner(key: str, table_b: str, on_a: str, on_b: str, ticket_id):
    """
    联合别的数据库表检查工单信息

    :param key: 需要的值
    :param table_b: 联合的表
    :param on_a: 表a联合的关键（也就是ticket的联合的关键）
    :param on_b: 表b联合的关键
    :param ticket_id: 工单ID
    """
    sql_str = "SELECT %s FROM ticket a INNER JOIN %s b ON a.%s = b.%s WHERE a.id = %s" % (key, table_b, on_a, on_b, ticket_id)
    result = mysql.cursor_conn(sql_str)
    if len(result) == 0 or result[0][0] is None:
        return None
    elif type(result[0][0]) is bytes:
        return str(result[0][0], encoding="utf-8")
    return str(result[0][0])


def ticket_mysql_old_owner(ticket_id, owner):
    """
    检查工单ticket_id上一所有者的值
    ps.因交互单会改变该值，故未更改BUG前暂时规避

    :param ticket_id: 工单ID
    :param owner: 工单负责人的名称
    """
    sql_str = "SELECT full_name FROM ticket_history a " \
              "INNER JOIN users b on SUBSTRING_INDEX(SUBSTRING_INDEX(a.name,'%%',4),'%%',-1) = b.login " \
              "WHERE ticket_id= {} AND history_type_id = 23 ORDER BY a.id desc".format(ticket_id)
    result = mysql.cursor_conn(sql_str)
    return ["" if len(result) <= 1 else result[0][0], owner]


def ticket_age(ticket_id):
    """
    检查工单ticket_id的总时长
    """
    create_time, state_id = mysql.get_value('ticket', 'create_time,ticket_state_id', 'id', ticket_id)[0]
    if mysql_get_value('ticket_state', 'type_id', 'id', state_id) != '3':  # 若工单未关闭，则取当前时间与创建时间的时间差
        end_time = datetime.datetime.now()
    else:  # 若工单已关闭，则取关闭时间与创建时间的时间差
        sql_str = "SELECT a.change_time FROM ticket_history a " \
                  "INNER JOIN ticket_state b ON a.state_id = b.id " \
                  "WHERE history_type_id in (1,27) AND b.type_id = 3 AND a.ticket_id = %s ORDER BY a.id DESC" % ticket_id
        end_time = mysql.cursor_conn(sql_str)[0][0]
    age_time = end_time - create_time
    age_hours = int(age_time.seconds/3600)
    if age_time.days > 0:
        return "%s 天 %s 时 " % (age_time.days, age_hours)
    elif age_hours > 0:
        return "%s 时 %s 分" % (age_hours, int((age_time.seconds-3600*age_hours)/60))
    else:
        return "%s 分" % int(age_time.seconds/60)


@allure.step("工单SLA相关信息")
def ticket_SLA_check(info, ticket_id):
    """
    检查工单SLA相关信息,待补充、

    :param info: 工单信息json，一般为re_json['data']['TicketInformation']
    :param ticket_id: 工单ID
    """
    sla_id = mysql_get_value('ticket', 'sla_id', 'id', ticket_id)
    if sla_id is None:
        assert 'SLAID' not in info['BaseData'], "若无SLA，则无SLA信息"
    else:
        assert mysql_get_value('sla', 'name', 'id', sla_id) == info['BaseData']['SLAID']['value'], "SLA-id的值"


@allure.step("右侧客户信息栏")
def ticket_customer_check(sign, info, ticket_id):
    """
    检查工单ticket_id客户相关信息

    :param sign: （4 or 3）代表customer端或user端
    :param info: 工单信息json，一般为re_json['data']['TicketInformation']
    :param ticket_id: 工单ID
    """
    customer_id, customer_user_id = mysql.get_value('ticket', 'customer_id,customer_user_id', 'id', ticket_id)[0]
    # 检查客户id和返回体相关数据是否都为空
    if customer_id is None:
        assert customer_user_id is None, "若工单未选择客户, 数据库客户用户id为空"
        assert info['CustomerID'] is None, "若工单未选择客户, 客户id为空"
        assert info['CustomerUser'] == {"Phone": None, "Address": "", "Email": None, "Name": None,
                                        "Company": None}, "若工单未选择客户, 客户信息为空"
        assert 'CustomerUserData' not in info, "若工单未选择客户, 客户用户信息为空"
        assert info['CustomerUserID'] is None, "若工单未选择客户, 客户用户id为空"
    # 若工单选择客户，检查客户信息
    elif customer_id == info['CustomerID']:
        sql_config = yaml.load(mysql_get_value('customer_company_config', 'content', 'id', sign), Loader=yaml.FullLoader)
        # 检查客户信息
        assert info['CustomerUserData']['CustomerCompany']['FieldOrder'] == sql_config['CustomerCompany']['FieldOrder'], "客户信息字段配置顺序"
        is_Edit = ''
        if sign == 4 and config_read('ServiceCool', 'url_customer') not in \
                mysql_get_list('customer_company_responsible', 'customer_user_login', 'customer_id', customer_id):
            is_Edit = '1'  # 在客户用户端，非客户主管无法编辑客户相关信息
        customer_check('CustomerCompany', info['CustomerUserData']['CustomerCompany']['FieldData'], sql_config,
                       customer_id, is_Edit)  # 遍历检查字段
        # 检查客户用户信息
        if customer_user_id == '': pass  # 若未选客户用户，跳过
        elif mysql_get_value('customer_user', '*', 'login', customer_user_id) is None:
            assert info['CustomerUser']['Name'] is None, "若客户用户不存在了，不显示即为正确"
        else:  # 若客户用户存在
            assert info['CustomerUserData']['CustomerUser']['FieldOrder'] == sql_config['CustomerUser']['FieldOrder'], "客户用户信息字段配置顺序"
            customer_check('CustomerUser', info['CustomerUserData']['CustomerUser']['FieldData'],
                           sql_config, customer_user_id, is_Edit)  # 遍历检查字段


@allure.step("遍历检查字段")
def customer_check(sign, info, sql_config, id_value, is_Edit):
    """
    检查工单客户和客户用户字段信息
    用于ticket_customer_check函数

    :param sign: （CustomerCompany或CustomerUser）代表客户或客户用户
    :param info: 返回的json的data.TicketInformation.[user].FieldData
    :param sql_config: 从sql中得到的客户信息展示配置
    :param id_value: 客户或客户用户id
    :param is_Edit: 在客户用户端，非客户主管无法编辑客户相关信息，1否2能编辑
    """
    for field in sql_config[sign]['FieldOrder']:  # 遍历显示的每个字段
        if sign == 'CustomerCompany' and is_Edit == '1':
            isEdit = '1'
        else:
            isEdit = get_isEdit_isRequired(field, 'isEdit', sql_config[sign])
        isRequired = get_isEdit_isRequired(field, 'isRequired', sql_config[sign])
        value = get_customer_value(sign, id_value, field)
        assert str(info[field]['isEdit']) == isEdit, "能否编辑，1否2能"
        assert info[field]['display'] == isRequired, "是否必填，1否2是"
        assert info[field]['default'] == value, "字段的值"


def get_isEdit_isRequired(field, sign, sql_config):
    """
    检查工单客户或客户用户字段field的isEdit或isRequired（sign）信息
    用于customer_check函数

    :param field: 字段名
    :param sign: （CustomerCompany或CustomerUser）代表客户或客户用户
    :param sql_config: 从sql中得到的客户信息展示配置
    """
    default_config = {"ValidID": {"isEdit": "1", "isRequired": "2"},
                      "CustomerCompanyDistrict": {"isEdit": "1", "isRequired": "1"},
                      "CustomerCompanyName": {"isRequired": "2"},
                      "CustomerID": {"isEdit": "1", "isRequired": "2"},
                      "CustomerCompanyCountry": {"isEdit": "1", "isRequired": "1"},
                      "UserCustomerID": {"isEdit": "1", "isRequired": "2"},
                      "UserFirstname": {"isRequired": "2"},
                      "UserDistrict": {"isEdit": "1", "isRequired": "1"},
                      "UserLastname": {"isRequired": "2"},
                      "UserLogin": {"isEdit": "1", "isRequired": "2"},
                      "UserFullname": {"isRequired": "2"}}  # 固定字段的isEdit和isRequired的固定值
    if 'FieldData' in sql_config and sign in sql_config['FieldData'][field]:  # 若sign已在设置中配置过则取配置的值
        return sql_config['FieldData'][field][sign]
    elif field in default_config and sign in default_config[field]:  # 若字段的sign已有固定值，则取固定值
        return default_config[field][sign]
    else:  # 以上都无则取默认值1
        return '1'


def get_customer_value(sign, id_value, field):
    """
    检查工单客户或客户用户（sign）字段field的值信息
    用于customer_check函数
    id_value 客户或客户用户id
    """
    table, id_name, sign = ['customer_company', 'customer_id', sign] if sign == 'CustomerCompany'\
        else ['customer_user', 'login', 'User']  # 区分客户和客户用户不同的部分
    if sign in field:  # 若为带CustomerCompany或User前缀的固定字段
        if field == 'UserCustomerID':  # 取数据库中customer_id列的值
            return mysql_get_value(table, 'customer_id', id_name, id_value)
        elif field == 'CustomerCompanyDistrict':
            sql_str = "SELECT b.name FROM customer_company a INNER JOIN district b ON a.district = b.id " \
                      "WHERE a.customer_id = '%s'" % id_value
            return mysql_format_trans2(mysql.cursor_conn(sql_str))
        elif field == 'UserDistrict':
            sql_str = "SELECT c.name FROM customer_user a " \
                      "INNER JOIN customer_company b ON a.customer_id = b.customer_id " \
                      "INNER JOIN district c ON b.district = c.id " \
                      "WHERE a.login = '%s'" % id_value
            return mysql_format_trans2(mysql.cursor_conn(sql_str))
        elif field.endswith('name') and len(field[len(sign):]) > 4:  # 若后缀带name，则转换为下划格式，取对应数据库对应的值
            return mysql_format_trans2(mysql.get_value(table, field[len(sign):-4] + '_name', id_name, id_value))
        elif field.endswith('Comment'):
            return mysql_get_value(table, 'comments', id_name, id_value)
        return mysql_format_trans2(mysql.get_value(table, field[len(sign):], id_name, id_value))
    elif field == 'ValidID':
        return mysql_get_value(table, 'valid_id', id_name, id_value)
    elif field == 'CustomerID':
        return id_value
    else:  # 若为自定义字段，则联合自定义字段表取值
        field_id, field_type = mysql.get_value('dynamic_field', 'id,field_type', 'name', field[13:])[0]
        if field_id != 'Date':
            field_type = 'Text'
        sql_str = "SELECT a.value_{0} FROM dynamic_field_value a " \
                  "INNER JOIN dynamic_field_obj_id_name b on a.object_id = b.object_id " \
                  "WHERE a.field_id = {1} and b.object_name = '{2}' " \
                  "and b.object_type LIKE '%{3}%'".format(field_type, field_id, id_value, sign)
        result = mysql.cursor_conn(sql_str)
        return mysql_format_trans2(result)


def get_base_data_order(ticket_id):
    """
    获取ticket_id的data::TicketInformation::BaseDataOrder的值
    """
    ticket_state_id, until_time = mysql.get_value('ticket', 'ticket_state_id, until_time', 'id', ticket_id)[0]
    if until_time > 0 and mysql_get_value('ticket_state', 'valid_id', 'id', ticket_state_id) in ('4', '5'):
        return ["TypeID", "Age", "Created", "State", "PendingUntil", "Priority", "ServiceID", "SLAID"]
    else:
        return ["TypeID", "Age", "Created", "State", "Priority", "ServiceID", "SLAID"]


def get_user_tag_list():
    """
    获取table中key字段的random_size个随机值
    """
    url_user = config_read('ServiceCool', 'url_user')
    user_role = get_user_role(mysql_get_value('users', 'id', 'login', url_user))
    if user_role is None:
        tag_list = []
    else:
        if len(user_role) == 1:
            field_str = "field_value = %d" % user_role[0]
        else:
            field_str = "field_value IN %s" % str(tuple(user_role))
        sql_str = "SELECT concat(c.name,'###',tag.name),a.* FROM permission_tag_field_value a " \
                  "INNER JOIN tag ON a.tag_id=tag.id " \
                  "INNER JOIN tag_type c on a.tag_type_id = c.id " \
                  "WHERE field='Queue' AND %s" % field_str
        sql_result = mysql.cursor_conn(sql_str)
        tag_list = None if len(sql_result) == 0 or sql_result[0][0] is None else [x[0] for x in sql_result]
    return tag_list


def get_random_ticketid():
    """
    获取random_size个随机的有权限查看的工单ID
    """
    es_ticket_data = config_read('Elasticsearch', 'ticket_data')
    if es_ticket_data == "":
        return mysql_get_list('ticket', 'id', '', '',
                              'tn>100000000000000 ORDER BY RAND() LIMIT %s' % config_read('ServiceCool', 'random_size'))
    tag_list = get_user_tag_list()
    es_str = {
        "query": {
            "bool": {
                "should": [{"match": {"Tags": config_read('ServiceCool', 'url_user')}}],
                "must_not": [{"match": {"DynamicField_TicketTypeID.keyword": "InteractiveTicket"}}]}},
        "sort": {
            "_script": {
                "script": "Math.random()",
                "type": "number",
                "order": "asc"
            }
        },
        "_source": ["TicketID"],
        "size": config_read('ServiceCool', 'random_size')
        }
    for i in tag_list:
        es_str["query"]["bool"]["should"].append({"match": {"Tags.keyword": i}})
    result = es_search_list(config_read('Elasticsearch', 'ticket_data'), es_str, "TicketID")
    return result


def get_random_no_permissions_ticketid():
    """
    获取random_size个随机的无权限查看的工单ID
    """
    es_ticket_data = config_read('Elasticsearch', 'ticket_data')
    if es_ticket_data == "" or config_read('ServiceCool', 'url_user') == 'root@localhost':
        return []
    tag_list = get_user_tag_list()
    es_str = {
        "query": {
            "bool": {
                "must_not":
                    [{"match": {"DynamicField_TicketTypeID.keyword": "InteractiveTicket"}},
                     {"match": {"Tags": config_read('ServiceCool', 'url_user')}}]}},
        "sort": {
            "_script": {
                "script": "Math.random()",
                "type": "number",
                "order": "asc"
            }
        },
        "_source": ["TicketID"],
        "size": config_read('ServiceCool', 'random_size')
        }
    for i in tag_list:
        es_str["query"]["bool"]["must_not"].append({"match": {"Tags.keyword": i}})
    result = es_search_list(es_ticket_data, es_str, "TicketID")
    return result
