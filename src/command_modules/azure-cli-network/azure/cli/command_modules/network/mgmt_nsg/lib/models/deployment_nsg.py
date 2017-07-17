# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
#pylint: skip-file
# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator 0.17.0.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DeploymentNsg(Model):
    """
    Deployment operation parameters.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar uri: URI referencing the template. Default value:
     "https://azuresdkci.blob.core.windows.net/templatehost/CreateNsg_2016-07-18/azuredeploy.json"
     .
    :vartype uri: str
    :param content_version: If included it must match the ContentVersion in
     the template.
    :type content_version: str
    :param location: Location for the network security group.
    :type location: str
    :param name: Name of the network security group.
    :type name: str
    :param tags: Tags object.
    :type tags: object
    :ivar mode: Gets or sets the deployment mode. Default value:
     "Incremental" .
    :vartype mode: str
    """ 

    _validation = {
        'uri': {'required': True, 'constant': True},
        'name': {'required': True},
        'mode': {'required': True, 'constant': True},
    }

    _attribute_map = {
        'uri': {'key': 'properties.templateLink.uri', 'type': 'str'},
        'content_version': {'key': 'properties.templateLink.contentVersion', 'type': 'str'},
        'location': {'key': 'properties.parameters.location.value', 'type': 'str'},
        'name': {'key': 'properties.parameters.name.value', 'type': 'str'},
        'tags': {'key': 'properties.parameters.tags.value', 'type': 'object'},
        'mode': {'key': 'properties.mode', 'type': 'str'},
    }

    uri = "https://azuresdkci.blob.core.windows.net/templatehost/CreateNsg_2016-07-18/azuredeploy.json"

    mode = "Incremental"

    def __init__(self, name, content_version=None, location=None, tags=None):
        self.content_version = content_version
        self.location = location
        self.name = name
        self.tags = tags