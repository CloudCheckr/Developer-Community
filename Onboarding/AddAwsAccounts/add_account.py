import numpy as np
import boto3
import requests
import sys
import json
import time

"""
To run this you use python add_account.py admin_profile 0000000000000000000000000000000000000000000000000000000000000000 AlecAccount alec-cloudtrail-bucket

To run this are the following input parameters cloudcheckr-admin-api-key unique-account-name-in-cloudcheckr cloudtrail-bucket-name billing-bucket-name

The CloudCheckr admin api key is a 64 character string.
The CloudCheckr Account name is the name of the new account in CloudCheckr.
The cloudtrail-bucket-name is the name of the s3 bucket with cloudtrail data. If this is blank, then no cloudtrail data will be added.
The billing-bucket-name is the name of the s3 bucket with the DBR. For payee accounts this can be left blank.


The role used by boto3 must have permissions to create cloudformation stacks and IAM Admin actions such as create roles and create policies.
"""

def get_role_arn_from_stack(cloudformation, stack_id):
	"""
	Uses the stack id to get the role arn from describe_stacks.
	"""

	if stack_id is None:
		print("A stack id was not returned. Exiting")
		return None

	cloudformation_stack_description = cloudformation.describe_stacks(StackName=stack_id)
	if "Stacks" in cloudformation_stack_description:
		Stacks = cloudformation_stack_description["Stacks"]
		if len(Stacks) > 0:
			if "Outputs" in Stacks[0]:
				Outputs = Stacks[0]["Outputs"]
				if len(Outputs) > 0:
					
					if "OutputKey" in Outputs[0]:
						print("Created a " + Outputs[0]["OutputKey"])
						print("Created " + Outputs[0]["OutputValue"])
						if Outputs[0]["OutputKey"] == "RoleArn":
							print("Found role. Waiting 10 seconds before adding to CloudCheckr.")
							# AWS makes you wait ten seconds before adding a role to CloudCheckr sometimes.
							time.sleep(10)
							return Outputs[0]["OutputValue"]
						else:
							if len(Outputs) > 1:
								if "OutputKey" in Outputs[1]:
									print("Created a " + Outputs[1]["OutputKey"])
									print("Created " + Outputs[1]["OutputValue"])
									if Outputs[1]["OutputKey"] == "RoleArn":
										print("Found role. Waiting 10 seconds before adding to CloudCheckr.")
										# AWS makes you wait ten seconds before adding a role to CloudCheckr sometimes.
										time.sleep(10)
										return Outputs[1]["OutputValue"]
								else:
									print("First and second returned values in the stack were neither a role arn. Investigate stack output")
									return None
					else:
						print("Could not find an output key in the first cloudformation stack output")
				else:
					print("The number of Outputs was 0")
			else:
				print("Could not find Outputs in the first stack values. Trying again in 10 seconds to let stack complete")
				time.sleep(10)
				return get_role_arn_from_stack(cloudformation, stack_id)
		else:
			print("The number of stacks was 0")
	else:
		print("Could not find any stacks in the cloudformation stack description")


def add_role_to_cloudcheckr(env, admin_api_key, account_name, role_arn):
	"""
	Uses the cross-account role created by the cloud formation stack to add it to CloudCheckr.
	Uses the edit_credential Admin API call.
	"""

	if role_arn is None:
		print("Role Arn from Cloudformation stack was not found, so not credentials were added to CloudCheckr")
		return None

	api_url = env + "/api/account.json/edit_credential"

	edit_credential_info = json.dumps({"use_account": account_name, "aws_role_arn": role_arn})

	r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = edit_credential_info)

	if "Message" in r7.json():
		print("Successfully added the role " + str(role_arn) + " to the CloudCheckr Account " + account_name)
		print(r7.json())
	else:
		print("FAILED to add the role " + str(role_arn) + " to the CloudCheckr Account " + account_name)
		print(r7.json())
	return None


def create_iam_role_from_cloud_formation(profile_name, external_id, billing_bucket, cloudtrail_bucket, cur_bucket):
	session = boto3.Session(profile_name=profile_name)

	cloudformation = session.client(service_name="cloudformation", region_name="us-east-1")

	cloudformation_output = cloudformation.create_stack(StackName="cc-iam-stack-api", TemplateURL="https://s3.amazonaws.com/cf-cc-4172017/cc_aws_cfn_iam_stack.template.json", Capabilities=["CAPABILITY_IAM"],
		Parameters=[
			{
				"ParameterKey": "ExternalId",
				"ParameterValue": external_id
			},
			{
				"ParameterKey": "BillingBucket",
				"ParameterValue": billing_bucket
			},
			{
				"ParameterKey": "CloudTrailBucket",
				"ParameterValue": cloudtrail_bucket
			},
			{
				"ParameterKey": "CurBucket",
				"ParameterValue": cur_bucket
			}
		])

	print(cloudformation_output)

	stack_id = None

	if "StackId" in cloudformation_output:
		stack_id = cloudformation_output["StackId"]
	else:
		print("Was not able to create role")
		return None

	# wait thirty seconds to complete the stack creation process
	print("Built in wait of 30 seconds to allow stack to be created")
	time.sleep(30)

	role_arn = get_role_arn_from_stack(cloudformation, stack_id)

	return role_arn


def create_account_in_cloudcheckr(env, admin_api_key, account_name):
	"""
	Creates an account in CloudCheckr that is an empty slate. This will return the external_id
	"""

	api_url = env + "/api/account.json/add_account_v3"

	add_account_info = json.dumps({"account_name": account_name})

	r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = add_account_info)

	if "cc_external_id" in r7.json():
		print("Successfully created the account " + account_name + " with external_id " + r7.json()["cc_external_id"])
		print(r7.json())
		return r7.json()["cc_external_id"]
	else:
		print(r7.json())
		return None



def main():
	try:
		profile_name = str(sys.argv[1])
	except IndexError:
		print("Must include profile name")
		return

	try:
		admin_api_key = str(sys.argv[2])
	except IndexError:
		print("Must include an admin api key in the command line")
		return

	try:
		account_name = str(sys.argv[3])
	except IndexError:
		print("Must include an account name")
		return

	try:
		cloudtrail_bucket = str(sys.argv[4])
	except IndexError:
		print("No cloud trail bucket found. The IAM policy will not include access to a cloudtrail access. This account will not import CloudTrail data.")
		cloudtrail_bucket = "cloudtrail_bucket"

	try:
		dbr_bucket = str(sys.argv[5])
	except IndexError:
		print("No DBR billing bucket found. The IAM policy will not include access to a billing bucket. This will be blank for payee accounts.")
		dbr_bucket = "billing_bucket"

	try:
		cur_bucket = str(sys.argv[6])
	except IndexError:
		print("No CUR billing bucket found. The IAM policy will not include access to a billing bucket. This will be blank for payee accounts.")
		cur_bucket = "cur_billing_bucket"		


	env = "https://api.cloudcheckr.com"

	external_id = create_account_in_cloudcheckr(env, admin_api_key, account_name)

	if external_id is None:
		print("Was not able to successfully create an account in CloudCheckr")
		return

	role_arn = create_iam_role_from_cloud_formation(profile_name, external_id, dbr_bucket, cloudtrail_bucket, cur_bucket)

	add_role_to_cloudcheckr(env, admin_api_key, account_name, role_arn)


if __name__ == "__main__":
	main()