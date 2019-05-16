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
                     scope_map_name=None,
                     certificates=None,
                     resource_group_name=None):

    resource_group_name = get_resource_group_name_by_registry_name(cmd, registry_name, resource_group_name)

    from ._constants import REGISTRY_RESOURCE_TYPE
    from ._utils import _arm_get_resource_by_name

    token_create_parameters = {}

    if scope_map_name:
        arm_resource = _arm_get_resource_by_name(cmd.cli_ctx, registry_name, REGISTRY_RESOURCE_TYPE)
        scope_map_id = arm_resource.id + "/scopeMaps/" + scope_map_name
        token_create_parameters["ScopeMapId"] = scope_map_id

    certificates = _certificate_handler(certificates)
    if certificates:
        token_create_parameters["Credentials"] = {
            "Certificates": certificates
        }

    from msrest.exceptions import ValidationError
    try:
        return client.create(
            resource_group_name,
            registry_name,
            token_name,
            token_create_parameters
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
                     scope_map_name=None,
                     resource_group_name=None):

    resource_group_name = get_resource_group_name_by_registry_name(cmd, registry_name, resource_group_name)

    from ._constants import REGISTRY_RESOURCE_TYPE
    from ._utils import _arm_get_resource_by_name

    if scope_map_name is not None:
        arm_resource = _arm_get_resource_by_name(cmd.cli_ctx, registry_name, REGISTRY_RESOURCE_TYPE)
        scope_map_id = arm_resource.id + "/scopeMaps/" + scope_map_name
    else:
        scope_map_id = None

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

def acr_token_credential_generate(cmd,
                                  client,
                                  registry_name,
                                  token_name,
                                  resource_group_name=None):

    from ._constants import REGISTRY_RESOURCE_TYPE
    from ._utils import _arm_get_resource_by_name
    from msrest.exceptions import ValidationError

    resource_group_name = get_resource_group_name_by_registry_name(cmd, registry_name, resource_group_name)
    arm_resource = _arm_get_resource_by_name(cmd.cli_ctx, registry_name, REGISTRY_RESOURCE_TYPE)
    token_id = arm_resource.id + "/tokens/" + token_name
    generate_credentials_parameters = {"TokenId": token_id}

    try:
        return client.generate_credentials(
            resource_group_name,
            registry_name,
            generate_credentials_parameters
        )
    except ValidationError as e:
        raise CLIError(e)

def acr_token_credential_list(cmd,
                              client,
                              registry_name,
                              token_name,
                              certificate=None,
                              resource_group_name=None):

    certificate = _certificate_handler(certificate)

def acr_token_credential_reset(cmd,
                               client,
                               registry_name,
                               token_name,
                               certificate=None,
                               create_certificate=None,
                               end_date=None,
                               years=1,
                               resource_group_name=None):

    import datetime
    from dateutil.parser import parse

    if not end_date:
        end_date_datetime = datetime.datetime.now() + datetime.timedelta(days=365*years)
    else:
        try:
            end_date_datetime = parse(end_date)
        except ValueError:
            raise CLIError("Format {} is invalid or not supported. Please tr another date format.".format(end_date))

    certificate = _certificate_handler(certificate)

def acr_token_credential_delete(cmd,
                                client,
                                registry_name,
                                token_name,
                                key_id,
                                certificate=None,
                                resource_group_name=None):
    return "Not implemented"

# Utilities functions

def _certificate_handler(certificates):
    from base64 import b64encode
    parsed_certificates = []
    names = ["certificate1", "certificate2"]
    total = 0

    if certificates is not None:
        for certificate in certificates:
            if total >= 2:
                break
            try:
                certificate_file = open(certificate, "r")
                certificate_content = certificate_file.read()
                certificate_b64 = b64encode(certificate_content.encode())
                certificate_b64 = str(certificate_b64.decode())
                parsed_certificates.append({
                    "Name": names[total],
                    "EncodedPEMCertificate": certificate_b64
                })
                total = total + 1
            except IOError as e:
                raise CLIError('Could not read certificate {}. Exception: {}'.format(certificate, str(e)))

    return parsed_certificates
