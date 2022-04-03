from base.common import mysql_get_value, config_write


def common_data(name,
                valid_id="1",
                service_id="",
                children_service=None,
                external_comments=None,
                internal_comments=None):
    """
        创建服务请求body

        :param name: 服务名称
        :param valid_id: 有效性ID
        :param service_id: 服务ID
        :param children_service: 属于服务
        :param external_comments: 外部备注
        :param internal_comments: 内部备注
    """
    data_body = {
        "ValidID": valid_id,
        "Name": name,
        "ExternalComments": external_comments,
        "ChildrenService": children_service,
        "InternalComments": internal_comments,
        "ServiceID": service_id,
        "IsLeaf": 0}
    return data_body

