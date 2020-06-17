import numpy as np
import boto3
import requests
import sys
import json
import time

"""
To run this you use python add_azure_account.py <CloudCheckrApiKey> <NameOfCloudCheckrAccount> <AzureDirectoryId> <AzureApplicationId> <AzureApplictionSecretKey> <AzureSubscriptionId> 

To run this are the following input parameters cloudcheckr-admin-api-key unique-account-name-in-cloudcheckr azure-active-directory-id azure-application-id azure-application-secret azure-subscription-id

The CloudCheckr admin api key is a 64 character string.
The CloudCheckr Account name is the name of the new account in CloudCheckr.
The azure-active-directory-id is the GUID directory id. This will generally be the same for all subscriptions that have the same parent. (Parent being their associated CSP or EA account that contains cost data)
The azure-application-id is the GUID id of the application that was created previously. It can be re-used for multiple subscriptions, but have to give the application permissions in each subscription.
The azure-application-secret is the secret key that was created previously. This is shown only once when generating the key. It can last 1 year, 2 years, or forever.
The azure-subscription-id is the GUID that corresponds to the id of the subscription. This subscription will be different for every account that is added to CloudCheckr. 

"""

def create_azure_account(env, admin_api_key, account_name, azure_ad_id, azure_app_id, azure_api_access_key, azure_subscription_id):
	"""
	Creates an Azure Account in CloudCheckr. It will populate it with azure subscription credentials that were provided.
	"""

	api_url = env + "/api/account.json/add_azure_inventory_account"

	add_azure_account_info = json.dumps({"account_name": account_name, "azure_ad_id": azure_ad_id, "azure_app_id": azure_app_id, "azure_api_access_key": azure_api_access_key, "azure_subscription_id": azure_subscription_id})

	r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = add_azure_account_info)

	print(r7.json())

def main():
	try:
		admin_api_key = str(sys.argv[1])
	except IndexError:
		print("Must include an admin api key in the command line")
		return

	try:
		account_name = str(sys.argv[2])
	except IndexError:
		print("Must include a cloudcheckr account name")
		return

	try:
		azure_ad_id = str(sys.argv[3])
	except IndexError:
		print("Must include an Azure Directory Id")
		return

	try:
		azure_app_id = str(sys.argv[4])
	except IndexError:
		print("Must include an Azure Application Id")
		return

	try:
		azure_api_access_key = str(sys.argv[5])
	except IndexError:
		print("Must include an Azure Api Access Key")
		return

	try:
		azure_subscription_id = str(sys.argv[6])
	except IndexError:
		print("Must include an Azure Subscription Id")
		return

	# can change this it eu.cloudcheckr.com or au.cloudcheckr.com for different environments
	env = "https://api.cloudcheckr.com"

	create_azure_account(env, admin_api_key, account_name, azure_ad_id, azure_app_id, azure_api_access_key, azure_subscription_id)

if __name__ == "__main__":
	main()
