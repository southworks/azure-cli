# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import uuid
import json
import requests
from azure.cli.core.util import CLIError
from azure.cli.command_modules.ams._completers import get_mru_type_completion_list


_rut_dict = {0: 'S1',
             1: 'S2',
             2: 'S3'}


def get_mru(cmd, resource_group_name, account_name):
    mru = MediaV2Client(cmd.cli_ctx, resource_group_name, account_name).get_mru()
    return _map_mru(mru)


def set_mru(cmd, resource_group_name, account_name, count=None, type=None):
    client = MediaV2Client(cmd.cli_ctx, resource_group_name, account_name)
    mru = client.get_mru()

    count = count if count is None else int(mru['CurrentReservedUnits'])

    if type is None:
        type = int(mru['ReservedUnitType'])
    else:
        try:
            type = int(list(_rut_dict.keys())[list(_rut_dict.values()).index(type)])
        except:
            raise CLIError('Invalid --type. Allowed values: {}'.format(get_mru_type_completion_list))

    client.set_mru(mru['AccountId'], count, type)
    return _map_mru(client.get_mru())


def _map_mru(mru):
    mapped_obj = {}
    mapped_obj['count'] = mru['CurrentReservedUnits']
    mapped_obj['type'] = _rut_dict[mru['ReservedUnitType']]
    return mapped_obj


class MediaV2Client(object):
    """ Media V2 Client """
    def __init__(self, cli_ctx, resource_group_name, account_name):
        from azure.cli.core._profile import Profile
        self.profile = Profile(cli_ctx=cli_ctx)
        self._old_rp_api_version = '2015-10-01'
        self.v2_media_api_resource = 'https://rest.media.azure.net'
        self.api_endpoint = self._get_v2_api_endpoint(cli_ctx, resource_group_name, account_name)
        self.access_token = self._get_v2_access_token(cli_ctx)

    def _get_v2_api_endpoint(self, cli_ctx, resource_group_name, account_name):
        from msrestazure.tools import resource_id
        from azure.cli.command_modules.ams._sdk_utils import (get_media_namespace, get_media_type)
        from azure.cli.core.commands.client_factory import get_subscription_id

        refresh_token_obj = self.profile.get_refresh_token()
        access_token = refresh_token_obj[2]

        media_old_rp_url = resource_id(subscription=get_subscription_id(cli_ctx),
                                       resource_group=resource_group_name,
                                       namespace=get_media_namespace(), type=get_media_type(),
                                       name=account_name) + '?api-version={}'.format(self._old_rp_api_version)

        media_service_res = requests.get(cli_ctx.cloud.endpoints.resource_manager[:-1] + media_old_rp_url,
                                         headers={'Authorization': 'Bearer {}'.format(access_token)})
        if not media_service_res.ok:
            raise CLIError('There was an error while trying to request v2 Media API endpoint from {} Media Services API.'.format(self._old_rp_api_version))

        media_service = media_service_res.json()
        api_endpoints = media_service.get('properties').get('apiEndpoints')
        api_endpoint = next((x for x in api_endpoints if x.get('majorVersion') == '2'), api_endpoints[0])
        if not api_endpoint:
            raise CLIError('v2 Media API endpoint was not found.')

        return api_endpoint


    def _get_v2_access_token(self, cli_ctx):
        from adal import AuthenticationContext

        refresh_token_obj = self.profile.get_refresh_token()

        refresh_token = refresh_token_obj[1]
        tenant = refresh_token_obj[3]
        client_id = self.profile.get_login_credentials()[0]._token_retriever()[2]['_clientId']

        authority = '{}/{}'.format(cli_ctx.cloud.endpoints.active_directory, tenant)
        return AuthenticationContext(authority).acquire_token_with_refresh_token(refresh_token, client_id, self.v2_media_api_resource).get('accessToken')


    def set_mru(self, account_id, count, type):
        headers = {}
        headers['Authorization'] = 'Bearer {}'.format(self.access_token)
        headers['Content-Type'] = 'application/json;odata=verbose'
        headers['Accept'] = 'application/json;odata=verbose'

        s = requests.Session()
        req = requests.Request('PUT', "{}EncodingReservedUnitTypes(guid'{}')?api-version=2.19".format(self.api_endpoint.get('endpoint'), account_id),
                               headers=headers,
                               data="{{\"ReservedUnitType\":{},\"CurrentReservedUnits\":{}}}".format(count, type))
        response = s.send(req.prepare())

        if not response.ok:
            raise CLIError('Request to EncodingReservedUnitTypes v2 API endpoint failed.')


    def get_mru(self):
        headers = {}
        headers['Authorization'] = 'Bearer {}'.format(self.access_token)
        headers['Content-Type'] = 'application/json;odata=minimalmetadata'
        headers['Accept'] = 'application/json;odata=minimalmetadata'
        headers['Accept-Charset'] = 'UTF-8'

        response = requests.get('{}EncodingReservedUnitTypes?api-version=2.19'.format(self.api_endpoint.get('endpoint')), headers=headers)
        if not response.ok:
            raise CLIError('Request to EncodingReservedUnitTypes v2 API endpoint failed.')
        return response.json().get('value')[0]
