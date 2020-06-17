**Onboard Azure Accounts with the CloudCheckr API**

---

## Steps to Setup Environment


1. Install python 3. https://www.python.org/downloads/release/python-365/
2. Install requests python libraries with pip. https://github.com/boto/boto3, http://docs.python-requests.org/en/master/user/install/, https://docs.scipy.org/doc/numpy-1.15.1/user/install.html

---

## Steps to Setup in Azure


1. Get the Azure Directory Id. (Part 1 through 4 of Step 1 here: [Configure Azure Subscription](https://success.cloudcheckr.com/article/lh39ppglft-configure-a-subscription-account-onboarding)). This Azure Directory Id will generally be the same for all subscriptions that are under a single Parent Account. The Parent account is the CSP or EA that contains the cost data.
2. Create and register an application in Azure. This application should have a specific purpose of being used for credentials with CloudCheckr. Then create the Azure Application secret. This only has to be done once per tenant. (Part 5 through 12 of Step 1 here: [Configure Azure Subscription](https://success.cloudcheckr.com/article/lh39ppglft-configure-a-subscription-account-onboarding))
3. Add a Role Assignment for the application to a subscription. This part has to be done for every subscription that is planning to be
added to CloudCheckr. (Step 2 here: [Configure Azure Subscription](https://success.cloudcheckr.com/article/lh39ppglft-configure-a-subscription-account-onboarding))

Note: This part has to be done for each subscription. A potential improvement is to automate this step using the global admin.
[elevate-access-global](https://docs.microsoft.com/en-us/azure/role-based-access-control/elevate-access-global-admin)

The global admin credentials can likely be used to automatically add the role assignment to each subscription using this Azure Role Assignment API call.
[role-assignments-rest](https://docs.microsoft.com/en-us/azure/role-based-access-control/role-assignments-rest)

4. Get the Subscription Id. The subscription id will be different for every subscription. (This is Parts 13 through 16 of Step 1 here: [Configure Azure Subscription](https://success.cloudcheckr.com/article/lh39ppglft-configure-a-subscription-account-onboarding))

---

## Steps to Run Script


1. Create a CloudCheckr Admin API key. This can be found by logging in to the Core CloudCheckr application. Then navigate to Admin Functions -> Admin API Key. Then click create an Admin API Key.
2. Determine the name of the CloudCheckr Account. This name will represent a subscription.
3. Gather the Azure Directory Id, Azure Application Id, Azure Application Secret, and Azure Subscription Id from the above.
4. Run the below.

```
python add_azure_account.py <CloudCheckrApiKey> <NameOfCloudCheckrAccount> <AzureDirectoryId> <AzureApplicationId> <AzureApplictionSecretKey> <AzureSubscriptionId>
```
* The CloudCheckr admin api key is a 64 character string.
* The CloudCheckr Account name is the name of the new account in CloudCheckr.
* The azure-active-directory-id is the GUID directory id. This will generally be the same for all subscriptions that have the same parent. (Parent being their associated CSP or EA account that contains cost data)
* The azure-application-id is the GUID id of the application that was created previously. It can be re-used for multiple subscriptions, but have to give the application permissions in each subscription.
* The azure-application-secret is the secret key that was created previously. This is shown only once when generating the key. It can last 1 year, 2 years, or forever.
* The azure-subscription-id is the GUID that corresponds to the id of the subscription. This subscription will be different for every account that is added to CloudCheckr. 
9. Output will log the actions done.

---

## How the program works


CloudCheckr has an admin api key that can be used to assist in onboarding accounts to CloudCheckr. The python program will take the input names and keys and preform the [add_azure_inventory_account](https://success.cloudcheckr.com/article/eem9bajrak-api-reference-guide-azure#addazureinventoryaccount) API call. This will create a new account in CloudCheckr and it will populate the account with the specified Azure Credentials.

---

## Assumptions


1. The environment https://api.cloudcheckr.com is being used. This can be adjusted on line 73 if required.
2. The program can use python 3 and the requests library.
3. The Azure application has already been created, registered, and been granted the Reader role in the required Azure subscription.
4. This program should be run once per subscription.
