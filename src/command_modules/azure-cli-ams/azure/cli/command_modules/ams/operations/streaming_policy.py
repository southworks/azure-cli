# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


def create_streaming_policy(cmd, resource_group_name, account_name,
                            streaming_policy_name,
                            download=False, dash=False, hls=False, smooth_streaming=False,
                            default_content_key_policy_name=None,
                            cenc_default_key_label=None, cenc_default_key_policy_name=None,
                            cenc_clear_tracks=None, cenc_key_to_track_mappings=None,
                            cenc_play_ready_url_template=None, cenc_play_ready_attributes=None,
                            cenc_widevine_url_template=None,
                            cenc_download=None, cenc_dash=None, cenc_hls=None, cenc_smooth_streaming=None):
    from azure.cli.command_modules.ams._client_factory import get_streaming_policies_client
    from azure.mgmt.media.models import (StreamingPolicy, NoEncryption, EnabledProtocols,
                                         CommonEncryptionCenc, TrackSelection, TrackPropertyCondition,
                                         StreamingPolicyContentKeys, DefaultKey, StreamingPolicyContentKey,
                                         CencDrmConfiguration, StreamingPolicyPlayReadyConfiguration,
                                         StreamingPolicyWidevineConfiguration)

    enabled_protocols = EnabledProtocols(download=download, dash=dash, hls=hls, smooth_streaming=smooth_streaming)
    cenc_enabled_protocols = EnabledProtocols(download=cenc_download, dash=cenc_dash, hls=cenc_hls, smooth_streaming=cenc_smooth_streaming)

    # TODO: Remove this after adding support for parsing JSON data
    track_property_condition = TrackPropertyCondition(property='FourCC', operation='Equal', value='testValue')

    cenc_play_ready_config = StreamingPolicyPlayReadyConfiguration(
        custom_license_acquisition_url_template=cenc_play_ready_url_template,
        play_ready_custom_attributes=cenc_play_ready_attributes)

    cenc_widevine_config = StreamingPolicyWidevineConfiguration(
        custom_license_acquisition_url_template=cenc_widevine_url_template)

    # TODO: Remove this after adding support for parsing JSON data
    cenc_key_to_track_mappings = [StreamingPolicyContentKey(label='testLabel',
                                                            policy_name='ckp',
                                                            tracks=[TrackSelection(track_selections=[track_property_condition])])]

    common_encryption_cenc = CommonEncryptionCenc(enabled_protocols=cenc_enabled_protocols,
                                                  clear_tracks=[TrackSelection(track_selections=[track_property_condition])],
                                                  content_keys=StreamingPolicyContentKeys(
                                                      default_key=DefaultKey(label=cenc_default_key_label,
                                                                             policy_name=cenc_default_key_policy_name),
                                                      key_to_track_mappings=cenc_key_to_track_mappings),
                                                  drm=CencDrmConfiguration(play_ready=cenc_play_ready_config, widevine=cenc_widevine_config))

    streaming_policy = StreamingPolicy(default_content_key_policy_name=default_content_key_policy_name,
                                       no_encryption=NoEncryption(enabled_protocols=enabled_protocols),
                                       common_encryption_cenc=common_encryption_cenc)

    return get_streaming_policies_client(cmd.cli_ctx).create(resource_group_name, account_name,
                                                             streaming_policy_name, streaming_policy)
