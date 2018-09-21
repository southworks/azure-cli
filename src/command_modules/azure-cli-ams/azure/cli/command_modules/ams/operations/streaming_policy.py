# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json

from azure.mgmt.media.models import (StreamingPolicy, NoEncryption, EnabledProtocols,
                                     CommonEncryptionCenc, TrackSelection, TrackPropertyCondition,
                                     StreamingPolicyContentKeys, DefaultKey, StreamingPolicyContentKey,
                                     StreamingPolicyContentKeys,
                                     CencDrmConfiguration, StreamingPolicyPlayReadyConfiguration,
                                     StreamingPolicyWidevineConfiguration, EnabledProtocols)
from azure.cli.command_modules.ams._client_factory import get_streaming_policies_client


def create_streaming_policy(cmd, resource_group_name, account_name,
                            streaming_policy_name,
                            no_encryption_protocols=None,
                            default_content_key_policy_name=None,
                            cenc_default_key_label=None, cenc_default_key_policy_name=None,
                            cenc_clear_tracks=None, cenc_key_to_track_mappings=None,
                            cenc_play_ready_url_template=None, cenc_play_ready_attributes=None,
                            cenc_widevine_url_template=None,
                            cenc_protocols=None):

    no_encryption = _no_encryption_factory(no_encryption_protocols)

    common_encryption_cenc = _cenc_encryption_factory(cenc_protocols, cenc_widevine_url_template,
                                                      cenc_default_key_label, cenc_default_key_policy_name,
                                                      cenc_key_to_track_mappings, cenc_clear_tracks,
                                                      cenc_play_ready_url_template, cenc_play_ready_attributes)

    streaming_policy = StreamingPolicy(default_content_key_policy_name=default_content_key_policy_name,
                                       no_encryption=no_encryption,
                                       common_encryption_cenc=common_encryption_cenc)

    return get_streaming_policies_client(cmd.cli_ctx).create(resource_group_name, account_name,
                                                             streaming_policy_name, streaming_policy)


def _no_encryption_factory(no_encryption_protocols):
    enabled_protocols = _build_enabled_protocols_object(no_encryption_protocols)
    return NoEncryption(enabled_protocols=enabled_protocols)


def _cenc_encryption_factory(cenc_protocols, cenc_widevine_url_template,
                             cenc_default_key_label, cenc_default_key_policy_name,
                             cenc_key_to_track_mappings, cenc_clear_tracks,
                             cenc_play_ready_url_template, cenc_play_ready_attributes):
    cenc_enabled_protocols = _build_enabled_protocols_object(cenc_protocols)

    cenc_enabled_protocols = EnabledProtocols(download=cenc_download, dash=cenc_dash, hls=cenc_hls, smooth_streaming=cenc_smooth_streaming)

    cenc_content_keys = StreamingPolicyContentKeys(default_key=DefaultKey(label=cenc_default_key_label,
                                                                          policy_name=cenc_default_key_policy_name),
                                                   key_to_track_mappings = _parse_key_to_track_mappings_json(cenc_key_to_track_mappings))

    cenc_play_ready_config = StreamingPolicyPlayReadyConfiguration(
        custom_license_acquisition_url_template=cenc_play_ready_url_template,
        play_ready_custom_attributes=cenc_play_ready_attributes)

    cenc_widevine_config = StreamingPolicyWidevineConfiguration(
        custom_license_acquisition_url_template=cenc_widevine_url_template)

    return CommonEncryptionCenc(enabled_protocols=cenc_enabled_protocols,
                                clear_tracks=cenc_clear_tracks,
                                content_keys=cenc_content_keys,
                                drm=CencDrmConfiguration(play_ready=cenc_play_ready_config, widevine=cenc_widevine_config))


def _parse_key_to_track_mappings_json(cenc_key_to_track_mappings):
    key_to_track_mappings = []
    with open(cenc_key_to_track_mappings) as cenc_key_to_track_mappings_stream:
        cenc_key_to_track_mappings_json = json.load(cenc_key_to_track_mappings_stream)
        for str_policy_content_key_json in cenc_key_to_track_mappings_json:
            str_policy_content_key = StreamingPolicyContentKey(**str_policy_content_key_json)
            key_to_track_mappings.append(str_policy_content_key)
    return key_to_track_mappings


def _build_enabled_protocols_object(protocols):
    return EnabledProtocols(download='Download' in protocols,
                            dash='Dash' in protocols,
                            hls='HLS' in protocols,
                            smooth_streaming='SmoothStreaming' in protocols)
