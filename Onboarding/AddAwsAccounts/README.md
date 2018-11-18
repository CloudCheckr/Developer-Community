**Onboard Accounts with CloudFormation and CloudCheckr API**

---

## Steps to Run


1. Install python 3. https://www.python.org/downloads/release/python-365/
2. Install boto3, numpy, and requests python libraries with pip. https://github.com/boto/boto3, http://docs.python-requests.org/en/master/user/install/, https://docs.scipy.org/doc/numpy-1.15.1/user/install.html
3. Create an role with the permissions to create cloud formation stacks and IAM roles/policies. https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html
4. Create an IAM User that can assume that role.
5. Create an access key from that user and add to a profile on your local machine.
6. Create a new local profile for that role and specify that user as what should be used to assume the role. This profile will have a name that is an input value to the script. https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html (alternatively you can name it something else, you just have to edit the create_iam_role_from_cloud_formation() function to have to new profile name)
7. Log in to CloudCheckr and create an Admin API access key.
8. Run python add_account.py <profile_name> <cloudcheckr-admin-api-key> <cloudcheckr-account-name> <cloudtrail-bucket> <dbr-bucket>
The profile_name is the name of the profile that is saved to the local machine. This profile should either be a user or a role that has IAM Admin permissions and create CloudFormation stack permissions.
The name CloudCheckr admin api key is a 64 character string.
The CloudCheckr Account name is the name of the new account in CloudCheckr. This account name should be unique.
The cloudtrail-bucket-name is the name of the s3 bucket with cloudtrail data. If this is blank, then no cloudtrail data will be added.
The billing-bucket-name is the name of the s3 bucket with the DBR. For payee accounts this can be left blank.
The bucket names are optional, but the admin api key and account name are required.
9. Output will log the actions done.

---

## How the program works

CloudCheckr has an admin api key that can be used to assist in onboarding accounts to CloudCheckr.

The first step is to use [add_account_v3](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#add_account_v3) to add an AWS account to CloudCheckr. This will be account will be an account with empty credentials and will return an external id for future use.

The second step is to use the CloudCheckr [CloudFormation Stack](https://support.cloudcheckr.com/getting-started-with-cloudcheckr/complete-iam-policy/) to create a cloudformation stack. This stack will create an IAM role with the external id generated in the previous step. Then the stack will create the various IAM Policies for each service based on the input data. It will create policies that give specific permissions for s3 bucket access if there is an input for it. This can be used to limit permissions to specific buckets with DBR or CloudTrail data. Then these policies will be attached to the previously created role. It usually takes around 30 seconds for this to complete and will return a cross account role. The boto3 API calls [create_stack](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.create_stack) and [describe_stacks](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html#CloudFormation.Client.describe_stacks) are used for this.

The third step is to use [edit_credential](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#edit_credential) to add the cross-account role to CloudCheckr.

---

## Assumptions

1. The environment https://api.cloudcheckr.com is being used. This can be adjusted on line 181 if required.
2. The machine that is running the computer has an AWS credentials profile. This profile is an input to the script. This user or role has the permissions to create stacks and create IAM roles/policies.
3. Program only allows for adding a CloudTrail bucket, but not a DBR bucket. If you want to add a DBR bucket, but not a CloudTrail bucket you can adjust the inputs around lines 161 to 172 to account for this.
4. These accounts are only commercial accounts. GovCloud accounts will require adding them through the UI.