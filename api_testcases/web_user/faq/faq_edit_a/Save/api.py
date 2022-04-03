from base.common import mysql_get_value, config_write


def common_data(title, body_content, category_id_parent, valid_id="1", item_id=""):
    """
     :param       title:分类名称
     :param       body_content：内容
     :param       category_id_parent：父id
     :param       valid_id：有效性
     :param       Attachment：附件
     :param       TopEndTime：  置顶开始时间
     :param       Keywords：关键字
     :param       TopStartTime：置顶结束时间
     :param       EffectiveStartTime：有效启用时间
     :param       EffectiveEndTime：有效停止时间
     :param       Top：置顶
     :param       StateID：状态(内外部)
     :param       Effective：
     :param       EffectiveContinueTime：
     :param       FormID：
     :param       item_id：  当前文章id
    """

    data_body = {
        'ValidID': valid_id,
        'Attachment': None,
        'Field1': body_content,
        'CategoryID': category_id_parent,
        'TopEndTime': None,
        'Keywords': None,
        'Title': title,
        'TopStartTime': None,
        'EffectiveStartTime': None,
        'EffectiveEndTime': None,
        'Top': '1',
        'StateID': '2',
        'Effective': '1',
        'EffectiveContinueTime': '0',
        'TopContinueTime': '0',
        'FormID': '1644394660.6735998.25663008',   # 必须有
        'ItemID': item_id
    }
    return data_body


def common_assert(faq_name,  re_json):
    """
    创建知识库文章的的固定校验

    :param faq_name: 知识库概览中，新增知识库文章名称
    :param re_json: 请求返回的json格式
    """
    faq_id = mysql_get_value("faq_item", "id", "f_subject", faq_name, "")
    assert re_json["data"]["message"] == "Added successfully!", "添加成功提示"
    assert re_json["data"]["data"]["ItemID"] == faq_id, "接口返回的知识库文章id校验"

