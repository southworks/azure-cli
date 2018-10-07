# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import requests
import json
from adal import AuthenticationContext
from azure.cli.core._profile import Profile


def get_mru(cmd, client, resource_group_name, account_name):
    
    refresh_token = Profile(cli_ctx=cmd.cli_ctx).get_refresh_token()[1]



    authority = 'https://login.microsoftonline.com/{0}'.format('mediasouthworksdirectory.onmicrosoft.com')
    #format('479473dc-cfef-474c-ba12-cba2854af0f6')
    context = AuthenticationContext(
        authority=authority,
        validate_authority=True,
        api_version=None
    )

    je = context.acquire_token_with_refresh_token(refresh_token, 'd476653d-842c-4f52-862d-397463ada5e7', 'https://rest.media.azure.net/')

    code = context.acquire_user_code(
        resource='https://rest.media.azure.net/',
        client_id='04b07795-8ddb-461a-bbee-02f9e1bf7b46',
    )

    token = context.acquire_token_with_device_code(
        resource='https://rest.media.azure.net/',
        user_code_info=code,
        client_id='04b07795-8ddb-461a-bbee-02f9e1bf7b46'
    )

    je = token['accessToken']
    
    oauth_data = {'grant_type': 'client_credentials',
                  'client_id': 'http://spEod20181005',
                  'client_secret': '123123',
                  'resource': 'https://rest.media.azure.net'}

    oauth_headers = {'Content-Type': 'application/x-www-form-urlencoded',
                     'Keep-Alive':'true'}

    oauth = requests.post('https://login.microsoftonline.com/479473dc-cfef-474c-ba12-cba2854af0f6/oauth2/token', headers=oauth_headers, data=oauth_data)

    oaa = json.loads(oauth.text)

    headers = {'Authorization': 'Bearer {}'.format(oaa.get('access_token'))}
    response = requests.get('https://fbesteiro.restv2.brazilsouth.media.azure.net/api/EncodingReservedUnitTypes?api-version=2.19', headers=headers)

    obj = response.json()['d']['results'][0].get('CurrentReservedUnits')
