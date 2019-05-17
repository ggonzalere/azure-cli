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
                     resource_group_name=None):

    resource_group_name = get_resource_group_name_by_registry_name(cmd, registry_name, resource_group_name)

    from ._constants import REGISTRY_RESOURCE_TYPE
    from ._utils import _arm_get_resource_by_name

    token_create_parameters = { 
        "Properties": {
            "ScopeMapId": None,
            "Credentials": {
                "Certificates": []
            }
        }
    }

    if scope_map_name:
        arm_resource = _arm_get_resource_by_name(cmd.cli_ctx, registry_name, REGISTRY_RESOURCE_TYPE)
        scope_map_id = arm_resource.id + "/scopeMaps/" + scope_map_name
        token_create_parameters["Properties"]["ScopeMapId"] = scope_map_id

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

    token_update_parameters = { "ScopeMapId": scope_map_id }

    from msrest.exceptions import ValidationError
    try:
        return client.update(
            resource_group_name,
            registry_name,
            token_name,
            token_update_parameters
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
                                  password1=False,
                                  password2=False,
                                  expiry=None,
                                  years=None,
                                  resource_group_name=None):

    from ._constants import REGISTRY_RESOURCE_TYPE
    from ._utils import _arm_get_resource_by_name
    from msrest.exceptions import ValidationError

    resource_group_name = get_resource_group_name_by_registry_name(cmd, registry_name, resource_group_name)
    arm_resource = _arm_get_resource_by_name(cmd.cli_ctx, registry_name, REGISTRY_RESOURCE_TYPE)
    token_id = arm_resource.id + "/tokens/" + token_name
    generate_credentials_parameters = {"TokenId": token_id}

    if password1 ^ password2: # We only want to specify a password if only one wass passed.
        generate_credentials_parameters["Name"] = "password1" if password1 else "password2"

    if expiry:
        generate_credentials_parameters["Expiry"] = expiry
    elif years is not None:
        if int(years) <= 0:
            raise CLIError("Number of years must be positive.")
        from datetime import datetime
        expiry_date = datetime.now()
        expiry_date = expiry_date.replace(year=min(expiry_date.year + int(years), 9999))
        generate_credentials_parameters["Expiry"] = expiry_date.isoformat(sep='T')

    try:
        return client.generate_credentials(
            resource_group_name,
            registry_name,
            generate_credentials_parameters
        )
    except ValidationError as e:
        raise CLIError(e)


def acr_token_credential_delete(cmd,
                                client,
                                registry_name,
                                token_name,
                                certificate1=False,
                                certificate2=False,
                                password1=False,
                                password2=False,
                                resource_group_name=None):

    if (certificate1 or certificate2 or password1 or password2) is False:
        raise CLIError("Nothing to delete")

    token = acr_token_show(cmd,
                           client,
                           registry_name,
                           token_name,
                           resource_group_name)

    new_certificates = token.credentials.certificates
    if certificate1:
        new_certificates = [cert for cert in new_certificates if cert.name != "certificate1"]
    if certificate2:
        new_certificates = [cert for cert in new_certificates if cert.name != "certificate2"]

    new_certificates_payload = []
    for cert in new_certificates:
        new_certificates_payload.append({
            "Name": cert.name
        })

    new_passwords = token.credentials.passwords
    if password1:
        new_passwords = [password for password in new_passwords if password.name != "password1"]
    if password2:
        new_passwords = [password for password in new_passwords if password.name != "password2"]

    new_passwords_payload = []
    for password in new_passwords:
        new_passwords_payload.append({
            "Name": password.name
        })

    token_update_parameters = {
        "Credentials": {
            "Certificates": new_certificates_payload,
            "Passwords": new_passwords_payload
        }
    }

    from msrest.exceptions import ValidationError
    try:
        return client.update(
            resource_group_name,
            registry_name,
            token_name,
            token_update_parameters
        )
    except ValidationError as e:
        raise CLIError(e)


def acr_token_credential_add_certificate(cmd,
                                         client,
                                         registry_name,
                                         token_name,
                                         certificate1=None,
                                         certificate2=None,
                                         resource_group_name=None):

    if certificate1 is None and certificate2 is None:
        raise CLIError("At least one of the certificates must be provided")

    token = acr_token_show(cmd,
                           client,
                           registry_name,
                           token_name,
                           resource_group_name)

    certificates_dict = {}
    for certificate in token.credentials.certificates:
        certificates_dict[certificate.name] = None
    certificates_dict = _handle_add_certificate(certificates_dict, certificate1, certificate2)

    certificates_payload = []
    for key in certificates_dict:
        value = certificates_dict[key]
        if value:
            certificate = {
                "Name": key,
                "EncodedPEMCertificate": value
            }
        else:
            certificate = {
                "Name": key
            }
        certificates_payload.append(certificate)

    certificates_payload.sort(key = lambda cert: cert["Name"])

    token_update_parameters = {
        "Credentials": {
            "Certificates": certificates_payload
        }
    }
    
    from msrest.exceptions import ValidationError
    try:
        return client.update(
            resource_group_name,
            registry_name,
            token_name,
            token_update_parameters
        )
    except ValidationError as e:
        raise CLIError(e)


def _handle_add_certificate(certificates_dict, certificate1, certificate2):
    from base64 import b64encode

    if certificate1:
        try:
            certificate1_content = open(certificate1, "r").read()
            certificate1_b64 = b64encode(certificate1_content.encode())
            certificate1_b64 = str(certificate1_b64.decode())
            certificates_dict["certificate1"] = certificate1_b64
        except IOError as e:
            raise CLIError("Could not read certificate {}. Exception: {}".format(certificate1, str(e)))

    if certificate2:
        try:
            certificate2_content = open(certificate2, "r").read()
            certificate2_b64 = b64encode(certificate2_content.encode())
            certificate2_b64 = str(certificate2_b64.decode())
            certificates_dict["certificate2"] = certificate2_b64
        except IOError as e:
            raise CLIError("Could not read certificate {}. Exception: {}".format(certificate1, str(e)))

    return certificates_dict
