# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json

from knack.util import CLIError

from azure.mgmt.media.models import (AssetFilter, FilterTrackSelection, FilterTrackPropertyCondition,
                                     PresentationTimeRange, FirstQuality)

def create_asset_filter(client, account_name, resource_group_name, asset_name, filter_name,
                        start_timestamp=None, end_timestamp=None, presentation_window_duration=None,
                        live_backoff_duration=None, timescale=None, force_end_timestamp=False, bitrate=None,
                        tracks=None):
    first_quality = None
    presentation_time_range = None

    if bitrate:
        first_quality = FirstQuality(bitrate=bitrate)

    if any([start_timestamp, end_timestamp, presentation_window_duration,
            live_backoff_duration, timescale]):
        presentation_time_range = PresentationTimeRange(
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            presentation_window_duration=presentation_window_duration,
            live_backoff_duration=live_backoff_duration,
            timescale=timescale,
            force_end_timestamp=force_end_timestamp
        )

    asset_filter = AssetFilter(
        presentation_time_range=presentation_time_range,
        first_quality=first_quality,
        tracks=_parse_filter_tracks_json(tracks)
    )

    return client.create_or_update(resource_group_name, account_name, asset_name, filter_name, asset_filter)


def _parse_filter_tracks_json(tracks):
    tracks_result = None
    if tracks is not None:
        tracks_result = []
        try:
            tracks_json = json.loads(tracks)
            for track_selection_json in tracks_json:
                track_properties = []
                for track_property_json in track_selection_json.get('trackSelections'):
                    track_property = FilterTrackPropertyCondition(**track_property_json)
                    track_properties.append(track_property)
                tracks_result.append(FilterTrackSelection(track_selections=track_properties))
        except TypeError as ex:
            errorMessage = 'Malformed JSON.'
            raise CLIError('{}. {}'.format(str(ex), errorMessage))
    return tracks_result
