# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.util import CLIError


def list_mediaservices(cmd, client, resource_group_name=None):

    #import requests
    #import json

    ##from azure.cli.core._profile import (Profile, CredsCache)
    ##profile = Profile(cli_ctx=cmd.cli_ctx)
    ###creds_cache = CredsCache(cmd.cli_ctx)
    ##profile2 = profile.get_refresh_token()
    ###profile3 = profile.get_access_token_for_resource()
    ###profile.auth_ctx_factory(cmd.cli_ctx).acquire_token_with_refresh_token(refresh_token='', client_id='', resource='http://rest.media.azure.net/')
    ###token = client.config.credentials._token_retriever()
    ###token_ejej = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Imk2bEdrM0ZaenhSY1ViMkMzbkVRN3N5SEpsWSIsImtpZCI6Imk2bEdrM0ZaenhSY1ViMkMzbkVRN3N5SEpsWSJ9.eyJhdWQiOiJodHRwczovL3Jlc3QubWVkaWEuYXp1cmUubmV0IiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvNDc5NDczZGMtY2ZlZi00NzRjLWJhMTItY2JhMjg1NGFmMGY2LyIsImlhdCI6MTUzODYwMDc3NywibmJmIjoxNTM4NjAwNzc3LCJleHAiOjE1Mzg2MDQ5NzYsImFjciI6IjEiLCJhaW8iOiJBWFFBaS84SUFBQUFTWU9nVlZ6TFB0Y1dJcjJDNHVJVHdtWTc4aXBSdDV6STVMamZjYmZaYit1dUYyWCt5czV3VzI0L1FvZE1xTWJUTzJxNXBBU0pWa3lNWHN3VjFCRUZxblNlNHBIRDFNTnZwQ0o5VldwMUtJMVR2RHgwSmpvV2lqYjBEbEIxaTc2Vm9PSk9kMHZHNGlpbm4zUlViQy9iVmc9PSIsImFsdHNlY2lkIjoiNTo6MTAwMzNGRkZBRDJGQzAwRSIsImFtciI6WyJyc2EiXSwiYXBwaWQiOiJlMjY0NjRhYS1mNjc1LTQzMTMtYTQ5OS04OWU5ZGI5MzA5NDkiLCJhcHBpZGFjciI6IjIiLCJlX2V4cCI6MjYzMDk5LCJlbWFpbCI6InYtanVkYW1hQG1pY3Jvc29mdC5jb20iLCJncm91cHMiOlsiMjhiOTliYWItYTkyYS00OWRjLWE4YTMtZDBhNGJlZTFiYTNmIl0sImlkcCI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzcyZjk4OGJmLTg2ZjEtNDFhZi05MWFiLTJkN2NkMDExZGI0Ny8iLCJpcGFkZHIiOiIxOTAuMTg5LjExMS4xNzQiLCJuYW1lIjoiSnVhbiBEXHUwMDI3QW1hdG8gKFNvdXRod29ya3MgU1JMKSIsIm9pZCI6Ijk1ZDIyOTczLWYzZDEtNDM5ZS1hYzdmLWUzZTc3OTMxY2I1NyIsInB1aWQiOiIxMDAzMDAwMEFDREU2RDRBIiwic2NwIjoidXNlcl9pbXBlcnNvbmF0aW9uIiwic3ViIjoiYVhIeGU3Y195TjFNMGx0R2dLb1ZNNGJ6cWNxN194U3JQREQ2WnVvRkNOWSIsInRpZCI6IjQ3OTQ3M2RjLWNmZWYtNDc0Yy1iYTEyLWNiYTI4NTRhZjBmNiIsInVuaXF1ZV9uYW1lIjoidi1qdWRhbWFAbWljcm9zb2Z0LmNvbSIsInV0aSI6IlV3dFNQdjNZNkVXVXlzbmw2ek1XQWciLCJ2ZXIiOiIxLjAifQ.VBWw_NCuKHHxlSzFLeMgcI6dhAE97jobmpXEjl6O8CCyV41MoFHU6uR_anKQt91H04VOAagfBQpF2l1wCwU2DPi7711e0S3ZfRcniCvRtsuH-hO3pbVcjzt6LPZ02055rZlNLU1-1osl8-dUKWUXMlO1byCQWGFfWttrVn6WGm-nFUVgZRneXaZ_D0eHxpj-2qKiHl5oWS4RRKPqw53ajM_Oo6EGsGeW_Sq29X2QyY9xpP_B4mHCRd8LUn8skcRdyLKkeHX-a7C6HMHyE8s3DC3vhKi0pQvaRlJu1CAXq94g2ID6HwAh5vfU3yWuELQkZe15Pbs8PICbHrSLcRXAEw'
    ###headers = {'Authorization': '{} {}'.format(token[0], token[1])}
    
    ##from adal import AuthenticationContext
    ##authority = 'https://login.windows.net/{0}'.format(profile2[3])
    ##context = AuthenticationContext(
    ##    authority=authority,
    ##    validate_authority=True,
    ##    api_version=None
    ##)

    ##jojo = context.acquire_user_code(client_id='04b07795-8ddb-461a-bbee-02f9e1bf7b46', resource='http://rest.media.azure.net/')
    ##jojo2 = context.acquire_token_with_device_code(resource='http://rest.media.azure.net/', user_code_info=jojo, client_id='04b07795-8ddb-461a-bbee-02f9e1bf7b46')

    ##jeje = context.acquire_token_with_refresh_token(refresh_token=profile2[1], client_id='04b07795-8ddb-461a-bbee-02f9e1bf7b46', resource='http://rest.media.azure.net/')


    #oauth_data = {'grant_type': 'client_credentials',
    #              'client_id': 'http://mrusp',
    #              'client_secret': 'mrusp',
    #              'resource': 'https://rest.media.azure.net'}

    #oauth_headers = {'Content-Type': 'application/x-www-form-urlencoded',
    #                 'Keep-Alive':'true'}

    #oauth = requests.post('https://login.microsoftonline.com/479473dc-cfef-474c-ba12-cba2854af0f6/oauth2/token', headers=oauth_headers, data=oauth_data)

    #oaa = json.loads(oauth.text)

    #headers = {'Authorization': 'Bearer {}'.format(oaa.get('access_token'))}
    #response = requests.get('https://juaniams.restv2.westus2-2.media.azure.net/api/EncodingReservedUnitTypes?api-version=2.19', headers=headers)

    #obj = response.json()['d']['results'][0].get('CurrentReservedUnits')

    return client.list(resource_group_name) if resource_group_name else client.list_by_subscription()


def create_mediaservice(client, resource_group_name, account_name, storage_account, location=None, tags=None):   
    from azure.mgmt.media.models import StorageAccount
    storage_account_primary = StorageAccount(type='Primary', id=storage_account)

    return create_or_update_mediaservice(client, resource_group_name, account_name, [storage_account_primary],
                                         location,
                                         tags)


def add_mediaservice_secondary_storage(client, resource_group_name, account_name, storage_account):
    ams = client.get(resource_group_name, account_name)

    storage_accounts_filtered = list(filter(lambda s: storage_account in s.id, ams.storage_accounts))

    from azure.mgmt.media.models import StorageAccount
    storage_account_secondary = StorageAccount(type='Secondary', id=storage_account)

    if not storage_accounts_filtered:
        ams.storage_accounts.append(storage_account_secondary)

    return create_or_update_mediaservice(client, resource_group_name, account_name,
                                         ams.storage_accounts,
                                         ams.location,
                                         ams.tags)


def remove_mediaservice_secondary_storage(client, resource_group_name, account_name, storage_account):
    ams = client.get(resource_group_name, account_name)

    storage_accounts_filtered = list(filter(lambda s: storage_account not in s.id and 'Secondary' in s.type.value,
                                            ams.storage_accounts))

    primary_storage_account = list(filter(lambda s: 'Primary' in s.type.value, ams.storage_accounts))[0]
    storage_accounts_filtered.append(primary_storage_account)

    return create_or_update_mediaservice(client, resource_group_name, account_name, storage_accounts_filtered,
                                         ams.location,
                                         ams.tags)


def create_or_update_mediaservice(client, resource_group_name, account_name, storage_accounts=None,
                                  location=None,
                                  tags=None):

    from azure.mgmt.media.models import MediaService
    media_service = MediaService(location=location, storage_accounts=storage_accounts, tags=tags)

    return client.create_or_update(resource_group_name, account_name, media_service)


def mediaservice_update_getter(client, resource_group_name, account_name):
    from azure.mgmt.media.models import ApiErrorException

    try:
        return client.get(resource_group_name, account_name)
    except ApiErrorException as ex:
        raise CLIError(ex.message)


def update_mediaservice(instance, tags=None):
    if tags:
        instance.tags = tags

    return instance


def check_name_availability(client, location, account_name):
    availability = client.check_name_availability(location_name=location, name=account_name,
                                                  type='MICROSOFT.MEDIA/MEDIASERVICES')

    if availability.name_available:
        return 'Name available.'

    return availability.message
