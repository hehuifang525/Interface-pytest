from base.common import mysql_get_value, config_write


def common_data(name, parent_id=None, valid_id="1", comment=None):
    """
     :param       name:分类名称
     :param       parent_id：父id
     :param       valid_id：有效性
     :param       comment：备注
    """

    data_body = {
        "ValidID": valid_id,
        "Name": name,
        "ParentID": parent_id,
        "Comment": comment

    }
    return data_body


def common_assert(faq_category_name, re_json):
    """
    创建知识库类别固定校验

    :param faq_category_name: 知识库概览中，新增知识库文章名称
    :param re_json: 请求返回的json格式
    """
    category_id = mysql_get_value("faq_category", "id", "NAME", faq_category_name, "")
    assert re_json["data"]["message"] == "Added successfully!", "添加成功提示"
    assert re_json["data"]["data"]["CategoryID"] == category_id, "接口返回的知识库分类id"



