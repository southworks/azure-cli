# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json

import os

from knack.util import 

from azure.cli.command_modules.ams._client_factory import get_streaming_policies_client
from azure.mgmt.media.models import (StreamingPolicy, NoEncryption, EnabledProtocols,
                                        CommonEncryptionCenc, TrackSelection, TrackPropertyCondition,
                                        StreamingPolicyContentKeys, DefaultKey, StreamingPolicyContentKey,
                                        CencDrmConfiguration, StreamingPolicyPlayReadyConfiguration,
                                        StreamingPolicyWidevineConfiguration, EnvelopeEncryption)

def create_streaming_policy(cmd, resource_group_name, account_name,
                            streaming_policy_name, no_encryption_protocols=None,
                            default_content_key_policy_name=None, cenc_protocols=None,
                            cenc_default_key_label=None, cenc_default_key_policy_name=None,
                            cenc_clear_tracks=None, cenc_key_to_track_mappings=None,
                            cenc_play_ready_url_template=None, cenc_play_ready_attributes=None,
                            cenc_widevine_url_template=None, envelope_protocols=None,
                            envelope_clear_tracks=None, envelope_key_to_track_mappings=None,
                            envelope_custom_key_acquisition_url_template=None,
                            envelope_default_key_label=None, envelope_default_key_policy_name=None):

    no_encryption_enabled_protocols = _build_enabled_protocols_object(no_encryption_protocols)
    cenc_enabled_protocols = _build_enabled_protocols_object(cenc_protocols)

    
    # TODO: Remove this after adding support for parsing JSON data
    track_property_condition = TrackPropertyCondition(property='FourCC', operation='Equal', value='testValue')
    # TODO: Remove this after adding support for parsing JSON data
    cenc_key_to_track_mappings = [StreamingPolicyContentKey(label='testLabel',
                                                            policy_name='x512Policy',
                                                            tracks=[TrackSelection(track_selections=[track_property_condition])])]

    cenc_clear_tracks = []
    with open(envelope_clear_tracks) as envelope_clear_tracks_stream:
	    envelope_clear_tracks_json = json.load(envelope_clear_tracks_stream)
	    for track_selection_json in envelope_clear_tracks_json:
		    track_selection = TrackSelection(**track_selection_json)
		    envelope_encryption.clear_tracks.append(track_selection)

    cenc_play_ready_config = StreamingPolicyPlayReadyConfiguration(
        custom_license_acquisition_url_template=cenc_play_ready_url_template,
        play_ready_custom_attributes=cenc_play_ready_attributes)

    cenc_widevine_config = StreamingPolicyWidevineConfiguration(
        custom_license_acquisition_url_template=cenc_widevine_url_template)

    # TODO: Remove this after adding support for parsing JSON data
    cenc_key_to_track_mappings = [StreamingPolicyContentKey(label=cenc_default_key_label,
                                                            policy_name=cenc_default_key_policy_name,
                                                            tracks=cenc_tracks)]

    envelope_encryption_enabled_protocols = _build_enabled_protocols_object(envelope_protocols)

    envelope_encryption = _envelope_encryption_factory(envelope_encryption_enabled_protocols, envelope_clear_tracks,
                                                       envelope_content_keys, envelope_custom_key_acquisition_url_template,
                                                       envelope_default_key_label, envelope_default_key_policy_name,
                                                       envelope_streaming_policy_content_key, envelope_key_to_track_mappings)

    common_encryption_cenc = CommonEncryptionCenc(enabled_protocols=cenc_enabled_protocols,
                                                  clear_tracks=cenc_tracks,
                                                  content_keys=StreamingPolicyContentKeys(
                                                      default_key=DefaultKey(label=cenc_default_key_label,
                                                                             policy_name=cenc_default_key_policy_name),
                                                      key_to_track_mappings=cenc_key_to_track_mappings),
                                                  drm=CencDrmConfiguration(play_ready=cenc_play_ready_config, widevine=cenc_widevine_config))

    streaming_policy = StreamingPolicy(default_content_key_policy_name=default_content_key_policy_name,
                                       no_encryption=NoEncryption(enabled_protocols=no_encryption_enabled_protocols),
                                       common_encryption_cenc=common_encryption_cenc,
                                       envelope_encryption=envelope_encryption)

    return get_streaming_policies_client(cmd.cli_ctx).create(resource_group_name, account_name,
                                                             streaming_policy_name, streaming_policy)

def _build_enabled_protocols_object(protocols):
    from azure.mgmt.media.models import EnabledProtocols

    enabled_protocols = EnabledProtocols(download=False, dash=False, hls=False, smooth_streaming=False)
    if protocols is not None:
        for protocol in protocols:
            if protocol == 'Download':
                enabled_protocols.download = True
            elif protocol == 'Dash':
                enabled_protocols.dash = True
            elif protocol == 'HLS':
                enabled_protocols.hls = True
            elif protocol == 'SmoothStreaming':
                enabled_protocols.smooth_streaming = True
            else:
                raise CLIError('Unknown protocol {}.'.format(protocol))
    return enabled_protocols

def _envelope_encryption_factory(envelope_encryption_enabled_protocols, envelope_clear_tracks,
                                 envelope_content_keys, envelope_custom_key_acquisition_url_template,
                                 envelope_default_key_label, envelope_default_key_policy_name,
                                 envelope_streaming_policy_content_key, envelope_key_to_track_mappings):
    
    envelope_content_keys = StreamingPolicyContentKeys(default_key=DefaultKey(label=envelope_default_key_label,
                                                                              policy_name=envelope_default_key_policy_name),
                                                       key_to_track_mappings=None)

    envelope_encryption = EnvelopeEncryption(enabled_protocols=envelope_encryption_enabled_protocols,
                                             clear_tracks=None,
                                             content_keys=envelope_content_keys,
                                             custom_key_acquisition_url_template=envelope_custom_key_acquisition_url_template)

    if envelope_key_to_track_mappings is not None:
        with open(envelope_key_to_track_mappings) as envelope_key_to_track_mappings_stream:
	        envelope_key_to_track_mappings_json = json.load(envelope_key_to_track_mappings_stream)
	        for streaming_policy_content_key_json in envelope_key_to_track_mappings_json:
		        streaming_policy_content_key = StreamingPolicyContentKey(**streaming_policy_content_key_json)
		        envelope_encryption.content_keys.key_to_track_mappings.append(streaming_policy_content_key)

    if envelope_clear_tracks is not None:
        with open(envelope_clear_tracks) as envelope_clear_tracks_stream:
	        envelope_clear_tracks_json = json.load(envelope_clear_tracks_stream)
	        for track_selection_json in envelope_clear_tracks_json:
		        track_selection = TrackSelection(**track_selection_json)
		        envelope_encryption.clear_tracks.append(track_selection)

    return envelope_encryption