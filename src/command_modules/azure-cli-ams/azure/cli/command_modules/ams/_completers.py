# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.decorators import Completer

from azure.cli.command_modules.ams.operations.sp import list_role_definitions
from azure.cli.command_modules.ams._sdk_utils import (get_stand_alone_presets, get_cdn_providers,
                                                      get_default_streaming_policies,
                                                      get_allowed_languages_for_preset,
                                                      get_protocols)

from azure.mgmt.media.models import EncoderNamedPreset


@Completer
def get_role_definition_name_completion_list(cmd):
    definitions = list_role_definitions(cmd)
    return [x.properties.role_name for x in list(definitions)]


def get_presets_definition_name_completion_list():
    encoder_name_presets_list = [e.value for e in EncoderNamedPreset]
    encoder_name_presets_list.extend(get_stand_alone_presets())
    return encoder_name_presets_list


def get_cdn_provider_completion_list():
    cdn_provider_list = get_cdn_providers()
    return cdn_provider_list


def get_default_streaming_policies_completion_list():
    default_streaming_policies = get_default_streaming_policies()
    return default_streaming_policies

def get_protocols_completion_list():
    protocols = get_protocols()
    return protocols

def get_allowed_languages_for_preset_completion_list():
    languages = get_allowed_languages_for_preset()
    return languages
