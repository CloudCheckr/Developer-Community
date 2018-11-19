# Get CloudTrail Alerts with the CloudCheckr API

---

## Steps to Run


1. Install python 3. https://www.python.org/downloads/release/python-365/
2. Install numpy and requests python libraries with pip. https://github.com/boto/boto3, http://docs.python-requests.org/en/master/user/install/, https://docs.scipy.org/doc/numpy-1.15.1/user/install.html, https://pandas.pydata.org/pandas-docs/stable/install.html
3. Log in to CloudCheckr and create an Admin API access key.
4. Enter the name of the account that you would like to get the changes of on line 51.
7. Run python add_saved_filters.py <cloudcheckr-admin-api-key>

---

## How the program works

It uses the [get_cloudtrail_alert_results_v2](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-api-reference-guide/#get_cloudtrail_alert_results_v2) API call to export all of the cloud trail alerts found by CloudCheckr. You can filter on a specific alert with the alert_name parameter.

You can view Change Monitoring through the UI with Security -> Alerts -> CloudTrail -> Results.

---

## Assumptions

1. The environment https://api.cloudcheckr.com is being used. This can be adjusted on line 51 if required.