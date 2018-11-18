import requests
import json
import numpy as np
import sys
import logging
logging.basicConfig(filename='logging_for_add_cost_alerts.log',level=logging.INFO)

"""
This python script is used to add cost alerts to all non mav AWS accounts
python3 add_cost_alerts.py 0000000000000000000000000000000000000000000000000000000000000000
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

    # checks for AWS and non-mav
    if "Provider" in r7.json() and "Type" in r7.json():
        if r7.json()["Provider"] == "Amazon Web Services" and r7.json()["Type"] == "General":
            return True
    return False


def add_cost_alert(admin_api_key, env, cc_account_id, alert_name, emails, budget, percent_of_budget, budget_period):

    if check_invalid_env(env):
        return None
    
    api_url = env + "/api/alert.json/add_cost_alert"

    add_cost_alert_info = json.dumps({"use_cc_account_id": cc_account_id, "alert_name": alert_name, "emails": emails, "budget": budget, "percent_of_budget": percent_of_budget, "budget_period": budget_period})

    r7 = requests.post(api_url, headers = {"Content-Type": "application/json", "access_key": admin_api_key}, data = add_cost_alert_info)

    if "Code" in r7.json():
        log_information("Successfully added the cost alert " + alert_name + " to the CloudCheckr account with id " + str(cc_account_id))
        log_information(r7.json())
        log_information("")
    else:
        log_information("Unable to add cost alert")
        log_information(r7.json())


def cycle_accounts(admin_api_key, env, accounts_list, alert_name, emails, budget, percent_of_budget, budget_period):
    log_information("Started adding cost alerts")

    for i in np.arange(0, np.shape(accounts_list)[0]):
        if check_aws(admin_api_key, env, accounts_list[i]):
            add_cost_alert(admin_api_key, env, accounts_list[i], alert_name, emails, budget, percent_of_budget, budget_period)

    log_information("Finished adding cost alerts")

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

    # add emails here, can add multiple by separating by comma
    emails = "alec.rajeev+addcostalerttest3@cloudcheckr.com"

    # add alert name here
    alert_name = "Onboarding Alert Api"

    # budget amount here
    budget = "100"

    # percet of budget here
    percent_of_budget = "75"

    # budget period here
    budget_period = "monthly"

    accounts_list = get_accounts(admin_api_key, env)

    if accounts_list is None:
        return

    cycle_accounts(admin_api_key, env, accounts_list, alert_name, emails, budget, percent_of_budget, budget_period)


if __name__ == '__main__':
    main()
