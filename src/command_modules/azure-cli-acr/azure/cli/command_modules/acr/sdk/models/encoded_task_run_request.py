# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from .run_request import RunRequest


class EncodedTaskRunRequest(RunRequest):
    """The parameters for a quick task run request.

    :param is_archive_enabled: The value that indicates whether archiving is
     enabled for the run or not. Default value: False .
    :type is_archive_enabled: bool
    :param type: Constant filled by server.
    :type type: str
    :param encoded_task_content: Base64 encoded value of the
     template/definition file content.
    :type encoded_task_content: str
    :param encoded_values_content: Base64 encoded value of the
     parameters/values file content.
    :type encoded_values_content: str
    :param values: The collection of overridable values that can be passed
     when running a task.
    :type values:
     list[~azure.mgmt.containerregistry.v2019_05_01_preview.models.SetValue]
    :param timeout: Run timeout in seconds. Default value: 3600 .
    :type timeout: int
    :param platform: The platform properties against which the run has to
     happen.
    :type platform:
     ~azure.mgmt.containerregistry.v2019_05_01_preview.models.PlatformProperties
    :param agent_configuration: The machine configuration of the run agent.
    :type agent_configuration:
     ~azure.mgmt.containerregistry.v2019_05_01_preview.models.AgentProperties
    :param source_location: The URL(absolute or relative) of the source
     context. It can be an URL to a tar or git repository.
     If it is relative URL, the relative path should be obtained from calling
     listBuildSourceUploadUrl API.
    :type source_location: str
    :param credentials: The properties that describes a set of credentials
     that will be used when this run is invoked.
    :type credentials:
     ~azure.mgmt.containerregistry.v2019_05_01_preview.models.Credentials
    """

    _validation = {
        'type': {'required': True},
        'encoded_task_content': {'required': True},
        'timeout': {'maximum': 28800, 'minimum': 300},
        'platform': {'required': True},
    }

    _attribute_map = {
        'is_archive_enabled': {'key': 'isArchiveEnabled', 'type': 'bool'},
        'type': {'key': 'type', 'type': 'str'},
        'encoded_task_content': {'key': 'encodedTaskContent', 'type': 'str'},
        'encoded_values_content': {'key': 'encodedValuesContent', 'type': 'str'},
        'values': {'key': 'values', 'type': '[SetValue]'},
        'timeout': {'key': 'timeout', 'type': 'int'},
        'platform': {'key': 'platform', 'type': 'PlatformProperties'},
        'agent_configuration': {'key': 'agentConfiguration', 'type': 'AgentProperties'},
        'source_location': {'key': 'sourceLocation', 'type': 'str'},
        'credentials': {'key': 'credentials', 'type': 'Credentials'},
    }

    def __init__(self, encoded_task_content, platform, is_archive_enabled=False, encoded_values_content=None, values=None, timeout=3600, agent_configuration=None, source_location=None, credentials=None):
        super(EncodedTaskRunRequest, self).__init__(is_archive_enabled=is_archive_enabled)
        self.encoded_task_content = encoded_task_content
        self.encoded_values_content = encoded_values_content
        self.values = values
        self.timeout = timeout
        self.platform = platform
        self.agent_configuration = agent_configuration
        self.source_location = source_location
        self.credentials = credentials
        self.type = 'EncodedTaskRunRequest'
