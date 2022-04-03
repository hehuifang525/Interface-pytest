from base.common import mysql_get_list


def get_user_role(user):
    """
    根据user_id来获取服务人员对应的角色列表

    :param user: user用户名
    """
    if user == "0":
        return 0
    result = mysql_get_list("queue_user", "queue_id", "user_id", user)
    return result
