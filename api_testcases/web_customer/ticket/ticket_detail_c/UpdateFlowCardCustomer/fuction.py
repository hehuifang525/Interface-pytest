from base.common import mysql_get_value


def customer_ticket_flow_card_default(user_id):
    """
    获取当前customer账号user_id默认工单信件展开方式值
    """
    result = mysql_get_value('customer_preferences', 'preferences_value', '', '',
                             "user_id = '%s' AND preferences_key = 'CustomerTicketZoomCool-FlowCard'" % user_id)
    return '0' if result is None else result
