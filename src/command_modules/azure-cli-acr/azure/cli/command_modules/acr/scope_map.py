# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.util import CLIError

from ._utils import get_resource_group_name_by_registry_name

def _validate_and_parse_actions(actions):
    valid_actions = ['pull', 'push', 'read', 'delete', '*']
    actions = actions.split(',')
    for action in actions:
        is_valid = False
        for valid_action in valid_actions:
            if action == valid_action:
                is_valid = True
        if not is_valid:
            return False, actions
    return True, actions

def _validate_and_generate_actions_from_allowed_repositories(allow_respository):
    actions = []

    for rule in allow_respository:
        splitted = rule.split(',', 2)
        if len(splitted) != 2:
            return False, rule
        repository, actions_allowed = rule[0], rule[1]
        valid_actions, actions_allowed = _validate_and_parse_actions(actions_allowed)
        if not valid_actions:
            return False, rule
        for action_allowed in actions_allowed:
            actions.append("repositories/" + repository + "/" + action_allowed)

    return True, actions

def acr_scope_map_create(cmd,
                          client,
                          registry_name,
                          scope_map_name,
                          allow_repository,
                          resource_group_name=None,
                          description=None):

    validated, actions = _validate_and_generate_actions_from_allowed_repositories(allow_repository)
    if not validated:
        raise CLIError("Rule {} has invalid syntax.".format(actions))

    resource_group_name = get_resource_group_name_by_registry_name(cmd, registry_name, resource_group_name)

    from msrest.exceptions import ValidationError
    try:
        return client.create(
            resource_group_name,
            registry_name,
            scope_map_name,
            actions,
            description
        )
    except ValidationError as e:
        raise CLIError(e)

def acr_scope_map_delete(cmd,
                          client,
                          registry_name,
                          scope_map_name,
                          resource_group_name=None):

    resource_group_name = get_resource_group_name_by_registry_name(cmd, registry_name, resource_group_name)
    return client.delete(resource_group_name, registry_name, scope_map_name)

def acr_scope_map_update(cmd,
                          client,
                          registry_name,
                          scope_map_name,
                          allow_repository=None,
                          resource_group_name=None,
                          description=None):

    if not (allow_repository or description):
        raise CLIError("At least one of the following parameters must be provided: \
                        --allow-repository, --description.")

    validated, actions = _validate_and_generate_actions_from_allowed_repositories(allow_repository)
    if not validated:
        raise CLIError("Rule {} has invalid syntax.".format(actions))

    resource_group_name = get_resource_group_name_by_registry_name(cmd, registry_name, resource_group_name)

    from msrest.exceptions import ValidationError
    try:
        return client.update(
            resource_group_name,
            registry_name,
            scope_map_name,
            actions,
            description
        )
    except ValidationError as e:
        raise CLIError(e)

def acr_scope_map_show(cmd,
                        client,
                        registry_name,
                        scope_map_name,
                        resource_group_name=None):

    resource_group_name = get_resource_group_name_by_registry_name(cmd, registry_name, resource_group_name)

    from msrest.exceptions import ValidationError
    try:
        return client.get(
            resource_group_name,
            registry_name,
            scope_map_name
        )
    except ValidationError as e:
        raise CLIError(e)

def acr_scope_map_list(cmd,
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
