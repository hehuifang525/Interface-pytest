from api_testcases.web_user.action_re_body import action_body
from base.common import mysql_get_value, config_write, get_32_random, config_get_list_value


def init_data(process_name, processType_id):
    """
    创建流程初始化请求body

    :param process_name: 流程名称
    :param processType_id: 流程类型ID
    """
    StartNode = "Node-%s" % get_32_random()
    EndNode = "Node-%s" % get_32_random()
    ProcessNode1 = "Node-%s" % get_32_random()
    ProcessNode2 = "Node-%s" % get_32_random()
    Transition1 = "Transition-%s" % get_32_random()
    Transition2 = "Transition-%s" % get_32_random()
    Transition3 = "Transition-%s" % get_32_random()
    data_body = {
        "processName": process_name,
        "processStateEntityID": "S1",
        "processType": processType_id,
        "processDescription": "Hrun创建测试流程",
        "processConfig": {
            "StartNode": StartNode,
            "Path": {
                StartNode: {
                    Transition1: {
                        "NextNode": ProcessNode1,
                        "TransitionAction": []
                    }
                },
                ProcessNode1: {
                    Transition2: {
                        "NextNode": ProcessNode2,
                        "TransitionAction": []
                    }
                },
                ProcessNode2: {
                    Transition3: {
                        "NextNode": EndNode,
                        "TransitionAction": []
                    }
                },
                EndNode: {}
            },
            "EndNode": EndNode,
            "Description": "",
            "FirstNode": ProcessNode1,
            "transitionActionValue": {},
            "groupInfo": {
                "order": [],
                "value": {}
            }
        },
        "nodeLocation": {
            StartNode: {
                "left": "350px",
                "top": "100px"
            },
            EndNode: {
                "left": "349px",
                "top": "407px"
            },
            ProcessNode1: {
                "left": "295px",
                "top": "190px"
            },
            ProcessNode2: {
                "left": "285px",
                "top": "280px"
            }
        },
        "nodeValue": {
            StartNode: {
                "id": "",
                "templateList": [],
                "name": "Start"
            },
            EndNode: {
                "id": "",
                "templateList": [],
                "name": "End"
            },
            ProcessNode1: {
                "id": "",
                "templateList": config_get_list_value('ticket_init', ["Agent-CreateNormal", "Customer-CreateNormal"]),
                "name": "Process node1"
            },
            ProcessNode2: {
                "id": "",
                "templateList": config_get_list_value('ticket_init', ["Agent-Deal", "Customer-Deal"]),
                "name": "Process node2"
            }
        },
        "transitionValue": {
            Transition1: {
                "conditionLinking": "or",
                "conditionName": "Process transition1",
                "Count": [],
                "id": "",
                "Condition": {}
            },
            Transition2: {
                "conditionLinking": "or",
                "conditionName": "Process transition2",
                "Count": [1],
                "sourceP": "Bottom",
                "targetP": "Top",
                "id": "",
                "Condition": {
                    "1": {
                        "Fields": {
                            "order": [
                                {
                                    "id": 1,
                                    "key": "TypeID"
                                }
                            ],
                            "TypeID": {
                                "FieldName": "TypeID",
                                "FieldType": "Dropdown",
                                "Compare": "ioo",
                                "FieldValue": ["1", "2", "3", "4", "5"]
                            }
                        },
                        "Type": "or"
                    }
                }
            },
            Transition3: {
                "conditionLinking": "or",
                "conditionName": "Process transition3",
                "Count": [],
                "sourceP": "Bottom",
                "targetP": "Top",
                "id": "",
                "Condition": {}
            }
        },
        "processID": "",
        "nodeDelete": [],
        "transitionDelete": [
            ""
        ],
        "transitionActionDelete": []
    }
    return data_body, [StartNode, EndNode, ProcessNode1, ProcessNode2], [Transition1, Transition2, Transition3]


def common_assert(processType_id, process_id, process_name):
    """
    创建流程固定校验

    :param processType_id: 流程类型ID
    :param process_id: 流程ID
    :param process_name: 流程名称
    """
    assert mysql_get_value('pm_process_c', 'name', 'id', process_id) == process_name, "流程数据库中的流程名称"
    assert mysql_get_value('pm_process_c', 'process_type', 'id', process_id) == processType_id, "流程数据库中的流程类型ID"
    assert mysql_get_value('pm_process_c', 'state_entity_id', 'id', process_id) == "S1", "流程数据库中的流程状态"
