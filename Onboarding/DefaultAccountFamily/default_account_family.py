import requests
import json
import sys
import logging
logging.basicConfig(filename='logging_for_default_account_family.log',level=logging.INFO)

"""
This python script is used to add all unmapped accounts to a single account family
python default_account_family.py admin_api_key project_id account_family
(example) python3 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 5 "183698509299 (Aaron Gettings)"
"""

def log_information(log_string):
    logging.info(log_string)
    print(log_string)


def get_accounts(admin_api_key, env, project_id, default_account_family):
    """
    Uses admin API key to get account data for modify_account_family API call
    """
    
    half_url = f"{env}/api/billing.json/get_account_family_v2"
    api_parameters = {"use_cc_account_id": project_id}
    resp = requests.get(half_url, params=api_parameters, headers = {"access_key": admin_api_key})
    
    account_families = []
    existing_accounts = []
    unmapped_accounts = []
    accounts = []
    account_string = []

    if "Code" in resp.json():
        account_families = resp.json()["AccountFamilies"]
        for account_familiy in account_families:
            if account_familiy["Name"] == default_account_family:
                existing_accounts = account_familiy["Accounts"]
        unmapped_accounts = resp.json()["UnmappedAccounts"]
        accounts = existing_accounts + unmapped_accounts
        for account in accounts:
            account_string.append(account.split(" ")[0])
        log_information("Obtained account data")
    else:
        log_information("Failed to obtain account data")
        return
    
    return ",".join(account_string)
    

def modify_account_family(admin_api_key, env, project_id, default_account_family, accounts):
    """
    Uses admin API key to add all unmapped accounts to default account family
    """

    half_url = f"{env}/api/billing.json/modify_account_family"
    api_parameters = {"use_cc_account_id": project_id, "name": default_account_family, "accounts": accounts}
    resp = requests.post(half_url, data=json.dumps(api_parameters), headers = {"Content-type": "application/json", "access_key": admin_api_key})

    if "Code" in resp.json():
        log_information(f"Modified account family: {default_account_family}")
    else:
        log_information(f"Falied to modifify account family: {default_account_family}")


def validate_env(env):
    """
    Validates enviroment. By default, it checks for api, eu, au, gov and qa.
    If you are using a standalone environment, then you must add it to the environments list
    """

    enviroments = ["https://api.cloudcheckr.com", "https://eu.cloudcheckr.com", "https://au.cloudcheckr.com", "https://gov.cloudcheckr.com", "https://qa.cloudcheckr.com"]

    if env not in enviroments:
        log_information(f"The environment {env} is not valid. If this is a standalone environment, please add the url to the validate_env function.")
        return


def main():
    try:
        admin_api_key = str(sys.argv[1])
    except IndexError:
        log_information("Must include admin API key")
        return

    try:
        project_id = str(sys.argv[2])
    except IndexError:
        log_information("Must include project id")
        return

    try:
        account_family = str(sys.argv[3])
    except IndexError:
        log_information("Must include default account family")
        return
    
    env = "https://api.cloudcheckr.com"
    validate_env(env)
    
    account_string = get_accounts(admin_api_key, env, project_id, account_family)
    modify_account_family(admin_api_key, env, project_id, account_family, account_string)


if __name__ == '__main__':
    main()