# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json

from azure.cli.core.util import CLIError

from azure.mgmt.media.models import (StreamingPolicy, NoEncryption,
                                     CommonEncryptionCenc, TrackSelection, TrackPropertyCondition,
                                     StreamingPolicyContentKeys, DefaultKey, StreamingPolicyContentKey,
                                     CbcsDrmConfiguration, CommonEncryptionCbcs,
                                     CencDrmConfiguration, StreamingPolicyPlayReadyConfiguration,
                                     StreamingPolicyWidevineConfiguration, EnabledProtocols,
                                     EnvelopeEncryption, StreamingPolicyFairPlayConfiguration)
from azure.cli.command_modules.ams._client_factory import get_streaming_policies_client


def create_streaming_policy(cmd, resource_group_name, account_name,  # pylint: disable=too-many-locals
                            streaming_policy_name, no_encryption_protocols=None,
                            default_content_key_policy_name=None,
                            cenc_default_key_label=None, cenc_default_key_policy_name=None,
                            cenc_clear_tracks=None, cenc_key_to_track_mappings=None,
                            cenc_play_ready_url_template=None, cenc_play_ready_attributes=None,
                            cenc_widevine_url_template=None, cenc_protocols=None,
                            envelope_clear_tracks=None, envelope_key_to_track_mappings=None,
                            envelope_custom_key_acquisition_url_template=None,
                            envelope_default_key_label=None, envelope_default_key_policy_name=None,
                            envelope_protocols=None, cbcs_protocols=None,
                            cbcs_default_key_label=None, cbcs_clear_tracks=None,
                            cbcs_default_key_policy_name=None,
                            cbcs_key_to_track_mappings=None, cbcs_play_ready_url_template=None,
                            cbcs_play_ready_attributes=None, cbcs_widevine_url_template=None,
                            cbcs_custom_license_acquisition_url_template=None,
                            cbcs_allow_persistent_license=False):

    envelope_encryption = None
    if any([envelope_protocols, envelope_clear_tracks, envelope_custom_key_acquisition_url_template,
            envelope_default_key_label, envelope_default_key_policy_name, envelope_key_to_track_mappings]):
        envelope_encryption = _envelope_encryption_factory(envelope_protocols, envelope_clear_tracks,
                                                           envelope_custom_key_acquisition_url_template,
                                                           envelope_default_key_label, envelope_default_key_policy_name,
                                                           envelope_key_to_track_mappings)

    common_encryption_cenc = None
    if any([cenc_protocols, cenc_widevine_url_template, cenc_default_key_label, cenc_default_key_policy_name,
            cenc_key_to_track_mappings, cenc_clear_tracks, cenc_play_ready_url_template, cenc_play_ready_attributes]):
        common_encryption_cenc = _cenc_encryption_factory(cenc_protocols, cenc_widevine_url_template,
                                                          cenc_default_key_label, cenc_default_key_policy_name,
                                                          cenc_key_to_track_mappings, cenc_clear_tracks,
                                                          cenc_play_ready_url_template, cenc_play_ready_attributes)

    common_encryption_cbcs = None
    if any([cbcs_protocols, cbcs_widevine_url_template, cbcs_default_key_label, cbcs_default_key_policy_name,
            cbcs_key_to_track_mappings, cbcs_clear_tracks, cbcs_play_ready_url_template, cbcs_play_ready_attributes,
            cbcs_custom_license_acquisition_url_template, cbcs_allow_persistent_license]):
        common_encryption_cbcs = _cbcs_encryption_factory(cbcs_protocols, cbcs_widevine_url_template,
                                                          cbcs_default_key_label, cbcs_default_key_policy_name,
                                                          cbcs_key_to_track_mappings, cbcs_clear_tracks,
                                                          cbcs_play_ready_url_template, cbcs_play_ready_attributes,
                                                          cbcs_custom_license_acquisition_url_template,
                                                          cbcs_allow_persistent_license)

    no_encryption = None
    if not any([envelope_encryption, common_encryption_cenc, common_encryption_cbcs]) or no_encryption_protocols:
        no_encryption = _no_encryption_factory(no_encryption_protocols)

    streaming_policy = StreamingPolicy(default_content_key_policy_name=default_content_key_policy_name,
                                       no_encryption=no_encryption,
                                       envelope_encryption=envelope_encryption,
                                       common_encryption_cenc=common_encryption_cenc,
                                       common_encryption_cbcs=common_encryption_cbcs)

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

    cenc_play_ready_config = None
    if cenc_play_ready_url_template or cenc_play_ready_attributes:
        cenc_play_ready_config = StreamingPolicyPlayReadyConfiguration(
            custom_license_acquisition_url_template=cenc_play_ready_url_template,
            play_ready_custom_attributes=cenc_play_ready_attributes)

    cenc_widevine_config = None
    if cenc_widevine_url_template:
        cenc_widevine_config = StreamingPolicyWidevineConfiguration(
            custom_license_acquisition_url_template=cenc_widevine_url_template)

    key_to_track_mappings = _parse_key_to_track_mappings_json(cenc_key_to_track_mappings)
    cenc_content_keys = StreamingPolicyContentKeys(default_key=DefaultKey(label=cenc_default_key_label,
                                                                          policy_name=cenc_default_key_policy_name),
                                                   key_to_track_mappings=key_to_track_mappings)

    return CommonEncryptionCenc(enabled_protocols=cenc_enabled_protocols,
                                clear_tracks=_parse_clear_tracks_json(cenc_clear_tracks),
                                content_keys=cenc_content_keys,
                                drm=CencDrmConfiguration(play_ready=cenc_play_ready_config,
                                                         widevine=cenc_widevine_config))


def _cbcs_encryption_factory(cbcs_protocols, cbcs_widevine_url_template,
                             cbcs_default_key_label, cbcs_default_key_policy_name,
                             cbcs_key_to_track_mappings, cbcs_clear_tracks,
                             cbcs_play_ready_url_template, cbcs_play_ready_attributes,
                             cbcs_custom_license_acquisition_url_template,
                             cbcs_allow_persistent_license):
    cbcs_enabled_protocols = _build_enabled_protocols_object(cbcs_protocols)

    cbcs_play_ready_config = None
    if cbcs_play_ready_url_template or cbcs_play_ready_attributes:
        cbcs_play_ready_config = StreamingPolicyPlayReadyConfiguration(play_ready_custom_attributes=cbcs_play_ready_attributes,  # pylint: disable=line-too-long
                                                                       custom_license_acquisition_url_template=cbcs_play_ready_url_template)  # pylint: disable=line-too-long

    cbcs_widevine_config = None
    if cbcs_widevine_url_template:
        cbcs_widevine_config = StreamingPolicyWidevineConfiguration(
            custom_license_acquisition_url_template=cbcs_widevine_url_template)

    cbcs_fair_play_config = None
    if cbcs_allow_persistent_license or cbcs_custom_license_acquisition_url_template:
        cbcs_fair_play_config = StreamingPolicyFairPlayConfiguration(allow_persistent_license=cbcs_allow_persistent_license,  # pylint: disable=line-too-long
                                                                            custom_license_acquisition_url_template=cbcs_custom_license_acquisition_url_template)  # pylint: disable=line-too-long

    cbcs_content_keys = StreamingPolicyContentKeys(default_key=DefaultKey(label=cbcs_default_key_label,
                                                                          policy_name=cbcs_default_key_policy_name),
                                                   key_to_track_mappings=_parse_key_to_track_mappings_json(cbcs_key_to_track_mappings))  # pylint: disable=line-too-long

    return CommonEncryptionCbcs(enabled_protocols=cbcs_enabled_protocols,
                                clear_tracks=_parse_clear_tracks_json(cbcs_clear_tracks),
                                content_keys=cbcs_content_keys,
                                drm=CbcsDrmConfiguration(play_ready=cbcs_play_ready_config, widevine=cbcs_widevine_config,  # pylint: disable=line-too-long
                                                         fair_play=cbcs_fair_play_config))


def _parse_key_to_track_mappings_json(key_to_track_mappings):
    errorMessage = '''Malformed key-to-track-mappings JSON argument. Please, make sure you are sending a StreamingPolicyContentKeys. 
                    For further information, please refer to 
    https://docs.microsoft.com/en-us/rest/api/media/streamingpolicies/create#streamingpolicycontentkeys'''
    key_to_track_mappings_result = None
    if key_to_track_mappings is not None:
        key_to_track_mappings_result = []
        with open(key_to_track_mappings) as key_to_track_mappings_stream:
            key_to_track_mappings_json = json.load(key_to_track_mappings_stream)
            try:
                for str_policy_content_key_json in key_to_track_mappings_json:
                    str_policy_content_key = StreamingPolicyContentKey(**str_policy_content_key_json)
                    key_to_track_mappings_result.append(str_policy_content_key)
            except:
                raise CLIError(errorMessage)  # pylint: disable=line-too-long
    return key_to_track_mappings_result


def _parse_clear_tracks_json(clear_tracks):
    errorMessage = '''Malformed key-to-track-mappings JSON argument. Please, make sure you are sending a list of TrackSelection. 
                    For further information, please refer to 
                    https://docs.microsoft.com/en-us/rest/api/media/streamingpolicies/create#trackselection'''
    clear_tracks_result = None
    if clear_tracks is not None:
        clear_tracks_result = []
        with open(clear_tracks) as clear_tracks_result_stream:
            clear_tracks_json = json.load(clear_tracks_result_stream)
            try:
                for track_selection_json in clear_tracks_json:
                    track_properties = []
                    for track_property_json in track_selection_json.get('trackSelections'):
                        track_property = TrackPropertyCondition(**track_property_json)
                        track_properties.append(track_property)
                    clear_tracks_result.append(TrackSelection(track_selections=track_properties))
            except:
                raise CLIError(errorMessage)  # pylint: disable=line-too-long
    return clear_tracks_result


def _build_enabled_protocols_object(protocols):
    if protocols is None:
        protocols = []

    return EnabledProtocols(download='Download' in protocols,
                            dash='Dash' in protocols,
                            hls='HLS' in protocols,
                            smooth_streaming='SmoothStreaming' in protocols)


def _envelope_encryption_factory(envelope_protocols, envelope_clear_tracks,
                                 envelope_custom_key_acquisition_url_template,
                                 envelope_default_key_label, envelope_default_key_policy_name,
                                 envelope_key_to_track_mappings):

    envelope_content_keys = StreamingPolicyContentKeys(default_key=DefaultKey(label=envelope_default_key_label,
                                                                              policy_name=envelope_default_key_policy_name),  # pylint: disable=line-too-long
                                                       key_to_track_mappings=_parse_key_to_track_mappings_json(envelope_key_to_track_mappings))  # pylint: disable=line-too-long

    envelope_encryption = EnvelopeEncryption(enabled_protocols=_build_enabled_protocols_object(envelope_protocols),
                                             clear_tracks=_parse_clear_tracks_json(envelope_clear_tracks),
                                             content_keys=envelope_content_keys,
                                             custom_key_acquisition_url_template=envelope_custom_key_acquisition_url_template)  # pylint: disable=line-too-long

    return envelope_encryption
