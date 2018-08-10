# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


def create_streaming_endpoint(client, resource_group_name, account_name, streaming_endpoint_name, auto_start=None, tags=None,
                              location, description=None, scale_units=None, availability_set_name=None, max_cache_age=None,
                              cdn_enabled=None, cdn_provider=None, cdn_profile=None, custom_host_names=None,
                              client_access_policy=None, cross_domain_policy=None):
    from azure.mgmt.media.models import (StreamingEndpoint)

    policies = create_cross_site_access_policies(client_access_policy, cross_domain_policy)

    streaming_endpoint = StreamingEndpoint(max_cache_age=None, tags=tags, location=location, description=description, 
                                           scale_units=scale_units, cdn_profile=cdn_profile, custom_host_names=custom_host_names,
                                           availability_set_name=availability_set_name, cdn_enabled=cdn_enabled,
                                           cdn_provider=cdn_provider, cross_site_access_policies=policies)
    
    return client.create(resource_group_name=resource_group_name, account_name=account_name, auto_start=auto_start,
                         streaming_endpoint_name=streaming_endpoint_name, parameters=streaming_endpoint)


def sdk_no_wait(no_wait, func, *args, **kwargs):
    if no_wait:
        kwargs.update({'raw': True, 'polling': False})
    return func(*args, **kwargs)


def create_cross_site_access_policies(client_access_policy, cross_domain_policy):
    from azure.mgmt.media.models import CrossSiteAccessPolicies

    policies = CrossSiteAccessPolicies()

    if client_access_policy:
        policies.client_access_policy = read_xml_policy(client_access_policy)

    if cross_domain_policy:
        policies.cross_domain_policy = read_xml_policy(cross_domain_policy)

    return policies


def read_xml_policy(xml_policy_path):
    with open(xml_policy_path, 'r') as file:
        return file.read()
