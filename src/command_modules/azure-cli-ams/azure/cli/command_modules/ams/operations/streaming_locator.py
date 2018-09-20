# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json

from knack.util import CLIError

from azure.mgmt.media.models import (StreamingLocatorContentKey, TrackSelection,
                                     TrackPropertyCondition)

def create_streaming_locator(client, resource_group_name, account_name,
                             streaming_locator_name, streaming_policy_name,
                             asset_name, start_time=None, default_content_key_policy_name=None,
                             end_time=None, streaming_locator_id=None, alternative_media_id=None,
                             content_keys=None):
    from azure.mgmt.media.models import StreamingLocator

    if not _valid_content_keys(content_keys):
        raise CLIError('Malformed content keys.')

    content_keys = _build_content_keys(content_keys)

    streaming_locator = StreamingLocator(asset_name=asset_name,
                                         start_time=start_time, end_time=end_time,
                                         streaming_policy_name=streaming_policy_name,
                                         default_content_key_policy_name=default_content_key_policy_name,
                                         streaming_locator_id=streaming_locator_id,
                                         alternative_media_id=alternative_media_id,
                                         content_keys=content_keys)

    return client.create(resource_group_name, account_name, streaming_locator_name, streaming_locator)


def list_content_keys(client, resource_group_name, account_name,
                      streaming_locator_name):
    return client.list_content_keys(resource_group_name, account_name,
                                    streaming_locator_name).content_keys

def _build_content_keys(content_keys):
    def __track_selection_builder(sel):
        return TrackPropertyCondition(
            property=sel.get('property'),
            operation=sel.get('operation'),
            value=sel.get('value')
        )

    def __track_builder(tracks):
        return TrackSelection(
            track_selections=[__track_selection_builder(t) 
                              for t in tracks.get('trackSelections')]
                              if tracks.get('trackSelections') else None)

    def __content_key_builder(key):
        return StreamingLocatorContentKey(
            id=key.get('id'),
            type=key.get('type'),
            label=key.get('label'),
            value=key.get('value'),
            tracks=[__track_builder(t) for t in key.get('tracks')] if key.get('tracks') else None
        )

    return [__content_key_builder(k) for k in json.loads(content_keys)]

def _valid_content_keys(content_keys):
    if content_keys is None:
        return True

    def __valid_property_conditions(conds):
        return (conds.get('property') in ['Unknown', 'FourCC'] and
                conds.get('operation') in ['Unknown', 'Equal'])

    def __valid_track(track):
        return (track.get('trackSelections') is None or
                all(__valid_property_conditions(s) for s in track.get('trackSelections')))

    def __valid_content_key(key):
        return (key.get('id') and
                (key.get('tracks') is None or all(__valid_track(t) for t in key.get('tracks'))))

    obj = None
    try:
        obj = json.loads(content_keys)
    except ValueError as err:
        raise CLIError('Malformed JSON: ' + str(err))

    return isinstance(obj, list) and all(__valid_content_key(k) for k in obj)
