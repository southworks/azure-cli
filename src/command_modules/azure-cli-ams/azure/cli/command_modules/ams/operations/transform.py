# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import importlib

from knack.util import CLIError

# pylint: disable=line-too-long


def create_transform(cmd, client, account_name, resource_group_name,
                     transform_name, preset_names=None, description=None,
                     custom_preset_path=None):
    outputs = []

    if custom_preset_path is None and preset_names is None:
            raise CLIError("Missing required arguments.\nEither --preset-names "
                           "or --custom-preset must be specified.")

    if preset_names:
        for preset in preset_names:
            outputs.append(get_transform_output(preset))

    if custom_preset_path:
        import json
        try:
            with open(custom_preset_path) as json_data:
                custom_preset_json = json.load(json_data)
                models_module = importlib.import_module('azure.mgmt.media.models')
                codecs = []
                for codec in custom_preset_json['Codecs']:
                    codec_type = getattr(models_module, codec['Type'])
                    codec_instance = codec_type()
                    from azure.mgmt.media.models import H264Layer
                    if codec['Type'] is not 'CopyAudio':
                        codec_instance.layers = [H264Layer()]
                    codecs.append(codec_instance)

                from azure.mgmt.media.models import (StandardEncoderPreset, TransformOutput)
                standard_encoder_preset = StandardEncoderPreset(codecs=codecs)
                outputs.append(TransformOutput(preset=standard_encoder_preset))
        except (OSError, IOError) as e:
            raise CLIError("Can't find a valid custom preset JSON definition in '{}'".format(custom_preset_path))

    return client.create_or_update(resource_group_name, account_name, transform_name, outputs, description)


def add_transform_output(client, account_name, resource_group_name, transform_name, preset_names):
    transform = client.get(resource_group_name, account_name, transform_name)

    set_preset_names = set(preset_names)
    set_existent_preset_names = set(map(lambda x: x.preset.preset_name.value, transform.outputs))

    set_preset_names = set_preset_names.difference(set_existent_preset_names)

    for preset in set_preset_names:
        transform.outputs.append(get_transform_output(preset))

    return client.create_or_update(resource_group_name, account_name, transform_name, transform.outputs)


def remove_transform_output(client, account_name, resource_group_name, transform_name, preset_names):
    transform = client.get(resource_group_name, account_name, transform_name)

    set_preset_names = set(preset_names)
    set_existent_preset_names = set(map(lambda x: x.preset.preset_name.value, transform.outputs))

    set_existent_preset_names = set_existent_preset_names.difference(set_preset_names)

    transform_output_list = list(filter(lambda x: x.preset.preset_name.value in set_existent_preset_names,
                                        transform.outputs))

    return client.create_or_update(resource_group_name, account_name, transform_name, transform_output_list)


def transform_update_setter(client, resource_group_name,
                            account_name, transform_name, parameters):
    parameters.outputs = list(map(lambda x: get_transform_output(x) if isinstance(x, str) else x, parameters.outputs))
    return client.create_or_update(resource_group_name, account_name, transform_name,
                                   parameters.outputs, parameters.description)


def update_transform(instance, description=None, preset_names=None):
    if not instance:
        raise CLIError('The transform resource was not found.')

    if description:
        instance.description = description

    if preset_names:
        instance.outputs = []
        for preset in preset_names:
            instance.outputs.append(get_transform_output(preset))

    return instance


def get_transform_output(preset):
    from azure.mgmt.media.models import (TransformOutput, BuiltInStandardEncoderPreset, VideoAnalyzerPreset, AudioAnalyzerPreset)
    from azure.cli.command_modules.ams._completers import (get_stand_alone_presets, is_audio_analyzer)

    if preset in get_stand_alone_presets():
        if is_audio_analyzer(preset_name=preset):
            transform_preset = AudioAnalyzerPreset()
        else:
            transform_preset = VideoAnalyzerPreset()
    else:
        transform_preset = BuiltInStandardEncoderPreset(preset_name=preset)

    transform_output = TransformOutput(preset=transform_preset)
    return transform_output
