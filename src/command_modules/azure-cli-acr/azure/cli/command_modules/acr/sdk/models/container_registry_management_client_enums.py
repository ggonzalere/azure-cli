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

from enum import Enum


class ImportMode(Enum):

    no_force = "NoForce"
    force = "Force"


class SkuName(Enum):

    classic = "Classic"
    basic = "Basic"
    standard = "Standard"
    premium = "Premium"


class SkuTier(Enum):

    classic = "Classic"
    basic = "Basic"
    standard = "Standard"
    premium = "Premium"


class ProvisioningState(Enum):

    creating = "Creating"
    updating = "Updating"
    deleting = "Deleting"
    succeeded = "Succeeded"
    failed = "Failed"
    canceled = "Canceled"


class DefaultAction(Enum):

    allow = "Allow"
    deny = "Deny"


class Action(Enum):

    allow = "Allow"


class PasswordName(Enum):

    password = "password"
    password2 = "password2"


class RegistryUsageUnit(Enum):

    count = "Count"
    bytes = "Bytes"


class PolicyStatus(Enum):

    enabled = "enabled"
    disabled = "disabled"


class TrustPolicyType(Enum):

    notary = "Notary"


class WebhookStatus(Enum):

    enabled = "enabled"
    disabled = "disabled"


class WebhookAction(Enum):

    push = "push"
    delete = "delete"
    quarantine = "quarantine"
    chart_push = "chart_push"
    chart_delete = "chart_delete"


class RunStatus(Enum):

    queued = "Queued"
    started = "Started"
    running = "Running"
    succeeded = "Succeeded"
    failed = "Failed"
    canceled = "Canceled"
    error = "Error"
    timeout = "Timeout"


class RunType(Enum):

    quick_build = "QuickBuild"
    quick_run = "QuickRun"
    auto_build = "AutoBuild"
    auto_run = "AutoRun"


class OS(Enum):

    windows = "Windows"
    linux = "Linux"


class Architecture(Enum):

    amd64 = "amd64"
    x86 = "x86"
    arm = "arm"


class Variant(Enum):

    v6 = "v6"
    v7 = "v7"
    v8 = "v8"


class TaskStatus(Enum):

    disabled = "Disabled"
    enabled = "Enabled"


class BaseImageDependencyType(Enum):

    build_time = "BuildTime"
    run_time = "RunTime"


class SourceControlType(Enum):

    github = "Github"
    visual_studio_team_service = "VisualStudioTeamService"


class TokenType(Enum):

    pat = "PAT"
    oauth = "OAuth"


class SourceTriggerEvent(Enum):

    commit = "commit"
    pullrequest = "pullrequest"


class TriggerStatus(Enum):

    disabled = "Disabled"
    enabled = "Enabled"


class BaseImageTriggerType(Enum):

    all = "All"
    runtime = "Runtime"


class SourceRegistryLoginMode(Enum):

    none = "None"
    default = "Default"


class SecretObjectType(Enum):

    opaque = "Opaque"


class TokenPasswordName(Enum):

    password = "password"
    password2 = "password2"
