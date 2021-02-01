**Get Advanced Grouping Data with the CloudCheckr API**

---

## Steps to Run


1. Install python 3. https://www.python.org/downloads/release/python-365/
2. Install numpy, and requests python libraries with pip. https://github.com/boto/boto3, http://docs.python-requests.org/en/master/user/install/, https://docs.scipy.org/doc/numpy-1.15.1/user/install.html
3. Log in to CloudCheckr and create an Admin API access key.
4. Enter the CloudCheckr Account name of the payer account to line 54 in the variable cc_account_name.
5. Run python process_cost.py <cloudcheckr-admin-api-key> <saved_filter_name> <start_date> <end_date>

---

## How the program works

It uses the [get_detailed_billing_v2](https://success.cloudcheckr.com/article/7sskuffbg6-api-reference-guide#list_results_from_an_advanced_grouping_saved_filter) API call pull results from a specified saved filter


You can create a saved filter by following the instructions on [advanced-grouping-report](https://success.cloudcheckr.com/article/5s11l0k4fo-advanced-grouping-report).


---

## Assumptions

1. The environment https://api.cloudcheckr.com is being used. This can be adjusted on line 51 if required.