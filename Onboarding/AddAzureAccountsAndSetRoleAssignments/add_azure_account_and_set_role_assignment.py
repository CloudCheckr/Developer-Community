import numpy as np
import boto3
import requests
import sys
import json
import time
import uuid

"""
To run this you use python add_azure_account.py <CloudCheckrApiKey> <NameOfCloudCheckrAccount> <AzureDirectoryId> <AzureSubscriptionId> <AzureAdminApplicationId> <AzureAdminApplicationSecret> <AzureCloudCheckrApplicationName> <AzureCloudCheckrApplicationSecret>

To run this are the following input parameters cloudcheckr-admin-api-key unique-account-name-in-cloudcheckr azure-active-directory-id azure-subscription-id azure-admin-application-id azure-admin-application-secret

The CloudCheckr admin api key is a 64 character string.
The CloudCheckr Account name is the name of the new account in CloudCheckr.
The azure-active-directory-id is the GUID directory id. This will generally be the same for all subscriptions that have the same parent. (Parent being their associated CSP or EA account that contains cost data)
The azure-subscription-id is the GUID that corresponds to the id of the subscription. This subscription will be different for every account that is added to CloudCheckr.
The azure-admin-application-id is the GUID id of the application that was created previously that has admin permissions. It needs to be able to set application role assignments for the specified subscriptoin. It needs to be able to read from the Microsoft Graph API with Application.Read.All, Application.ReadWrite.All, Directory.Read.All permissions.
The azure-application-secret is the secret key that was created previously for the application with admin permissions. This is shown only once when generating the key. It can last 1 year, 2 years, or forever.
The azure-cloudcheckr-application-name is the name of the application that was created specifically for CloudCheckr. It will get the reader role assigned to it.
The azure-cloudcheckr-application-secret is the secret key that was created previously for the CloudCheckr application. This is shown only once when generating the key. It can last 1 year, 2 years, or forever.

"""

def create_azure_account(env, CloudCheckrApiKey, account_name, AzureDirectoryId, AzureCloudCheckrApplicationId, AzureCloudCheckrApplicationSecret, AzureSubscriptionId):
	"""
	Creates an Azure Account in CloudCheckr. It will populate it with azure subscription credentials that were provided.
	"""

	api_url = env + "/api/account.json/add_azure_inventory_account"

	add_azure_account_info = json.dumps({"account_name": account_name, "azure_ad_id": AzureDirectoryId, "azure_app_id": AzureCloudCheckrApplicationId, "azure_api_access_key": AzureCloudCheckrApplicationSecret, "azure_subscription_id": AzureSubscriptionId})

	r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": CloudCheckrApiKey}, data = add_azure_account_info)

	print(r7.json())

def get_azure_reader_role_id(AzureApiBearerToken, AzureSubscriptionId):
    """
    Gets the id of the reader role for this subscription.

    https://docs.microsoft.com/en-us/rest/api/authorization/roleassignments/list
    """

    api_url = "https://management.azure.com/subscriptions/" + AzureSubscriptionId + "/providers/Microsoft.Authorization/roleDefinitions?api-version=2015-07-01&$filter=roleName eq 'Reader'"
    authorization_value = "Bearer " + AzureApiBearerToken

    response = requests.get(api_url, headers={"Authorization": authorization_value})

    if "value" in response.json():
        value = (response.json()["value"])[0]
        if "id" in value:
            return value["id"]
    print("Failed to get the Azure Reader Role Id")
    return None

def get_azure_cloudcheckr_service_principal_id(AzureGraphApiBearerToken, AzureCloudCheckrApplicationName):
    """
    Gets the service principal id Azure Application that was specifically created for CloudCheckr.
    Note: This is not the application id. The service principal id is required for the role assignment.
    This uses the microsoft Graph API.

    https://docs.microsoft.com/en-us/graph/api/serviceprincipal-list?view=graph-rest-1.0&tabs=http
    """

    api_url = "https://graph.microsoft.com/v1.0/servicePrincipals?$filter=displayName eq '" + AzureCloudCheckrApplicationName + "'"
    authorization_value = "Bearer " + AzureGraphApiBearerToken

    response = requests.get(api_url, headers={"Authorization": authorization_value})

    if "value" in response.json():
        value = (response.json()["value"])[0]
        if ("id" in value) and ("appId" in value):
            return value["id"], value["appId"]
    print("Failed to get the Azure CloudCheckr Application Service principal Id")
    return None


def set_azure_cloudcheckr_application_service_assignment(AzureApiBearerToken, AzureReaderRoleId, AzureCloudCheckrApplicationServicePrincipalId, AzureSubscriptionId):
    """
    Sets the previously created CloudCheckr application to have a reader role assignment.

    https://docs.microsoft.com/en-us/azure/role-based-access-control/role-assignments-rest
    """

    RoleAssignmentId = str(uuid.uuid1())

    api_url = "https://management.azure.com/subscriptions/" +  AzureSubscriptionId + "/providers/Microsoft.Authorization/roleAssignments/" + RoleAssignmentId + "?api-version=2015-07-01"
    authorization_value = "Bearer " + AzureApiBearerToken
    role_assignment_data = json.dumps({"properties": {"principalId": AzureCloudCheckrApplicationServicePrincipalId, "roleDefinitionId": AzureReaderRoleId}})

    response = requests.put(api_url, headers={"Authorization": authorization_value, "Content-Type": "application/json"}, data=role_assignment_data)
    print(response.json())

    if "properties" in response.json():
        properties = response.json()["properties"]
        if "roleDefinitionId" in properties:
            return properties["roleDefinitionId"]
    print("Failed to set role assignment for the CloudCheckr Application to the specified subscription")
    return None


def get_azure_bearer_token(resource_url, azure_directory_id, azure_admin_application_id, azure_admin_application_secret):
    """
    Uses OAuth 2.0 to get the bearer token based on the client id and client secret.
    """

    api_url = "https://login.microsoftonline.com/" + azure_directory_id + "/oauth2/token"

    client = {'grant_type': 'client_credentials',
            'client_id': azure_admin_application_id,
            'client_secret': azure_admin_application_secret,
            'resource': resource_url,
    }

    response = requests.post(api_url, data=client)

    if "access_token" in response.json():
        return response.json()["access_token"]
    print("Could not get Bearer token")
    return None

def main():
    try:
        CloudCheckrApiKey = str(sys.argv[1])
    except IndexError:
        print("Must include an admin api key in the command line")
        return

    try:
        NameOfCloudCheckrAccount = str(sys.argv[2])
    except IndexError:
        print("Must include a cloudcheckr account name")
        return

    try:
        AzureDirectoryId = str(sys.argv[3])
    except IndexError:
        print("Must include an Azure Directory Id")
        return
    
    try:
        AzureSubscriptionId = str(sys.argv[4])
    except IndexError:
        print("Must include an Azure Subscription Id")
        return

    try:
        AzureAdminApplicationId = str(sys.argv[5])
    except IndexError:
        print("Must include an Azure Admin ApplictApi Id")
        return

    try:
        AzureAdminApplicationSecret = str(sys.argv[6])
    except IndexError:
        print("Must include an Azure Admin Application Secret")
        return

    try:
        AzureCloudCheckrApplicationName = str(sys.argv[7])
    except IndexError:
        print("Must include an Azure CloudCheckr Application Name")
        return

    try:
        AzureCloudCheckrApplicationSecret = str(sys.argv[8])
    except IndexError:
        print("Must include an Azure CloudCheckr Application Secret")
        return
    
    env = "https://glacier.cloudcheckr.com"

    AzureApiBearerToken = get_azure_bearer_token("https://management.azure.com/", AzureDirectoryId, AzureAdminApplicationId, AzureAdminApplicationSecret)
    AzureGraphApiBearerToken = get_azure_bearer_token("https://graph.microsoft.com/", AzureDirectoryId, AzureAdminApplicationId, AzureAdminApplicationSecret)
    AzureReaderRoleId = get_azure_reader_role_id(AzureApiBearerToken, AzureSubscriptionId)
    AzureCloudCheckrApplicationServicePrincipalId, AzureCloudCheckrApplicationId = get_azure_cloudcheckr_service_principal_id(AzureGraphApiBearerToken, AzureCloudCheckrApplicationName)
    set_azure_cloudcheckr_application_service_assignment(AzureApiBearerToken, AzureReaderRoleId, AzureCloudCheckrApplicationServicePrincipalId, AzureSubscriptionId)
    create_azure_account(env, CloudCheckrApiKey, NameOfCloudCheckrAccount, AzureDirectoryId, AzureCloudCheckrApplicationId, AzureCloudCheckrApplicationSecret, AzureSubscriptionId)

if __name__ == "__main__":
	main()