import pytest
import allure
from .admin_processmanagement_edit_a.ProcessNewAction.test_cases import init_create_process
from .admin_processmanagement_overview_a.ProcessTypeAddAction.test_cases import init_create_processType
from .admin_processmanagement_overview_a.ProcessSync.test_cases import process_sync


@pytest.mark.run(order=5)
@allure.severity('Blocker')
def test_init_process():
    """
    创建初始化流程类型和流程
    """
    processType_id = init_create_processType()  # 创建流程类型
    init_create_process(processType_id)  # 创建流程
    process_sync()  # 部署流程
