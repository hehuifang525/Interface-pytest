from base.common import mysql_get_value, config_write


def common_data(district_name, parent_id=None, valid_id=1, comment=None,districtd_id=None):
    """
     :param       district_name:区域名称
     :param       parent_id：父区域id
     :param       valid_id：有效性
     :param       comment：备注
     :param       districtd_id: 区域id
    """
    if districtd_id is None:
        data_body = {
            "ValidID": valid_id,
            "Name": district_name,
            "ParentID": parent_id,
            "Comment": comment

        }
    else:
        data_body = {
            "ValidID": valid_id,
            "Name": district_name,
            "ParentID": parent_id,
            "Comment": comment,
            "DistrictID":districtd_id

        }

    return data_body



