# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os

from azure.cli.testsdk import ScenarioTest, ResourceGroupPreparer, StorageAccountPreparer


class AmsStreamingEndpointsTests(ScenarioTest):
    def _get_test_data_file(self, filename):
        filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', filename)
        self.assertTrue(os.path.isfile(filepath), 'File {} does not exist.'.format(filepath))
        return filepath

    @ResourceGroupPreparer()
    @StorageAccountPreparer(parameter_name='storage_account_for_show')
    def test_ams_streaming_endpoint_show(self, storage_account_for_show):
        amsname = self.create_random_name(prefix='ams', length=12)
        streaming_endpoint_name = self.create_random_name(prefix="strep", length=12)

        self.kwargs.update({
            'amsname': amsname,
            'storageAccount': storage_account_for_show,
            'location': 'westus2',
            'streamingEndpointName': streaming_endpoint_name,
            'availabilitySetName' : 'availaTest',
            'cdnProvider': 'StandardVerizon',
            'cdnProfile': 'testProfile',
            'description': 'test streaming description',
            'maxCacheAge': 11,
            'scaleUnits': 4,
            'tags': 'foo=bar',
            'clientAccessPolicy': self._get_test_data_file('clientAccessPolicy.xml'),
            'crossDomainPolicy': self._get_test_data_file('crossDomainPolicy.xml')
        })

        self.cmd('az ams account create -n {amsname} -g {rg} --storage-account {storageAccount} -l {location}'])

        self.cmd('az ams streaming endpoint create -g {rg} -a {amsname} -n {streamingEndpointName} -l {location} --availability-set-name {availabilitySetName} --cdn-provider {cdnProvider} --cdn-profile {cdnProfile} --description "{description}" --max-cache-age {maxCacheAge} --scale-units {scaleUnits} --tags "{tags}" --client-access-policy "{clientAccessPolicy}" --cross-domain-policy "{crossDomainPolicy}"')

        self.cmd('az ams streaming endpoint show -g {rg} -a {amsname} --streaming-endpoint-name {streamingEndpointName}', checks=[
            self.check('name', '{streamingEndpointName}'),
            self.check('resourceGroup', '{rg}'),
            self.check('location', 'West US 2'),
            self.check('availabilitySetName', '{availabilitySetName}'),
            self.check('cdnProvider', '{cdnProvider}'),
            self.check('cdnProfile', '{cdnProfile}'),
            self.check('description', '{description}'),
            self.check('maxCacheAge', '{maxCacheAge}'),
            self.check('scaleUnits', '{scaleUnits}'),
            self.check('length(tags)', 1)
        ])

        self.cmd('az ams streaming endpoint delete -g {rg} -a {amsname} --streaming-endpoint-name {streamingEndpointName}')

    @ResourceGroupPreparer()
    @StorageAccountPreparer(parameter_name='storage_account_for_delete')
    def test_ams_streaming_endpoint_delete(self, storage_account_for_delete):
        amsname = self.create_random_name(prefix='ams', length=12)
        streaming_endpoint_name1 = self.create_random_name(prefix="strep", length=12)
        streaming_endpoint_name2 = self.create_random_name(prefix="strep", length=12)

        self.kwargs.update({
            'amsname': amsname,
            'storageAccount': storage_account_for_delete,
            'location': 'westus2',
            'streamingEndpointName1': streaming_endpoint_name1,
            'streamingEndpointName2': streaming_endpoint_name2,
            'availabilitySetName' : 'availaTest',
            'cdnProvider': 'StandardVerizon',
            'cdnProfile': 'testProfile',
            'description': 'test streaming description',
            'maxCacheAge': 11,
            'scaleUnits': 4,
            'tags': 'foo=bar',
            'clientAccessPolicy': self._get_test_data_file('clientAccessPolicy.xml'),
            'crossDomainPolicy': self._get_test_data_file('crossDomainPolicy.xml')
        })

        self.cmd('az ams account create -n {amsname} -g {rg} --storage-account {storageAccount} -l {location}')

        self.cmd('az ams streaming endpoint create -g {rg} -a {amsname} -n {streamingEndpointName1} -l {location} --availability-set-name {availabilitySetName} --cdn-provider {cdnProvider} --cdn-profile {cdnProfile} --description "{description}" --max-cache-age {maxCacheAge} --scale-units {scaleUnits} --tags "{tags}" --client-access-policy "{clientAccessPolicy}" --cross-domain-policy "{crossDomainPolicy}"')
        self.cmd('az ams streaming endpoint create -g {rg} -a {amsname} -n {streamingEndpointName2} -l {location} --availability-set-name {availabilitySetName} --cdn-provider {cdnProvider} --cdn-profile {cdnProfile} --description "{description}" --max-cache-age {maxCacheAge} --scale-units {scaleUnits} --tags "{tags}" --client-access-policy "{clientAccessPolicy}" --cross-domain-policy "{crossDomainPolicy}"')

        self.cmd('az ams streaming endpoint list -g {rg} -a {amsname}', checks=[
            self.check('length(@)', 2)
        ])

        self.cmd('az ams streaming endpoint delete -g {rg} -a {amsname} --streaming-endpoint-name {streamingEndpointName1}')

        self.cmd('az ams streaming endpoint list -g {rg} -a {amsname}', checks=[
            self.check('length(@)', 1)
        ])

        self.cmd('az ams streaming endpoint delete -g {rg} -a {amsname} --streaming-endpoint-name {streamingEndpointName2}')

        self.cmd('az ams streaming endpoint list -g {rg} -a {amsname}', checks=[
            self.check('length(@)', 0)
        ])
