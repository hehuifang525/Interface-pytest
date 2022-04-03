import pytest
import allure
from .admin_tickettemplate_edit_a.Save.test_cases import check_icon_color, create_common_template
from .admin_tickettemplate_edit_a.TicketTemplateAdd.test_cases import check_normal
from api_testcases.web_user.process.admin_processmanagement_edit_a.ProcessNewAction.test_cases import init_create_process
from api_testcases.web_user.process.admin_processmanagement_edit_a.ProcessNew.test_cases import check_template_attribute
from api_testcases.web_user.process.admin_processmanagement_overview_a.ProcessSync.test_cases import process_sync
from api_testcases.web_user.ticket.ticket_apply_a.GetTicketApplyData.test_cases import page_check_icon_color


@allure.severity('Minor')
@pytest.mark.parametrize('TicketColor', ['#326882', '#e8e252'])
@pytest.mark.parametrize('TemplateIcon', ['wrench', 'book'])
def test_SC_Template_11_13(TicketColor, TemplateIcon):
    """
    SC_Template_11&13-修改颜色，修改图片，二次进入查看，创单页面查看

    :param TicketColor: 模板颜色
    :param TemplateIcon: 模板图片
    """
    template_id = check_icon_color(TicketColor, TemplateIcon)  # 创建工单模板
    init_create_process(template_id)  # 创建流程
    process_sync()  # 部署流程
    page_check_icon_color(TicketColor, TemplateIcon, template_id)  # 创建工单页面检查模板的显示


@allure.severity('Minor')
@pytest.mark.parametrize('TemplateType1,TemplateType', [["CreateNormal", "Deal"], ["Deal", "CreateNormal"]])
@pytest.mark.parametrize('Frontend1,Frontend', [["Agent", "Customer"], ["Customer", "Agent"]])
@pytest.mark.parametrize('ValidID1,ValidID', [["1", "2"], ["2", "1"]])
def test_SC_Template_29_30(TemplateType1, TemplateType, Frontend1, Frontend, ValidID1, ValidID):
    """
    SC_Template_29&30-必填项填写的工单模板创建和编辑检查初始列表值

    :param TemplateType1: 修改前模板类型
    :param TemplateType: 修改后模板类型
    :param Frontend1: 修改前模板使用对象
    :param Frontend: 修改后模板使用对象
    :param ValidID1: 修改前模板有无效
    :param ValidID: 修改后模板有无效
    """
    template_id, TemplateName = create_common_template(Frontend1, TemplateType1, ValidID1)  # 创建工单模板
    check_normal(template_id, TemplateName, Frontend1, TemplateType1, ValidID1)  # 进入模板检查创建填入初始列表值
    list2 = create_common_template(Frontend, TemplateType, ValidID, template_id)  # 编辑工单模板
    check_normal(template_id, list2[1], Frontend, TemplateType, ValidID)  # 二次进入模板检查创建填入初始列表值


@allure.severity('Minor')
@pytest.mark.parametrize('TemplateType', [pytest.param('CreateNormal', id='创建'),
                                          pytest.param('Deal', id='处理')])
@pytest.mark.parametrize('Frontend', [pytest.param('Agent', id='服务人员'),
                                      pytest.param('Customer', id='客户用户')])
def test_SC_Template_31(Frontend, TemplateType):
    """
    SC_Template_31-无效模板（创建/处理模板）不能显示在流程配置页面以供使用
    """
    TemplateID, TemplateName = create_common_template(Frontend, TemplateType, '2')  # 创建工单模板
    check_template_attribute(TemplateID, 'ValidID', '2')
