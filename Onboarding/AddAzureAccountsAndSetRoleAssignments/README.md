**Onboard Azure Accounts with the CloudCheckr API And Set Role Assignments With the Azure API**

---

## Steps to Setup Environment


1. Install python 3. https://www.python.org/downloads/release/python-365/
2. Install requests python libraries with pip. https://github.com/boto/boto3, http://docs.python-requests.org/en/master/user/install/, https://docs.scipy.org/doc/numpy-1.15.1/user/install.html

---

## Steps to Setup in Azure


1. Get the Azure Directory Id. This will be referred to as the AzureDirectoryId. (Part 1 through 4 of Step 1 here: [Configure Azure Subscription](https://success.cloudcheckr.com/article/lh39ppglft-configure-a-subscription-account-onboarding)). This Azure Directory Id will generally be the same for all subscriptions that are under a single Parent Account. The Parent account is the CSP or EA that contains the cost data.
2. Create and register an application in Azure. This application should have a specific purpose of being used for credentials with CloudCheckr. Then create the Azure Application secret. This will be referred to as the AzureCloudCheckrApplicationSecret. This only has to be done once per tenant. Ensure that the name of the application is known. This will be referred to as the AzureCloudCheckrApplicationName (Part 5 through 12 of Step 1 here: [Configure Azure Subscription](https://success.cloudcheckr.com/article/lh39ppglft-configure-a-subscription-account-onboarding))
3. Create and register an Application with Admin permissions. This application may already exist for a previous use-case. It will be used to set the Role Assignment of the previously created application to the subscription. This application must have the permissions to set role assignments with the Azure REST API. (`Microsoft.Authorization/roleAssignments/write`) It also has to have permissions to list service principals from the Microsoft Graph API. (`Application.Read.All, Application.ReadWrite.All, Directory.Read.All`). Once the Azure CloudCheckr Application has been assigned to a subscription these admin level permissions are no longer required. It is a one-time API call to set the role assignment.

* https://docs.microsoft.com/en-us/azure/role-based-access-control/role-assignments-rest (Microsoft Rest API)
* https://docs.microsoft.com/en-us/graph/api/serviceprincipal-list?view=graph-rest-1.0&tabs=http (Microsoft Graph API)

Note: This part has to be done for each subscription. A potential improvement is to use the global admin credentials to set the role assignment. However, the global admin should only be used in limited cases for security reasons.
[elevate-access-global](https://docs.microsoft.com/en-us/azure/role-based-access-control/elevate-access-global-admin)

4. Get the Subscription Id. The subscription id will be different for every subscription. (This is Parts 13 through 16 of Step 1 here: [Configure Azure Subscription](https://success.cloudcheckr.com/article/lh39ppglft-configure-a-subscription-account-onboarding))

---

## Steps to Run Script


1. Create a CloudCheckr Admin API key. This can be found by logging in to the Core CloudCheckr application. Then navigate to Admin Functions -> Admin API Key. Then click create an Admin API Key.
2. Determine the name of the CloudCheckr Account. This name will represent a subscription.
3. Gather the Azure Directory Id, Azure Subscription Id, Azure Admin Application Id, Azure Admin Application Secret, Azure CloudCheckr Application Name, Azure CloudCheckr Application Secret
4. Run the below.

```
python add_azure_account.py <CloudCheckrApiKey> <NameOfCloudCheckrAccount> <AzureDirectoryId> <AzureSubscriptionId> <AzureAdminApplicationId> <AzureAdminApplicationSecret> <AzureCloudCheckrApplicationName> <AzureCloudCheckrApplicationSecret>
```
* The `CloudCheckrApiKey` is a 64 character string.
* The `NameOfCloudCheckrAccount` is the name of the new account in CloudCheckr.
* The `AzureDirectoryId` is the GUID directory id. This will generally be the same for all subscriptions that have the same parent. (Parent being their associated CSP or EA account that contains cost data)
* The `AzureSubscriptionId` is the GUID that corresponds to the id of the subscription. This subscription will be different for every account that is added to CloudCheckr.
* The `AzureAdminApplicationId` is the GUID id of the application that was created previously that has admin permissions. It needs to be able to set application role assignments for the specified subscriptoin. It needs to be able to read from the Microsoft Graph API with Application.Read.All, Application.ReadWrite.All, Directory.Read.All permissions.
* The `AzureAdminApplicationSecret` is the secret key that was created previously for the application with admin permissions. This is shown only once when generating the key. It can last 1 year, 2 years, or forever.
* The `AzureCloudCheckrApplicationName` is the name of the application that was created specifically for CloudCheckr. It will get the reader role assigned to it.
* The `AzureCloudCheckrApplicationSecret` is the secret key that was created previously for the CloudCheckr application. This is shown only once when generating the key. It can last 1 year, 2 years, or forever.
9. Output will log the actions done.

---

## How the program works

The first part of the script interacts with two Microsoft APIs. The script will use the Admin Azure application to get a bearer token for the [Microsoft Azure REST API](https://docs.microsoft.com/en-us/rest/api/resources/) and the [Microsoft Graph API](https://docs.microsoft.com/en-us/graph/api/overview?view=graph-rest-1.0).

It will use the Microsoft REST API to get the Azure Role Reader Assignment Id using the [roleAssignments](https://docs.microsoft.com/en-us/rest/api/authorization/roleassignments/list) API call.

Then it will use the Microsoft Graph API to get the CloudCheckr Application's [Service Principal Id](https://docs.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals). It will also get the Application Id. It will use the name of the previously created CloudCheckr application as an input for this. The list [/serviceprincipals](https://docs.microsoft.com/en-us/graph/api/serviceprincipal-list?view=graph-rest-1.0&tabs=http) API call is used to do this. This step requires the `Application.Read.All, Application.ReadWrite.All, Directory.Read.All` permissions. See the [Microsoft Graph Permissions](https://docs.microsoft.com/en-us/graph/auth/auth-concepts#microsoft-graph-permissions) document for how to set permissions.

Then it will set the CloudCheckr application to have a role assignment with a permission set of Reader. It will use the Service Principal Id and the Reader Role Assignment Id to do this. It will use the [roleAssignment](https://docs.microsoft.com/en-us/azure/role-based-access-control/role-assignments-rest) API call to do this. This step requires the `Microsoft.Authorization/roleAssignments/write` permissions. See [Add Role Assignment](https://docs.microsoft.com/en-us/azure/role-based-access-control/role-assignments-portal) for how to set these permissions. (Coincidentally this program is basically automating this role assignment step to set the CloudCheckr application to have a reader role. However, some users already have an Admin application set up that can be used for this)

Once the Azure CloudCheckr application has the correct role it can set up the CloudCheckr part.

CloudCheckr has an admin api key that can be used to assist in onboarding accounts to CloudCheckr. The python program will take the input names and keys and preform the [add_azure_inventory_account](https://success.cloudcheckr.com/article/eem9bajrak-api-reference-guide-azure#addazureinventoryaccount) API call. This will create a new account in CloudCheckr and it will populate the account with the specified Azure Credentials.

---

## Assumptions


1. The environment https://api.cloudcheckr.com is being used. This can be adjusted on line 73 if required.
2. The program can use python 3 and the requests library.
3. The Azure Admin application has been created and has the required permissions.
3. The Azure CloudCheckr application has already been created, registered. It does not have its role assignment yet.
4. This program should be run once per subscription.
