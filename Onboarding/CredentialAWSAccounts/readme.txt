CredentialAWSAccounts.py
Author: Kurt Jordan


The purpose of this script is to programatically check for all accounts which are either in a "failed" or "not credentialed" state and credential it after you have created a stack set.

The stack set should create an IAM role for each of your sub accounts and provide an ARN we will use for credentialing. 


requirements:
edit the config.txt file to include the following:
APIKey -  use the following to create the api key and secret. https://success.cloudcheckr.com/article/93urirlmng-cloudcheckr-cmx-api
APISecret - permissions needed should need at minimum "Account Management"
customerNumber - can be obtained in the URL of CloudCheckr behind https://app-us.cloudcheckr.com/customers/xxxxxx
roleIdentifier - 
	this will be the last part of the arn following role/
	for example arn:aws:iam::123456789:role/cc-role-test-1    you would enter cc-role-test-1 as the roleIdentifier
	if each account is being created with random trailing digits you will need to edit the template used to deploy the stack set.
	Do this by adding "RoleName" : cc-iam-role to the cloudformation template. This removes the random string of characters appended normally at the end.  
	https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html


