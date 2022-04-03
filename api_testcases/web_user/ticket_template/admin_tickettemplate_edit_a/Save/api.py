from base.common import mysql_get_value, config_write


def common_data(Frontend, TemplateType, TemplateName):
    """
    创建工单模板默认请求body

    :param Frontend: 使用对象，Agent服务人员，Customer客户用户
    :param TemplateType: 工单模板类型，CreateNormal创建，Deal处理
    :param TemplateName: 工单模板名称
    """
    data_body = {
                "ValidID": "1",
                "TicketColor": "#99ABB4",
                "Frontend": Frontend,
                "TemplateType": TemplateType,
                "TemplateIcon": "award",
                "Name": TemplateName,
                "ShowLocation": [
                    "web",
                    "windows",
                    "mobile"
                ],
                "TypeID_display": "2",
                "CustomerUser_display": "1",
                "CustomerID_display": "3",
                "ConfigItems_display": "1",
                "QueueID_display": "2",
                "OwnerID_display": "1",
                "ResponsibleID_display": "1",
                "Subject_display": "2",
                "Body_display": "2",
                "StateID_display": "2",
                "PriorityID_display": "2",
                "DefalutFieldOrder": [
                    "TypeID",
                    "CustomerUser",
                    "CustomerID",
                    "ConfigItems",
                    "QueueID",
                    "OwnerID",
                    "ResponsibleID",
                    "Subject",
                    "Body",
                    "StateID",
                    "PriorityID"
                ]
            }
    return data_body


def common_assert(Frontend, TemplateType, TemplateName, re_json):
    """
    创建工单模板固定校验

    :param Frontend: 使用对象，Agent服务人员，Customer客户用户
    :param TemplateType: 工单模板类型，CreateNormal创建，Deal处理
    :param TemplateName: 工单模板名称
    :param re_json: 请求返回的json格式
    :return: 模板ID
    """
    template_id = re_json['data']['templateData']['TemplateID']
    assert re_json['data']['templateData']['Name'] == TemplateName, "接口返回的模板名称"
    assert mysql_get_value('ticket_template_c', 'name', 'id', template_id) == TemplateName, "数据库中保存的模板名称"
    assert mysql_get_value('ticket_template_c', 'template_type', 'id', template_id) == TemplateType, "数据库中保存的模板类型"
    assert mysql_get_value('ticket_template_c', 'available_in', 'id', template_id) == Frontend, "数据库中保存的模板使用对象"
    config_write('ticket_init', "%s-%s" % (Frontend, TemplateType), template_id)
    return template_id
