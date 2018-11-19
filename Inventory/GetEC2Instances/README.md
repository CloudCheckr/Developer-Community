# Get EC2 Instances with the CloudCheckr API

---

## Steps to Run


1. Install python 3. https://www.python.org/downloads/release/python-365/
2. Install numpy and requests python libraries with pip. https://github.com/boto/boto3, http://docs.python-requests.org/en/master/user/install/, https://docs.scipy.org/doc/numpy-1.15.1/user/install.html, https://pandas.pydata.org/pandas-docs/stable/install.html
3. Log in to CloudCheckr and create an Admin API access key.
4. Enter the name of the account that you would like to get the changes of on line 87. You can use an All Accounts MAV to pull of the instances in a MAV.
7. Run python get_ec2_instances.py <cloudcheckr-admin-api-key>

---

## How the program works

It uses the [get_resources_ec2_details_V4](https://support.cloudcheckr.com/cloudcheckr-api-userguide/api-reference-guide-inventory/#get_resources_ec2_details_V3) API call to export all of the EC2 Instances in an account. It will loop through all tokens or pages of the call.

You can view EC2 Inventory through the UI with Inventory -> EC2 -> List of EC2 Instances.

---

## Assumptions

1. The environment https://api.cloudcheckr.com is being used. This can be adjusted on line 84 if required.