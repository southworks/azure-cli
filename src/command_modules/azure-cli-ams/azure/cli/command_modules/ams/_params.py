# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long

from knack.arguments import CLIArgumentType

from azure.cli.core.commands.validators import get_default_location_from_resource_group
from azure.cli.core.commands.parameters import (get_location_type, get_enum_type, tags_type, get_three_state_flag)
from azure.cli.command_modules.ams._completers import (get_role_definition_name_completion_list, get_cdn_provider_completion_list,
                                                       get_default_streaming_policies_completion_list)

from azure.mgmt.media.models import (Priority, AssetContainerPermission, LiveEventInputProtocol, LiveEventEncodingType,
                                     StreamOptionsFlag, ContentKeyPolicyRestrictionTokenType)

from ._validators import validate_storage_account_id, datetime_format, validate_correlation_data, validate_token_claim


def load_arguments(self, _):  # pylint: disable=too-many-locals, too-many-statements
    name_arg_type = CLIArgumentType(options_list=['--name', '-n'], id_part='name', help='The name of the Azure Media Services account.', metavar='NAME')
    account_name_arg_type = CLIArgumentType(options_list=['--account-name', '-a'], id_part='name', help='The name of the Azure Media Services account.', metavar='ACCOUNT_NAME')
    storage_account_arg_type = CLIArgumentType(options_list=['--storage-account'], validator=validate_storage_account_id, metavar='STORAGE_NAME')
    password_arg_type = CLIArgumentType(options_list=['--password', '-p'], metavar='PASSWORD_NAME')
    transform_name_arg_type = CLIArgumentType(options_list=['--transform-name', '-t'], metavar='TRANSFORM_NAME')
    expiry_arg_type = CLIArgumentType(options_list=['--expiry'], type=datetime_format, metavar='EXPIRY_TIME')
    default_policy_name_arg_type = CLIArgumentType(options_list=['--content-key-policy-name'], help='The default content key policy name used by the streaming locator.', metavar='DEFAULT_CONTENT_KEY_POLICY_NAME')
    correlation_data_type = CLIArgumentType(validator=validate_correlation_data, help="Customer provided correlation data that will be returned in Job completed events. This data is in key=value format separated by spaces.", nargs='*', metavar='CORRELATION_DATA')
    token_claim_type = CLIArgumentType(validator=validate_token_claim, help='A list of required token claims in key=value format separated by spaces.')

    with self.argument_context('ams') as c:
        c.argument('account_name', name_arg_type)

    with self.argument_context('ams account') as c:
        c.argument('location', arg_type=get_location_type(self.cli_ctx),
                   validator=get_default_location_from_resource_group)
        c.argument('tags', arg_type=tags_type)

    with self.argument_context('ams account create') as c:
        c.argument('storage_account', storage_account_arg_type,
                   help='The name or resource ID of the primary storage account to attach to the Azure Media Services account. Blob only accounts are not allowed as primary.')

    with self.argument_context('ams account check-name') as c:
        c.argument('account_name', options_list=['--name', '-n'], id_part=None,
                   help='The name of the Azure Media Services account')
        c.argument('location', arg_type=get_location_type(self.cli_ctx))

    with self.argument_context('ams account storage') as c:
        c.argument('account_name', account_name_arg_type)
        c.argument('storage_account', name_arg_type,
                   help='The name or resource ID of the secondary storage account to detach from the Azure Media Services account.',
                   validator=validate_storage_account_id)

    with self.argument_context('ams account storage sync-storage-keys') as c:
        c.argument('id', required=True)

    with self.argument_context('ams account sp') as c:
        c.argument('account_name', account_name_arg_type)
        c.argument('sp_name', name_arg_type,
                   help="The app name or app URI to associate the RBAC with. If not present, a default name like '{amsaccountname}-access-sp' will be generated.")
        c.argument('sp_password', password_arg_type,
                   help="The password used to log in. Also known as 'Client Secret'. If not present, a random secret will be generated.")
        c.argument('role', help='The role of the service principal.', completer=get_role_definition_name_completion_list)
        c.argument('xml', action='store_true', help='Enables xml output format.')
        c.argument('years', help='Number of years for which the secret will be valid. Default: 1 year.', type=int, default=None)

    with self.argument_context('ams transform') as c:
        c.argument('account_name', account_name_arg_type)
        c.argument('transform_name', name_arg_type, id_part='child_name_1',
                   help='The name of the transform.')
        c.argument('presets',
                   nargs='+',
                   help='Space-separated list of preset names. Allowed values: {}. In addition to the allowed values, you can also pass the local full path to a custom preset JSON file.'
                   .format(", ".join(get_cdn_provider_completion_list())))
        c.argument('description', help='The description of the transform.')

    with self.argument_context('ams transform list') as c:
        c.argument('account_name', id_part=None)

    with self.argument_context('ams asset') as c:
        c.argument('account_name', account_name_arg_type)
        c.argument('asset_name', name_arg_type, id_part='child_name_1',
                   help='The name of the asset.')

    with self.argument_context('ams asset list') as c:
        c.argument('account_name', id_part=None)

    with self.argument_context('ams asset create') as c:
        c.argument('alternate_id', help='The alternate id of the asset.')
        c.argument('description', help='The asset description.')
        c.argument('asset_name', name_arg_type, help='The name of the asset.')
        c.argument('storage_account', help='The name of the storage account.')
        c.argument('container', help='The name of the asset blob container.')

    with self.argument_context('ams asset update') as c:
        c.argument('alternate_id', help='The alternate id of the asset.')
        c.argument('description', help='The asset description.')

    with self.argument_context('ams asset get-sas-urls') as c:
        c.argument('permissions', arg_type=get_enum_type(AssetContainerPermission),
                   help='The permissions to set on the SAS URL.')
        c.argument('expiry_time', expiry_arg_type, help="Specifies the UTC datetime (Y-m-d'T'H:M:S'Z') at which the SAS becomes invalid.")

    with self.argument_context('ams job') as c:
        c.argument('account_name', account_name_arg_type)
        c.argument('transform_name', transform_name_arg_type, id_part='child_name_1',
                   help='The name of the transform.')
        c.argument('job_name', name_arg_type, id_part='child_name_2',
                   help='The name of the job.')

    with self.argument_context('ams job list') as c:
        c.argument('account_name', id_part=None)

    with self.argument_context('ams job start') as c:
        c.argument('priority', arg_type=get_enum_type(Priority),
                   help='The priority with which the job should be processed.')
        c.argument('description', help='The job description.')
        c.argument('input_asset_name',
                   arg_group='Asset Job Input',
                   help='The name of the input asset.')
        c.argument('output_asset_names',
                   nargs='+', help='Space-separated list of output asset names.')
        c.argument('base_uri',
                   arg_group='Http Job Input',
                   help='Base uri for http job input. It will be concatenated with provided file names. If no base uri is given, then the provided file list is assumed to be fully qualified uris.')
        c.argument('files',
                   nargs='+',
                   help='Space-separated list of files. It can be used to tell the service to only use the files specified from the input asset.')
        c.argument('label', help='A label that is assigned to a JobInput, that is used to satisfy a reference used in the Transform.')
        c.argument('correlation_data', arg_type=correlation_data_type)

    with self.argument_context('ams job cancel') as c:
        c.argument('delete', action='store_true', help='Delete the job being cancelled.')

    with self.argument_context('ams content-key-policy') as c:
        c.argument('account_name', account_name_arg_type)
        c.argument('content_key_policy_name', name_arg_type,
                   help='The content key policy name.')
        c.argument('description', help='The content key policy description.')
        c.argument('clear_key_configuration',
                   action='store_true',
                   arg_group='Basic Policy Options',
                   help='Use Clear Key configuration, a.k.a AES encryption. It\'s intended for non-DRM keys.')
        c.argument('open_restriction',
                   action='store_true',
                   arg_group='Basic Policy Options',
                   help='Use open restriction. License or key will be delivered on every request.')
        c.argument('policy_option_name',
                   help='The name of the policy option.')

    with self.argument_context('ams content-key-policy options add') as c:
        c.argument('policy_option_name', help='The content key policy option name.')
        c.argument('issuer', arg_group='Token Restriction Parameters', help='The token issuer.')
        c.argument('audience', arg_group='Token Restriction Parameters', help='The audience for the token.')
        c.argument('symmetric_token_key', arg_group='Token Restriction Parameters', help='The key value of the key.')
        c.argument('rsa_token_key_exponent', arg_group='Token Restriction Parameters', help='The RSA Parameter exponent.')
        c.argument('rsa_token_key_modulus', arg_group='Token Restriction Parameters', help='The RSA Parameter modulus.')
        c.argument('x509_certificate_token_key', arg_group='Token Restriction Parameters', help='The raw data field of a certificate in PKCS 12 format (X509Certificate2 in .NET) with \\n as newlines')
        c.argument('alt_symmetric_token_keys', arg_group='Token Restriction Parameters', help='A list of alternative symmetric token keys separated by spaces.')
        c.argument('alt_rsa_token_key_exponents', arg_group='Token Restriction Parameters', help='A list of alternative rsa token key exponents separated by spaces.')
        c.argument('alt_rsa_token_key_modulus', arg_group='Token Restriction Parameters', help='A list of alternative rsa token key modulus separated by spaces.')
        c.argument('alt_x509_certificate_token_keys', arg_group='Token Restriction Parameters', help='A list of x509 certificate token keys separated by spaces.')
        c.argument('token_claims', arg_group='Token Restriction Parameters',
                   arg_type=token_claim_type)
        c.argument('restriction_token_type', arg_group='Token Restriction Parameters',
                   arg_type=get_enum_type(ContentKeyPolicyRestrictionTokenType), help='The type of token.')
        c.argument('open_id_connect_discovery_document', arg_group='Token Restriction Parameters', help='The OpenID connect discovery document.')

    with self.argument_context('ams streaming') as c:
        c.argument('account_name', account_name_arg_type)
        c.argument('default_content_key_policy_name', default_policy_name_arg_type)

    with self.argument_context('ams streaming locator') as c:
        c.argument('streaming_locator_name', name_arg_type, id_part='child_name_1',
                   help='The name of the streaming locator.')
        c.argument('asset_name',
                   help='The name of the asset used by the streaming locator.')
        c.argument('streaming_policy_name',
                   help='The name of the streaming policy used by the streaming locator. You can either create one with `az ams streaming policy create` or use any of the predefined policies: {}'.format(", ".join(get_default_streaming_policies_completion_list())))
        c.argument('start_time', type=datetime_format,
                   help="Start time (Y-m-d'T'H:M:S'Z') of the streaming locator.")
        c.argument('end_time', type=datetime_format,
                   help="End time (Y-m-d'T'H:M:S'Z') of the streaming locator.")
        c.argument('streaming_locator_id', help='The identifier of the streaming locator.')
        c.argument('alternative_media_id', help='An alternative media identifier associated with the streaming locator.')

    with self.argument_context('ams streaming locator list') as c:
        c.argument('account_name', id_part=None)

    with self.argument_context('ams streaming policy') as c:
        c.argument('streaming_policy_name', name_arg_type, id_part='child_name_1',
                   help='The name of the streaming policy.')
        c.argument('download',
                   arg_type=get_three_state_flag(),
                   arg_group='Encryption Protocols',
                   help='Enable Download protocol.')
        c.argument('dash',
                   arg_type=get_three_state_flag(),
                   arg_group='Encryption Protocols',
                   help='Enable Dash protocol.')
        c.argument('hls',
                   arg_type=get_three_state_flag(),
                   arg_group='Encryption Protocols',
                   help='Enable HLS protocol.')
        c.argument('smooth_streaming',
                   arg_type=get_three_state_flag(),
                   arg_group='Encryption Protocols',
                   help='Enable SmoothStreaming protocol.')

    with self.argument_context('ams streaming policy list') as c:
        c.argument('account_name', id_part=None)

    with self.argument_context('ams streaming endpoint') as c:
        c.argument('streaming_endpoint_name', name_arg_type, help='The name of the streaming endpoint.')
        c.argument('account_name', account_name_arg_type)

    with self.argument_context('ams streaming endpoint create') as c:
        c.argument('tags', arg_type=tags_type)
        c.argument('location', arg_type=get_location_type(self.cli_ctx))
        c.argument('description', help='The streaming endpoint description.')
        c.argument('scale_units', help='The number of scale units.')
        c.argument('availability_set_name', help='AvailabilitySet name.')
        c.argument('max_cache_age', help='Max cache age.')
        c.argument('custom_host_names', nargs='+', help='Space-separated list of custom host names for the streaming endpoint. Use "" to clear existing list.')
        c.argument('cdn_provider', arg_group='CDN Support', help='The CDN provider name. Allowed values: {}'.format(", ".join(get_cdn_provider_completion_list())))
        c.argument('cdn_profile', arg_group='CDN Support', help='The CDN profile name.')
        c.argument('client_access_policy', help='The local full path to the clientaccesspolicy.xml used by Silverlight.')
        c.argument('cross_domain_policy', help='The local full path to the crossdomain.xml used by Silverlight.')
        c.argument('auto_start', action='store_true', help='Start the streaming endpoint automatically after creating it.')
        c.argument('ips', nargs='+', arg_group='Access Control Support', help='Space-separated list of allowed IP addresses for access control. Use "" to clear existing list.')

    with self.argument_context('ams streaming endpoint update') as c:
        c.argument('tags', arg_type=tags_type)
        c.argument('description', help='The streaming endpoint description.')
        c.argument('max_cache_age', help='Max cache age.')
        c.argument('custom_host_names', nargs='+', help='Space-separated list of custom host names for the streaming endpoint. Use "" to clear existing list.')
        c.argument('cdn_provider', arg_group='CDN Support', help='The CDN provider name. Allowed values: {}'.format(", ".join(get_cdn_provider_completion_list())))
        c.argument('cdn_profile', arg_group='CDN Support', help='The CDN profile name.')
        c.argument('client_access_policy', help='The local full path to the clientaccesspolicy.xml used by Silverlight.')
        c.argument('cross_domain_policy', help='The local full path to the crossdomain.xml used by Silverlight.')
        c.argument('ips', nargs='+', arg_group='Access Control Support', help='Space-separated list of allowed IP addresses for access control. Use "" to clear existing list.')
        c.argument('disable_cdn', arg_group='CDN Support', action='store_true', help='Use this flag to disable CDN for the streaming endpoint.')

    with self.argument_context('ams streaming endpoint scale') as c:
        c.argument('scale_unit', options_list=['--scale-units'], help='The number of scale units.')

    with self.argument_context('ams streaming endpoint akamai add') as c:
        c.argument('identifier', help='Identifier of the key.')
        c.argument('base64_key', help='Authentication key.')
        c.argument('expiration', help='The exact time for the authentication key to expire.')

    with self.argument_context('ams streaming endpoint akamai remove') as c:
        c.argument('identifier', help='Identifier of the key.')

    with self.argument_context('ams live event') as c:
        c.argument('account_name', account_name_arg_type)
        c.argument('live_event_name', name_arg_type, help='The name of the live event.')

    with self.argument_context('ams live event create') as c:
        c.argument('streaming_protocol', arg_type=get_enum_type(LiveEventInputProtocol),
                   help='The streaming protocol for the live event.')
        c.argument('auto_start', action='store_true', help='Start the live event automatically after creating it.')
        c.argument('encoding_type', arg_type=get_enum_type(LiveEventEncodingType),
                   help='The encoding type for live event.')
        c.argument('preset_name', help='The encoding preset name.')
        c.argument('tags', arg_type=tags_type)
        c.argument('key_frame_interval_duration', help='ISO 8601 timespan duration of the key frame interval duration.')
        c.argument('access_token', help='The access token.')
        c.argument('description', help='The live event description.')
        c.argument('ips', nargs='+', help='Space-separated list of allowed IP addresses for access control.')
        c.argument('preview_locator', help='The preview locator Guid.')
        c.argument('streaming_policy_name', help='The name of streaming policy used for live event preview.')
        c.argument('alternative_media_id', help='An alternative media identifier associated with the preview URL. This identifier can be used to distinguish the preview of different live events for authorization purposes in the custom license acquisition URL template or the custom key acquisition URL template of the streaming policy specified in the streaming policy name field.')
        c.argument('vanity_url', action='store_true', help='The live event vanity URL flag.')
        c.argument('client_access_policy', help='The local full path to the clientaccesspolicy.xml used by Silverlight.')
        c.argument('cross_domain_policy', help='The local full path to the crossdomain.xml used by Silverlight.')
        c.argument('stream_options', nargs='+', arg_type=get_enum_type(StreamOptionsFlag), help='The stream options.')

    with self.argument_context('ams live event update') as c:
        c.argument('description', help='The live event description.')
        c.argument('ips', nargs='+', help='Space-separated list of allowed IP addresses for access control. Use "" to clear existing list.')
        c.argument('tags', arg_type=tags_type)
        c.argument('client_access_policy', help='The local full path to the clientaccesspolicy.xml used by Silverlight.')
        c.argument('cross_domain_policy', help='The local full path to the crossdomain.xml used by Silverlight.')
        c.argument('key_frame_interval_duration', help='ISO 8601 timespan duration of the key frame interval duration.')

    with self.argument_context('ams live event stop') as c:
        c.argument('remove_outputs_on_stop', action='store_true', help='Remove live outputs on stop.')

    with self.argument_context('ams live output') as c:
        c.argument('account_name', account_name_arg_type)
        c.argument('live_event_name', help='The name of the live event.')
        c.argument('live_output_name', name_arg_type, help='The name of the live output.')

    with self.argument_context('ams live output create') as c:
        c.argument('asset_name', help='The name of the asset.')
        c.argument('manifest_name', help='The manifest file name.')
        c.argument('archive_window_length', help='ISO 8601 timespan duration of the archive window length. This is the duration that customer want to retain the recorded content.')
        c.argument('description', help='The live output description.')
        c.argument('fragments_per_ts_segment', help='The amount of fragments per HLS segment.')
        c.argument('output_snap_time', help='The output snapshot time.')
