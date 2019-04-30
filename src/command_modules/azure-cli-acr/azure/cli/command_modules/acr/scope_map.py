# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.util import CLIError

from ._utils import get_resource_group_name_by_registry_name

def _validate_and_parse_actions(actions):
    valid_actions = ['contentWrite', 'contentRead', 'contentDelete', 'read', 'write', 'delete']
    actions = actions.split(',')
    for action in actions:
        is_valid = False
        for valid_action in valid_actions:
            if action == valid_action:
                is_valid = True
        if not is_valid:
            return False, actions
    return True, actions

def _validate_and_generate_actions_from_repositories(allow_or_deny_respository):
    actions = []

    for rule in allow_or_deny_respository:
        splitted = rule.split(',', 2)
        if len(splitted) != 2:
            return False, rule
        repository, actions_allowed = splitted[0], splitted[1]
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

    validated, actions = _validate_and_generate_actions_from_repositories(allow_repository)
    if not validated:
        raise CLIError("Rule {} has invalid syntax.".format(actions))
    actions.sort()

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
                         deny_repository=None,
                         reset_map=None,
                         resource_group_name=None,
                         description=None):

    if not (allow_repository or deny_repository or reset_map or description):
        raise CLIError("At least one of the following parameters must be provided: \
                        --allow-repository, --deny-repository, --reset, --description.")

    current_scope_map = acr_scope_map_show(cmd, client, registry_name, scope_map_name, resource_group_name)

    if reset_map:
        current_actions = []
    else:
        current_actions = current_scope_map.actions

    if description is None:
        description = current_scope_map.description

    if deny_repository is not None:
        validated, removed_actions = _validate_and_generate_actions_from_repositories(deny_repository)
        if not validated:
            raise CLIError("Rule {} has invalid syntax.".format(removed_actions))
        current_actions = list(set(current_actions) - set(removed_actions))

    if allow_repository is not None:
        validated, added_actions = _validate_and_generate_actions_from_repositories(allow_repository)
        if not validated:
            raise CLIError("Rule {} has invalid syntax.".format(added_actions))
        current_actions = list(set(current_actions) | set(added_actions))

    current_actions.sort()

    resource_group_name = get_resource_group_name_by_registry_name(cmd, registry_name, resource_group_name)

    from msrest.exceptions import ValidationError
    try:
        return client.update(
            resource_group_name,
            registry_name,
            scope_map_name,
            description,
            current_actions
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
