import random
import datetime
import allure
import yaml

from base.common import es, mysql, config_read, mysql_get_value, mysql_format_trans2, es_search_list, mysql_get_list


def get_customer_random_ticket_id():
    """
    获取random_size个客户用户的工单ID
    """
    user_id = config_read('ServiceCool', 'url_customer')
    sql_str = "SELECT id FROM ticket a " \
              "WHERE customer_user_id = '%s' " \
              "OR customer_id = (SELECT customer_id FROM customer_user WHERE login = '%s') " \
              "ORDER BY RAND() LIMIT %s" % (user_id, user_id, config_read('ServiceCool', 'random_size'))
    result = mysql.cursor_conn(sql_str)
    return None if len(result) == 0 or result[0][0] is None else [x[0] for x in result]


def get_customer_random_no_permissions_ticket_id():
    """
    获取table中key字段的random_size个随机值
    """
    user_id = config_read('ServiceCool', 'url_customer')
    sql_str = "SELECT id FROM ticket a " \
              "WHERE customer_user_id != '%s' " \
              "AND customer_id != (SELECT customer_id FROM customer_user WHERE login = '%s') " \
              "ORDER BY RAND() LIMIT %s" % (user_id, user_id, config_read('ServiceCool', 'random_size'))
    result = mysql.cursor_conn(sql_str)
    return None if len(result) == 0 or result[0][0] is None else [x[0] for x in result]


def customer_ticket_creator(ticket_id):
    """
    获取工单的创建者
    """
    create_customer, create_by = mysql.get_value('ticket', 'create_customer, create_by', 'id', ticket_id)[0]
    if create_customer is None:
        return mysql_get_value('users', 'full_name', 'id', create_by)
    else:
        return mysql_get_value('customer_user', 'full_name', 'login', create_customer)


def customer_articles_check(articles, ticket_id):
    """
    随机抽取random_size个工单ticket_id的信件articles
    检查信件的主题、操作时间、模板名称、节点名称、操作人类型、操作人名称、操作人所在单位信息
    """
    random_size = int(config_read('ServiceCool', 'random_size'))
    time_difference = int(config_read('ServiceCool', 'time_difference'))
    create_transition_id = mysql_get_value('ticket_history', 'transition_id', '', '',
                                           "ticket_id = {} AND history_type_id = 1 "
                                           "AND name NOT LIKE 'New interactive ticket:%'".format(ticket_id))  # 创建信件的transition_id
    for article in random.sample(articles, min(random_size, len(articles))):
        article_id = article['ArticleID']
        with allure.step("检查ID为%s的article" % article_id):
            # 检查信件是否是该工单的信件、是否为用户可见
            assert mysql_get_value('article', 'ticket_id', 'id', article_id) == str(ticket_id), "信件是否是该工单的信件"
            assert mysql_get_value('article', 'is_visible_for_customer', 'id', article_id) == '1', "信件是否为用户可见"
            # 检查信件的主题、操作时间、模板名称
            transition_id = mysql_get_value('ticket_history', 'transition_id', 'article_id', article_id)  # 转换id
            is_interactive = mysql_get_value('ticket_history', '*', '', '',
                                             "article_id = {} AND history_type_id = 1 "
                                             "AND name LIKE 'New interactive ticket:%'".format(article_id))
            if is_interactive:  # 若信件为交互单合并信件，则信件的主题名和模板名为固定的值
                a_subject = 'Session merge'  # 主题名
                action_name = ''  # 模板名
            else:
                a_subject = mysql_get_value('article_data_mime', 'a_subject', 'article_id', article_id)
                action_name = mysql.cursor_conn('SELECT case when b.name is null then a.detail_action else b.name end '
                                                'FROM ticket_history a '
                                                'LEFT JOIN ticket_template_c b ON detail_action = b.id '
                                                'WHERE article_id = %s' % article_id)[0][0]
            create_time = datetime.datetime.strptime(mysql_get_value('article', 'create_time', 'id', article_id),
                                                     "%Y-%m-%d %H:%M:%S")
            assert article['Subject']['value']['Value'] == a_subject.strip(), "信件的主题"
            assert abs(create_time-datetime.datetime.strptime(
                article['ActionOperationTime'], "%Y-%m-%d %H:%M:%S")).seconds <= time_difference, "信件的操作时间"
            assert action_name == article['ActionName'], "信件的模板名称"
            # 检查信件的节点名称
            activity_id = mysql.cursor_conn("SELECT b.name FROM ticket_history a INNER JOIN pm_activity_c b "
                                            "ON SUBSTRING_INDEX(SUBSTRING_INDEX(a.name,'%%',-3),'%%',1) = entity_id "
                                            "WHERE ticket_id = {} AND a.name like '%ProcessManagementActivityID%' "
                                            "AND transition_id <= '{}' ORDER BY a.id DESC"
                                            .format(ticket_id, transition_id))
            if action_name.startswith('AdminMail'):
                assert article['ProcessManagementActivityName'] is None, "若为邮件创单，则无流程也无流程节点名称"
            elif mysql_get_value('ticket_history', 'create_time', '', '',
                                 "article_id = '%s' AND history_type_id = 69 " % article_id):
                assert article['ProcessManagementActivityName'] is None, "若为小岛交互单，则也无流程名"
            elif transition_id == create_transition_id:
                assert activity_id[-1][0] == article['ProcessManagementActivityName'], "若当前信件transition_id等于创建信件的transition_id则取创建节点名称"
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
                    elif order == 'ActionAttribute': continue  # 客户用户端不显示基础信息
                    bar_order.append(order)
            assert article['ToolBarOrder'] == bar_order, "图标列表"
