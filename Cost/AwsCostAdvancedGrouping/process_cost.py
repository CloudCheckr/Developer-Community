import requests
import json
import numpy as np
import sys
import pandas as pd
from pandas.io.json import json_normalize

"""
This python script is used to find cost per customer id.
python ProcessCost.py 0000000000000000000000000000000000000000000000000000000000000000 "MonthlyTotal-CC" "2020-03-01" "2020-03-31"
"""

def get_cc_cost(env, admin_api_key, saved_filter_name, cc_account_name, start_date, end_date):
	"""
	Get cost from CloudCheckr Core Billing API
	"""

	api_url = env + "/api/billing.json/get_detailed_billing_with_grouping_v2"
	saved_filter_info = json.dumps({"saved_filter_name": saved_filter_name, "use_account": cc_account_name, "start": start_date, "end": end_date})


	request_output = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data=saved_filter_info, timeout=1000)

	if "CostsByGroup" in request_output.json():
		CostsByGroup = request_output.json()["CostsByGroup"]
		normalized = json_normalize(CostsByGroup)

		return normalized[['GroupValue', 'Cost']]
	else:
		print("Error from CC API")
		print(request_output.json())

def save_to_csv(normalized):
	"""
	Save data to csv file
	"""

	normalized.to_csv('cost_by_service.csv', index=False)

def main():
    try:
        admin_api_key = str(sys.argv[1])
        saved_filter_name = str(sys.argv[2])
        start_date = str(sys.argv[3])
        end_date = str(sys.argv[4])
    except IndexError:
        print("Must have an admin_api_key, start date, and end date as arguments")
        return

    # environment to pull cost data
    env = "https://api.cloudcheckr.com"

    # name of the account in cloudcheckr
    cc_account_name = "Test Payer"

    normalized1 = get_cc_cost(env, admin_api_key, saved_filter_name, cc_account_name, start_date, end_date)
    normalized1 = normalized1.rename(columns={'Cost': 'Dec2020'})

    save_to_csv(normalized1)



if __name__ == '__main__':
    main()