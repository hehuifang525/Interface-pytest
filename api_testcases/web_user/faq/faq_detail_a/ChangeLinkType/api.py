from base.common import mysql_get_value, config_write


def common_add_link_data(faq_id, link_type, link_target_keys):
    """
    添加链接
     :param       faq_id: 链接的知识库文章id
     :param       link_type：链接类型
     :param       link_target_keys：链接的对应id_list

    """
    data_body = {
        "TypeIdentifier": "Normal::Source",
        "SourceObject": "FAQ",
        "LinkTargetKeys": [link_target_keys],
        "SourceKey": str(faq_id),
        "TargetIdentifier": {"TargetObject": link_type, "TargetKey": ""},
        "Method": "AddLink"}

    return data_body


def common_del_link_data(faq_id, link_type, ticket_id):
    """
    添加链接
     :param       faq_id: 链接的知识库文章id
     :param       link_type：链接类型 Ticket,FAQ,ITSMConfigItem
     :param       link_target_keys：链接的对应id_list

    """
    data_body = {
        "SourceObject":"FAQ",
        "SourceKey":faq_id,
        "LinkDeleteIdentifier": [link_type +"::"+ ticket_id +"::Normal"],
        "Method":"LinkDelete"}
    return data_body