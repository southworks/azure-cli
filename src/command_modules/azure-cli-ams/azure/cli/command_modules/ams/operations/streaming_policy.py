# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


def create_streaming_policy(cmd, resource_group_name, account_name,
                            streaming_policy_name,
                            download=False, dash=False, hls=False, smooth_streaming=False,
                            default_content_key_policy_name=None, cenc_track_properties=None,
                            cenc_default_key_label=None, cenc_default_key_policy_name=None,
                            cenc_key_label=None, cenc_key_policy_name=None, cenc_key_track_properties=None,
                            cenc_play_ready_url_template=None, cenc_play_ready_attributes=None,
                            cenc_widevine_url_template=None, envelope_protocols=None,
                            envelope_clear_tracks=None, envelope_key_to_track_mappings=None,
                            custom_key_acquisition_url_template=None, envelope_label=None,
                            envelope_policy_name=None):
    from azure.cli.command_modules.ams._client_factory import get_streaming_policies_client
    from azure.mgmt.media.models import (StreamingPolicy, NoEncryption, EnabledProtocols,
                                         CommonEncryptionCenc, TrackSelection, TrackPropertyCondition,
                                         StreamingPolicyContentKeys, DefaultKey, StreamingPolicyContentKey,
                                         CencDrmConfiguration, StreamingPolicyPlayReadyConfiguration,
                                         StreamingPolicyWidevineConfiguration, EnvelopeEncryption)

    enabled_protocols = EnabledProtocols(download=download, dash=dash, hls=hls, smooth_streaming=smooth_streaming)
    cenc_enabled_protocols = EnabledProtocols(download=download, dash=dash, hls=hls, smooth_streaming=True)

    # TODO: Support Unknown value too
    track_selections = list(map(lambda x: TrackPropertyCondition(property='FourCC',
                                                                 operation='Equal',
                                                                 value=x), cenc_track_properties))

    # TODO: Support Unknown value too
    key_track_selections = list(map(lambda x: TrackPropertyCondition(property='FourCC',
                                                                     operation='Equal',
                                                                     value=x), cenc_key_track_properties))

    cenc_play_ready_config = StreamingPolicyPlayReadyConfiguration(
        custom_license_acquisition_url_template=cenc_play_ready_url_template,
        play_ready_custom_attributes=cenc_play_ready_attributes)

    cenc_widevine_config = StreamingPolicyWidevineConfiguration(
        custom_license_acquisition_url_template=cenc_widevine_url_template)

    # TODO: Allow multiple content keys to track
    cenc_key_to_track_mappings = [StreamingPolicyContentKey(label=cenc_key_label,
                                                            policy_name=cenc_key_policy_name,
                                                            tracks=[TrackSelection(track_selections=key_track_selections)])]

    envelope_encryption_enabled_protocols = EnabledProtocols()
    for protocol in envelope_encryption_enabled_protocols:
        if protocol == 'Download':
            envelope_encryption_enabled_protocols.download = True
        elif protocol == 'Dash':
            envelope_encryption_enabled_protocols.dash = True
        elif protocol == 'HLS':
            envelope_encryption_enabled_protocols.hls = True
        elif protocol == 'SmoothStreaming':
            envelope_encryption_enabled_protocols.smooth_streaming = True
        else:
            raise CLIError('Unknown protocol {}.'.format(protocol))
            


    # TODO: Define envelope_streaming_policy_content_key (StreamingPolicyContentKey list) json: envelope_key_to_track_mappings

    envelope_content_keys = StreamingPolicyContentKeys(default_key=DefaultKey(label=envelope_label,
                                                                              policy_name=envelope_policy_name),
                                                       key_to_track_mappings=envelope_streaming_policy_content_key)

    envelope_encryption = EnvelopeEncryption(enabled_protocols=envelope_encryption_enabled_protocols,
                                             clear_tracks=track_selection,
                                             content_keys=envelope_content_keys,
                                             custom_key_acquisition_url_template=custom_key_acquisition_url_template)

    common_encryption_cenc = CommonEncryptionCenc(enabled_protocols=cenc_enabled_protocols,
                                                  clear_tracks=[TrackSelection(track_selections=track_selections)],
                                                  content_keys=StreamingPolicyContentKeys(
                                                      default_key=DefaultKey(label=cenc_default_key_label,
                                                                             policy_name=cenc_default_key_policy_name),
                                                      key_to_track_mappings=cenc_key_to_track_mappings),
                                                  drm=CencDrmConfiguration(play_ready=cenc_play_ready_config, widevine=cenc_widevine_config))

    streaming_policy = StreamingPolicy(default_content_key_policy_name=default_content_key_policy_name,
                                       no_encryption=NoEncryption(enabled_protocols=enabled_protocols),
                                       common_encryption_cenc=common_encryption_cenc,
                                       envelope_encryption=envelope_encryption)

    return get_streaming_policies_client(cmd.cli_ctx).create(resource_group_name, account_name,
                                                             streaming_policy_name, streaming_policy)
