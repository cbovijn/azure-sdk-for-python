# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from azure.identity import DefaultAzureCredential
from azure.mgmt.eventgrid import EventGridManagementClient

"""
# PREREQUISITES
    pip install azure-identity
    pip install azure-mgmt-eventgrid
# USAGE
    python partner_configurations_unauthorize_partner.py

    Before run the sample, please set the values of the client ID, tenant ID and client secret
    of the AAD application as environment variables: AZURE_CLIENT_ID, AZURE_TENANT_ID,
    AZURE_CLIENT_SECRET. For more info about how to get the value, please see:
    https://docs.microsoft.com/azure/active-directory/develop/howto-create-service-principal-portal
"""


def main():
    client = EventGridManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="8f6b6269-84f2-4d09-9e31-1127efcd1e40",
    )

    response = client.partner_configurations.unauthorize_partner(
        resource_group_name="examplerg",
        partner_info={
            "authorizationExpirationTimeInUtc": "2022-01-28T01:20:55.142Z",
            "partnerName": "Contoso.Finance",
            "partnerRegistrationImmutableId": "941892bc-f5d0-4d1c-8fb5-477570fc2b71",
        },
    )
    print(response)


# x-ms-original-file: specification/eventgrid/resource-manager/Microsoft.EventGrid/preview/2023-12-15-preview/examples/PartnerConfigurations_UnauthorizePartner.json
if __name__ == "__main__":
    main()
