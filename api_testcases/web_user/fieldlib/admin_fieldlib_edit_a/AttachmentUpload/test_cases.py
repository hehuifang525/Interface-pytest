import pytest
import allure
import ntpath
from api_testcases.web_user.action_re_body import *
from base.common import send_request, success_assert, mysql_get_value, config_read


def params(form_id):
    """
    上传附件固定请求body
    """
    params_body = {
                    "Action": "admin_fieldlib_edit_a",
                    "Subaction": "AttachmentUpload",
                    "FormID": form_id,
                    "menuKey": "admin_fieldlib_edit_a",
                    "OTRSAgentInterface": config_read('ServiceCool', 'OTRSAgentInterface')
                }
    return params_body


@allure.severity('normal')
@allure.step('上传文件')
def upload_attachment(form_id, file_path):
    """
    上传文件
    """
    result = send_request(method, url, headers=headers(), params=params(form_id), file_path=file_path)
    re_json = result.json()

    assert result.status_code == 200, "请求状态码"
    file_name = ntpath.basename(file_path)
    assert re_json[0]['Filename'] == file_name, "文件名"
    assert re_json[0]['Disposition'] == "attachment", "附件标识"
    assert re_json[0]['ContentType'] == mysql_get_value('web_upload_cache', 'content_type', 'form_id', form_id), "文件类型"
    assert file_name == mysql_get_value('web_upload_cache', 'filename', 'form_id', form_id), "文件名"
