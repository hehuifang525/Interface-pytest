import pytest
import allure
from .admin_fieldlib_edit_a.AddAction.test_cases import init_text
from .admin_fieldlib_edit_a.Change.test_cases import get_form_id
from .admin_fieldlib_edit_a.AttachmentUpload.test_cases import upload_attachment
from .admin_fieldlib_edit_a.ChangeAction.test_cases import get_tree_cascader_change


@pytest.mark.run(order=2)
@allure.severity('Blocker')
@pytest.mark.parametrize('FieldType', [pytest.param('TreeCascader', id='级联字段')])
@pytest.mark.parametrize('ObjectType', ['Ticket'])
def test_init_treecascader(ObjectType, FieldType):
    """
    创建自定义字段-级联字段初始化

    :param ObjectType: 系统字段对象
    :param FieldType: 字段类型
    """
    field_id, field_name = init_text(ObjectType, FieldType)  # 创建级联字段
    form_id = get_form_id(field_id)  # 查看级联字段的FormID
    upload_attachment(form_id, "api_testcases/web_user/fieldlib/admin_fieldlib_edit_a/AttachmentUpload/data"
                               "/ticket_init_treecascader.xlsx")  # 上传附件
    # 提交编辑级联字段
    SelectOptions = ["测试1::测试1-1::测试1-1-1::测试1-1-1-1", "测试1::测试1-1::测试1-1-1::测试1-1-1-2",
                     "测试1::测试1-1::测试1-1-1::测试1-1-1-3", "测试1::测试1-1::测试1-1-2::测试1-1-2-1",
                     "测试1::测试1-1::测试1-1-3", "测试1::测试1-2", "测试2", "测试3::测试3-1", "测试3::测试3-2::测试3-2-1"]
    add_body = {"CascaderField": ["产品一级分类", "产品二级分类", "产品三级分类", "产品四级分类"]}
    get_tree_cascader_change(ObjectType, field_name, SelectOptions, field_id, form_id, add_body)
