import requests
import json
import numpy as np
import sys
import logging
logging.basicConfig(filename='logging_for_add_saved_filter.log',level=logging.INFO)

"""
This python script is used to add cost alerts to all non mav AWS accounts
python3 add_saved_filter.py 0000000000000000000000000000000000000000000000000000000000000000
"""

def log_information(log_string):
    logging.info(log_string)
    print(log_string)


def get_accounts(admin_api_key, env):

    if check_invalid_env(env):
        return

    api_url = env + "/api/account.json/get_accounts_v4"

    r7 = requests.get(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key})

    # print(r7.json())

    accounts_list = []

    if "accounts_and_users" in r7.json():
        accounts_and_users = r7.json()["accounts_and_users"]
        for i in np.arange(0, np.shape(accounts_and_users)[0]):
            if "cc_account_id" in accounts_and_users[i]:
                accounts_list.append(accounts_and_users[i]["cc_account_id"])

    return accounts_list

def check_aws(admin_api_key, env, cc_account_id):
    """
    Checks if an account is an AWS Account with get_account API call
    """

    api_url = env + "/api/account.json/get_account"

    get_account_info = json.dumps({"account_id": cc_account_id})

    r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = get_account_info)

    # checks for AWS (works for mav and non-mav)
    if "Provider" in r7.json():
        if r7.json()["Provider"] == "Amazon Web Services":
            return True
    return False


def add_saved_filter(admin_api_key, env, cc_account_id, saved_filter_name, emails, group_by, cost_type, include_usage_quantity, include_zero_costs):

    if check_invalid_env(env):
        return None
    
    api_url = env + "/api/billing.json/create_detailed_billing_grouped_filter_v2"

    add_saved_filter_info = json.dumps({"use_cc_account_id": cc_account_id, "filter_name": saved_filter_name, "emails": emails, "group_by": group_by, "cost_type": cost_type, "include_usage_quantity": include_usage_quantity, "include_zero_costs": include_zero_costs})

    r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = add_saved_filter_info)

    if "Code" in r7.json():
        log_information("Successfully added the cost alert " + saved_filter_name + " to the CloudCheckr account with id " + str(cc_account_id))
        log_information(r7.json())
        log_information("")
    else:
        log_information("Unable to add saved filter")
        log_information(r7.json())


def cycle_accounts(admin_api_key, env, accounts_list, saved_filter_name, emails, group_by, cost_type, include_usage_quantity, include_zero_costs):
    log_information("Started adding saved filters")

    for i in np.arange(0, np.shape(accounts_list)[0]):
        if check_aws(admin_api_key, env, accounts_list[i]): # this API all will work for Azure, but the parameters are different
            add_saved_filter(admin_api_key, env, accounts_list[i], saved_filter_name, emails, group_by, cost_type, include_usage_quantity, include_zero_costs)

    log_information("Finished adding saved filters")

def check_invalid_env(env):
    """
    This will check for an invalid enviroment. Currently it will only check for api, eu, au, or gov.
    If you are using a standalone environment, then you MUST add that to this function
    """

    Enviroments = ["https://api.cloudcheckr.com", "https://eu.cloudcheckr.com", "https://au.cloudcheckr.com", "https://gov.cloudcheckr.com", "https://qa.cloudcheckr.com"]


    if not(env in Enviroments):
        log_information("The environment " + str(env) + " is not valid. If this is a standalone environment, please add the url to the check_invalid_env function.")
        return True
    return False


def main():
    try:
        admin_api_key = str(sys.argv[1])
    except IndexError:
        print("Must admin_api_key")
        return

    env = "https://api.cloudcheckr.com"

    saved_filter_name = "Saved Filter API"

    # add emails here, can add multiple by separating by comma in the list
    emails = ["alec.rajeev+savedfilterApi3@cloudcheckr.com"]

    # add group_by here
    group_by = ["Account", "Service", "Region"]

    # add cost type here
    cost_type = "List"

    # add include usage quantity here
    include_usage_quantity = True

    # add include zero costs here
    include_zero_costs = True


    accounts_list = get_accounts(admin_api_key, env)

    if accounts_list is None:
        return

    cycle_accounts(admin_api_key, env, accounts_list, saved_filter_name, emails, group_by, cost_type, include_usage_quantity, include_zero_costs)


if __name__ == '__main__':
    main()
