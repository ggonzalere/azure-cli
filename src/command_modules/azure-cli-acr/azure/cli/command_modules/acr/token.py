# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.util import CLIError

from ._utils import get_resource_group_name_by_registry_name

def acr_token_create(cmd,
                     client,
                     registry_name,
                     token_name,
                     scope_map_name,
                     resource_group_name=None):

    resource_group_name = get_resource_group_name_by_registry_name(cmd, registry_name, resource_group_name)

    from ._constants import REGISTRY_RESOURCE_TYPE
    from ._utils import _arm_get_resource_by_name

    registry_id = _arm_get_resource_by_name(cmd.cli_ctx, registry_name, REGISTRY_RESOURCE_TYPE)
    scope_map_id = registry_id + "/scopeMaps/" + scope_map_name

    from msrest.exceptions import ValidationError
    try:
        return client.create(
            resource_group_name,
            registry_name,
            token_name,
            scope_map_id
        )
    except ValidationError as e:
        raise CLIError(e)

def acr_token_delete(cmd,
                     client,
                     registry_name,
                     token_name,
                     resource_group_name=None):

    resource_group_name = get_resource_group_name_by_registry_name(cmd, registry_name, resource_group_name)
    return client.delete(resource_group_name, registry_name, token_name)

def acr_token_update(cmd,
                     client,
                     registry_name,
                     token_name,
                     scope_map_name,
                     resource_group_name=None):

    resource_group_name = get_resource_group_name_by_registry_name(cmd, registry_name, resource_group_name)

    from ._constants import REGISTRY_RESOURCE_TYPE
    from ._utils import _arm_get_resource_by_name

    registry_id = _arm_get_resource_by_name(cmd.cli_ctx, registry_name, REGISTRY_RESOURCE_TYPE)
    scope_map_id = registry_id + "/scopeMaps/" + scope_map_name

    from msrest.exceptions import ValidationError
    try:
        return client.update(
            resource_group_name,
            registry_name,
            token_name,
            scope_map_id
        )
    except ValidationError as e:
        raise CLIError(e)

def acr_token_show(cmd,
                   client,
                   registry_name,
                   token_name,
                   resource_group_name=None):

    resource_group_name = get_resource_group_name_by_registry_name(cmd, registry_name, resource_group_name)

    from msrest.exceptions import ValidationError
    try:
        return client.get(
            resource_group_name,
            registry_name,
            token_name
        )
    except ValidationError as e:
        raise CLIError(e)

def acr_token_list(cmd,
                   client,
                   registry_name,
                   resource_group_name=None):

    resource_group_name = get_resource_group_name_by_registry_name(cmd, registry_name, resource_group_name)

    from msrest.exceptions import ValidationError
    try:
        return client.list(
            resource_group_name,
            registry_name
        )
    except ValidationError as e:
        raise CLIError(e)

# Credential functions

def acr_token_credential_list(cmd,
                              client,
                              registry_name,
                              token_name,
                              certificate=None):

    pass

def acr_token_credential_reset(cmd,
                               client,
                               registry_name,
                               token_name,
                               certificate=None,
                               create_certificate=None,
                               end_date=None,
                               years=1):

    import datetime
    from dateutil.parser import parse

    if not end_date:
        end_date_datetime = datetime.datetime.now() + datetime.timedelta(days=365*years)
    else:
        try:
            end_date_datetime = parse(end_date)
        except ValueError:
            raise CLIError("Format {} is invalid or not supported. Please tr another date format.".format(end_date))

def acr_token_credential_delete(cmd,
                                client,
                                registry_name,
                                token_name,
                                key_id,
                                certificate=None):
    pass
