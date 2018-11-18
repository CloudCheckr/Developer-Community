**Add Budget Alerts with the CloudCheckr API**

---

## Steps to Run


1. Install python 3. https://www.python.org/downloads/release/python-365/
2. Install numpy and requests python libraries with pip. https://github.com/boto/boto3, http://docs.python-requests.org/en/master/user/install/, https://docs.scipy.org/doc/numpy-1.15.1/user/install.html, https://pandas.pydata.org/pandas-docs/stable/install.html
3. Log in to CloudCheckr and create an Admin API access key.
4. Enter the emails that you would like the alert to go to on line 111.
5. Enter the budget alert name on line 114.
6. Enter the budget amount on line 117.
7. Enter the budget period on line 123. It will default to monthly.
8. Run python add_budget_alerts.py <cloudcheckr-admin-api-key>

---

## How the program works

It uses the [add_cost_alert](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-api-reference-guide/#add_cost_alert) Admin API call to add a budget alert to every account.

This API call will only work with AWS and Non-MAV accounts, so it uses the [get_accounts_v4](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#get_accounts_v4) to get all of the accounts. Then uses the [get_account](https://support.cloudcheckr.com/cloudcheckr-api-userguide/cloudcheckr-admin-api-reference-guide/#get_account) API call to check the type.


You can view the budget alerts by going to Cost -> Alerts -> Manager.

---

## Assumptions

1. The environment https://api.cloudcheckr.com is being used. This can be adjusted on line 108 if required.
2. Every account gets the same budget amount.