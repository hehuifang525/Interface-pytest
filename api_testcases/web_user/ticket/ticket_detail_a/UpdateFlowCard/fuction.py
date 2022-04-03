from base.common import mysql_get_value


def ticket_flow_card_default(user_id):
    """
    获取当前账号user_id默认工单信件展开方式值
    """
    result = mysql_get_value('user_preferences', 'preferences_value', '', '',
                             "user_id = %s AND preferences_key = 'AgentTicketZoomCool-FlowCard'" % user_id)
    return '0' if result is None else result
