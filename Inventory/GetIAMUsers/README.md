# Get IAM Users with the CloudCheckr API

---

## Steps to Run


1. Install python 3. https://www.python.org/downloads/release/python-365/
2. Install numpy and requests python libraries with pip. https://github.com/boto/boto3, http://docs.python-requests.org/en/master/user/install/, https://docs.scipy.org/doc/numpy-1.15.1/user/install.html, https://pandas.pydata.org/pandas-docs/stable/install.html
3. Log in to CloudCheckr and create an Admin API access key.
4. Enter the name of the account that you would like to get the changes of on line 87. You can use an All Accounts MAV to pull of the IAM Users in a MAV.
7. Run python get_iam_users.py <cloudcheckr-admin-api-key>

---

## How the program works

It uses the [get_resources_iam_users](https://support.cloudcheckr.com/cloudcheckr-api-userguide/api-reference-guide-inventory/#get_resources_iam_users) API call to export all of the IAM Users in an account. It will loop through all tokens or pages of the call.

You can view IAM User Inventory through the UI with Inventory -> IAM -> List of Users.

---

## Assumptions

1. The environment https://api.cloudcheckr.com is being used. This can be adjusted on line 84 if required.