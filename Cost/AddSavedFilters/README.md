**Add Saved Filters with the CloudCheckr API**

---

## Steps to Run


1. Install python 3. https://www.python.org/downloads/release/python-365/
2. Install numpy and requests python libraries with pip. https://github.com/boto/boto3, http://docs.python-requests.org/en/master/user/install/, https://docs.scipy.org/doc/numpy-1.15.1/user/install.html, https://pandas.pydata.org/pandas-docs/stable/install.html
3. Log in to CloudCheckr and create an Admin API access key.
4. Enter the emails that you would like the alert to go to on line 113.
5. Enter the group bys on line 116.
6. Enter the cost type on line 119.
7. Run python add_saved_filters.py <cloudcheckr-admin-api-key>

---

## How the program works

It uses the [create_detailed_billing_grouped_filter_v2](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-api-reference-guide/#create_detailed_billing_grouped_filter_v2) API call to add a saved filter to every AWS Account.

This API call will work with both AWS and Azure accounts, but the input parameters are slightly different. This script is optimized for the AWS version and uses the [get_accounts_v4](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#get_accounts_v4) to get all of the accounts. Then uses the [get_account](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#get_account) API call to check the type.


You can view the saved filter by going to Cost -> AWS Billing -> Custom Reporting -> Advanced Grouping.

---

## Assumptions

1. The environment https://api.cloudcheckr.com is being used. This can be adjusted on line 108 if required.
2. Every account gets the same saved filter.